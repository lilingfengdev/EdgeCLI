"""
Crypto Service
加密服务 - 提供证书生成、UUID 生成等加密相关功能
"""

import uuid
import json
import base64
import secrets
import string
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from typing import Tuple, List, Dict, Any


class CryptoService:
    """加密服务"""
    
    @staticmethod
    def generate_uuid() -> str:
        """
        生成随机 UUID 用于 XRay 客户端 ID

        Returns:
            UUID 字符串
        """
        return str(uuid.uuid4())

    @staticmethod
    def generate_random_path() -> str:
        """
        生成随机16位字符串用于路径

        Returns:
            16位随机字符串
        """
        # 使用字母和数字生成16位随机字符串
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(16))
    
    @staticmethod
    def generate_self_signed_cert(domain: str, validity_days: int = 90) -> Tuple[List[str], List[str]]:
        """
        为指定域名生成自签名证书
        
        Args:
            domain: 域名
            validity_days: 有效期天数
            
        Returns:
            (证书行列表, 私钥行列表)
        """
        # 生成私钥
        private_key = ec.generate_private_key(ec.SECP256R1())
        
        # 创建证书主题
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Xray Inc"),
            x509.NameAttribute(NameOID.COMMON_NAME, "Xray Inc"),
        ])
        
        # 创建证书
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=validity_days)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(domain),
            ]),
            critical=False,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=False,
                content_commitment=False,
                data_encipherment=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.ExtendedKeyUsage([
                x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
            ]),
            critical=True,
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True,
        ).sign(private_key, hashes.SHA256())
        
        # 序列化证书
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)
        cert_lines = cert_pem.decode('utf-8').strip().split('\n')
        
        # 序列化私钥
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        key_lines = key_pem.decode('utf-8').strip().split('\n')
        
        return cert_lines, key_lines
    
    @staticmethod
    def format_txt_record(client_id: str, domain: str, path: str, additional_info: Dict[str, Any] = None) -> str:
        """
        格式化 DNS TXT 记录

        Args:
            client_id: 客户端 ID
            domain: 域名
            path: 路径
            additional_info: 额外信息

        Returns:
            TXT 记录字符串
        """
        record_data = {
            "id": client_id,
            "domain": domain,
            "protocol": "vless",
            "port": 443,
            "path": path
        }

        if additional_info:
            record_data.update(additional_info)

        # 创建紧凑的 JSON 字符串
        txt_content = json.dumps(record_data, separators=(',', ':'))

        return f"v=edgecli1; {txt_content}"
    
    @staticmethod
    def format_edge_link(client_id: str, domain: str, path: str, additional_info: Dict[str, Any] = None) -> str:
        """
        格式化 edge:// 链接用于便捷分享

        Args:
            client_id: 客户端 ID
            domain: 域名
            path: 路径
            additional_info: 额外信息

        Returns:
            edge:// 链接字符串
        """
        record_data = {
            "id": client_id,
            "domain": domain,
            "protocol": "vless",
            "port": 443,
            "path": path
        }

        if additional_info:
            record_data.update(additional_info)

        # 创建紧凑的 JSON 字符串
        json_content = json.dumps(record_data, separators=(',', ':'))

        # 编码为 base64
        base64_content = base64.b64encode(json_content.encode('utf-8')).decode('ascii')

        return f"edge://{base64_content}"
    
    @staticmethod
    def parse_edge_link(edge_link: str) -> Dict[str, Any]:
        """
        解析 edge:// 链接并返回配置数据
        
        Args:
            edge_link: edge:// 链接
            
        Returns:
            配置数据字典
            
        Raises:
            ValueError: 链接格式无效
        """
        if not edge_link.startswith('edge://'):
            raise ValueError("无效的 edge:// 链接格式")
        
        try:
            # 提取 base64 部分
            base64_part = edge_link[7:]  # 移除 'edge://'
            
            # 从 base64 解码
            json_content = base64.b64decode(base64_part).decode('utf-8')
            
            # 解析 JSON
            config_data = json.loads(json_content)
            
            # 验证必需字段
            required_fields = ['id', 'domain', 'protocol', 'port']
            if not all(field in config_data for field in required_fields):
                raise ValueError("edge:// 链接中缺少必需字段")
            
            return config_data
            
        except (base64.binascii.Error, json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ValueError(f"无效的 edge:// 链接格式: {str(e)}")
    
    @staticmethod
    def validate_edge_link(edge_link: str) -> bool:
        """
        验证 edge:// 链接格式
        
        Args:
            edge_link: edge:// 链接
            
        Returns:
            是否有效
        """
        try:
            CryptoService.parse_edge_link(edge_link)
            return True
        except ValueError:
            return False

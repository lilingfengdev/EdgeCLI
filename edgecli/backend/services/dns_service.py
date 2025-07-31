"""
DNS Service
DNS 服务 - 提供 DNS TXT 记录查询和验证功能
"""

import dns.resolver
import json
from typing import Dict, Any, Optional


class DNSService:
    """DNS 服务"""
    
    @staticmethod
    def query_txt_record(domain: str) -> Optional[Dict[str, Any]]:
        """
        从 _auth.<domain> 查询 TXT 记录并解析 EdgeCLI 配置
        
        Args:
            domain: 域名
            
        Returns:
            配置数据字典或 None
        """
        auth_domain = f"_auth.{domain}"
        
        try:
            # 查询 TXT 记录
            answers = dns.resolver.resolve(auth_domain, 'TXT')
            
            for rdata in answers:
                txt_content = ''.join([
                    part.decode('utf-8') if isinstance(part, bytes) else str(part) 
                    for part in rdata.strings
                ])
                
                # 检查是否为 EdgeCLI 记录
                if txt_content.startswith('v=edgecli1;'):
                    try:
                        # 提取 JSON 部分
                        json_part = txt_content[11:].strip()  # 移除 'v=edgecli1; '
                        config_data = json.loads(json_part)
                        
                        # 验证必需字段
                        required_fields = ['id', 'domain', 'protocol', 'port']
                        if all(field in config_data for field in required_fields):
                            return config_data
                        
                    except json.JSONDecodeError:
                        continue
            
            return None
            
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
            return None
    
    @staticmethod
    def validate_txt_record_format(txt_content: str) -> bool:
        """
        验证 TXT 记录格式
        
        Args:
            txt_content: TXT 记录内容
            
        Returns:
            是否有效
        """
        if not txt_content.startswith('v=edgecli1;'):
            return False
        
        try:
            json_part = txt_content[11:].strip()
            config_data = json.loads(json_part)
            
            # 检查必需字段
            required_fields = ['id', 'domain', 'protocol', 'port']
            return all(field in config_data for field in required_fields)
        except:
            return False
    
    @staticmethod
    def get_dns_record_info(domain: str, txt_record: str) -> dict:
        """
        获取 DNS 记录信息

        Args:
            domain: 域名
            txt_record: TXT 记录内容

        Returns:
            DNS 记录信息字典
        """
        return {
            "record_type": "TXT",
            "host_record": f"_auth.{domain}",
            "record_value": txt_record,
            "ttl": 600,
            "domain": domain
        }

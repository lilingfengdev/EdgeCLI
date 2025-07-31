"""
Link Service
链接服务 - 提供配置链接的生成和解析功能
"""

from typing import Dict, Any
from .crypto_service import CryptoService
from .dns_service import DNSService


class LinkService:
    """链接服务"""
    
    def __init__(self):
        """初始化链接服务"""
        self.crypto_service = CryptoService()
        self.dns_service = DNSService()
    
    def generate_txt_record(self, client_id: str, domain: str, additional_info: Dict[str, Any] = None) -> str:
        """
        生成 DNS TXT 记录
        
        Args:
            client_id: 客户端 ID
            domain: 域名
            additional_info: 额外信息
            
        Returns:
            TXT 记录字符串
        """
        return self.crypto_service.format_txt_record(client_id, domain, additional_info)
    
    def generate_edge_link(self, client_id: str, domain: str, additional_info: Dict[str, Any] = None) -> str:
        """
        生成 edge:// 链接
        
        Args:
            client_id: 客户端 ID
            domain: 域名
            additional_info: 额外信息
            
        Returns:
            edge:// 链接字符串
        """
        return self.crypto_service.format_edge_link(client_id, domain, additional_info)
    
    def parse_edge_link(self, edge_link: str) -> Dict[str, Any]:
        """
        解析 edge:// 链接
        
        Args:
            edge_link: edge:// 链接
            
        Returns:
            配置数据字典
        """
        return self.crypto_service.parse_edge_link(edge_link)
    
    def validate_edge_link(self, edge_link: str) -> bool:
        """
        验证 edge:// 链接
        
        Args:
            edge_link: edge:// 链接
            
        Returns:
            是否有效
        """
        return self.crypto_service.validate_edge_link(edge_link)
    
    def query_dns_config(self, domain: str) -> Dict[str, Any]:
        """
        从 DNS 查询配置
        
        Args:
            domain: 域名
            
        Returns:
            配置数据字典或 None
        """
        return self.dns_service.query_txt_record(domain)
    
    def get_dns_record_info(self, domain: str, txt_record: str) -> dict:
        """
        获取 DNS 记录信息

        Args:
            domain: 域名
            txt_record: TXT 记录内容

        Returns:
            DNS 记录信息字典
        """
        return self.dns_service.get_dns_record_info(domain, txt_record)
    
    def get_sharing_data(self, client_id: str, domain: str) -> Dict[str, Any]:
        """
        获取所有分享数据

        Args:
            client_id: 客户端 ID
            domain: 域名

        Returns:
            分享数据字典
        """
        txt_record = self.generate_txt_record(client_id, domain)
        edge_link = self.generate_edge_link(client_id, domain)

        return {
            "txt_record": txt_record,
            "edge_link": edge_link,
            "dns_record_info": self.get_dns_record_info(domain, txt_record),
            "connection_info": {
                "id": client_id,
                "domain": domain,
                "protocol": "vless",
                "port": 443,
                "path": f"/{self.crypto_service.generate_random_path()}"
            }
        }

"""
Client Configuration Model
客户端配置数据模型
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ClientConfig:
    """客户端配置模型"""
    
    name: str
    remote_domain: str
    local_port: int
    server_config: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClientConfig':
        """
        从字典创建配置对象
        
        Args:
            data: 配置数据字典
            
        Returns:
            客户端配置对象
        """
        return cls(
            name=data['name'],
            remote_domain=data['remote_domain'],
            local_port=data['local_port'],
            server_config=data['server_config']
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            配置数据字典
        """
        return asdict(self)
    
    def generate_xray_config(self) -> Dict[str, Any]:
        """
        生成 XRay 客户端配置
        
        Returns:
            XRay 配置字典
        """
        return {
            "log": {
                "loglevel": "warning"
            },
            "inbounds": [
                {
                    "port": self.local_port,
                    "protocol": "dokodemo-door",
                    "settings": {
                        "address": "127.0.0.1",
                        "port": 25565,
                        "network": "tcp"
                    }
                }
            ],
            "outbounds": [
                {
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": self.remote_domain,
                                "port": self.server_config.get("port", 443),
                                "users": [
                                    {
                                        "id": self.server_config["id"],
                                        "encryption": "none"
                                    }
                                ]
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "xhttp",
                        "security": "tls",
                        "xhttpSettings": {
                            "host": self.remote_domain,
                            "mode": "auto",
                            "path": self.server_config.get("path", "/mcproxy"),
                            "extra": {
                                "scMaxEachPostBytes": "1000000-10000000",
                                "scMinPostsIntervalMs": "0-100"
                            }
                        },
                        "tlsSettings": {
                            "serverName": self.remote_domain,
                            "allowInsecure": True,
                            "fingerprint": "chrome",
                            "alpn": [
                                "h3",
                                "h2"
                            ]
                        }
                    }
                }
            ]
        }
    
    def get_local_address(self) -> str:
        """
        获取本地连接地址
        
        Returns:
            本地地址字符串
        """
        return f"127.0.0.1:{self.local_port}"
    
    def get_server_info(self) -> Dict[str, Any]:
        """
        获取服务器信息
        
        Returns:
            服务器信息字典
        """
        return {
            "domain": self.remote_domain,
            "server_id": self.server_config.get("id", ""),
            "protocol": self.server_config.get("protocol", "vless"),
            "port": self.server_config.get("port", 443),
            "path": self.server_config.get("path", "/mcproxy")
        }
    
    def validate(self) -> List[str]:
        """
        验证配置
        
        Returns:
            错误信息列表
        """
        errors = []
        
        if not self.name:
            errors.append("配置名称不能为空")
        
        if not self.remote_domain:
            errors.append("远程域名不能为空")
        
        if not (1 <= self.local_port <= 65535):
            errors.append("本地端口必须在 1-65535 范围内")
        
        if not self.server_config:
            errors.append("服务器配置不能为空")
        else:
            # 验证服务器配置必需字段
            required_fields = ['id', 'domain', 'protocol', 'port']
            for field in required_fields:
                if field not in self.server_config:
                    errors.append(f"服务器配置缺少必需字段: {field}")
        
        return errors
    
    def is_valid(self) -> bool:
        """
        检查配置是否有效
        
        Returns:
            是否有效
        """
        return len(self.validate()) == 0

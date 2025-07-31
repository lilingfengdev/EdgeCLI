"""
Server Configuration Model
服务端配置数据模型
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ServerConfig:
    """服务端配置模型"""
    
    name: str
    frontend_host: str
    backend_ip: str
    backend_port: int
    client_id: str
    certificate: List[str]
    private_key: List[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ServerConfig':
        """
        从字典创建配置对象
        
        Args:
            data: 配置数据字典
            
        Returns:
            服务端配置对象
        """
        return cls(
            name=data['name'],
            frontend_host=data['frontend_host'],
            backend_ip=data['backend_ip'],
            backend_port=data['backend_port'],
            client_id=data['client_id'],
            certificate=data['certificate'],
            private_key=data['private_key']
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
        生成 XRay 服务端配置
        
        Returns:
            XRay 配置字典
        """
        return {
            "log": {
                "loglevel": "warning"
            },
            "inbounds": [
                {
                    "port": 443,
                    "protocol": "vless",
                    "settings": {
                        "clients": [
                            {
                                "id": self.client_id,
                                "flow": ""
                            }
                        ],
                        "decryption": "none"
                    },
                    "streamSettings": {
                        "network": "xhttp",
                        "security": "tls",
                        "xhttpSettings": {
                            "host": self.frontend_host,
                            "mode": "auto",
                            "path": "/mcproxy",
                            "scMaxBufferedPosts": 200,
                            "scStreamUpServerSecs": "20-80"
                        },
                        "tlsSettings": {
                            "serverName": self.frontend_host,
                            "alpn": ["h3", "h2", "http/1.1"],
                            "minVersion": "1.2",
                            "certificates": [
                                {
                                    "certificate": self.certificate,
                                    "key": self.private_key
                                }
                            ]
                        }
                    }
                }
            ],
            "outbounds": [
                {
                    "protocol": "freedom",
                    "settings": {
                        "redirect": f"{self.backend_ip}:{self.backend_port}"
                    }
                }
            ]
        }
    
    def get_connection_info(self) -> Dict[str, Any]:
        """
        获取连接信息
        
        Returns:
            连接信息字典
        """
        return {
            "id": self.client_id,
            "domain": self.frontend_host,
            "protocol": "vless",
            "port": 443,
            "path": "/mcproxy"
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
        
        if not self.frontend_host:
            errors.append("前端域名不能为空")
        
        if not self.backend_ip:
            errors.append("后端 IP 不能为空")
        
        if not (1 <= self.backend_port <= 65535):
            errors.append("后端端口必须在 1-65535 范围内")
        
        if not self.client_id:
            errors.append("客户端 ID 不能为空")
        
        if not self.certificate:
            errors.append("证书不能为空")
        
        if not self.private_key:
            errors.append("私钥不能为空")
        
        return errors
    
    def is_valid(self) -> bool:
        """
        检查配置是否有效
        
        Returns:
            是否有效
        """
        return len(self.validate()) == 0

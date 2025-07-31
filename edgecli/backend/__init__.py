"""
EdgeCLI Backend Module
后端模块 - 核心业务逻辑和数据处理
"""

__version__ = "1.0.0"
__author__ = "EdgeCLI Team"

# 导出主要的后端组件
from .core.config_manager import ConfigManager
from .core.xray_manager import XRayManager
from .core.proxy_manager import ProxyManager

from .models.server_config import ServerConfig
from .models.client_config import ClientConfig

from .services.crypto_service import CryptoService
from .services.dns_service import DNSService
from .services.link_service import LinkService

__all__ = [
    'ConfigManager',
    'XRayManager', 
    'ProxyManager',
    'ServerConfig',
    'ClientConfig',
    'CryptoService',
    'DNSService',
    'LinkService'
]

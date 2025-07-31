"""
Proxy Manager
代理管理器 - 统一管理服务端和客户端代理
"""

from typing import Dict, Any, Optional
from .config_manager import ConfigManager
from .xray_manager import XRayManager
from ..models.server_config import ServerConfig
from ..models.client_config import ClientConfig


class ProxyManager:
    """代理管理器"""
    
    def __init__(self):
        """初始化代理管理器"""
        self.config_manager = ConfigManager()
        self.xray_manager = XRayManager()
        self.current_config = None
        self.current_config_name = None
        self.current_mode = None  # 'server' or 'client'
    
    def create_server_config(self, config_data: Dict[str, Any]) -> ServerConfig:
        """
        创建服务端配置
        
        Args:
            config_data: 配置数据
            
        Returns:
            服务端配置对象
        """
        return ServerConfig.from_dict(config_data)
    
    def create_client_config(self, config_data: Dict[str, Any]) -> ClientConfig:
        """
        创建客户端配置
        
        Args:
            config_data: 配置数据
            
        Returns:
            客户端配置对象
        """
        return ClientConfig.from_dict(config_data)
    
    def load_server_config(self, config_name: str) -> Optional[ServerConfig]:
        """
        加载服务端配置
        
        Args:
            config_name: 配置名称
            
        Returns:
            服务端配置对象或 None
        """
        config_data = self.config_manager.load_config(config_name, "server")
        if config_data:
            return ServerConfig.from_dict(config_data)
        return None
    
    def load_client_config(self, config_name: str) -> Optional[ClientConfig]:
        """
        加载客户端配置
        
        Args:
            config_name: 配置名称
            
        Returns:
            客户端配置对象或 None
        """
        config_data = self.config_manager.load_config(config_name, "client")
        if config_data:
            return ClientConfig.from_dict(config_data)
        return None
    
    def save_server_config(self, config: ServerConfig, config_name: str) -> bool:
        """
        保存服务端配置
        
        Args:
            config: 服务端配置对象
            config_name: 配置名称
            
        Returns:
            是否成功
        """
        return self.config_manager.save_config(config.to_dict(), config_name, "server")
    
    def save_client_config(self, config: ClientConfig, config_name: str) -> bool:
        """
        保存客户端配置
        
        Args:
            config: 客户端配置对象
            config_name: 配置名称
            
        Returns:
            是否成功
        """
        return self.config_manager.save_config(config.to_dict(), config_name, "client")
    
    def start_server(self, config: ServerConfig, config_name: str) -> bool:
        """
        启动服务端
        
        Args:
            config: 服务端配置
            config_name: 配置名称
            
        Returns:
            是否成功启动
        """
        # 生成 XRay 配置
        xray_config = config.generate_xray_config()
        
        # 保存 XRay 配置
        xray_config_path = self.config_manager.save_xray_config(
            xray_config, config_name, "server"
        )
        
        # 启动 XRay
        if self.xray_manager.start_xray(xray_config_path):
            self.current_config = config
            self.current_config_name = config_name
            self.current_mode = "server"
            return True
        
        return False
    
    def start_client(self, config: ClientConfig, config_name: str) -> bool:
        """
        启动客户端
        
        Args:
            config: 客户端配置
            config_name: 配置名称
            
        Returns:
            是否成功启动
        """
        # 生成 XRay 配置
        xray_config = config.generate_xray_config()
        
        # 保存 XRay 配置
        xray_config_path = self.config_manager.save_xray_config(
            xray_config, config_name, "client"
        )
        
        # 启动 XRay
        if self.xray_manager.start_xray(xray_config_path):
            self.current_config = config
            self.current_config_name = config_name
            self.current_mode = "client"
            return True
        
        return False
    
    def stop_proxy(self) -> bool:
        """
        停止代理
        
        Returns:
            是否成功停止
        """
        result = self.xray_manager.stop_xray()
        if result:
            self.current_config = None
            self.current_config_name = None
            self.current_mode = None
        return result
    
    def is_running(self) -> bool:
        """
        检查代理是否正在运行
        
        Returns:
            是否正在运行
        """
        return self.xray_manager.is_running()
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取代理状态
        
        Returns:
            状态信息
        """
        return {
            "running": self.is_running(),
            "mode": self.current_mode,
            "config_name": self.current_config_name,
            "xray_version": self.xray_manager.get_version()
        }
    
    def list_server_configs(self) -> list:
        """
        列出所有服务端配置
        
        Returns:
            配置名称列表
        """
        return self.config_manager.list_configs("server")
    
    def list_client_configs(self) -> list:
        """
        列出所有客户端配置
        
        Returns:
            配置名称列表
        """
        return self.config_manager.list_configs("client")
    
    def delete_config(self, config_name: str, config_type: str) -> bool:
        """
        删除配置
        
        Args:
            config_name: 配置名称
            config_type: 配置类型
            
        Returns:
            是否成功
        """
        return self.config_manager.delete_config(config_name, config_type)

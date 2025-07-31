"""
Configuration Manager
配置管理器 - 负责配置文件的创建、读取、保存和管理
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from ..utils.system_utils import SystemUtils


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_dir: str = "configs"):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置文件目录
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.system_utils = SystemUtils()
    
    def list_configs(self, config_type: str) -> List[str]:
        """
        列出指定类型的配置文件
        
        Args:
            config_type: 配置类型 (server/client)
            
        Returns:
            配置名称列表
        """
        pattern = f"*_{config_type}.json"
        configs = []
        
        for config_file in self.config_dir.glob(pattern):
            # 提取配置名称（移除后缀）
            config_name = config_file.stem.replace(f"_{config_type}", "")
            configs.append(config_name)
        
        return sorted(configs)
    
    def config_exists(self, config_name: str, config_type: str) -> bool:
        """
        检查配置是否存在
        
        Args:
            config_name: 配置名称
            config_type: 配置类型
            
        Returns:
            是否存在
        """
        config_path = self.config_dir / f"{config_name}_{config_type}.json"
        return config_path.exists()
    
    def load_config(self, config_name: str, config_type: str) -> Optional[Dict[str, Any]]:
        """
        加载配置文件
        
        Args:
            config_name: 配置名称
            config_type: 配置类型
            
        Returns:
            配置数据或 None
        """
        config_path = self.config_dir / f"{config_name}_{config_type}.json"
        
        if not config_path.exists():
            return None
        
        try:
            return self.system_utils.load_json_config(str(config_path))
        except Exception as e:
            raise ValueError(f"加载配置失败: {str(e)}")
    
    def save_config(self, config: Dict[str, Any], config_name: str, config_type: str) -> bool:
        """
        保存配置文件
        
        Args:
            config: 配置数据
            config_name: 配置名称
            config_type: 配置类型
            
        Returns:
            是否成功
        """
        config_path = self.config_dir / f"{config_name}_{config_type}.json"
        
        try:
            self.system_utils.save_json_config(config, str(config_path))
            return True
        except Exception as e:
            raise ValueError(f"保存配置失败: {str(e)}")
    
    def delete_config(self, config_name: str, config_type: str) -> bool:
        """
        删除配置文件
        
        Args:
            config_name: 配置名称
            config_type: 配置类型
            
        Returns:
            是否成功
        """
        config_path = self.config_dir / f"{config_name}_{config_type}.json"
        
        if not config_path.exists():
            return False
        
        try:
            config_path.unlink()
            return True
        except Exception:
            return False
    
    def save_xray_config(self, xray_config: Dict[str, Any], config_name: str, config_type: str) -> str:
        """
        保存 XRay 配置文件
        
        Args:
            xray_config: XRay 配置
            config_name: 配置名称
            config_type: 配置类型
            
        Returns:
            配置文件路径
        """
        xray_config_path = self.config_dir / f"{config_name}_{config_type}_xray.json"
        
        try:
            self.system_utils.save_json_config(xray_config, str(xray_config_path))
            return str(xray_config_path)
        except Exception as e:
            raise ValueError(f"保存 XRay 配置失败: {str(e)}")
    
    def get_config_info(self, config_name: str, config_type: str) -> Optional[Dict[str, Any]]:
        """
        获取配置信息
        
        Args:
            config_name: 配置名称
            config_type: 配置类型
            
        Returns:
            配置信息
        """
        config_path = self.config_dir / f"{config_name}_{config_type}.json"
        
        if not config_path.exists():
            return None
        
        stat = config_path.stat()
        
        return {
            "name": config_name,
            "type": config_type,
            "path": str(config_path),
            "size": stat.st_size,
            "modified": stat.st_mtime
        }

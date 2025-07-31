"""
System Utils
系统工具 - 提供系统相关的工具函数
"""

import os
import platform
import json
from pathlib import Path
from typing import Dict, Any, Tuple


class SystemUtils:
    """系统工具类"""
    
    @staticmethod
    def get_platform() -> Tuple[str, str]:
        """
        获取当前平台信息
        
        Returns:
            (平台名称, 架构)
        """
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if system == "windows":
            return "windows", "64" if machine in ["amd64", "x86_64"] else "32"
        elif system == "darwin":
            return "macos", "64"
        elif system == "linux":
            if machine in ["aarch64", "arm64"]:
                return "linux", "arm64"
            elif machine.startswith("arm"):
                return "linux", "arm32"
            else:
                return "linux", "64" if machine in ["amd64", "x86_64"] else "32"
        else:
            raise ValueError(f"不支持的平台: {system}")
    
    @staticmethod
    def setup_directories(directories: list = None) -> None:
        """
        设置必需的目录
        
        Args:
            directories: 目录列表，默认为 ["configs", "logs", "bin"]
        """
        if directories is None:
            directories = ["configs", "logs", "bin"]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
    
    @staticmethod
    def load_json_config(file_path: str) -> Dict[str, Any]:
        """
        加载 JSON 配置文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            配置数据字典
            
        Raises:
            FileNotFoundError: 文件不存在
            ValueError: JSON 格式无效
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件未找到: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"配置文件 JSON 格式无效: {e}")
    
    @staticmethod
    def save_json_config(config: Dict[str, Any], file_path: str) -> None:
        """
        保存配置到 JSON 文件
        
        Args:
            config: 配置数据字典
            file_path: 文件路径
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """
        获取系统信息
        
        Returns:
            系统信息字典
        """
        platform_name, arch = SystemUtils.get_platform()
        
        return {
            "platform": platform_name,
            "architecture": arch,
            "python_version": platform.python_version(),
            "working_directory": os.getcwd(),
            "system": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
    
    @staticmethod
    def check_file_permissions(file_path: str) -> Dict[str, bool]:
        """
        检查文件权限
        
        Args:
            file_path: 文件路径
            
        Returns:
            权限信息字典
        """
        path = Path(file_path)
        
        return {
            "exists": path.exists(),
            "readable": os.access(file_path, os.R_OK) if path.exists() else False,
            "writable": os.access(file_path, os.W_OK) if path.exists() else False,
            "executable": os.access(file_path, os.X_OK) if path.exists() else False
        }
    
    @staticmethod
    def ensure_executable(file_path: str) -> bool:
        """
        确保文件可执行
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否成功
        """
        try:
            if SystemUtils.get_platform()[0] != "windows":
                os.chmod(file_path, 0o755)
            return True
        except Exception:
            return False

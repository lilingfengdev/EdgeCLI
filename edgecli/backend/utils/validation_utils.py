"""
Validation Utils
验证工具 - 提供各种数据验证功能
"""

import re
import ipaddress
from typing import Union


class ValidationUtils:
    """验证工具类"""
    
    @staticmethod
    def validate_ip_address(ip: str) -> bool:
        """
        验证 IP 地址格式
        
        Args:
            ip: IP 地址字符串
            
        Returns:
            是否有效
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_domain(domain: str) -> bool:
        """
        验证域名格式
        
        Args:
            domain: 域名字符串
            
        Returns:
            是否有效
        """
        pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        return bool(re.match(pattern, domain))
    
    @staticmethod
    def validate_port(port: Union[str, int]) -> bool:
        """
        验证端口号
        
        Args:
            port: 端口号（字符串或整数）
            
        Returns:
            是否有效
        """
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_uuid(uuid_str: str) -> bool:
        """
        验证 UUID 格式
        
        Args:
            uuid_str: UUID 字符串
            
        Returns:
            是否有效
        """
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(uuid_pattern, uuid_str.lower()))
    
    @staticmethod
    def validate_config_name(name: str) -> bool:
        """
        验证配置名称
        
        Args:
            name: 配置名称
            
        Returns:
            是否有效
        """
        if not name or not name.strip():
            return False
        
        # 配置名称只能包含字母、数字、下划线和连字符
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, name.strip()))
    
    @staticmethod
    def validate_path(path: str) -> bool:
        """
        验证路径格式
        
        Args:
            path: 路径字符串
            
        Returns:
            是否有效
        """
        if not path:
            return False
        
        # 路径应该以 / 开头
        if not path.startswith('/'):
            return False
        
        # 检查是否包含非法字符
        illegal_chars = ['<', '>', ':', '"', '|', '?', '*']
        return not any(char in path for char in illegal_chars)
    
    @staticmethod
    def validate_protocol(protocol: str) -> bool:
        """
        验证协议名称
        
        Args:
            protocol: 协议名称
            
        Returns:
            是否有效
        """
        valid_protocols = ['vless', 'vmess', 'trojan', 'shadowsocks']
        return protocol.lower() in valid_protocols
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        清理文件名，移除非法字符
        
        Args:
            filename: 原始文件名
            
        Returns:
            清理后的文件名
        """
        # 移除或替换非法字符
        illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        sanitized = filename
        
        for char in illegal_chars:
            sanitized = sanitized.replace(char, '_')
        
        # 移除前后空格和点
        sanitized = sanitized.strip(' .')
        
        # 确保不为空
        if not sanitized:
            sanitized = "unnamed"
        
        return sanitized
    
    @staticmethod
    def validate_json_structure(data: dict, required_fields: list) -> tuple[bool, list]:
        """
        验证 JSON 数据结构
        
        Args:
            data: 要验证的数据字典
            required_fields: 必需字段列表
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        if not isinstance(data, dict):
            errors.append("数据必须是字典格式")
            return False, errors
        
        for field in required_fields:
            if field not in data:
                errors.append(f"缺少必需字段: {field}")
            elif data[field] is None or data[field] == "":
                errors.append(f"字段 {field} 不能为空")
        
        return len(errors) == 0, errors

"""
Menu Components
菜单组件 - 提供各种菜单功能
"""

from rich.console import Console
from typing import Dict, Any, List, Optional, Callable
from .display import Display
from .input_handler import InputHandler

console = Console()


class Menu:
    """菜单组件类"""
    
    def __init__(self):
        """初始化菜单组件"""
        self.display = Display()
        self.input_handler = InputHandler()
    
    def show_main_menu(self) -> str:
        """
        显示主菜单并获取用户选择
        
        Returns:
            用户选择的选项
        """
        self.display.show_main_menu()
        
        return self.input_handler.get_choice_input(
            "请选择操作",
            ["0", "1", "2", "3"],
            "1"
        )
    
    def show_settings_menu(self) -> str:
        """
        显示设置菜单并获取用户选择
        
        Returns:
            用户选择的选项
        """
        self.display.show_settings_menu()
        
        return self.input_handler.get_choice_input(
            "请选择操作",
            ["0", "1", "2", "3"],
            "0"
        )
    
    def show_config_menu(self, configs: List[str], config_type: str) -> Optional[str]:
        """
        显示配置菜单并获取用户选择
        
        Args:
            configs: 配置列表
            config_type: 配置类型
            
        Returns:
            选择的配置名称或特殊选项
        """
        console.print(f"\n[bold cyan]📋 {config_type}配置管理[/bold cyan]")
        
        if configs:
            self.display.show_config_list(configs, config_type)
        
        return self.input_handler.get_menu_selection(configs, config_type)
    
    def show_sharing_menu(self) -> str:
        """
        显示分享选项菜单并获取用户选择
        
        Returns:
            用户选择的选项
        """
        self.display.show_sharing_options()
        
        return self.input_handler.get_choice_input(
            "请选择分享方式",
            ["1", "2", "3"],
            "3"
        )
    
    def create_server_config_wizard(self) -> Optional[Dict[str, Any]]:
        """
        服务端配置创建向导
        
        Returns:
            配置数据字典或 None
        """
        console.clear()
        self.display.show_title("🆕 创建 Minecraft 代理服务端配置")
        
        console.print("[bold yellow]📝 请按照提示输入配置信息:[/bold yellow]\n")
        
        # 获取配置名称
        config_name = self.input_handler.get_config_name_input("配置名称 (用于标识此配置)")
        
        # 获取前端域名
        console.print("\n[bold blue]🌐 前端域名配置[/bold blue]")
        console.print("[dim]这是客户端连接的域名，需要指向您的服务器[/dim]")
        frontend_host = self.input_handler.get_domain_input("前端域名")
        
        # 获取后端配置
        console.print("\n[bold green]🎮 后端 Minecraft 服务器配置[/bold green]")
        console.print("[dim]这是实际的 Minecraft 服务器地址[/dim]")
        backend_ip = self.input_handler.get_ip_input("后端服务器 IP")
        backend_port = self.input_handler.get_port_input("后端服务器端口", "25565")
        
        return {
            "name": config_name,
            "frontend_host": frontend_host,
            "backend_ip": backend_ip,
            "backend_port": backend_port
        }
    
    def create_client_config_wizard(self) -> Optional[Dict[str, Any]]:
        """
        客户端配置创建向导
        
        Returns:
            配置数据字典或 None
        """
        console.clear()
        self.display.show_title("🆕 创建 Minecraft 代理客户端配置")
        
        console.print("[bold yellow]📝 请按照提示输入配置信息:[/bold yellow]\n")
        
        # 获取配置名称
        config_name = self.input_handler.get_config_name_input("配置名称 (用于标识此配置)")
        
        # 获取远程服务器域名
        console.print("\n[bold blue]🌐 远程服务器配置[/bold blue]")
        console.print("[dim]请输入代理服务器的域名，系统将自动获取连接信息[/dim]")
        remote_domain = self.input_handler.get_domain_input("代理服务器域名")
        
        # 获取本地监听端口
        console.print("\n[bold green]🎮 本地 Minecraft 配置[/bold green]")
        console.print("[dim]这是您的 Minecraft 客户端连接的本地端口[/dim]")
        local_port = self.input_handler.get_port_input("本地监听端口", "25565")
        
        return {
            "name": config_name,
            "remote_domain": remote_domain,
            "local_port": local_port
        }
    
    def create_edge_config_wizard(self) -> Optional[Dict[str, Any]]:
        """
        从 Edge 链接创建配置向导
        
        Returns:
            配置数据字典或 None
        """
        console.clear()
        self.display.show_title("🔗 从 Edge 链接导入配置")
        
        console.print("[bold yellow]📝 请按照提示输入配置信息:[/bold yellow]\n")
        
        # 获取配置名称
        config_name = self.input_handler.get_config_name_input("配置名称 (用于标识此配置)")
        
        # 获取 Edge 链接
        console.print("\n[bold blue]🔗 Edge 链接配置[/bold blue]")
        console.print("[dim]请粘贴从服务端获取的 edge:// 链接[/dim]")
        edge_link = self.input_handler.get_edge_link_input("Edge 链接")
        
        # 获取本地监听端口
        console.print("\n[bold green]🎮 本地 Minecraft 配置[/bold green]")
        console.print("[dim]这是您的 Minecraft 客户端连接的本地端口[/dim]")
        local_port = self.input_handler.get_port_input("本地监听端口", "25565")
        
        return {
            "name": config_name,
            "edge_link": edge_link,
            "local_port": local_port
        }
    
    def confirm_config_creation(self, config_data: Dict[str, Any]) -> bool:
        """
        确认配置创建
        
        Args:
            config_data: 配置数据
            
        Returns:
            是否确认创建
        """
        self.display.show_config_summary(config_data)
        
        return self.input_handler.get_confirmation(
            "确认创建此配置？",
            True
        )
    
    def show_manual_server_config_menu(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        显示手动服务器配置菜单
        
        Args:
            domain: 域名
            
        Returns:
            服务器配置或 None
        """
        console.print("\n[bold yellow]🔧 手动配置服务器信息[/bold yellow]")
        console.print("[dim]请手动输入服务器连接信息[/dim]")
        
        client_id = self.input_handler.get_text_input("客户端 ID")
        protocol = self.input_handler.get_text_input("协议", "vless")
        port = self.input_handler.get_port_input("端口", "443")
        path = self.input_handler.get_text_input("路径", "/mcproxy")
        
        return {
            "id": client_id,
            "domain": domain,
            "protocol": protocol,
            "port": port,
            "path": path
        }
    
    def handle_interrupt(self) -> bool:
        """
        处理用户中断
        
        Returns:
            是否退出程序
        """
        console.print("\n\n[yellow]⚠️  程序被用户中断[/yellow]")
        return self.input_handler.get_confirmation("是否退出程序？", True)

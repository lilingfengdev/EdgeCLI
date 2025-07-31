"""
Server CLI
服务端命令行界面 - 服务端模式的用户界面
"""

import signal
import sys
from rich.console import Console
from typing import Optional, Dict, Any

from ..ui.display import Display
from ..ui.menu import Menu
from ..utils.clipboard_utils import ClipboardUtils
from ...backend.core.proxy_manager import ProxyManager
from ...backend.models.server_config import ServerConfig
from ...backend.services.crypto_service import CryptoService
from ...backend.services.link_service import LinkService

console = Console()


class ServerCLI:
    """服务端命令行界面"""
    
    def __init__(self, proxy_manager: ProxyManager):
        """
        初始化服务端 CLI
        
        Args:
            proxy_manager: 代理管理器
        """
        self.proxy_manager = proxy_manager
        self.display = Display()
        self.menu = Menu()
        self.clipboard_utils = ClipboardUtils()
        self.crypto_service = CryptoService()
        self.link_service = LinkService()
        
        self.current_config = None
        self.current_config_name = None
    
    def run(self):
        """运行服务端模式"""
        try:
            # 选择或创建配置
            config_name = self._select_or_create_config()
            
            if config_name == 'new':
                # 创建新配置
                self.current_config, self.current_config_name = self._create_new_config()
            elif config_name:
                # 加载现有配置
                self.current_config = self.proxy_manager.load_server_config(config_name)
                self.current_config_name = config_name
                console.print(f"[green]✅ 已加载配置: {config_name}[/green]")
            else:
                return
            
            if self.current_config is None:
                return
            
            # 启动服务端
            self._start_server()
            
        except Exception as e:
            console.print(f"[red]❌ 服务端启动失败: {str(e)}[/red]")
            self.menu.input_handler.wait_for_enter("按回车键返回主菜单")
    
    def _select_or_create_config(self) -> Optional[str]:
        """
        选择或创建配置
        
        Returns:
            配置名称或特殊选项
        """
        configs = self.proxy_manager.list_server_configs()
        return self.menu.show_config_menu(configs, "服务端")
    
    def _create_new_config(self) -> tuple[Optional[ServerConfig], Optional[str]]:
        """
        创建新的服务端配置
        
        Returns:
            (配置对象, 配置名称) 或 (None, None)
        """
        # 获取配置信息
        config_data = self.menu.create_server_config_wizard()
        if not config_data:
            return None, None
        
        # 确认创建
        if not self.menu.confirm_config_creation(config_data):
            console.print("[yellow]⚠️  配置创建已取消[/yellow]")
            return None, None
        
        # 生成安全凭据
        console.print("\n[cyan]🔐 正在生成安全凭据...[/cyan]")
        client_id = self.crypto_service.generate_uuid()
        cert_lines, key_lines = self.crypto_service.generate_self_signed_cert(config_data["frontend_host"])
        
        # 创建配置对象
        server_config = ServerConfig(
            name=config_data["name"],
            frontend_host=config_data["frontend_host"],
            backend_ip=config_data["backend_ip"],
            backend_port=config_data["backend_port"],
            client_id=client_id,
            certificate=cert_lines,
            private_key=key_lines
        )
        
        # 保存配置
        if self.proxy_manager.save_server_config(server_config, config_data["name"]):
            console.print(f"[green]✅ 服务端配置 '{config_data['name']}' 创建成功！[/green]")
            self.menu.input_handler.wait_for_enter()
            return server_config, config_data["name"]
        else:
            console.print("[red]❌ 配置保存失败[/red]")
            return None, None
    
    def _start_server(self):
        """启动服务端"""
        # 启动 XRay
        if self.proxy_manager.start_server(self.current_config, self.current_config_name):
            # 显示配置分享选项
            self._display_sharing_options()
            
            # 设置信号处理
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            # 保持运行
            console.print("\n[green]服务端正在运行...[/green]")
            console.print("[yellow]按 Ctrl+C 停止服务[/yellow]")
            
            try:
                while self.proxy_manager.is_running():
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        else:
            console.print("[red]XRay 启动失败![/red]")
    
    def _display_sharing_options(self):
        """显示配置分享选项"""
        choice = self.menu.show_sharing_menu()
        
        if choice == "1":
            self._display_txt_record()
        elif choice == "2":
            self._display_edge_link()
        elif choice == "3":
            console.print("\n[bold yellow]📋 DNS TXT 记录方式:[/bold yellow]")
            self._display_txt_record()
            
            console.print("\n" + "="*80)
            console.print("\n[bold yellow]🔗 Edge 链接方式:[/bold yellow]")
            self._display_edge_link()
    
    def _display_txt_record(self):
        """显示 DNS 配置说明和 TXT 记录"""
        connection_info = self.current_config.get_connection_info()

        # 获取分享数据
        sharing_data = self.link_service.get_sharing_data(
            connection_info["id"],
            connection_info["domain"]
        )

        # 显示说明
        self.display.show_dns_instructions(sharing_data["dns_record_info"])

        # 复制 TXT 记录到剪贴板
        self.clipboard_utils.copy_with_simple_feedback(
            sharing_data["txt_record"],
            "DNS TXT 记录值"
        )

        # 显示主机记录名称
        host_record = sharing_data["dns_record_info"]["host_record"]
        console.print(f"\n[dim]💡 主机记录名称: {host_record}[/dim]")
        console.print("[dim]（如需复制主机记录名称，请手动选择复制）[/dim]")
    
    def _display_edge_link(self):
        """显示 Edge 链接配置"""
        connection_info = self.current_config.get_connection_info()

        # 获取分享数据
        sharing_data = self.link_service.get_sharing_data(
            connection_info["id"],
            connection_info["domain"]
        )

        # 显示说明
        self.display.show_edge_link_instructions(sharing_data["edge_link"])

        # 复制 Edge 链接到剪贴板
        self.clipboard_utils.copy_with_simple_feedback(
            sharing_data["edge_link"],
            "Edge 链接"
        )
    
    def _signal_handler(self, signum, frame):
        """处理关闭信号"""
        console.print("\n[yellow]正在停止服务端...[/yellow]")
        self.proxy_manager.stop_proxy()
        sys.exit(0)

"""
Client CLI
客户端命令行界面 - 客户端模式的用户界面
"""

import signal
import sys
from rich.console import Console
from typing import Optional, Dict, Any

from ..ui.display import Display
from ..ui.menu import Menu
from ..utils.clipboard_utils import ClipboardUtils
from ...backend.core.proxy_manager import ProxyManager
from ...backend.models.client_config import ClientConfig
from ...backend.services.crypto_service import CryptoService
from ...backend.services.dns_service import DNSService

console = Console()


class ClientCLI:
    """客户端命令行界面"""
    
    def __init__(self, proxy_manager: ProxyManager):
        """
        初始化客户端 CLI
        
        Args:
            proxy_manager: 代理管理器
        """
        self.proxy_manager = proxy_manager
        self.display = Display()
        self.menu = Menu()
        self.clipboard_utils = ClipboardUtils()
        self.crypto_service = CryptoService()
        self.dns_service = DNSService()
        
        self.current_config = None
        self.current_config_name = None
    
    def run(self, config_path: Optional[str] = None):
        """
        运行客户端模式
        
        Args:
            config_path: 指定的配置文件路径
        """
        try:
            if config_path:
                # 加载指定配置
                self.current_config = self.proxy_manager.load_client_config(config_path)
                self.current_config_name = config_path
            else:
                # 选择或创建配置
                config_name = self._select_or_create_config()
                
                if config_name == 'edge':
                    # 从 Edge 链接导入配置
                    self.current_config, self.current_config_name = self._create_config_from_edge_link()
                elif config_name == 'new':
                    # 创建新配置
                    self.current_config, self.current_config_name = self._create_new_config()
                elif config_name:
                    # 加载现有配置
                    self.current_config = self.proxy_manager.load_client_config(config_name)
                    self.current_config_name = config_name
                    console.print(f"[green]✅ 已加载配置: {config_name}[/green]")
                else:
                    return
            
            if self.current_config is None:
                return
            
            # 启动客户端
            self._start_client()
            
        except Exception as e:
            console.print(f"[red]❌ 客户端启动失败: {str(e)}[/red]")
            self.menu.input_handler.wait_for_enter("按回车键返回主菜单")
    
    def _select_or_create_config(self) -> Optional[str]:
        """
        选择或创建配置
        
        Returns:
            配置名称或特殊选项
        """
        configs = self.proxy_manager.list_client_configs()
        return self.menu.show_config_menu(configs, "客户端")
    
    def _create_new_config(self) -> tuple[Optional[ClientConfig], Optional[str]]:
        """
        创建新的客户端配置
        
        Returns:
            (配置对象, 配置名称) 或 (None, None)
        """
        # 获取配置信息
        config_data = self.menu.create_client_config_wizard()
        if not config_data:
            return None, None
        
        # 查询 DNS TXT 记录
        console.print(f"\n[cyan]🔍 正在查询 {config_data['remote_domain']} 的服务器配置信息...[/cyan]")
        
        with console.status("[cyan]查询中...", spinner="dots"):
            server_config = self.dns_service.query_txt_record(config_data['remote_domain'])
        
        if not server_config:
            console.print(f"[red]❌ 无法从 DNS 获取服务器配置信息[/red]")
            
            if not self.menu.input_handler.get_confirmation("是否手动输入服务器信息？", False):
                console.print("[yellow]⚠️  配置创建已取消[/yellow]")
                return None, None
            
            # 手动输入服务器信息
            server_config = self.menu.show_manual_server_config_menu(config_data['remote_domain'])
            if not server_config:
                return None, None
        else:
            console.print(f"[green]✅ 成功获取服务器配置信息！[/green]")
        
        # 确认创建
        summary_data = {
            "配置名称": config_data["name"],
            "远程服务器": config_data["remote_domain"],
            "本地端口": config_data["local_port"],
            "服务器ID": server_config.get("id", "未知")[:8] + "..."
        }
        
        if not self.menu.confirm_config_creation(summary_data):
            console.print("[yellow]⚠️  配置创建已取消[/yellow]")
            return None, None
        
        # 创建配置对象
        client_config = ClientConfig(
            name=config_data["name"],
            remote_domain=config_data["remote_domain"],
            local_port=config_data["local_port"],
            server_config=server_config
        )
        
        # 保存配置
        if self.proxy_manager.save_client_config(client_config, config_data["name"]):
            console.print(f"[green]✅ 客户端配置 '{config_data['name']}' 创建成功！[/green]")
            self.menu.input_handler.wait_for_enter()
            return client_config, config_data["name"]
        else:
            console.print("[red]❌ 配置保存失败[/red]")
            return None, None
    
    def _create_config_from_edge_link(self) -> tuple[Optional[ClientConfig], Optional[str]]:
        """
        从 Edge 链接创建客户端配置
        
        Returns:
            (配置对象, 配置名称) 或 (None, None)
        """
        # 获取配置信息
        config_data = self.menu.create_edge_config_wizard()
        if not config_data:
            return None, None
        
        # 解析 Edge 链接
        console.print(f"\n[cyan]🔍 正在解析 Edge 链接...[/cyan]")
        
        try:
            with console.status("[cyan]解析中...", spinner="dots"):
                server_config = self.crypto_service.parse_edge_link(config_data['edge_link'])
            
            console.print(f"[green]✅ 成功解析配置信息！[/green]")
            console.print(f"[dim]服务器域名: {server_config['domain']}[/dim]")
            console.print(f"[dim]协议: {server_config['protocol']}[/dim]")
            console.print(f"[dim]端口: {server_config['port']}[/dim]")
            
        except Exception as e:
            console.print(f"[red]❌ 解析 Edge 链接失败: {str(e)}[/red]")
            self.menu.input_handler.wait_for_enter()
            return None, None
        
        # 确认创建
        summary_data = {
            "配置名称": config_data["name"],
            "服务器域名": server_config["domain"],
            "本地端口": config_data["local_port"],
            "协议": server_config["protocol"]
        }
        
        if not self.menu.confirm_config_creation(summary_data):
            console.print("[yellow]⚠️  配置创建已取消[/yellow]")
            return None, None
        
        # 创建配置对象
        client_config = ClientConfig(
            name=config_data["name"],
            remote_domain=server_config["domain"],
            local_port=config_data["local_port"],
            server_config=server_config
        )
        
        # 保存配置
        if self.proxy_manager.save_client_config(client_config, config_data["name"]):
            console.print(f"[green]✅ 客户端配置 '{config_data['name']}' 创建成功！[/green]")
            console.print(f"[cyan]💡 您的 Minecraft 客户端连接地址: {client_config.get_local_address()}[/cyan]")
            
            # 复制本地地址到剪贴板
            self.clipboard_utils.copy_with_simple_feedback(
                client_config.get_local_address(), 
                "本地代理地址"
            )
            
            self.menu.input_handler.wait_for_enter()
            return client_config, config_data["name"]
        else:
            console.print("[red]❌ 配置保存失败[/red]")
            return None, None
    
    def _start_client(self):
        """启动客户端"""
        # 启动 XRay
        if self.proxy_manager.start_client(self.current_config, self.current_config_name):
            # 显示连接信息
            local_address = self.current_config.get_local_address()
            console.print(f"\n[green]✅ 客户端启动成功！[/green]")
            console.print(f"[cyan]🎮 Minecraft 连接地址: {local_address}[/cyan]")
            
            # 复制本地地址到剪贴板
            self.clipboard_utils.copy_with_simple_feedback(local_address, "本地代理地址")
            
            # 设置信号处理
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            # 保持运行
            console.print("\n[green]客户端正在运行...[/green]")
            console.print("[yellow]按 Ctrl+C 停止服务[/yellow]")
            
            try:
                while self.proxy_manager.is_running():
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        else:
            console.print("[red]XRay 启动失败![/red]")
    
    def _signal_handler(self, signum, frame):
        """处理关闭信号"""
        console.print("\n[yellow]正在停止客户端...[/yellow]")
        self.proxy_manager.stop_proxy()
        sys.exit(0)

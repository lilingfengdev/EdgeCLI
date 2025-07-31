"""
Main CLI
主命令行界面 - 程序主入口和菜单控制
"""

import sys
from rich.console import Console
from typing import Optional

from ..ui.display import Display
from ..ui.menu import Menu
from .server_cli import ServerCLI
from .client_cli import ClientCLI
from ...backend.core.proxy_manager import ProxyManager
from ...backend.utils.system_utils import SystemUtils

console = Console()


class MainCLI:
    """主命令行界面"""
    
    def __init__(self):
        """初始化主 CLI"""
        self.display = Display()
        self.menu = Menu()
        self.proxy_manager = ProxyManager()
        self.system_utils = SystemUtils()
        
        # 初始化子 CLI
        self.server_cli = ServerCLI(self.proxy_manager)
        self.client_cli = ClientCLI(self.proxy_manager)
    
    def run(self, config_path: Optional[str] = None):
        """
        运行主程序
        
        Args:
            config_path: 指定的配置文件路径
        """
        # 设置目录
        self.system_utils.setup_directories()
        
        # 如果指定了配置路径，直接运行
        if config_path:
            self._run_with_config(config_path)
            return
        
        # 运行主菜单循环
        self._run_main_loop()
    
    def _run_with_config(self, config_path: str):
        """
        使用指定配置运行
        
        Args:
            config_path: 配置文件路径
        """
        try:
            # 这里可以添加直接运行指定配置的逻辑
            console.print(f"[yellow]直接运行配置功能待实现: {config_path}[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ 运行配置失败: {str(e)}[/red]")
    
    def _run_main_loop(self):
        """运行主菜单循环"""
        while True:
            try:
                console.clear()
                self.display.show_banner()
                
                # 检查 XRay 二进制文件
                if not self._check_xray_binary():
                    if not self.menu.input_handler.get_confirmation("是否继续运行程序？", False):
                        console.print("[yellow]👋 程序已退出[/yellow]")
                        sys.exit(1)
                
                # 显示主菜单并获取选择
                choice = self.menu.show_main_menu()
                
                if choice == "0":
                    console.print("\n[green]👋 感谢使用 EdgeCLI！[/green]")
                    break
                elif choice == "1":
                    # 服务端模式
                    console.print("\n[bold green]🖥️  启动服务端模式...[/bold green]")
                    self.server_cli.run()
                elif choice == "2":
                    # 客户端模式
                    console.print("\n[bold blue]💻 启动客户端模式...[/bold blue]")
                    self.client_cli.run()
                elif choice == "3":
                    # 设置菜单
                    self._handle_settings()
                
            except KeyboardInterrupt:
                if self.menu.handle_interrupt():
                    console.print("[green]👋 程序已退出[/green]")
                    break
                else:
                    continue
            except Exception as e:
                console.print(f"\n[red]❌ 发生错误: {str(e)}[/red]")
                if self.menu.input_handler.get_confirmation("是否继续运行？", True):
                    continue
                else:
                    break
    
    def _check_xray_binary(self) -> bool:
        """
        检查并下载 XRay 二进制文件
        
        Returns:
            是否准备就绪
        """
        if not self.proxy_manager.xray_manager.check_xray_binary():
            console.print("[yellow]📥 XRay 核心文件未找到，正在下载...[/yellow]")
            
            with console.status("[cyan]正在下载 XRay 核心文件...", spinner="dots"):
                if not self.proxy_manager.xray_manager.download_xray():
                    console.print("[red]❌ XRay 核心文件下载失败！[/red]")
                    console.print("[yellow]💡 请检查网络连接或手动下载 XRay 到 bin 目录[/yellow]")
                    return False
            
            console.print("[green]✅ XRay 核心文件下载成功！[/green]")
        else:
            console.print("[green]✅ XRay 核心文件已就绪[/green]")
        
        return True
    
    def _handle_settings(self):
        """处理设置菜单"""
        while True:
            console.clear()
            self.display.show_banner()
            
            choice = self.menu.show_settings_menu()
            
            if choice == "0":
                break
            elif choice == "1":
                # 查看配置文件
                self._show_config_files()
            elif choice == "2":
                # 删除配置文件
                self._delete_config_files()
            elif choice == "3":
                # 系统信息
                self._show_system_info()
    
    def _show_config_files(self):
        """显示配置文件"""
        server_configs = self.proxy_manager.list_server_configs()
        client_configs = self.proxy_manager.list_client_configs()
        
        console.print("\n[bold cyan]📁 配置文件列表[/bold cyan]")
        
        if server_configs:
            console.print("\n[bold yellow]🖥️ 服务端配置:[/bold yellow]")
            for config in server_configs:
                console.print(f"  • {config}")
        
        if client_configs:
            console.print("\n[bold yellow]💻 客户端配置:[/bold yellow]")
            for config in client_configs:
                console.print(f"  • {config}")
        
        if not server_configs and not client_configs:
            console.print("[dim]暂无配置文件[/dim]")
        
        self.menu.input_handler.wait_for_enter()
    
    def _delete_config_files(self):
        """删除配置文件"""
        console.print("[yellow]🗑️  删除配置文件功能待实现[/yellow]")
        self.menu.input_handler.wait_for_enter()
    
    def _show_system_info(self):
        """显示系统信息"""
        system_info = self.system_utils.get_system_info()
        self.display.show_system_info(system_info)
        self.menu.input_handler.wait_for_enter()


def main():
    """主程序入口函数"""
    cli = MainCLI()
    cli.run()


if __name__ == "__main__":
    main()

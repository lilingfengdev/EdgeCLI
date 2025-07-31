"""
Display Components
显示组件 - 提供各种 UI 显示功能
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from typing import Dict, Any, List

console = Console()


class Display:
    """显示组件类"""
    
    @staticmethod
    def show_banner():
        """显示欢迎横幅"""
        banner_text = Text()
        banner_text.append("EdgeCLI", style="bold bright_blue")
        banner_text.append(" - Minecraft 代理工具", style="bright_white")

        subtitle = Text("基于 XRay 的高性能代理解决方案", style="dim cyan")

        banner_content = Align.center(banner_text + "\n" + subtitle)

        banner_panel = Panel(
            banner_content,
            border_style="bright_blue",
            padding=(1, 2),
            width=80
        )

        console.print("\n")
        console.print(Align.center(banner_panel))
        console.print()
    
    @staticmethod
    def show_main_menu():
        """显示主菜单"""
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("选项", style="bold cyan", width=8)
        menu_table.add_column("说明", style="white")

        menu_table.add_row("1", "🖥️  服务端模式 - 创建 Minecraft 代理服务器")
        menu_table.add_row("2", "💻 客户端模式 - 连接到代理服务器")
        menu_table.add_row("3", "⚙️  工具设置")
        menu_table.add_row("0", "❌ 退出程序")

        menu_panel = Panel(
            menu_table,
            title="[bold green]主菜单[/bold green]",
            border_style="green",
            padding=(1, 1),
            width=80
        )

        console.print(Align.center(menu_panel))
    
    @staticmethod
    def show_settings_menu():
        """显示设置菜单"""
        settings_table = Table(show_header=False, box=None, padding=(0, 2))
        settings_table.add_column("选项", style="bold cyan", width=8)
        settings_table.add_column("说明", style="white")

        settings_table.add_row("1", "📁 查看配置文件")
        settings_table.add_row("2", "🗑️  删除配置文件")
        settings_table.add_row("3", "📊 系统信息")
        settings_table.add_row("0", "🔙 返回主菜单")

        settings_panel = Panel(
            settings_table,
            title="[bold yellow]工具设置[/bold yellow]",
            border_style="yellow",
            padding=(1, 1),
            width=80
        )

        console.print(Align.center(settings_panel))
    
    @staticmethod
    def show_config_list(configs: List[str], config_type: str):
        """
        显示配置列表
        
        Args:
            configs: 配置名称列表
            config_type: 配置类型
        """
        if not configs:
            console.print(f"[yellow]暂无 {config_type} 配置文件[/yellow]")
            return

        config_table = Table(show_header=True, header_style="bold magenta", width=70)
        config_table.add_column("序号", style="dim", width=6)
        config_table.add_column("配置名称", style="cyan")
        config_table.add_column("状态", style="green")

        for i, config_name in enumerate(configs, 1):
            config_table.add_row(str(i), config_name, "✅ 可用")

        config_panel = Panel(
            config_table,
            title=f"[bold cyan]{config_type} 配置列表[/bold cyan]",
            border_style="cyan",
            width=80
        )
        console.print(Align.center(config_panel))
    
    @staticmethod
    def show_system_info(info: Dict[str, Any]):
        """
        显示系统信息
        
        Args:
            info: 系统信息字典
        """
        info_table = Table(show_header=False, box=None, width=60)
        info_table.add_column("项目", style="cyan", width=15)
        info_table.add_column("值", style="white")

        info_table.add_row("操作系统", info.get("platform", "未知"))
        info_table.add_row("架构", info.get("architecture", "未知"))
        info_table.add_row("Python 版本", info.get("python_version", "未知"))
        info_table.add_row("工作目录", info.get("working_directory", "未知"))

        info_panel = Panel(
            info_table,
            title="[bold blue]📊 系统信息[/bold blue]",
            border_style="blue",
            width=80
        )
        console.print("\n")
        console.print(Align.center(info_panel))
    
    @staticmethod
    def show_sharing_options():
        """显示配置分享选项菜单"""
        console.print("\n[bold cyan]📤 配置分享选项[/bold cyan]")
        console.print("[dim]请选择您希望使用的配置分享方式:[/dim]\n")
        
        # 创建选项表格
        options_table = Table(show_header=False, box=None, padding=(0, 2))
        options_table.add_column("选项", style="bold cyan", width=8)
        options_table.add_column("说明", style="white")
        
        options_table.add_row("1", "🌐 DNS TXT 记录 - 通过域名自动获取配置")
        options_table.add_row("2", "🔗 Edge 链接 - 直接分享配置链接")
        options_table.add_row("3", "📋 显示所有方式")
        
        options_panel = Panel(
            options_table,
            title="[bold green]分享方式[/bold green]",
            border_style="green",
            padding=(1, 1),
            width=80
        )
        
        console.print(Align.center(options_panel))
    
    @staticmethod
    def show_dns_instructions(dns_record_info: Dict[str, Any]):
        """
        显示 DNS 配置说明

        Args:
            dns_record_info: DNS 记录信息字典
        """
        domain = dns_record_info["domain"]
        host_record = dns_record_info["host_record"]
        record_value = dns_record_info["record_value"]
        ttl = dns_record_info["ttl"]

        instructions = f"""🌐 DNS 配置说明

请在您的 DNS 服务商管理面板中添加以下 TXT 记录:

📋 记录信息:
• 记录类型: TXT
• 主机记录: {host_record}
• 记录值: {record_value}
• TTL: {ttl} (或使用默认值)

✅ 设置完成后的效果:
客户端可以通过域名 {domain} 自动获取连接配置，无需手动输入服务器信息。

⏰ 重要提醒:
DNS 记录生效通常需要 5-30 分钟，某些情况下可能需要几小时。
建议使用在线 DNS 查询工具验证记录是否生效。

💡 常见 DNS 服务商设置方法:
• 阿里云: 云解析 DNS → 解析设置 → 添加记录
• 腾讯云: DNSPod → 我的域名 → 添加记录
• Cloudflare: DNS → Records → Add record"""

        dns_panel = Panel(
            instructions,
            title="[bold green]DNS 配置说明[/bold green]",
            border_style="green",
            width=100
        )
        console.print("\n")
        console.print(Align.center(dns_panel))
    
    @staticmethod
    def show_edge_link_instructions(edge_link: str):
        """
        显示 Edge 链接说明

        Args:
            edge_link: Edge 链接
        """
        instructions = f"""🔗 Edge 链接分享

这是一个包含完整配置信息的 edge:// 链接，可以直接分享给客户端用户：

📋 Edge 链接:
{edge_link}

✅ 使用方法:
1. 将此链接发送给需要连接的用户
2. 用户在客户端选择"从 Edge 链接导入配置"
3. 粘贴此链接即可自动配置连接

💡 优势:
• 无需配置 DNS 记录
• 即时生效，无需等待 DNS 传播
• 包含完整的连接信息
• 便于通过聊天工具分享

⚠️ 注意事项:
• 请妥善保管此链接，避免泄露给未授权用户
• 链接包含服务器的完整连接信息"""

        edge_panel = Panel(
            instructions,
            title="[bold blue]Edge 链接配置[/bold blue]",
            border_style="blue",
            width=100
        )
        console.print("\n")
        console.print(Align.center(edge_panel))
    
    @staticmethod
    def show_config_summary(config_data: Dict[str, Any]):
        """
        显示配置摘要
        
        Args:
            config_data: 配置数据
        """
        console.print("\n[bold magenta]📋 配置摘要[/bold magenta]")
        summary_table = Table(show_header=False, box=None)
        summary_table.add_column("项目", style="cyan")
        summary_table.add_column("值", style="white")

        for key, value in config_data.items():
            if isinstance(value, str) and len(value) > 50:
                value = value[:47] + "..."
            summary_table.add_row(key, str(value))

        console.print(summary_table)
    
    @staticmethod
    def show_title(title: str, style: str = "bold cyan"):
        """
        显示标题
        
        Args:
            title: 标题文本
            style: 样式
        """
        title_text = Text(title, style=style)
        console.print(Panel(Align.center(title_text), border_style="cyan", padding=(1, 2)))
    
    @staticmethod
    def show_status(message: str, status_type: str = "info"):
        """
        显示状态信息
        
        Args:
            message: 状态消息
            status_type: 状态类型 (info, success, warning, error)
        """
        styles = {
            "info": "[cyan]",
            "success": "[green]",
            "warning": "[yellow]",
            "error": "[red]"
        }
        
        style = styles.get(status_type, "[white]")
        console.print(f"{style}{message}[/{style.strip('[]')}]")

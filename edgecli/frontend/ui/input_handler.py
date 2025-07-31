"""
Input Handler
输入处理器 - 提供用户输入处理功能
"""

from rich.console import Console
from rich.prompt import Prompt, Confirm
from typing import Optional, List, Callable, Any
from ...backend.utils.validation_utils import ValidationUtils

console = Console()


class InputHandler:
    """输入处理器类"""
    
    def __init__(self):
        """初始化输入处理器"""
        self.validation_utils = ValidationUtils()
    
    def get_text_input(self, prompt: str, default: str = None, required: bool = True) -> Optional[str]:
        """
        获取文本输入
        
        Args:
            prompt: 提示信息
            default: 默认值
            required: 是否必需
            
        Returns:
            用户输入的文本或 None
        """
        while True:
            value = Prompt.ask(f"[cyan]{prompt}[/cyan]", default=default)
            
            if not required and not value:
                return None
            
            if value and value.strip():
                return value.strip()
            
            if required:
                console.print("[red]❌ 此项不能为空[/red]")
            else:
                return None
    
    def get_validated_input(self, prompt: str, validator: Callable[[str], bool], 
                          error_message: str, default: str = None) -> str:
        """
        获取经过验证的输入
        
        Args:
            prompt: 提示信息
            validator: 验证函数
            error_message: 错误消息
            default: 默认值
            
        Returns:
            验证通过的输入
        """
        while True:
            value = Prompt.ask(f"[cyan]{prompt}[/cyan]", default=default)
            
            if validator(value):
                return value
            
            console.print(f"[red]❌ {error_message}[/red]")
    
    def get_domain_input(self, prompt: str = "域名", default: str = None) -> str:
        """
        获取域名输入
        
        Args:
            prompt: 提示信息
            default: 默认值
            
        Returns:
            有效的域名
        """
        return self.get_validated_input(
            prompt,
            self.validation_utils.validate_domain,
            "请输入有效的域名（如：mc.example.com）",
            default
        )
    
    def get_ip_input(self, prompt: str = "IP 地址", default: str = None) -> str:
        """
        获取 IP 地址输入
        
        Args:
            prompt: 提示信息
            default: 默认值
            
        Returns:
            有效的 IP 地址
        """
        return self.get_validated_input(
            prompt,
            self.validation_utils.validate_ip_address,
            "请输入有效的 IP 地址",
            default
        )
    
    def get_port_input(self, prompt: str = "端口号", default: str = None) -> int:
        """
        获取端口号输入
        
        Args:
            prompt: 提示信息
            default: 默认值
            
        Returns:
            有效的端口号
        """
        port_str = self.get_validated_input(
            prompt,
            self.validation_utils.validate_port,
            "请输入有效的端口号 (1-65535)",
            default
        )
        return int(port_str)
    
    def get_config_name_input(self, prompt: str = "配置名称") -> str:
        """
        获取配置名称输入
        
        Args:
            prompt: 提示信息
            
        Returns:
            有效的配置名称
        """
        return self.get_validated_input(
            prompt,
            self.validation_utils.validate_config_name,
            "配置名称只能包含字母、数字、下划线和连字符",
            None
        )
    
    def get_choice_input(self, prompt: str, choices: List[str], default: str = None) -> str:
        """
        获取选择输入
        
        Args:
            prompt: 提示信息
            choices: 可选项列表
            default: 默认值
            
        Returns:
            用户选择
        """
        return Prompt.ask(
            f"\n[bold cyan]{prompt}[/bold cyan]",
            choices=choices,
            default=default
        )
    
    def get_confirmation(self, prompt: str, default: bool = True) -> bool:
        """
        获取确认输入
        
        Args:
            prompt: 提示信息
            default: 默认值
            
        Returns:
            用户确认结果
        """
        return Confirm.ask(f"[cyan]{prompt}[/cyan]", default=default)
    
    def get_edge_link_input(self, prompt: str = "Edge 链接") -> str:
        """
        获取 Edge 链接输入
        
        Args:
            prompt: 提示信息
            
        Returns:
            有效的 Edge 链接
        """
        from ...backend.services.crypto_service import CryptoService
        
        return self.get_validated_input(
            prompt,
            CryptoService.validate_edge_link,
            "请输入有效的 edge:// 链接",
            None
        )
    
    def get_menu_selection(self, configs: List[str], config_type: str) -> Optional[str]:
        """
        获取菜单选择
        
        Args:
            configs: 配置列表
            config_type: 配置类型
            
        Returns:
            选择的配置名称或特殊选项
        """
        if configs:
            console.print("\n[bold yellow]选项:[/bold yellow]")
            console.print("• 输入序号选择现有配置")
            console.print("• 输入 'new' 创建新配置")
            if config_type == "client":
                console.print("• 输入 'edge' 从 Edge 链接导入配置")
            console.print("• 输入 'back' 返回主菜单")

            while True:
                choice = Prompt.ask(
                    "\n[bold cyan]请选择操作[/bold cyan]",
                    default="new"
                )

                if choice.lower() == 'back':
                    return None
                elif choice.lower() == 'new':
                    return None
                elif choice.lower() == 'edge' and config_type == "client":
                    return 'edge'

                try:
                    index = int(choice) - 1
                    if 0 <= index < len(configs):
                        return configs[index]
                    else:
                        console.print("[red]❌ 无效的序号，请重新输入[/red]")
                except ValueError:
                    valid_options = ["'new'", "'back'"]
                    if config_type == "client":
                        valid_options.append("'edge'")
                    console.print(f"[red]❌ 请输入有效的数字或 {', '.join(valid_options)}[/red]")
        else:
            console.print(f"[yellow]📝 暂无{config_type}配置[/yellow]")
            console.print("\n[bold yellow]选项:[/bold yellow]")
            console.print("• 输入 'new' 创建新配置")
            if config_type == "client":
                console.print("• 输入 'edge' 从 Edge 链接导入配置")
            console.print("• 输入 'back' 返回主菜单")
            
            while True:
                choice = Prompt.ask(
                    "\n[bold cyan]请选择操作[/bold cyan]",
                    default="new"
                )
                
                if choice.lower() == 'back':
                    return None
                elif choice.lower() == 'new':
                    return None
                elif choice.lower() == 'edge' and config_type == "client":
                    return 'edge'
                else:
                    valid_options = ["'new'", "'back'"]
                    if config_type == "client":
                        valid_options.append("'edge'")
                    console.print(f"[red]❌ 请输入 {', '.join(valid_options)}[/red]")
    
    def wait_for_enter(self, message: str = "按回车键继续") -> None:
        """
        等待用户按回车键
        
        Args:
            message: 提示消息
        """
        Prompt.ask(f"\n{message}", default="")

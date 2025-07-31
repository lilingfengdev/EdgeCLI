"""
Clipboard Utils
剪贴板工具 - 提供剪贴板操作功能
"""

from rich.console import Console

console = Console()


class ClipboardUtils:
    """剪贴板工具类"""
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """
        复制文本到剪贴板
        
        Args:
            text: 要复制的文本
            
        Returns:
            是否成功
        """
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except ImportError:
            console.print("[yellow]⚠️  pyperclip 模块未安装，无法使用剪贴板功能[/yellow]")
            console.print("[dim]提示: 运行 'pip install pyperclip' 安装剪贴板支持[/dim]")
            return False
        except Exception as e:
            console.print(f"[red]❌ 复制到剪贴板失败: {str(e)}[/red]")
            return False
    
    @staticmethod
    def get_from_clipboard() -> str:
        """
        从剪贴板获取文本
        
        Returns:
            剪贴板文本内容
        """
        try:
            import pyperclip
            return pyperclip.paste()
        except ImportError:
            console.print("[yellow]⚠️  pyperclip 模块未安装，无法使用剪贴板功能[/yellow]")
            return ""
        except Exception as e:
            console.print(f"[red]❌ 从剪贴板读取失败: {str(e)}[/red]")
            return ""
    
    @staticmethod
    def copy_with_feedback(text: str, description: str = "文本") -> bool:
        """
        复制文本到剪贴板并显示反馈
        
        Args:
            text: 要复制的文本
            description: 描述信息
            
        Returns:
            是否成功
        """
        if ClipboardUtils.copy_to_clipboard(text):
            console.print(f"[green]✅ {description}已复制到剪贴板[/green]")
            return True
        else:
            console.print(f"[yellow]💡 请手动复制以下{description}:[/yellow]")
            console.print(f"[dim]{text}[/dim]")
            return False
    
    @staticmethod
    def copy_with_simple_feedback(text: str, description: str = "内容") -> bool:
        """
        简化版复制功能，减少用户交互
        
        Args:
            text: 要复制的文本
            description: 描述信息
            
        Returns:
            是否成功
        """
        if ClipboardUtils.copy_to_clipboard(text):
            console.print(f"[green]✅ {description}已复制到剪贴板[/green]")
            return True
        else:
            console.print(f"[yellow]⚠️ 自动复制失败，请手动复制{description}[/yellow]")
            return False

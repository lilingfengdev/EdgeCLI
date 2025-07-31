"""
EdgeCLI Frontend Module
前端模块 - 用户界面和交互逻辑
"""

__version__ = "1.0.0"
__author__ = "EdgeCLI Team"

# 导出主要的前端组件
from .cli.main_cli import MainCLI
from .cli.server_cli import ServerCLI
from .cli.client_cli import ClientCLI

from .ui.display import Display
from .ui.input_handler import InputHandler
from .ui.menu import Menu

__all__ = [
    'MainCLI',
    'ServerCLI',
    'ClientCLI',
    'Display',
    'InputHandler',
    'Menu'
]

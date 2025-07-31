#!/usr/bin/env python3
"""
EdgeCLI - Minecraft 代理工具
基于 XRay 的高性能 Minecraft 代理解决方案
"""

import sys
import os
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from edgecli.frontend.cli.main_cli import main

if __name__ == "__main__":
    main()

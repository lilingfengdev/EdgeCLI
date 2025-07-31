#!/usr/bin/env python3
"""
EdgeCLI Build Script
使用 Nuitka 构建 EdgeCLI 可执行文件
"""

import os
import sys
import argparse
import subprocess
import shutil
import platform
from pathlib import Path


def detect_platform() -> str:
    """
    自动检测当前平台

    Returns:
        平台名称 (windows/linux/macos)
    """
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    else:
        raise ValueError(f"不支持的平台: {system}")


def get_nuitka_args(target_platform: str, version: str, enable_upx: bool = True) -> list:
    """
    获取 Nuitka 构建参数

    Args:
        target_platform: 目标平台 (windows/linux/macos)
        version: 版本号
        enable_upx: 是否启用 UPX 压缩

    Returns:
        Nuitka 参数列表
    """
    args = [
        sys.executable, "-m", "nuitka",
        # 基本设置
        "--standalone",
        "--onefile",
        "--assume-yes-for-downloads",

        # 输出设置
        "--output-dir=dist",
        "--output-filename=EdgeCLI",

        # 包含必要的模块
        "--include-package=edgecli",

        # 优化设置
        "--enable-plugin=anti-bloat",
        "--show-anti-bloat-changes",
        "--noinclude-pytest-mode=nofollow",
        "--noinclude-setuptools-mode=nofollow",

        # 入口文件
        "main.py"
    ]

    # UPX 压缩设置
    if enable_upx:
        args.extend([
            "--enable-plugin=upx"
        ])

    # 平台特定设置
    if target_platform == "windows":
        args.extend([
            "--msvc=latest",
            "--windows-console-mode=disable",
            "--windows-icon-from-ico=assets/icon.ico" if Path("assets/icon.ico").exists() else None
        ])
        # 移除 None 值
        args = [arg for arg in args if arg is not None]

    elif target_platform == "linux":
        args.extend([
            "--linux-onefile-icon=assets/icon.png" if Path("assets/icon.png").exists() else None
        ])
        # 移除 None 值
        args = [arg for arg in args if arg is not None]

    elif target_platform == "macos":
        args.extend([
            "--macos-app-icon=assets/icon.icns" if Path("assets/icon.icns").exists() else None,
            "--macos-create-app-bundle"
        ])
        # 移除 None 值
        args = [arg for arg in args if arg is not None]

    return args


def clean_build_dir():
    """清理构建目录"""
    build_dirs = ["build", "dist", "EdgeCLI.build", "EdgeCLI.dist", "EdgeCLI.onefile-build"]

    for build_dir in build_dirs:
        if Path(build_dir).exists():
            print(f"🧹 清理目录: {build_dir}")
            shutil.rmtree(build_dir)


def create_dist_dir():
    """创建输出目录"""
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    return dist_dir


def build_with_nuitka(target_platform: str, version: str, enable_upx: bool = True) -> bool:
    """
    使用 Nuitka 构建项目

    Args:
        target_platform: 目标平台
        version: 版本号
        enable_upx: 是否启用 UPX 压缩

    Returns:
        构建是否成功
    """
    print(f"🔨 开始构建 EdgeCLI {version} for {target_platform}")
    if enable_upx:
        print("📦 启用 UPX 压缩")

    # 获取构建参数
    nuitka_args = get_nuitka_args(target_platform, version, enable_upx)

    print("📋 Nuitka 构建参数:")
    for arg in nuitka_args:
        if arg.startswith("--"):
            print(f"  {arg}")

    # 执行构建
    try:
        print("\n🚀 执行 Nuitka 构建...")
        subprocess.run(nuitka_args, check=True, text=True, stdout=sys.stdout)
        print("✅ Nuitka 构建成功!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Nuitka 构建失败!")
        print(f"错误代码: {e.returncode}")
        print(f"错误输出: {e.stderr}")
        return False


def verify_build(target_platform: str) -> bool:
    """
    验证构建结果

    Args:
        target_platform: 目标平台

    Returns:
        验证是否成功
    """
    executable_name = "EdgeCLI.exe" if target_platform == "windows" else "EdgeCLI"
    executable_path = Path("dist") / executable_name

    if not executable_path.exists():
        print(f"❌ 可执行文件不存在: {executable_path}")
        return False

    # 检查文件大小
    file_size = executable_path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)

    print(f"📊 构建结果:")
    print(f"  文件路径: {executable_path}")
    print(f"  文件大小: {file_size_mb:.2f} MB")

    # 基本的可执行性测试
    if target_platform != "windows":
        # 在非 Windows 平台上设置执行权限
        os.chmod(executable_path, 0o755)

    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="EdgeCLI 构建脚本")
    parser.add_argument("--version", required=True, help="版本号")
    parser.add_argument("--clean", action="store_true", help="构建前清理")
    parser.add_argument("--no-upx", action="store_true", help="禁用 UPX 压缩")

    args = parser.parse_args()

    # 自动检测平台
    current_platform = detect_platform()

    print(f"🎯 EdgeCLI 构建脚本")
    print(f"检测到平台: {current_platform}")
    print(f"版本: {args.version}")
    print(f"UPX 压缩: {'禁用' if args.no_upx else '启用'}")
    print("-" * 50)

    # 清理构建目录
    if args.clean:
        clean_build_dir()

    # 创建输出目录
    create_dist_dir()

    # 执行构建
    enable_upx = not args.no_upx
    if not build_with_nuitka(current_platform, args.version, enable_upx):
        sys.exit(1)

    # 验证构建结果
    if not verify_build(current_platform):
        sys.exit(1)

    print("\n🎉 构建完成!")


if __name__ == "__main__":
    main()

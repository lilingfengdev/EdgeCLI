"""
XRay Manager
XRay 管理器 - 负责 XRay 二进制文件的下载、管理和进程控制
"""

import os
import subprocess
import requests
import zipfile
import tarfile
from pathlib import Path
from typing import Optional
import signal
import time

from ..utils.system_utils import SystemUtils


class XRayManager:
    """XRay 管理器"""
    
    def __init__(self, bin_dir: str = "bin"):
        """
        初始化 XRay 管理器
        
        Args:
            bin_dir: 二进制文件目录
        """
        self.system_utils = SystemUtils()
        self.platform, self.arch = self.system_utils.get_platform()
        self.bin_dir = Path(bin_dir)
        self.bin_dir.mkdir(exist_ok=True)
        
        # XRay 二进制文件名
        if self.platform == "windows":
            self.xray_binary = self.bin_dir / "xray.exe"
        else:
            self.xray_binary = self.bin_dir / "xray"
        
        self.xray_process = None
        
    def check_xray_binary(self) -> bool:
        """
        检查 XRay 二进制文件是否存在且可执行
        
        Returns:
            是否存在且可执行
        """
        if not self.xray_binary.exists():
            return False
        
        # 检查是否可执行
        if self.platform != "windows":
            return os.access(self.xray_binary, os.X_OK)
        
        return True
    
    def get_download_url(self) -> str:
        """
        根据平台获取 XRay 下载 URL
        
        Returns:
            下载 URL
        """
        base_url = "https://github.com/XTLS/Xray-core/releases/latest/download/"
        
        if self.platform == "windows":
            if self.arch == "64":
                return f"{base_url}Xray-windows-64.zip"
            else:
                return f"{base_url}Xray-windows-32.zip"
        elif self.platform == "macos":
            return f"{base_url}Xray-macos-64.zip"
        elif self.platform == "linux":
            if self.arch == "64":
                return f"{base_url}Xray-linux-64.zip"
            elif self.arch == "arm64":
                return f"{base_url}Xray-linux-arm64-v8a.zip"
            elif self.arch == "arm32":
                return f"{base_url}Xray-linux-arm32-v7a.zip"
            else:
                return f"{base_url}Xray-linux-32.zip"
        else:
            raise ValueError(f"不支持的平台: {self.platform}")
    
    def download_xray(self, progress_callback=None) -> bool:
        """
        下载 XRay 二进制文件
        
        Args:
            progress_callback: 进度回调函数
            
        Returns:
            是否成功
        """
        try:
            download_url = self.get_download_url()
            
            # 下载文件
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            # 保存到临时文件
            temp_file = self.bin_dir / "xray_temp.zip"
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)
            
            # 解压文件
            self._extract_xray(temp_file)
            
            # 删除临时文件
            temp_file.unlink()
            
            # 设置执行权限（非 Windows）
            if self.platform != "windows":
                os.chmod(self.xray_binary, 0o755)
            
            return True
            
        except Exception as e:
            return False
    
    def _extract_xray(self, archive_path: Path) -> None:
        """
        解压 XRay 文件
        
        Args:
            archive_path: 压缩文件路径
        """
        if archive_path.suffix == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                # 查找 xray 可执行文件
                for file_info in zip_ref.filelist:
                    if file_info.filename.endswith(('xray', 'xray.exe')):
                        # 提取到指定位置
                        with zip_ref.open(file_info) as source:
                            with open(self.xray_binary, 'wb') as target:
                                target.write(source.read())
                        break
        else:
            # 处理 tar.gz 文件
            with tarfile.open(archive_path, 'r:gz') as tar_ref:
                for member in tar_ref.getmembers():
                    if member.name.endswith(('xray', 'xray.exe')):
                        tar_ref.extract(member, self.bin_dir)
                        # 重命名为标准名称
                        extracted_path = self.bin_dir / member.name
                        extracted_path.rename(self.xray_binary)
                        break
    
    def start_xray(self, config_path: str) -> bool:
        """
        启动 XRay 进程
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            是否成功启动
        """
        if not self.check_xray_binary():
            return False
        
        try:
            # 构建命令
            cmd = [str(self.xray_binary), "run", "-config", config_path]
            
            # 启动进程
            self.xray_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.bin_dir.parent)
            )
            
            # 等待一小段时间检查是否启动成功
            time.sleep(1)
            
            if self.xray_process.poll() is None:
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def stop_xray(self) -> bool:
        """
        停止 XRay 进程
        
        Returns:
            是否成功停止
        """
        if self.xray_process is None:
            return True
        
        try:
            # 发送终止信号
            if self.platform == "windows":
                self.xray_process.terminate()
            else:
                self.xray_process.send_signal(signal.SIGTERM)
            
            # 等待进程结束
            try:
                self.xray_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # 强制杀死进程
                self.xray_process.kill()
                self.xray_process.wait()
            
            self.xray_process = None
            return True
            
        except Exception as e:
            return False
    
    def is_running(self) -> bool:
        """
        检查 XRay 是否正在运行
        
        Returns:
            是否正在运行
        """
        if self.xray_process is None:
            return False
        
        return self.xray_process.poll() is None
    
    def get_version(self) -> Optional[str]:
        """
        获取 XRay 版本
        
        Returns:
            版本字符串或 None
        """
        if not self.check_xray_binary():
            return None
        
        try:
            result = subprocess.run(
                [str(self.xray_binary), "version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # 解析版本信息
                for line in result.stdout.split('\n'):
                    if 'Xray' in line and 'version' in line:
                        return line.strip()
            
            return None
            
        except Exception:
            return None

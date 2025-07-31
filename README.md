# EdgeCLI - Minecraft 代理工具

EdgeCLI 是一个专为 Minecraft 设计的高性能代理工具，基于 XRay 核心技术，提供稳定、安全的游戏连接体验。

## ✨ 功能特性

- **🎮 专为 Minecraft 优化**: 针对 MC 游戏流量特点进行优化
- **🖥️ 双模式运行**: 支持服务端和客户端模式，满足不同使用场景
- **🔧 交互式配置**: 全中文交互界面，无需复杂命令行参数
- **🔐 自动安全配置**: 自动生成 UUID、证书等安全凭据
- **🌐 DNS 智能配置**: 通过 DNS TXT 记录实现客户端自动配置
- **📱 跨平台支持**: 支持 Windows、macOS 和 Linux
- **⚡ 自动部署**: 自动下载和配置 XRay 核心文件
- **🎨 美观界面**: 使用 Rich 库提供现代化的命令行界面

## 🚀 快速开始

### 安装步骤

1. **下载项目**
   ```bash
   git clone https://github.com/your-repo/EdgeCLI.git
   cd EdgeCLI
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动程序**
   ```bash
   python main.py
   ```

### 基本使用

程序启动后会显示交互式菜单，按照提示操作即可：

```
╭─────────────────────────────────────────╮
│        EdgeCLI - Minecraft 代理工具        │
│         基于 XRay 的高性能代理解决方案         │
╰─────────────────────────────────────────╯

┌─────────────────── 主菜单 ───────────────────┐
│  1    🖥️  服务端模式 - 创建 Minecraft 代理服务器  │
│  2    💻 客户端模式 - 连接到代理服务器           │
│  3    ⚙️  工具设置                          │
│  0    ❌ 退出程序                           │
└─────────────────────────────────────────────┘
```

## 服务端模式

服务端模式用于创建和运行 XRay 服务器。

### 配置步骤

1. 选择运行模式为 "服务端"
2. 选择现有配置或创建新配置
3. 如果创建新配置，需要输入:
   - 配置名称
   - 前端绑定域名或IP地址
   - 后端IP地址和端口 (默认: 127.0.0.1:25565)

### 生成的配置

服务端会自动生成:
- UUID (客户端ID)
- 自签名TLS证书
- XRay 服务端配置文件
- DNS TXT 记录内容

### DNS 设置

服务端启动后会显示需要设置的 DNS TXT 记录，格式如下:

```
记录类型: TXT
主机记录: _auth.yourdomain.com
记录值: v=edgecli1; {"id":"uuid","domain":"yourdomain.com","protocol":"vless","port":443,"path":"/mcproxy"}
```

## 客户端模式

客户端模式用于连接到 XRay 服务器。

### 配置步骤

1. 选择运行模式为 "客户端"
2. 选择现有配置或创建新配置
3. 如果创建新配置，需要输入:
   - 配置名称
   - 远程域名
   - 本地监听端口 (默认: 25565)

### 自动配置

客户端会自动:
- 查询 `_auth.<域名>` 的 DNS TXT 记录
- 解析服务端配置信息
- 生成对应的客户端配置
- 启动本地代理

## 目录结构

```
EdgeCLI/
├── main.py              # 程序入口
├── requirements.txt     # Python 依赖
├── README.md           # 说明文档
├── edgecli/            # 主程序包
│   ├── __init__.py
│   ├── cli.py          # CLI 界面
│   ├── server.py       # 服务端管理
│   ├── client.py       # 客户端管理
│   ├── config.py       # 配置管理
│   ├── xray_manager.py # XRay 进程管理
│   ├── crypto_utils.py # 加密工具
│   ├── dns_utils.py    # DNS 工具
│   └── utils.py        # 通用工具
├── configs/            # 配置文件目录
├── logs/              # 日志目录
└── bin/               # XRay 二进制文件目录
```

## 依赖项

- click: 命令行界面
- colorama: 颜色支持
- cryptography: 证书生成
- dnspython: DNS 查询
- requests: HTTP 请求
- pyyaml: YAML 配置
- rich: 美观的命令行界面

## 注意事项

1. 首次运行时会自动下载对应平台的 XRay 二进制文件
2. 服务端需要在防火墙中开放 443 端口
3. DNS TXT 记录设置后可能需要几分钟到几小时生效
4. 建议在生产环境中使用有效的 TLS 证书

## 🔧 开发和构建

### 本地开发

1. **克隆项目**
   ```bash
   git clone https://github.com/lilingfengdev/EdgeCLI.git
   cd EdgeCLI
   ```

2. **安装开发依赖**
   ```bash
   pip install -r requirements.txt
   pip install nuitka
   ```

3. **运行项目**
   ```bash
   python main.py
   ```

### 构建可执行文件

使用 Nuitka 构建单文件可执行程序：

```bash
# Windows
python build.py --platform windows --version v1.0.0

# Linux
python build.py --platform linux --version v1.0.0

# macOS
python build.py --platform macos --version v1.0.0
```

### 自动化构建

项目使用 GitHub Actions 进行自动化构建：

- **正式发布**: 推送 tag（如 `v1.0.0`）时自动构建并发布到 Releases
- **Preview 版本**: 每次提交代码时自动构建 preview 版本
- **手动构建**: 在 Actions 页面手动触发构建

#### 发布流程

1. **创建正式版本**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Preview 版本**: 直接推送任何代码到任何分支即可自动构建 preview 版本

### 构建特性

- ✅ **Nuitka 编译**: 将 Python 代码编译为原生可执行文件，启动更快
- ✅ **UPX 压缩**: 使用 UPX 压缩可执行文件，减小体积
- ✅ **多平台支持**: 自动构建 Windows、Linux、macOS 版本
- ✅ **自动发布**: 构建完成后自动发布到 GitHub Releases
- ✅ **Preview 管理**: 自动清理旧的 preview 版本，保持仓库整洁

## 许可证

本项目基于 MIT 许可证开源。

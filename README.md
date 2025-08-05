# EdgeCLI - Minecraft 代理工具

基于 XRay 的 Minecraft 代理工具，将 MC TCP/UDP 流量通过 XHTTP 协议转换为 HTTP 流量，实现通过 CDN 加速游戏连接。

## 快速开始

```bash
# 直接运行
python main.py

# 或先安装依赖
pip install -r requirements.txt
python main.py
```

## 工作原理

使用 XRay 的 **XHTTP 协议**，将 Minecraft TCP 流量伪装成标准 HTTP 请求：

- **服务端**：接收 XHTTP 流量，解包后转发给 MC 服务器
- **客户端**：将 MC 连接封装为 XHTTP 流量发送给服务端
- **自动配置**：通过 DNS TXT 记录或 `edge://` 链接自动获取连接配置

## 使用方法

### 服务端部署

1. 运行程序选择"服务端模式"
2. 创建新配置，输入：
   - 配置名称
   - 前端域名（用于客户端连接）
   - 后端 MC 服务器地址（默认 127.0.0.1:25565）
3. 程序自动生成 UUID、TLS 证书和配置文件
4. 按提示设置 DNS TXT 记录

### 客户端连接

**方式一：DNS 自动配置**
1. 选择"客户端模式" → 创建新配置
2. 输入服务端域名，程序自动从 DNS 获取配置
3. 连接到本地代理端口（默认 25565）

**方式二：edge:// 链接**
1. 选择"客户端模式" → 从 Edge 链接创建
2. 输入 `edge://` 链接，自动解析配置
3. 连接到本地代理端口

### DNS 记录格式

```
记录类型: TXT
主机记录: _auth.yourdomain.com
记录值: v=edgecli1; {"id":"uuid","domain":"yourdomain.com","protocol":"vless","port":443,"path":"/mcproxy"}
```

## 注意事项

- 首次运行自动下载 XRay 核心文件
- 服务端需要开放 443 端口
- DNS 记录生效需要 5-30 分钟

## 开发构建

```bash
git clone https://github.com/lilingfengdev/EdgeCLI.git
cd EdgeCLI
pip install -r requirements.txt
python main.py

# 构建可执行文件
python build.py --platform windows --version v1.0.0
```

## 许可证

MIT License

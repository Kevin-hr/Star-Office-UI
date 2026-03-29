# Star Office UI (正式版 - 星案像素办公室)

一个为你的 AI 助手打造的微型“像素办公室”状态可视化界面。

- **像素风办公室背景**（俯视角度）
- **智能小人**：根据 `state` 在不同区域移动
- **动态效果**：可选的说话气泡 / 打字机效果
- **公网访问**：通过 Cloudflare Tunnel (quick tunnel) 支持手机端远程查看

> **语言提示**：本项目的发展代码和文档以中文为主。欢迎 PR 提供多语言支持。

## 视觉处理逻辑

- `idle / syncing / error` → **休息区** (breakroom)
- `writing / researching / executing` → **工作台** (desk area)

前端 UI 通过轮询 `/status` 接口，自动调度助手的点击位置和动作。

## 目录结构

```
star-office-ui/
  backend/        # Flask 后端 (服务 index + status)
  frontend/       # Phaser 前端 + office_bg.png 资产
  workspace/
    state.json    # 运行时状态文件
  set_state.py    # 状态更新辅助脚本
```

## 环境要求

- Python 3.9+
- Flask

## 快速开始 (本地)

### 1) 安装依赖

```bash
pip install flask
```

### 2) 准备背景图

将一张 **800×600** 的 PNG 图片放在：

```
star-office-ui/frontend/office_bg.png
```

### 3) 启动后端

```bash
cd star-office-ui/backend
python app.py
```

然后访问：

- http://127.0.0.1:18888

### 4) 更新状态

在项目根目录下执行：

```bash
python3 set_state.py writing "正在整理文档..."
python3 set_state.py idle "待命ing..."
```

## 公网访问 (Cloudflare quick tunnel)

安装 `cloudflared` 后，执行：

```bash
cloudflared tunnel --url http://127.0.0.1:18888
```

你将获得一个 `https://xxx.trycloudflare.com` 的地址，手机即可移动观测。

## 安全警示

- 任何拥有 Tunnel URL 的人都可以读取 `/status`。
- **请勿**在 `detail` 字段中放入敏感信息。
- 如需进一步安全，请为 `/status` 添加 Token 验证或限制返回数据。

## 开源许可

MIT

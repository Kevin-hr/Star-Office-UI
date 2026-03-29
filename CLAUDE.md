# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

Star Office UI is a pixel-art "office" visualization for AI assistants — a top-down pixel office with animated characters that move between areas based on state.

## Architecture

```
Star-Office-UI/
├── backend/app.py       # Flask 后端（提供 index.html + /status API）
├── frontend/index.html  # Phaser 3 前端（像素游戏渲染）
├── frontend/office_bg.png  # 背景图 (800×600 PNG)
├── frontend/shadowfiend.png # 主角图标
├── set_state.py        # 状态更新命令行工具
├── workspace/state.json # 运行时状态（自动生成，不在版本控制）
└── state.sample.json   # 状态文件模板
```

### 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Flask (Python 3.9+) |
| 前端 | Phaser 3 (CDN) |
| 状态存储 | JSON 文件 |

### 核心逻辑

| 文件:行 | 功能 |
|---------|------|
| `frontend/index.html:138-145` | STATES 定义（6状态 → 区域/颜色映射） |
| `frontend/index.html:147-154` | BUBBLE_TEXTS（状态对应气泡文案） |
| `frontend/index.html:156-160` | 关键时序常量（FETCH_INTERVAL=3s, BLINK_INTERVAL=2.5s） |
| `frontend/index.html:188-191` | 区域坐标（workdesk: 260,340 / breakroom: 660,170） |
| `frontend/index.html:193-223` | 角色创建（1个主角 + 5个同事星星） |
| `frontend/index.html:229-260` | 星星纹理生成（睁眼/闭眼） |
| `frontend/index.html:319-379` | moveStar() 移动逻辑 + 同事动画 |
| `frontend/index.html:382-398` | showBubble() 气泡系统 |
| `backend/app.py:73-82` | `/hero_asset` 代理（从 Steam CDN 获取 Shadow Fiend） |

### 状态与区域映射

| 状态 | 区域 | 位置 |
|------|------|------|
| `idle`, `syncing`, `error` | breakroom | (660, 170) |
| `writing`, `researching`, `executing` | workdesk | (260, 340) |

### 动态效果

- **打字机**：状态面板逐字显示，40ms/字符
- **气泡**：8秒间隔显示随机气泡文案
- **眨眼**：2.5秒间隔，所有星星同步眨眼
- **悬浮**：主角轻微上下浮动 (sin/400)
- **移动**：主角和5个同事在各区域随机游走

## Commands

### 启动后端

```bash
cd backend
pip install flask requests
python app.py
# http://127.0.0.1:18888
```

### 更新状态

```bash
python set_state.py <state> [detail]
```

**有效状态**：`idle`, `writing`, `researching`, `executing`, `syncing`, `error`

### 公网访问

```bash
cloudflared tunnel --url http://127.0.0.1:18888
```

## State API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 返回 index.html |
| `/status` | GET | 返回当前状态 JSON |
| `/shadowfiend.png` | GET | 直接提供主角图标 |
| `/hero_asset` | GET | 代理 Steam CDN 角色图（绕过 CORS） |
| `/health` | GET | 健康检查 |

**状态 JSON 格式**：
```json
{
  "state": "idle",
  "detail": "等待任务中...",
  "progress": 0,
  "updated_at": "2026-02-28T12:00:00"
}
```

## Notes

- `backend/app.py:100` 端口配置（默认 18888）
- 背景图 `frontend/office_bg.png` 需要 800×600 PNG，不存在时显示占位符
- `workspace/state.json` 不在版本控制中
- `/hero_asset` 端点需要 `requests` 库

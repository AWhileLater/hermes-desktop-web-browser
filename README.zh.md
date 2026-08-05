# Web Browser Plugin

一款 **Hermes Desktop 插件**，在 Hermes 中嵌入 webview 浏览器面板，无需切换窗口即可直接浏览网页。同时支持页面标注：标记网页元素并添加说明，一键发送给 AI agent 自动定位修改。

[English](README.md)

![Hermes Desktop Web Browser Plugin](screenshot.png)

## 功能

- **嵌入式浏览器** -- 它就是一款嵌入 Hermes 的浏览器：多标签页、地址栏、前进/后退、收藏夹等
- **页面标注** -- 标记页面元素并添加说明，支持快捷标签，一键发送给 AI agent 自动定位修改（详见 [Annotator](#annotator页面标注)）
- **缓存控制** -- 设置中可禁用浏览器缓存（新标签页走非持久化会话），并可清理缓存

## Annotator（页面标注）

可视化的「页面标注 → 自动修改」工作流：在页面上标记任意元素，把标注发送给你的 AI agent，agent 会自动定位到对应的代码并按你的说明进行修改 —— 无论是修 bug、调整样式、修改布局还是添加新功能都可以。你只需要说"改什么"，不用描述"在哪、怎么改"。

### 使用方法

1. 点击工具栏的画笔按钮进入标注模式
2. 点击页面上需要改动/调整/修复的元素 -- 弹出说明输入框
3. 输入需要做什么修改（或点快捷标签），保存
4. 复制提示词（或提示词+标注截图）发送给 agent / 粘贴到对话
5. agent 会精确定位到问题元素，并根据你输入的说明在代码中进行修改

### agent 为什么能精确定位

每条标注都携带精确的定位信息 -- **selector**、**domPath**、**text**、**position**，以及页面 URL 和视口。agent 依据这些信息在项目源码中定位到对应元素，并执行你的修改指令。你只需要描述要改什么，"在哪里改"交给 agent。

### 快捷标签

快捷标签可自动填入常用修改指令：**Bug**、**样式**、**布局**、**功能**、**优化**、**交互**。点击标签自动填入输入框，需要时再微调。

### 复制与粘贴

- **复制到输入框按钮** -- 点击后直接复制到 Hermes 对话输入框
- **复制提示词** -- 结构化文本（修改指令 + 定位信息），可直接发送给 agent
- **复制提示词+截图** -- 附带带编号气泡的页面截图，提示词中会包含截图说明

### 标注管理

标注面板列出全部标注，支持编辑 / 删除 / 清空。每条标注在页面上保持红色气泡高亮，滚动时气泡与区域会跟随页面元素移动。

### 设置项

- **复制时附带截图** -- 默认开启，截图用于提供辅助定位（帮助 agent 在视觉上确认目标元素）。如果模型不支持视觉（图片分析），可以关闭：关闭后不执行截图，提示词也不包含截图说明。元素定位不依赖视觉 -- 标注的 selector / domPath / text 已足够 agent 定位到对应元素。
- **快捷标注标签** -- 关闭后标注弹窗中不显示标签行

### 实现原理

标注引擎通过 `executeJavaScript` 注入到每个页面，与插件通过 `console-message` 桥通信（`__ANNO__` 前缀），并有轮询兜底。

## 安装

### 前提条件

- [Hermes Agent](https://hermes-agent.nousresearch.com) Desktop 版本（插件在 CLI 模式下不可用）

### 安装步骤

**方式 A -- 让 Hermes 帮你安装（推荐）**

直接复制下面这行，发给你的 Hermes Agent 即可：

```
帮我安装这个 Hermes Desktop 插件：https://github.com/AWhileLater/hermes-desktop-web-browser
```

一句话搞定，Hermes 会自动克隆仓库并配置好。

**方式 B -- 手动安装**

```bash
git clone https://github.com/AWhileLater/hermes-desktop-web-browser.git
cp -r hermes-desktop-web-browser ~/.hermes/desktop-plugins/hermes-desktop-web-browser
```

两种方式完成后，在命令面板（`Ctrl+K`）中运行 **Reload desktop plugins** 重新加载即可。

## 使用说明

1. 点击 Hermes Desktop 状态栏中的地球图标，或按下 `Ctrl+Shift+B` 打开浏览器面板
2. 在地址栏输入 URL 并回车
3. 使用工具栏按钮进行后退/前进/刷新；右键标签页可关闭/重载/复制 URL
4. 点击星标将当前页面加入收藏夹
5. 使用画笔按钮标注：点击页面元素、填写说明（或点快捷标签），然后复制到剪贴板或粘贴到对话
6. 打开设置（汉堡菜单 > 插件设置）：
   - **浏览器**：禁用浏览器缓存（开发用，新标签页走非持久化会话）、清理缓存
   - **标注**：复制时附带截图（关闭后不截图、提示词也不含截图部分）、快捷标注标签

## 项目结构

```
hermes-desktop-web-browser/
├── plugin.js             # 主插件文件 -- 纯 ESM JavaScript
├── script/
│   └── clear_cache.py    # 清理缓存脚本（删除插件分区的磁盘缓存）
├── README.md             # 英文文档
├── README.zh.md          # 中文文档（本文件）
├── LICENSE               # MIT 许可证
└── screenshot.png        # 运行截图
```

## 开发

插件是纯 ESM JavaScript，无需构建步骤。修改 `plugin.js` 后保存即热重载。

### 约定

- 插件 ID: `hermes-desktop-web-browser`
- 导出格式: `export default { id, name, register(ctx) }`
- 依赖仅限 `@hermes/plugin-sdk` 和 `react`

## 许可证

MIT

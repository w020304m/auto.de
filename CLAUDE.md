# PSEO Germany Handwerker - 开发者指南

> **文档版本**: v2.0 Professional Edition
> **最后更新**: 2025-01-10
> **状态**: 已更新 - 遵循 [README.md](./README.md) 核心参数

---

## 文档导航

| 文档 | 用途 |
|------|------|
| [README.md](./README.md) | ⭐ 项目索引和核心参数定义 |
| [blueprint.md](./blueprint.md) | ⭐⭐ 完整执行指南（实施权威） |
| [tasks.md](./tasks.md) | 详细任务清单 |
| **本文档** | 开发者规范和代码约定 |

---

## 核心参数（必须严格遵守）

```yaml
# Phase 1 配置
phase_1:
  cities: 30              # 城市（人口>50,000）
  services: 4             # 核心服务
  modifiers: 3            # Modifier（初期：主词、kosten、notdienst）
  total_pages: 360        # 30 × 4 × 3
  methodology: "零AI"     # 模板 + 数据，无需AI调用

# 6个Modifier（Phase 2+ 完整策略）
all_modifiers:
  - ""                    # 主词
  - "kosten"              # 成本
  - "preis"               # 价格
  - "notdienst"           # 紧急（最高CPC 3-5x）
  - "empfehlung"          # 推荐
  - "in-der-naehe"        # 附近
```

---

## 项目核心概念

这是一个**程序化SEO（Programmatic SEO）**项目。

### 核心公式
```
页面数量 = 城市数量 × 服务类型数量 × Modifier数量

Phase 1: 30 城市 × 4 服务 × 3 Modifier = 360 页面
Phase 2: 100 城市 × 8 服务 × 4 Modifier = 3,200 页面
Phase 3: 500 城市 × 8 服务 × 6 Modifier = 24,000 页面

自动化程度 = 100%（脚本自动化）
人工干预 = 接近零（仅初始配置）
```

### 零AI方法论（Phase 1）

```
Phase 1 不需要 AI：

├── 真实数据（OpenPLZ） ✅
├── HTML 模板（Jinja2） ✅
├── 预设 FAQ（按Modifier） ✅
├── Schema.org 结构化数据 ✅
└── AI 生成 ❌（Phase 2+ 可选）
```

**为什么零AI？**
- 成本：$0（无需API调用）
- 速度：秒级生成360页
- 可控：完全可预测的内容
- 合规：避免AI内容检测风险

---

## 技术栈约定

### 核心技术栈
| 技术 | 版本要求 | 用途 |
|------|---------|------|
| Python | 3.11+ | 脚本自动化 |
| Jinja2 | 3.1+ | HTML模板渲染 |
| requests | 2.31+ | API调用（OpenPLZ） |
| tqdm | 4.66+ | 进度条显示 |

### Python虚拟环境管理（必须遵守）

**⚠️ 重要**: 运行任何Python脚本前，必须先检查并激活虚拟环境。

#### 虚拟环境检查和激活流程

```bash
# 步骤1: 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "虚拟环境不存在，正在创建..."
    python -m venv venv
fi

# 步骤2: 激活虚拟环境
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 步骤3: 安装/更新依赖包
pip install -r requirements.txt

# 步骤4: 运行Python脚本
python scripts/your_script.py
```

#### 添加新Python依赖时的流程

```bash
# 1. 激活虚拟环境
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac

# 2. 安装新依赖
pip install package_name

# 3. 更新requirements.txt（必须！）
pip freeze > requirements.txt

# 4. 验证requirements.txt已更新
cat requirements.txt
```

#### 自动化脚本（推荐）

创建 `scripts/ensure_venv.sh`（Linux/Mac）或 `scripts/ensure_venv.bat`（Windows）:

```bash
# scripts/ensure_venv.bat (Windows)
@echo off
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
```

```bash
# scripts/ensure_venv.sh (Linux/Mac)
#!/bin/bash
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
```

#### 虚拟环境文件约定

```
pseo-handwerker/
├── venv/                 # 虚拟环境目录（必须在.gitignore中）
├── requirements.txt      # 依赖列表（必须提交）
├── requirements.lock     # 锁定版本（可选，用于生产环境）
└── scripts/
    ├── ensure_venv.bat   # Windows虚拟环境脚本
    └── ensure_venv.sh    # Linux/Mac虚拟环境脚本
```

### 部署平台（免费方案）
| 服务 | 用途 | 成本 |
|------|------|------|
| Cloudflare Pages | 静态托管 | 免费 |
| GitHub | 代码仓库 + CI/CD | 免费 |
| OpenPLZ API | 城市数据 | 免费 |
| Dr. Schwenke | 法律页面生成 | 免费 |

---

## 代码规范

### 项目目录结构

```
pseo-handwerker/
├── data/
│   ├── cities.json          # OpenPLZ城市数据
│   ├── services.json        # 服务配置（4个）
│   └── modifiers.json       # Modifier配置（3→6个）
├── templates/
│   ├── page.html            # 主页面模板（零AI友好）
│   ├── impressum.html       # 法律页面
│   └── datenschutz.html     # GDPR页面
├── scripts/
│   ├── fetch_cities.py      # 数据获取
│   ├── generate_pages.py    # 零AI页面生成 ⭐
│   └── generate_sitemap.py  # Sitemap生成
├── output/
│   ├── *.html               # 生成的页面
│   └── sitemap.xml
├── .env.example
├── requirements.txt
└── README.md
```

### 文件命名约定
```
scripts/          # 所有Python脚本
  fetch_cities.py      # 数据获取脚本
  generate_pages.py    # 零AI页面生成脚本
  generate_sitemap.py  # Sitemap生成脚本

templates/        # Jinja2模板
  page.html            # 单页面模板（主要）

data/            # 静态数据
  cities.json          # 德国城市数据
  services.json        # 服务配置数据
  modifiers.json       # Modifier配置数据

output/          # 构建输出（部署到Cloudflare Pages）
  *.html              # 生成的页面
  sitemap.xml         # 站点地图
```

### Python脚本结构约定
每个脚本必须遵循以下结构：
```python
#!/usr/bin/env python3
"""
脚本用途描述
"""

import json
from pathlib import Path

# 配置常量
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")

def main_function():
    """主要功能函数"""
    pass

if __name__ == "__main__":
    main_function()
```

### 变量命名约定
- 城市相关: `city_name`, `city_slug`, `postal_code`
- 服务相关: `service_name`, `service_slug`, `price_low`, `price_high`
- Modifier相关: `modifier_key`, `modifier_data`, `faqs`
- 文件路径: 使用 `pathlib.Path`
- 编码: 所有文件读写使用 `encoding="utf-8"`

---

## 数据模型约定

### 城市数据结构（不可修改）
```python
{
    "name": "Berlin",              # 城市名称（德语）
    "slug": "berlin",              # URL slug
    "population": 3644826,         # 人口数
    "state": "Berlin",             # 联邦州
    "postalCode": "10115",         # 邮政编码
    "lat": 52.52,                  # 纬度
    "lng": 13.405                  # 经度
}
```

### 服务数据结构（不可修改）
```python
{
    "slug": "klempner",            # URL slug
    "name": "Klempner",            # 服务名称（德语）
    "price_low": 80,               # 最低价格(€/h)
    "price_medium": 120,           # 中等价格(€/h)
    "price_high": 160,             # 最高价格(€/h)
    "price_emergency": 200,        # 紧急价格(€/h)
    "services": [                  # 服务列表
        "Rohrreinigung und Verstopfungsbeseitigung",
        "Leckortung und Rohrreparatur",
        ...
    ]
}
```

### Modifier数据结构（不可修改）
```python
{
    "modifiers": {
        "": {
            "name": "main",
            "title_suffix": "",
            "focus": "Preise & Notdienst",
            "faqs": [
                {
                    "question": "...",
                    "answer": "..."
                }
            ]
        },
        "kosten": {
            "name": "kosten",
            "title_suffix": " Kosten",
            "focus": "Was Sie erwarten müssen",
            "faqs": [...]
        },
        "notdienst": {
            "name": "notdienst",
            "title_suffix": " Notdienst",
            "focus": "24/7 Verfügbar",
            "faqs": [...]
        }
    }
}
```

---

## URL结构约定

### 页面URL格式
```
https://handwerker-ratgeber.de/{service_slug}-{city_slug}{modifier_suffix}.html
```

### Slug转换规则（必须严格遵守）
```python
def slugify(text: str) -> str:
    """
    将德语文本转换为URL友好的slug
    规则:
    - 转小写
    - 空格替换为连字符
    - ä → ae, ö → oe, ü → ue, ß → ss
    """
    text = text.lower()
    text = text.replace(" ", "-")
    text = text.replace("ä", "ae")
    text = text.replace("ö", "oe")
    text = text.replace("ü", "ue")
    text = text.replace("ß", "ss")
    return text
```

### 示例URL
| 城市 | 服务 | Modifier | URL |
|------|------|----------|-----|
| Berlin | Klempner | 无 | /klempner-berlin.html |
| Berlin | Klempner | kosten | /klempner-berlin-kosten.html |
| München | Elektriker | notdienst | /elektriker-muenchen-notdienst.html |

---

## 页面模板约定

### 必须包含的SEO元素
每个生成的页面必须包含：
1. **Title标签**: 根据Modifier动态生成
2. **Meta描述**: 包含服务、城市、价格区间
3. **Canonical URL**: 指向页面的规范URL
4. **LocalBusiness Schema**: 结构化数据
5. **H1标题**: 与title一致
6. **FAQ部分**: 至少3个常见问题（Schema.org FAQPage）

### 禁止的HTML实践
- ❌ 内联事件处理器（`onclick`, `onload`等）
- ❌ 外部CSS/JS文件（全部内联或使用CDN）
- ❌ 大型图片（使用外部图床或SVG）

---

## 构建流程约定

### Phase 1 构建顺序（零AI）
```bash
# 1. 获取城市数据（OpenPLZ）
python scripts/fetch_cities.py

# 2. 生成页面（零AI，模板+数据）
python scripts/generate_pages.py

# 3. 生成sitemap
python scripts/generate_sitemap.py

# 4. 部署（Cloudflare Pages 或 GitHub Pages）
# 自动触发或手动部署
```

### 环境变量
创建 `.env` 文件（不要提交到Git）：
```bash
# Phase 1 不需要 AI 配置（零AI）

# Phase 2+ 可选：AI服务配置
# AI_PROVIDER=openai
# AI_API_KEY=sk-xxx
# AI_MODEL=gpt-4o-mini
# AI_BASE_URL=https://api.openai.com/v1
```

---

## 测试要求

### 代码修改后的必测项
1. **数据完整性**: JSON文件格式验证
2. **模板渲染**: 至少渲染3个不同页面
3. **URL生成**: 验证slug转换正确
4. **HTML有效性**: 使用W3C验证器检查
5. **SEO检查**: 验证meta标签、结构化数据

### 验证命令
```bash
# JSON格式验证
python -m json.tool data/cities.json
python -m json.tool data/services.json
python -m json.tool data/modifiers.json

# 生成测试页面
python scripts/generate_pages.py
# 检查 output/ 目录
ls output/ | wc -l  # 应该输出 360
```

---

## 常见问题处理

### 如果OpenPLZ API调用失败

**OpenPLZ API正确用法**（重要）：

```python
# ❌ 错误用法（会返回400）
url = "https://openplzapi.org/de/Localities?page=1"

# ✅ 正确用法 - 方式1: 按联邦州获取
url = "https://openplzapi.org/de/FederalStates/01/Localities"  # 石勒苏益格-荷尔斯泰因

# ✅ 正确用法 - 方式2: 按邮编搜索
url = "https://openplzapi.org/de/Localities?postalCode=10115"

# ✅ 正确用法 - 方式3: 按名称搜索
url = "https://openplzapi.org/de/Localities?name=Berlin"
```

**联邦州代码参考**：
```
01 - Schleswig-Holstein
02 - Hamburg
03 - Niedersachsen
04 - Bremen
05 - Nordrhein-Westfalen
06 - Hessen
07 - Rheinland-Pfalz
08 - Baden-Württemberg
09 - Bayern
10 - Saarland
11 - Berlin
12 - Brandenburg
13 - Mecklenburg-Vorpommern
14 - Sachsen
15 - Sachsen-Anhalt
16 - Thüringen
```

**备选方案**：
- 使用静态城市数据文件（已包含31个主要城市）
- 无需API调用，直接使用 `data/cities.json`

### 其他故障排查

### 如果生成页面为空
- 检查模板路径是否正确
- 检查Jinja2变量是否匹配
- 检查数据文件是否存在

### 如果部署失败
- 检查构建配置
- 检查 `output/` 目录是否存在
- 查看部署日志

---

## 扩展规则

### 添加新服务时
1. 更新 `data/services.json`
2. 确认slug唯一性
3. 更新价格区间
4. 重新运行生成脚本

### 添加新城市时
- 使用 `scripts/fetch_cities.py` 获取
- 确保数据结构一致
- 批量添加时注意API限流

### 添加新Modifier时
1. 更新 `data/modifiers.json`
2. 为每个Modifier设计专门的FAQ
3. 重新生成所有页面

---

## 安全注意事项

### 敏感信息保护
- ✅ `.env` 文件加入 `.gitignore`
- ✅ API密钥使用环境变量（Phase 2+）
- ❌ 不要在代码中硬编码密钥

### 内容质量检查
- 生成内容需人工抽查
- 检测并过滤不当内容
- 确保符合德国广告法规

---

## 版本控制约定

### Git提交信息格式
```
feat: 添加新服务类型
fix: 修复模板渲染错误
docs: 更新部署说明
refactor: 优化页面生成速度
test: 添加验证脚本
```

### 分支策略
- `main`: 生产环境
- `dev`: 开发环境（可选）
- `feat/*`: 功能分支（可选）

---

## 重要提醒

### ⚠️ 修改前必读
1. 不要修改URL结构（会影响SEO）
2. 不要删除已生成的页面（使用更新代替）
3. 不要改变核心数据模型（向后兼容）
4. 任何模板修改需重新生成所有页面

### ✅ 修改前检查清单
- [ ] 已阅读相关代码
- [ ] 已理解现有逻辑
- [ ] 已备份数据文件
- [ ] 已在测试环境验证
- [ ] 已更新相关文档

---

## 快速参考

### 关键文件路径
```
scripts/fetch_cities.py          # 城市数据获取
scripts/generate_pages.py        # 零AI页面生成
scripts/generate_sitemap.py      # Sitemap生成
templates/page.html              # 主模板
data/services.json               # 服务配置
data/modifiers.json              # Modifier配置
output/                          # 构建输出
```

### Phase 1 快速开始

```bash
# 0. 检查并设置Python虚拟环境（必须！）
if [ ! -d "venv" ]; then python -m venv venv; fi
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 1. 安装依赖
pip install -r requirements.txt

# 2. 生成数据（或使用已有的静态数据）
python scripts/fetch_cities.py

# 3. 生成页面（372页）
python scripts/generate_pages.py

# 4. 生成sitemap
python scripts/generate_sitemap.py

# 5. 本地预览
cd output && python -m http.server 8000
```

### Windows快速开始（一行命令）

```batch
# 自动检查虚拟环境、安装依赖并生成页面
if not exist venv python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python scripts/generate_pages.py && python scripts/generate_sitemap.py
```

---

## Phase 2+ 准备

### Multi-Agent架构（Phase 2+可选）
如果Phase 1验证成功，可以引入Multi-Agent架构：

```
┌─────────────────────────────────────────────────────────────┐
│                   MASTER AGENT (主控)                        │
│  任务编排 | 状态监控 | 错误恢复 | Agent协调                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
    ┌───────────┬───────────┬───────────┬───────────┬───────────┐
    ↓           ↓           ↓           ↓           ↓           ↓
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│ Data │  │Content│  │Quality│  │ Legal│  │  SEO │  │Analytics│
│Agent │  │ Agent│  │ Agent│  │ Agent│  │ Agent│  │  Agent │
└──────┘  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘
数据获取   AI内容    质量检查   法律合规   SEO优化   自我进化
```

**注意**: Phase 1 不需要Agent架构，直接使用脚本即可。

---

**项目所有权**: 此项目属于程序化SEO项目，任何修改必须遵循SEO最佳实践。
**核心参数**: 以 [README.md](./README.md) 为准。
**实施指南**: 以 [blueprint.md](./blueprint.md) 为准。

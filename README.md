# PSEO Germany Handwerker - 项目文档索引

> **版本**: v2.0 Professional Edition
> **最后更新**: 2025-01-10
> **状态**: 生产就绪

---

## 核心参数（单一事实来源）

以下参数是整个项目的**唯一权威配置**，所有文档必须以此为准：

```yaml
# Phase 1 核心参数
phase_1:
  cities: 30              # 城市（人口>50,000）
  services: 4             # 核心服务类型
  modifiers: 3            # Modifier（初期：主词 + kosten + notdienst）
  total_pages: 360        # 30 × 4 × 3 = 360页

# 完整6个Modifier（Phase 2扩展）
all_modifiers:
  - ""                    # 主词：klempner-berlin
  - "kosten"              # 成本：klempner-berlin-kosten
  - "preis"               # 价格：klempner-berlin-preis
  - "notdienst"           # 紧急：klempner-berlin-notdienst（最高CPC）
  - "empfehlung"          # 推荐：klempner-berlin-empfehlung
  - "in-der-naehe"        # 附近：klempner-berlin-in-der-naehe

# Phase 1 方法论
phase_1_methodology: "零AI"   # 模板 + 真实数据，无需AI调用

# 扩展路径
scaling_path:
  - phase: 1
    pages: 360
    cities: 30
    services: 4
    modifiers: 3
  - phase: 2
    pages: 720
    cities: 30
    services: 4
    modifiers: 6
  - phase: 3
    pages: 2,400
    cities: 100
    services: 4
    modifiers: 6

# 4个核心服务
core_services:
  - Klempner              # 管道工
  - Elektriker            # 电工
  - Dachdecker            # 屋顶工
  - Maler                 # 油漆工
```

---

## 文档导航

### 新手入门顺序

```
1. README.md (本文件)
   └── 了解项目全局和核心参数

2. blueprint.md ⭐最重要
   └── 完整执行指南，包含6 Modifier策略和零AI Phase 1实现

3. CLAUDE.md
   └── 开发者规范，Multi-Agent架构说明

4. tasks.md
   └── 详细任务清单（需与blueprint对齐）
```

### 文档职责划分

| 文档 | 职责 | 权威性 |
|------|------|--------|
| **README.md** | 项目索引和核心参数定义 | ⭐ 最高优先级 |
| **blueprint.md** | 执行指南（0成本实现） | ⭐⭐ 实施权威 |
| **CLAUDE.md** | 开发者规范和Multi-Agent架构 | 开发参考 |
| **overview.md** | 项目背景和目标 | 背景参考 |
| **implementation.md** | 技术架构说明 | 架构参考 |
| **strategy.md** | 策略和风险分析 | 策略参考 |
| **tasks.md** | 任务清单 | 待更新 |
| **automation-architecture.md** | Multi-Agent详细设计 | Phase 2+参考 |

---

## 快速开始

### Day 1: 零成本启动（推荐）

```bash
# 1. 注册免费服务
# - Cloudflare Pages（托管）
# - GitHub（代码仓库）
# - DeepSeek（AI，Phase 2用）

# 2. 获取数据
# - OpenPLZ API：德国城市数据（免费）

# 3. 生成Phase 1页面（零AI）
python scripts/generate_phase1.py --cities 30 --services 4 --modifiers 3

# 4. 部署
# 推送到GitHub → Cloudflare Pages自动部署
```

### 核心代码结构

```
pseo-handwerker/
├── data/
│   ├── cities.json          # OpenPLZ城市数据（30个）
│   ├── services.json        # 4个核心服务配置
│   └── modifiers.json       # 6个Modifier配置
│
├── templates/
│   ├── page.html            # 主页面模板（零AI友好）
│   ├── impressum.html       # 法律页面
│   └── datenschutz.html     # GDPR页面
│
├── scripts/
│   ├── fetch_cities.py      # OpenPLZ数据获取
│   ├── generate_phase1.py   # 零AI页面生成 ⭐核心
│   └── generate_sitemap.py  # Sitemap生成
│
├── output/
│   ├── *.html               # 360个静态页面
│   └── sitemap.xml
│
└── vercel.json / _redirects  # 部署配置
```

---

## Phase 1 实现核心（零AI）

### 为什么零AI？

1. **成本**: Phase 1 完全免费
2. **速度**: 无需等待AI API调用
3. **控制**: 完全可控的内容质量
4. **合规**: 避免AI内容检测风险

### 零AI页面生成逻辑

```python
def generate_page_zero_ai(city, service, modifier):
    """零AI生成页面 - Phase 1"""

    # 1. 获取预设数据
    city_data = get_city_data(city)           # OpenPLZ真实数据
    service_data = get_service_data(service)   # 服务配置
    faq_data = get_modifier_faqs(modifier)     # Modifier对应FAQ

    # 2. 渲染模板
    html = template.render(
        city=city_data["name"],
        population=f"{city_data['population']:,}",
        districts=city_data["districts"],       # 真实行政区
        postal_codes=city_data["postal_codes"], # 真实邮编
        service=service_data["name"],
        price_range=f"€{service_data['price_low']}-{service_data['price_high']}",
        faqs=faq_data,                          # 预设FAQ（带Schema）
        modifier=modifier,
        current_year=2026
    )

    return html
```

### 真实数据示例

```python
# cities.json（来自OpenPLZ）
{
  "Berlin": {
    "name": "Berlin",
    "population": 3644826,
    "state": "Berlin",
    "postal_codes": ["10115", "10117", "10119", "10179", "10243", "10245", "10247", "10249"],
    "districts": ["Mitte", "Kreuzberg", "Neukölln", "Pankow", "Charlottenburg", "Wedding"]
  },
  "Hamburg": {
    "name": "Hamburg",
    "population": 1841179,
    "state": "Hamburg",
    "postal_codes": ["20095", "20097", "20099", "20144", "20146", "20148", "20149"],
    "districts": ["Altstadt", "HafenCity", "Eppendorf", "Winterhude", "Altona"]
  }
}
```

---

## 关键策略说明

### 6个Modifier策略（重要）

| Modifier | URL示例 | 意图 | CPC权重 |
|----------|---------|------|---------|
| 主词 | klempner-berlin | 导航型 | 基准 |
| kosten | klempner-berlin-kosten | 信息型 | 1.5x |
| preis | klempner-berlin-preis | 信息型 | 1.5x |
| notdienst | klempner-berlin-notdienst | 交易型 | **3-5x** |
| empfehlung | klempner-berlin-empfehlung | 调研型 | 1.2x |
| in-der-naehe | klempner-berlin-in-der-naehe | 交易型 | 2x |

### FAQ Schema（必须包含）

```html
<!-- 每个页面必须包含FAQPage Schema -->
<div itemscope itemtype="https://schema.org/FAQPage">
  <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">Was kostet ein {{ service }} in {{ city }}?</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <span itemprop="text">
        Die Preise für {{ service }} in {{ city }} liegen zwischen
        €{{ price_low }} und €{{ price_high }} pro Stunde.
      </span>
    </div>
  </div>
  <!-- 至少3-5个FAQ -->
</div>
```

---

## 免费合规方案

| 项目 | 免费方案 | 来源 |
|------|----------|------|
| Impressum | Dr. Thomas Schwenke 生成器 | schwenke.de |
| Datenschutz | 同上（GDPR合规） | schwenke.de |
| Cookie横幅 | CookieConsent 开源版 | github.com/insites/cookieconsent |

---

## 扩展时间线

```
Phase 1 (Week 1-2): 360页
├── 30城市 × 4服务 × 3 Modifier
├── 零AI实现
└── 目标：建立Google信任

Phase 2 (Month 2): 720页
├── 添加3个Modifier
├── 可选：AI内容增强
└── 目标：提升流量

Phase 3 (Month 3+): 2400页
├── 扩展到100城市
├── 6个Modifier全部启用
└── 目标：规模化流量
```

---

## 版本说明

### v2.0 Professional Edition (当前版本)

**重大变更**:
- ✅ 从16,000页缩减到360页（Phase 1）
- ✅ 扩展到6个Modifier策略
- ✅ 采用零AI方法论
- ✅ 强调真实数据（OpenPLZ）
- ✅ 免费合规方案

### v1.0（已废弃）

以下概念已被v2.0取代：
- ❌ 2000城市 × 8服务 = 16,000页（过于激进）
- ❌ Phase 1即使用AI（不必要）
- ❌ 3个Modifier（收入潜力未最大化）

---

## 常见问题

**Q: 为什么Phase 1只做360页？**
A: 新域名DA=0，Google爬取配额有限。先建立信任，再规模化。

**Q: 为什么不用AI？**
A: Phase 1目标是用真实数据+模板生成高质量内容。AI在Phase 2可选用于增强。

**Q: notdienst Modifier为什么重要？**
A: 紧急服务CPC是普通词的3-5倍，流量价值最高。

**Q: 如何确保不被Google惩罚？**
A:
1. 真实数据（OpenPLZ官方数据）
2. FAQ Schema结构化数据
3. 每个页面唯一的关键词组合
4. 解决真实用户问题

---

**文档所有权**: 本项目遵循PSEO最佳实践，blueprint.md为实施权威文档。

# PSEO Germany Handwerker - 技术实现方案（全自动化版）

## 架构设计

### Multi-Agent自动化架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MASTER AGENT (orchestrator)                      │
│  任务编排 | 状态监控 | 错误恢复 | Agent协调                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│  DATA AGENT   │           │CONTENT AGENT  │           │ QUALITY AGENT │
│ 数据获取专家  │           │  内容生成专家  │           │  质量检查专家  │
├───────────────┤           ├───────────────┤           ├───────────────┤
│ • 城市数据    │           │ • 文章生成    │           │ • SEO评分     │
│ • 服务配置    │           │ • Prompt优化  │           │ • 去重检测    │
│ • API调用     │           │ • 多样化处理  │           │ • 本地化检查  │
└───────────────┘           └───────────────┘           └───────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│  LEGAL AGENT  │           │  SEO AGENT    │           │ ANALYTICS AGT │
│ 法律合规专家  │           │  SEO优化专家  │           │  数据分析专家  │
├───────────────┤           ├───────────────┤           ├───────────────┤
│ • Impressum   │           │ • Sitemap     │           │ • A/B测试     │
│ • Datenschutz│           │ • Metadata    │           │ • 自动报告    │
│ • GDPR检查    │           │ • 结构化数据  │           │ • Prompt优化  │
└───────────────┘           └───────────────┘           └───────────────┘
```

### 数据流

```
1. Data Agent → 城市数据 → 数据库/JSON
                  ↓
2. Content Agent → AI生成 → 文章缓存
                  ↓
3. Quality Agent → 质量检查 → 标记重新生成
                  ↓
4. SEO Agent → 元数据优化 → HTML页面
                  ↓
5. Analytics Agent → A/B测试 → Prompt优化
                  ↓
6. 重新进入循环 → 持续改进
```

### 完全自动化工作流

```
GitHub Actions触发 (每周日00:00)
        ↓
Master Agent启动
        ↓
┌─────────────────────────────────────┐
│ Stage 1: Data Preparation          │
│ → Data Agent获取和验证数据          │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ Stage 2: Legal Pages               │
│ → Legal Agent生成法律页面           │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ Stage 3: Content Generation        │
│ → Content Agent生成所有文章         │
│ (使用多变体Prompt + 写作风格)       │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ Stage 4: Quality Assurance         │
│ → Quality Agent评分和去重           │
│ → 低分页面自动标记重新生成          │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ Stage 5: SEO Optimization          │
│ → SEO Agent生成Sitemap             │
│ → AI优化Metadata                   │
│ → 插入结构化数据                   │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ Stage 6: Analytics & Feedback      │
│ → Analytics Agent生成报告          │
│ → 运行A/B测试                      │
│ → 自动优化Prompt                   │
└─────────────────────────────────────┘
        ↓
Vercel自动部署
        ↓
Slack/Email通知完成状态
```

## 技术栈

### 核心技术
| 组件 | 技术选型 | 说明 |
|------|---------|------|
| 编程语言 | Python 3.11+ | 数据处理、脚本自动化 |
| 模板引擎 | Jinja2 | HTML页面模板渲染 |
| 静态生成 | Astro (可选) | 构建工具，或直接生成HTML |
| 托管部署 | Vercel | 免费静态托管 + CDN |
| 版本控制 | Git + GitHub | 代码管理 + CI/CD |

### AI服务（支持多供应商）
| 服务商 | 模型 | 用途 | 成本 |
|--------|------|------|------|
| OpenAI | gpt-4o-mini | 主要推荐 | ~$80-120/16K页 |
| DeepSeek | deepseek-chat | 高性价比 | ~¥300-500/16K页 |
| 智谱AI | glm-4-flash | 国产优选 | ~¥100-200/16K页 |
| 其他 | OpenAI兼容API | 通过环境变量配置 | 视供应商而定 |

**配置方式**:
```bash
# .env 文件
AI_PROVIDER=openai         # 或 deepseek, zhipu, custom
AI_API_KEY=sk-xxx
AI_MODEL=gpt-4o-mini       # 或对应服务商模型
AI_BASE_URL=https://api.openai.com/v1  # 可选自定义
```

### 数据源
| 数据源 | 内容 | 用途 |
|--------|------|------|
| OpenPLZ API | 城市名称、邮编、州、经纬度 | 页面地理数据 |

## 项目目录结构

```
pseo-handwerker/
├── .github/
│   └── workflows/
│       └── build.yml          # GitHub Actions CI/CD配置
│
├── data/
│   ├── cities.json            # 德国城市数据（从OpenPLZ获取）
│   ├── services.json          # 服务类型与价格配置
│   └── .gitkeep               # 保持目录结构
│
├── templates/
│   ├── page.html              # 单页面模板
│   ├── base.html              # 基础模板（可扩展）
│   └── components/            # 可复用组件
│       ├── header.html
│       ├── footer.html
│       └── faq.html
│
├── content/
│   └── ai_articles/           # AI生成的文章缓存
│       └── .gitkeep
│
├── scripts/
│   ├── fetch_cities.py        # 从OpenPLZ获取城市数据
│   ├── generate_content.py    # AI生成文章
│   ├── build_pages.py         # 生成HTML页面
│   ├── generate_sitemap.py    # 生成sitemap.xml
│   └── verify_links.py        # 验证生成页面完整性
│
├── public/
│   ├── pages/                 # 生成的HTML页面（输出目录）
│   ├── css/
│   │   └── styles.css         # 样式文件
│   ├── js/
│   │   └── main.js            # 交互脚本（最小化）
│   └── images/
│       └── .gitkeep
│
├── output/                    # 构建输出目录（部署到Vercel）
│   ├── *.html                 # 所有生成的页面
│   └── sitemap.xml
│
├── tests/
│   ├── test_fetch_cities.py   # 测试数据获取
│   ├── test_content_gen.py    # 测试内容生成
│   └── test_template.py       # 测试模板渲染
│
├── vercel.json                # Vercel配置
├── pyproject.toml             # Python项目配置
├── requirements.txt           # Python依赖
├── .gitignore                 # Git忽略文件
└── README.md                  # 项目说明
```

## 数据模型

### 城市数据 (cities.json)
```json
[
  {
    "name": "Berlin",
    "postalCode": "10115",
    "state": "Berlin",
    "lat": 52.52,
    "lng": 13.405,
    "population": 3644826
  },
  {
    "name": "Hamburg",
    "postalCode": "20095",
    "state": "Hamburg",
    "lat": 53.5511,
    "lng": 9.9937,
    "population": 1841179
  }
]
```

### 服务数据 (services.json)
```json
[
  {
    "name": "Klempner",
    "name_en": "Plumber",
    "price_low": 80,
    "price_high": 160,
    "slug": "klempner",
    "description": "Fachkraft für Installation, Wartung und Reparatur von Sanitär- und Heizungsanlagen"
  },
  {
    "name": "Elektriker",
    "name_en": "Electrician",
    "price_low": 70,
    "price_high": 150,
    "slug": "elektriker",
    "description": "Fachkraft für elektrotechnische Anlagen und Installationen"
  }
]
```

## 页面模板设计

### SEO元数据
```html
<title>Bester {{ service }} in {{ city }} 2026 – Preise, Tipps & Vergleich</title>
<meta name="description" content="Finden Sie den besten {{ service }} in {{ city }}. Preise: €{{ price_low }}-{{ price_high }}/h. Verified Tipps & Vergleich 2026.">
<link rel="canonical" href="https://handwerker-ratgeber.de/{{ service_slug }}-{{ city_slug }}">

<!-- Open Graph -->
<meta property="og:title" content="Bester {{ service }} in {{ city }} 2026">
<meta property="og:description" content="Vergleich der besten {{ service }} in {{ city }} mit Preisübersicht.">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">

<!-- Schema.org 结构化数据 -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "{{ service }} {{ city }}",
  "areaServed": {
    "@type": "City",
    "name": "{{ city }}"
  },
  "priceRange": "€{{ price_low }}-{{ price_high }}"
}
</script>
```

### 页面结构
```html
<article>
  <h1>Bester {{ service }} in {{ city }} 2026</h1>

  <section class="price-box">
    <p>💰 Durchschnittspreis: <strong>€{{ price_low }} – €{{ price_high }}</strong> pro Stunde</p>
  </section>

  <section class="quick-summary">
    <h2>📋 Kurzübersicht</h2>
    <ul>
      <li>⏱️ Reaktionszeit: 24-48 Stunden</li>
      <li>⭐ Bewertungen: 4.5/5 Durchschnitt</li>
      <li>📍 Verfügbarkeit in {{ city }}</li>
    </ul>
  </section>

  <section class="content">
    <h2>Warum {{ service }} in {{ city }} wichtig ist</h2>
    {{ article_content }}
  </section>

  <section class="comparison">
    <h2>🔍 Preisvergleich {{ city }}</h2>
    <table>
      <!-- 价格比较表 -->
    </table>
  </section>

  <section class="faq">
    <h2>❓ Häufige Fragen (FAQ)</h2>
    <div itemscope itemtype="https://schema.org/FAQPage">
      <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
        <h3 itemprop="name">Was kostet ein {{ service }} in {{ city }}?</h3>
        <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
          <span itemprop="text">{{ answer }}</span>
        </div>
      </div>
    </div>
  </section>
</article>
```

## AI内容生成策略

### Prompt模板
```python
prompt = f"""
Du bist ein erfahrener deutscher SEO-Redakteur. Schreibe einen informativen Artikel über: {service_name} in {city_name}.

Anforderungen:
- Sprache: Deutsch (DE)
- Länge: 800-1200 Wörter
- SEO-fokus: Hauptkeyword "{service_name} {city_name}", sekundäre Keywords inkludieren
- Struktur:
  1. Einleitung (Warum dieser Service wichtig ist)
  2. Preisinformationen (€{price_low}-{price_high}/h)
  3. Worauf man bei der Auswahl achten sollte
  4. Typische Aufgaben und Herausforderungen
  5. Fazit und Empfehlung

Schreibstil:
- Professionell, aber verständlich
- Lokale Bezüge zu {city_name}
- Prägnante Absätze
- Nutzwert für den Leser
"""
```

### 内容缓存策略
- AI生成内容持久化存储到 `content/ai_articles/`
- 文件命名：`{service_slug}_{city_slug}.txt`
- 避免重复调用API，节省成本

## CI/CD自动化

### GitHub Actions工作流
```yaml
name: Build and Deploy

on:
  schedule:
    - cron: '0 0 * * 0'  # 每周日UTC 00:00运行
  workflow_dispatch:      # 手动触发

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Fetch cities data
        env:
          OPENPLZ_API_KEY: ${{ secrets.OPENPLZ_API_KEY }}
        run: python scripts/fetch_cities.py

      - name: Generate AI content
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python scripts/generate_content.py

      - name: Build HTML pages
        run: python scripts/build_pages.py

      - name: Generate sitemap
        run: python scripts/generate_sitemap.py

      - name: Deploy to Vercel
        run: vercel --prod
```

## Sitemap生成策略

### Sitemap结构
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://handwerker-ratgeber.de/klempner-berlin</loc>
    <lastmod>2026-03-10</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <!-- 15999 more URLs -->
</urlset>
```

### Sitemap分片（超过50K URL时）
```
sitemap.xml (索引文件)
├── sitemap-services.xml (按服务分类)
├── sitemap-cities-1.xml (按城市分片)
├── sitemap-cities-2.xml
└── ...
```

## Vercel部署配置

### vercel.json
```json
{
  "buildCommand": "python scripts/build_pages.py",
  "outputDirectory": "output",
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600, s-maxage=86400"
        }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/home",
      "destination": "/",
      "permanent": true
    }
  ]
}
```

## 性能优化

1. **静态资源**
   - CSS内联关键样式
   - 图片使用WebP格式
   - 最小化JavaScript

2. **HTML优化**
   - 压缩HTML输出
   - 预加载关键资源
   - 延迟加载非关键内容

3. **CDN缓存**
   - Vercel Edge Network
   - 长期缓存策略

4. **SEO优化**
   - 结构化数据（Schema.org）
   - Meta标签完整
   - Sitemap自动提交

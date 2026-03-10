# PSEO Germany Handwerker - 实施任务清单

> **文档版本**: v2.0 Professional Edition
> **最后更新**: 2025-01-10
> **状态**: 已更新 - 遵循 [README.md](./README.md) 核心参数

---

## 核心参数（必须严格遵守）

```yaml
phase_1:
  cities: 30              # 城市（人口>50,000）
  services: 4             # 核心服务
  modifiers: 3            # Modifier（初期）
  total_pages: 360        # 30 × 4 × 3 = 360页
  methodology: "零AI"     # 模板 + 数据，无需AI调用

all_modifiers: 6          # Phase 2+ 完整覆盖
  - ""                    # 主词
  - "kosten"              # 成本
  - "preis"               # 价格
  - "notdienst"           # 紧急（最高CPC）
  - "empfehlung"          # 推荐
  - "in-der-naehe"        # 附近
```

---

## 目录

- [Phase 0: 基础准备](#phase-0-基础准备)
- [Phase 1: 零AI MVP（360页）](#phase-1-零ai-mvp360页)
- [Phase 2: 扩展（3200页）](#phase-2-扩展3200页)
- [Phase 3: 规模化（24000页）](#phase-3-规模化24000页)

---

## Phase 0: 基础准备（Day 1）

### Task 0.1: 项目结构搭建

**目录结构**:
```
pseo-handwerker/
├── data/
│   ├── cities.json          # OpenPLZ城市数据
│   ├── services.json        # 服务配置
│   └── modifiers.json       # Modifier配置
├── templates/
│   ├── page.html            # 主页面模板
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
└── requirements.txt
```

**验证**: 目录结构完整

### Task 0.2: 环境配置

**requirements.txt**:
```
requests>=2.31.0
jinja2>=3.1.2
python-dotenv>=1.0.0
beautifulsoup4>=4.12.0
```

**验证**: `pip install -r requirements.txt` 成功

### Task 0.3: 免费服务注册

| 服务 | 用途 | 成本 |
|------|------|------|
| Cloudflare Pages | 托管 | 免费 |
| GitHub | 代码仓库 | 免费 |
| OpenPLZ API | 城市数据 | 免费 |
| Dr. Schwenke | 法律页面 | 免费 |

**验证**: 所有账号创建完成

---

## Phase 1: 零AI MVP（360页）

### Task 1.1: 创建服务配置

**文件**: `data/services.json`

```json
[
  {
    "slug": "klempner",
    "name": "Klempner",
    "price_low": 80,
    "price_medium": 120,
    "price_high": 160,
    "price_emergency": 200,
    "services": [
      "Rohrreinigung und Verstopfungsbeseitigung",
      "Leckortung und Rohrreparatur",
      "Installation von Sanitäreinrichtungen",
      "Heizungswartung und -reparatur",
      "Badsanierung und -modernisierung",
      "Notdienst bei Wasserschäden"
    ]
  },
  {
    "slug": "elektriker",
    "name": "Elektriker",
    "price_low": 70,
    "price_medium": 110,
    "price_high": 150,
    "price_emergency": 180,
    "services": [
      "Elektrische Installationen",
      "Fehlerbehebung und Reparatur",
      "Lichtplanung und -installation",
      "Steckdoseninstallation",
      "LED-Umrüstung",
      "Notdienst bei Stromausfall"
    ]
  },
  {
    "slug": "schluesseldienst",
    "name": "Schlüsseldienst",
    "price_low": 60,
    "price_medium": 90,
    "price_high": 120,
    "price_emergency": 150,
    "services": [
      "Türöffnung",
      "Schlosswechsel",
      "Schlüssel-Duplizierung",
      "Notöffnung",
      "Sicherheitstechnik",
      "24/7 Notdienst"
    ]
  },
  {
    "slug": "rohrreinigung",
    "name": "Rohrreinigung",
    "price_low": 70,
    "price_medium": 100,
    "price_high": 130,
    "price_emergency": 160,
    "services": [
      "Rohrreinigung mit Kamera",
      "Verstopfungsbeseitigung",
      "Wartung und Inspektion",
      "Rohrrensanierung"
    ]
  }
]
```

**验证**: `python -m json.tool data/services.json`

### Task 1.2: 创建Modifier配置

**文件**: `data/modifiers.json`

```json
{
  "modifiers": {
    "": {
      "name": "main",
      "title_suffix": "",
      "focus": "Preise & Notdienst",
      "faqs": [
        {
          "question": "Worauf sollte man bei der Auswahl achten?",
          "answer": "Achten Sie auf Zertifizierungen, Kundenbewertungen und faire Preise."
        },
        {
          "question": "Sind die Anbieter zertifiziert?",
          "answer": "Die meisten Anbieter sind Meisterbetriebe mit entsprechender Zertifizierung."
        },
        {
          "question": "Wie lange dauert eine typische Reparatur?",
          "answer": "Die Dauer hängt von der Art der Leistung ab, meist zwischen 1-4 Stunden."
        }
      ]
    },
    "kosten": {
      "name": "kosten",
      "title_suffix": " Kosten",
      "focus": "Was Sie erwarten müssen",
      "faqs": [
        {
          "question": "Was kostet ein Grundservice?",
          "answer": "Ein Grundservice kostet typischerweise zwischen €70 und €120 pro Stunde."
        },
        {
          "question": "Was kostet ein Notdienst?",
          "answer": "Ein Notdienst kostet typischerweise zwischen €120 und €200 pro Stunde."
        },
        {
          "question": "Gibt es zusätzliche Kosten?",
          "answer": "Zusätzliche können entstehen für Material, Anfahrtswege oder Wochenendzuschläge."
        },
        {
          "question": "Wie wird abgerechnet?",
          "answer": "Die meisten Anbieter rechnen nach Aufwand ab, manche bieten Pauschalpreise an."
        }
      ]
    },
    "notdienst": {
      "name": "notdienst",
      "title_suffix": " Notdienst",
      "focus": "24/7 Verfügbar",
      "faqs": [
        {
          "question": "Wie schnell ist ein Notdienst vor Ort?",
          "answer": "Ein Notdienst ist meist innerhalb von 1-2 Stunden vor Ort, in Innenstädten oft schneller."
        },
        {
          "question": "Gibt es 24/7 Notdienst?",
          "answer": "Ja, viele Anbieter bieten rund um die Uhr Notdienst an."
        },
        {
          "question": "Was kostet ein Notdienst?",
          "answer": "Notdienste kosten etwa 20-50% mehr als der normale Preis."
        },
        {
          "question": "Welche Notfälle werden abgedeckt?",
          "answer": "Typische Notfälle: Wasserschäden, Rohrbrüche, Stromausfall, Türöffnung."
        }
      ]
    }
  }
}
```

**验证**: `python -m json.tool data/modifiers.json`

### Task 1.3: 获取城市数据

**文件**: `scripts/fetch_cities.py`

```python
#!/usr/bin/env python3
"""
从OpenPLZ API获取德国城市数据
只获取人口 > 50,000 的城市
"""
import requests
import json
from pathlib import Path

def slugify(text: str) -> str:
    """转换为URL slug"""
    text = text.lower()
    text = text.replace(" ", "-")
    text = text.replace("ä", "ae")
    text = text.replace("ö", "oe")
    text = text.replace("ü", "ue")
    text = text.replace("ß", "ss")
    return text

def fetch_cities(min_population: int = 50000, limit: int = 30) -> list:
    """从OpenPLZ获取城市数据"""
    cities = []
    url = "https://openplzapi.org/de/Localities"
    page = 1

    print(f"Fetching cities with population > {min_population}...")

    while len(cities) < limit:
        try:
            response = requests.get(f"{url}?page={page}", timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                break

            for item in data:
                if len(cities) >= limit:
                    break

                population = item.get("population", 0)
                if population >= min_population:
                    cities.append({
                        "name": item["name"],
                        "slug": slugify(item["name"]),
                        "population": population,
                        "state": item.get("state", ""),
                        "postalCode": item.get("postalCode", ""),
                        "lat": item.get("location", {}).get("lat"),
                        "lng": item.get("location", {}).get("lng")
                    })

            page += 1
            print(f"Page {page}: {len(cities)} cities found...")

        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

    return cities

if __name__ == "__main__":
    cities = fetch_cities(min_population=50000, limit=30)

    # 保存到文件
    output_path = Path("data/cities.json")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(cities, indent=2, ensure_ascii=False))

    print(f"\nSaved {len(cities)} cities to {output_path}")
    print(f"Population range: {min(c['population'] for c in cities):,} - {max(c['population'] for c in cities):,}")
```

**验证**:
```bash
python scripts/fetch_cities.py
# 应输出: Saved 30 cities to data/cities.json
python -m json.tool data/cities.json
```

### Task 1.4: 创建页面模板（零AI）

**文件**: `templates/page.html`

```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    <link rel="canonical" href="{{ canonical_url }}">

    <!-- LocalBusiness Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "{{ service }} {{ city }}",
      "areaServed": {
        "@type": "City",
        "name": "{{ city }}"
      },
      "priceRange": "€{{ price_low }}-{{ price_high }}",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "{{ city }}",
        "addressRegion": "{{ state }}",
        "addressCountry": "DE"
      }
      {% if lat and lng %}
      , "geo": {
        "@type": "GeoCoordinates",
        "latitude": {{ lat }},
        "longitude": {{ lng }}
      }
      {% endif %}
    }
    </script>
</head>
<body>
    <header>
        <h1>{{ h1_title }}</h1>
    </header>

    <main>
        <!-- 城市信息（真实数据） -->
        <section class="city-info">
            <h2>Über {{ city }}</h2>
            <p>{{ city }} ist eine Stadt in {{ state }} mit <strong>{{ population_formatted }} Einwohnern</strong>.</p>
            {% if postal_code %}
            <p>Die Postleitzahl ist {{ postal_code }}.</p>
            {% endif %}
        </section>

        <!-- 价格表 -->
        <section class="pricing">
            <h2>{{ service }} Preise in {{ city }}</h2>
            <table>
                <tr>
                    <th>Leistung</th>
                    <th>Preis</th>
                </tr>
                <tr>
                    <td>Grundservice</td>
                    <td>€{{ price_low }}-{{ price_medium }} pro Stunde</td>
                </tr>
                <tr>
                    <td>Notdienst</td>
                    <td>€{{ price_high }}-{{ price_emergency }} pro Stunde</td>
                </tr>
                {% if modifier == "notdienst" %}
                <tr>
                    <td>Wochenend/Zuschlag</td>
                    <td>+20-30%</td>
                </tr>
                {% endif %}
            </table>
        </section>

        <!-- 服务列表 -->
        <section class="services">
            <h2>Typische {{ service }} Leistungen in {{ city }}</h2>
            <ul>
                {% for service_item in service_list %}
                <li>{{ service_item }}</li>
                {% endfor %}
            </ul>
        </section>

        <!-- FAQ + FAQPage Schema -->
        <section class="faq">
            <h2>Häufige Fragen (FAQ)</h2>
            <div itemscope itemtype="https://schema.org/FAQPage">
                {% for faq in faqs %}
                <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
                    <h3 itemprop="name">{{ faq.question }}</h3>
                    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
                        <span itemprop="text">{{ faq.answer }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>
    </main>

    <footer>
        <p>© 2026 Handwerker Ratgeber. <a href="/impressum">Impressum</a> | <a href="/datenschutz">Datenschutz</a></p>
        <p class="disclaimer">⚠️ Die Preise sind Richtwerte und können je nach Aufwand und Region variieren.</p>
    </footer>
</body>
</html>
```

**验证**: 模板语法正确

### Task 1.5: 零AI页面生成脚本

**文件**: `scripts/generate_pages.py`

```python
#!/usr/bin/env python3
"""
零AI页面生成脚本
Phase 1: 30城市 × 4服务 × 3 Modifier = 360页
"""
import json
from pathlib import Path
from jinja2 import Template
from tqdm import tqdm

def format_population(population: int) -> str:
    """格式化人口数字"""
    return f"{population:,}".replace(",", ".")

def generate_title(city: str, service: str, modifier: str, modifier_data: dict) -> tuple:
    """生成页面标题和描述"""
    if modifier == "notdienst":
        title = f"{service} Notdienst {city} | 24/7 Verfügbar"
        h1 = f"{service} Notdienst in {city} – 24/7 Verfügbar 2026"
        desc = f"Notdienst {service} in {city}. Schnelle Hilfe bei Notfällen. 24/7 verfügbar."
    elif modifier == "kosten":
        title = f"{service} {city} Kosten | Was Sie erwarten müssen"
        h1 = f"{service} Kosten in {city} – Preisübersicht 2026"
        desc = f"Alle Kosten für {service} in {city}. Grundpreise, Notdienstpreise und Zuschläge."
    else:
        title = f"{service} in {city} – Preise & Notdienst 2026"
        h1 = f"{service} in {city} – Preise, Tipps & Notdienst"
        desc = f"Finden Sie den besten {service} in {city}. Preise: €70-160/h. 24/7 Notdienst verfügbar."

    return title, h1, desc

def main():
    # 加载数据
    cities = json.loads(Path("data/cities.json").read_text(encoding="utf-8"))
    services = json.loads(Path("data/services.json").read_text(encoding="utf-8"))
    modifiers = json.loads(Path("data/modifiers.json").read_text(encoding="utf-8"))["modifiers"]

    # 加载模板
    template = Template(Path("templates/page.html").read_text(encoding="utf-8"))

    # 创建输出目录
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # 生成页面
    total = len(cities) * len(services) * len(modifiers)
    print(f"Generating {total} pages...")

    count = 0
    for city in tqdm(cities, desc="Cities"):
        for service in services:
            for modifier_key, modifier_data in modifiers.items():
                # 生成标题
                title, h1_title, description = generate_title(
                    city["name"],
                    service["name"],
                    modifier_key,
                    modifier_data
                )

                # 文件名
                filename = f"{service['slug']}-{city['slug']}{modifier_key}.html"

                # 渲染模板
                html = template.render(
                    city=city["name"],
                    state=city.get("state", ""),
                    population_formatted=format_population(city["population"]),
                    postal_code=city.get("postalCode", ""),
                    lat=city.get("lat"),
                    lng=city.get("lng"),
                    service=service["name"],
                    service_slug=service["slug"],
                    price_low=service["price_low"],
                    price_medium=service["price_medium"],
                    price_high=service["price_high"],
                    price_emergency=service["price_emergency"],
                    service_list=service["services"],
                    modifier=modifier_key,
                    modifier_data=modifier_data,
                    faqs=modifier_data["faqs"],
                    title=title,
                    h1_title=h1_title,
                    description=description,
                    canonical_url=f"https://handwerker-ratgeber.de/{filename}",
                    current_year=2026
                )

                # 保存文件
                (output_dir / filename).write_text(html, encoding="utf-8")
                count += 1

    print(f"\nGenerated {count} pages in {output_dir}/")

if __name__ == "__main__":
    main()
```

**验证**:
```bash
python scripts/generate_pages.py
# 应输出: Generated 360 pages in output/
ls output/ | wc -l
# 应输出: 360
```

### Task 1.6: 生成Sitemap

**文件**: `scripts/generate_sitemap.py`

```python
#!/usr/bin/env python3
"""
生成sitemap.xml
"""
import json
from datetime import datetime
from pathlib import Path

def main():
    # 加载数据
    cities = json.loads(Path("data/cities.json").read_text(encoding="utf-8"))
    services = json.loads(Path("data/services.json").read_text(encoding="utf-8"))
    modifiers = json.loads(Path("data/modifiers.json").read_text(encoding="utf-8"))["modifiers"]

    base_url = "https://handwerker-ratgeber.de"
    urls = []

    # 收集所有URL
    for city in cities:
        for service in services:
            for modifier_key in modifiers.keys():
                filename = f"{service['slug']}-{city['slug']}{modifier_key}.html"
                urls.append(f"{base_url}/{filename}")

    # 添加法律页面
    urls.extend([
        f"{base_url}/impressum",
        f"{base_url}/datenschutz"
    ])

    # 生成XML
    today = datetime.now().strftime("%Y-%m-%d")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{base_url}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
"""
    for url in urls:
        xml += f"""
    <url>
        <loc>{url}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>"""

    xml += "\n</urlset>"

    # 保存文件
    Path("output/sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"Generated sitemap with {len(urls)} URLs")

if __name__ == "__main__":
    main()
```

**验证**:
```bash
python scripts/generate_sitemap.py
# 应输出: Generated sitemap with 360 URLs
```

### Task 1.7: 法律页面生成

**来源**: 使用 Dr. Thomas Schwenke 免费生成器

**步骤**:
1. 访问: https://www.dr-schwenke.de/datenschutz-generator-de/
2. 填写网站信息
3. 复制生成的 Impressum 和 Datenschutz
4. 保存到 `templates/impressum.html` 和 `templates/datenschutz.html`
5. 复制到 `output/` 目录

**验证**: 法律页面包含所有必需元素

### Task 1.8: 部署配置

**文件**: `.github/workflows/deploy.yml`

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests jinja2 tqdm

      - name: Fetch cities
        run: python scripts/fetch_cities.py

      - name: Generate pages
        run: python scripts/generate_pages.py

      - name: Generate sitemap
        run: python scripts/generate_sitemap.py

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: handwerker-ratgeber
          directory: output
```

**验证**: 推送到GitHub触发部署

### Task 1.9: 提交Google Search Console

1. 在Google Search Console添加域名
2. 验证域名所有权
3. 提交sitemap.xml: `https://handwerker-ratgeber.de/sitemap.xml`
4. 监控索引状态

**验证**: Search Console显示"已发现"URL数量

---

## Phase 2: 扩展（3200页）

### Task 2.1: 添加3个Modifier

**新增Modifier**:
- `preis` - 价格对比
- `empfehlung` - 推荐列表
- `in-der-naehe` - 附近覆盖

**文件**: 更新 `data/modifiers.json`

### Task 2.2: 扩展到100城市

**更新**: `scripts/fetch_cities.py` 中的limit参数

### Task 2.3: 添加4个新服务

- Dachdecker (屋顶工)
- Maler (油漆工)
- Fliesenleger (瓷砖工)
- Gärtner (园丁)

### Task 2.4: 可选：AI内容增强

使用DeepSeek或智谱AI进行内容差异化：
- 每个服务添加3-5个本地化段落
- 根据城市特点定制内容

---

## Phase 3: 规模化（24000页）

### Task 3.1: 扩展到500城市

- 人口 > 20,000
- 添加城市元数据（行政区、地标）

### Task 3.2: 完整6个Modifier

- 启用所有6个Modifier
- 收入潜力: $500-3000/月

### Task 3.3: 多语言扩展

- 奥地利 (at)
- 瑞士 (ch)

---

## 成功标准

### Phase 1 (Month 1-2)
- [ ] 360页全部生成
- [ ] 100-200页被Google索引
- [ ] 10-50访问/天
- [ ] 验证关键词效果

### Phase 2 (Month 3-6)
- [ ] 3200页全部生成
- [ ] 1500-2000页被索引
- [ ] 100-500访问/天
- [ ] $50-200/月收入

### Phase 3 (Month 7+)
- [ ] 24000页全部生成
- [ ] 15000+页被索引
- [ ] 500-5000访问/天
- [ ] $500-3000/月收入

---

## 相关文档

| 文档 | 用途 |
|------|------|
| [README.md](./README.md) | ⭐ 项目索引和核心参数 |
| [blueprint.md](./blueprint.md) | ⭐⭐ 完整执行指南 |
| [overview.md](./overview.md) | 项目概述 |
| [CLAUDE.md](./CLAUDE.md) | 开发者规范 |

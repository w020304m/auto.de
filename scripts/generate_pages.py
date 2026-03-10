#!/usr/bin/env python3
"""
零AI页面生成脚本 - 使用干净URL结构 + 增强SEO模块
Phase 1: 31城市 × 4服务 × 3 Modifier = 372页

新增SEO模块:
1. "Wann brauchen Sie" - 何时需要服务（200字）
2. "Servicegebiete" - 服务区域（200字）
3. "Andere Städte" - 城市内链（5+城市）
"""
import json
import sys
import io
from pathlib import Path
from jinja2 import Template
from random import sample

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

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

def get_nearby_cities(current_city: dict, all_cities: list, count: int = 7) -> list:
    """获取附近的城市用于内链（排除当前城市）"""
    # 选择人口最多或随机选择的城市
    other_cities = [c for c in all_cities if c['slug'] != current_city['slug']]

    # 优先选择大城市，然后随机补充
    sorted_by_pop = sorted(other_cities, key=lambda x: x['population'], reverse=True)

    # 前5个大城市 + 随机2个
    nearby = sorted_by_pop[:5]
    if len(other_cities) > 5:
        remaining = [c for c in other_cities if c not in nearby]
        nearby.extend(sample(remaining, min(count - len(nearby), len(remaining))))

    return nearby[:count]

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
    print(f"Generating {total} pages with enhanced SEO modules...")

    count = 0
    for city in cities:
        for service in services:
            # 获取附近城市（用于内链）
            nearby_cities = get_nearby_cities(city, cities, count=7)

            for modifier_key, modifier_data in modifiers.items():
                # 生成标题
                title, h1_title, description = generate_title(
                    city["name"],
                    service["name"],
                    modifier_key,
                    modifier_data
                )

                # 目录名和干净的URL
                modifier_suffix = f"-{modifier_key}" if modifier_key else ""
                url_path = f"{service['slug']}-{city['slug']}{modifier_suffix}"
                clean_url = f"https://auto-de.pages.dev/{url_path}/"

                # 创建目录并保存index.html
                page_dir = output_dir / url_path
                page_dir.mkdir(parents=True, exist_ok=True)

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
                    canonical_url=clean_url,
                    nearby_cities=nearby_cities,
                    current_year=2026
                )

                # 保存为 index.html
                (page_dir / "index.html").write_text(html, encoding="utf-8")
                count += 1

        print(f"Generated pages for {city['name']}: {count}/{total}")

    print(f"\nGenerated {count} pages in {output_dir}/")
    print(f"URL structure: /service-city/ (clean URLs)")
    print(f"SEO modules: When-needed + Service areas + City internal links")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
生成sitemap.xml - 使用干净URL结构
URL格式: /klempner-berlin/ (不是 .html)
"""
import json
from datetime import datetime
from pathlib import Path

def main():
    # 加载数据
    cities = json.loads(Path("data/cities.json").read_text(encoding="utf-8"))
    services = json.loads(Path("data/services.json").read_text(encoding="utf-8"))
    modifiers = json.loads(Path("data/modifiers.json").read_text(encoding="utf-8"))["modifiers"]

    base_url = "https://auto-de.pages.dev"
    urls = []

    # 收集所有URL（使用干净URL结构）
    for city in cities:
        for service in services:
            for modifier_key in modifiers.keys():
                modifier_suffix = f"-{modifier_key}" if modifier_key else ""
                # 干净URL: /klempner-berlin/ 而不是 /klempner-berlin.html
                url_path = f"{service['slug']}-{city['slug']}{modifier_suffix}/"
                urls.append(f"{base_url}/{url_path}")

    # 添加法律页面
    urls.extend([
        f"{base_url}/impressum/",
        f"{base_url}/datenschutz/"
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
    print(f"Generated sitemap with {len(urls)} clean URLs")
    print(f"URL format: /service-city/ (without .html)")

if __name__ == "__main__":
    main()

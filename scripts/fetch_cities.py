#!/usr/bin/env python3
"""
从OpenPLZ API获取德国城市数据
正确使用联邦州端点获取所有城市
API文档: https://www.openplzapi.org/de/germany/
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

# 德国16个联邦州代码
FEDERAL_STATES = {
    "01": "Schleswig-Holstein",
    "02": "Hamburg",
    "03": "Niedersachsen",
    "04": "Bremen",
    "05": "Nordrhein-Westfalen",
    "06": "Hessen",
    "07": "Rheinland-Pfalz",
    "08": "Baden-Württemberg",
    "09": "Bayern",
    "10": "Saarland",
    "11": "Berlin",
    "12": "Brandenburg",
    "13": "Mecklenburg-Vorpommern",
    "14": "Sachsen",
    "15": "Sachsen-Anhalt",
    "16": "Thüringen"
}

def fetch_cities_from_state(state_key: str, state_name: str) -> list:
    """从单个联邦州获取城市数据"""
    cities = []
    url = f"https://openplzapi.org/de/FederalStates/{state_key}/Localities"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        for item in data:
            # OpenPLZ API返回的数据结构
            cities.append({
                "name": item.get("name", ""),
                "slug": slugify(item.get("name", "")),
                "population": 0,  # OpenPLZ Localities端点不返回人口数据
                "state": state_name,
                "postalCode": item.get("postalCode", ""),
                "lat": None,
                "lng": None
            })

        print(f"Fetched {len(cities)} cities from {state_name}")

    except Exception as e:
        print(f"Error fetching {state_name}: {e}")

    return cities

def fetch_all_cities() -> list:
    """从所有联邦州获取城市"""
    all_cities = []

    for state_key, state_name in FEDERAL_STATES.items():
        cities = fetch_cities_from_state(state_key, state_name)
        all_cities.extend(cities)

    return all_cities

def get_major_cities_with_population(limit: int = 30) -> list:
    """
    获取德国主要城市数据
    注意：OpenPLZ Localities端点不提供人口数据，
    因此我们使用预定义的主要城市列表
    """
    # 德国30个主要城市（按人口排序），数据来源：德国联邦统计局
    major_cities = [
        {"name": "Berlin", "population": 3644826, "state": "Berlin", "postalCode": "10115", "lat": 52.52, "lng": 13.405},
        {"name": "Hamburg", "population": 1841179, "state": "Hamburg", "postalCode": "20095", "lat": 53.5511, "lng": 9.9937},
        {"name": "München", "population": 1471508, "state": "Bayern", "postalCode": "80331", "lat": 48.1351, "lng": 11.582},
        {"name": "Köln", "population": 1085664, "state": "Nordrhein-Westfalen", "postalCode": "50667", "lat": 50.9375, "lng": 6.9603},
        {"name": "Frankfurt am Main", "population": 753056, "state": "Hessen", "postalCode": "60311", "lat": 50.1109, "lng": 8.6821},
        {"name": "Stuttgart", "population": 634830, "state": "Baden-Württemberg", "postalCode": "70173", "lat": 48.7758, "lng": 9.1829},
        {"name": "Düsseldorf", "population": 619294, "state": "Nordrhein-Westfalen", "postalCode": "40210", "lat": 51.2277, "lng": 6.7735},
        {"name": "Leipzig", "population": 587857, "state": "Sachsen", "postalCode": "04109", "lat": 51.3406, "lng": 12.3747},
        {"name": "Dortmund", "population": 587010, "state": "Nordrhein-Westfalen", "postalCode": "44137", "lat": 51.5136, "lng": 7.4653},
        {"name": "Essen", "population": 583109, "state": "Nordrhein-Westfalen", "postalCode": "45127", "lat": 51.4556, "lng": 7.0116},
        {"name": "Bremen", "population": 569352, "state": "Bremen", "postalCode": "28195", "lat": 53.0793, "lng": 8.8017},
        {"name": "Dresden", "population": 556227, "state": "Sachsen", "postalCode": "01067", "lat": 51.0504, "lng": 13.7373},
        {"name": "Hannover", "population": 534049, "state": "Niedersachsen", "postalCode": "30159", "lat": 52.3759, "lng": 9.732},
        {"name": "Nürnberg", "population": 518365, "state": "Bayern", "postalCode": "90402", "lat": 49.4521, "lng": 11.0767},
        {"name": "Duisburg", "population": 498718, "state": "Nordrhein-Westfalen", "postalCode": "47051", "lat": 51.4345, "lng": 6.7623},
        {"name": "Bochum", "population": 364628, "state": "Nordrhein-Westfalen", "postalCode": "44787", "lat": 51.4818, "lng": 7.2162},
        {"name": "Wuppertal", "population": 354952, "state": "Nordrhein-Westfalen", "postalCode": "42103", "lat": 51.2562, "lng": 7.1508},
        {"name": "Bielefeld", "population": 333450, "state": "Nordrhein-Westfalen", "postalCode": "33602", "lat": 52.0302, "lng": 8.5325},
        {"name": "Bonn", "population": 330577, "state": "Nordrhein-Westfalen", "postalCode": "53111", "lat": 50.7374, "lng": 7.0982},
        {"name": "Münster", "population": 314519, "state": "Nordrhein-Westfalen", "postalCode": "48143", "lat": 51.9624, "lng": 7.6257},
        {"name": "Karlsruhe", "population": 308879, "state": "Baden-Württemberg", "postalCode": "76133", "lat": 49.0069, "lng": 8.4037},
        {"name": "Mannheim", "population": 307731, "state": "Baden-Württemberg", "postalCode": "68159", "lat": 49.4875, "lng": 8.466},
        {"name": "Augsburg", "population": 296582, "state": "Bayern", "postalCode": "86150", "lat": 48.3667, "lng": 10.8947},
        {"name": "Wiesbaden", "population": 277505, "state": "Hessen", "postalCode": "65183", "lat": 50.0783, "lng": 8.2398},
        {"name": "Gelsenkirchen", "population": 257769, "state": "Nordrhein-Westfalen", "postalCode": "45879", "lat": 51.5051, "lng": 7.0996},
        {"name": "Mönchengladbach", "population": 254891, "state": "Nordrhein-Westfalen", "postalCode": "41061", "lat": 51.185, "lng": 6.4426},
        {"name": "Braunschweig", "population": 246480, "state": "Niedersachsen", "postalCode": "38100", "lat": 52.2659, "lng": 10.5267},
        {"name": "Chemnitz", "population": 246165, "state": "Sachsen", "postalCode": "09107", "lat": 50.8323, "lng": 12.9211},
        {"name": "Kiel", "population": 246039, "state": "Schleswig-Holstein", "postalCode": "24103", "lat": 54.3233, "lng": 10.1228},
        {"name": "Aachen", "population": 245885, "state": "Nordrhein-Westfalen", "postalCode": "52062", "lat": 50.7753, "lng": 6.0839},
        {"name": "Halle (Saale)", "population": 234829, "state": "Sachsen-Anhalt", "postalCode": "06108", "lat": 51.4814, "lng": 11.9706}
    ]

    # 转换为目标格式
    result = []
    for city in major_cities[:limit]:
        result.append({
            "name": city["name"],
            "slug": slugify(city["name"]),
            "population": city["population"],
            "state": city["state"],
            "postalCode": city["postalCode"],
            "lat": city["lat"],
            "lng": city["lng"]
        })

    return result

if __name__ == "__main__":
    print("Fetching major German cities...")
    print("Note: Using predefined list with official population data from Destatis\n")

    cities = get_major_cities_with_population(limit=31)

    # 保存到文件
    output_path = Path("data/cities.json")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(cities, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"Saved {len(cities)} cities to {output_path}")
    print(f"Population range: {min(c['population'] for c in cities):,} - {max(c['population'] for c in cities):,}")
    print(f"{'='*60}")
    print("\nCities included:")
    for city in cities:
        print(f"  - {city['name']:25} ({city['population']:>10,} inhabitants)")

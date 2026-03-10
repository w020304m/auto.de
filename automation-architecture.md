# PSEO Germany Handwerker - Multi-Agent全自动化架构

本文档描述如何通过Multi-Agent协同实现全自动化PSEO，将人工干预降到最低。

---

## 一、自动化架构设计

### 1.1 Agent系统架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MASTER AGENT (orchestrator)                      │
│  任务编排 | 状态监控 | 错误恢复 | 性能优化                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│  DATA AGENT   │           │CONTENT AGENT  │           │ QUALITY AGENT │
│ 数据获取专家  │           │  内容生成专家  │           │  质量检查专家  │
├───────────────┤           ├───────────────┤           ├───────────────┤
│ • 城市数据    │           │ • 文章生成    │           │ • 内容评估    │
│ • 服务配置    │           │ • Prompt优化  │           │ • SEO检查     │
│ • API调用     │           │ • 多样化处理  │           │ • 相似度检测  │
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
│ • Impressum   │           │ • 关键词研究  │           │ • A/B测试     │
│ • Datenschutz │           │ • Meta优化    │           │ • 性能监控    │
│ • GDPR检查    │           │ • 结构化数据  │           │ • 自动报告    │
└───────────────┘           └───────────────┘           └───────────────┘
```

### 1.2 工作流编排

```yaml
# 完全自动化工作流
workflow:
  name: "PSEO Full Automation"
  trigger:
    - schedule: "0 0 * * 0"  # 每周日
    - manual: true
    - webhook: true

  stages:
    - stage: "Data Preparation"
      agent: "Data Agent"
      tasks:
        - fetch_cities
        - validate_services
        - enrich_metadata

    - stage: "Content Generation"
      agent: "Content Agent"
      parallel: true
      tasks:
        - generate_articles
        - generate_legal_pages
        - create_variants

    - stage: "Quality Assurance"
      agent: "Quality Agent"
      tasks:
        - check_seo_score
        - detect_duplicates
        - validate_localization

    - stage: "SEO Optimization"
      agent: "SEO Agent"
      tasks:
        - generate_sitemap
        - optimize_metadata
        - create_structured_data

    - stage: "Analytics & Feedback"
      agent: "Analytics Agent"
      tasks:
        - run_ab_tests
        - generate_reports
        - update_prompts
```

---

## 二、Agent详细设计

### 2.1 Master Agent (orchestrator)

**职责**: 任务编排、状态管理、错误恢复

```python
# agents/master_agent.py
from typing import List, Dict, Any
from enum import Enum
import asyncio

class AgentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

class MasterAgent:
    """
    主控Agent - 负责任务编排和协调
    """

    def __init__(self):
        self.agents = {
            "data": DataAgent(),
            "content": ContentAgent(),
            "quality": QualityAgent(),
            "legal": LegalAgent(),
            "seo": SEOAgent(),
            "analytics": AnalyticsAgent()
        }
        self.workflow_state = {}
        self.retry_config = {
            "max_retries": 3,
            "backoff_factor": 2,
            "initial_delay": 1
        }

    async def execute_workflow(self, workflow_config: Dict) -> Dict[str, Any]:
        """
        执行完整工作流
        """
        results = {}

        for stage in workflow_config["stages"]:
            stage_name = stage["stage"]
            agent_name = stage["agent"]

            print(f"[Master] Executing stage: {stage_name}")

            try:
                # 执行Agent任务
                result = await self._execute_agent(
                    agent_name,
                    stage.get("tasks", [])
                )

                results[stage_name] = {
                    "status": "completed",
                    "result": result
                }

            except Exception as e:
                # 自动错误恢复
                recovered = await self._handle_error(
                    stage_name, agent_name, e
                )

                if not recovered:
                    results[stage_name] = {
                        "status": "failed",
                        "error": str(e)
                    }
                    break  # 停止工作流

        return results

    async def _execute_agent(self, agent_name: str, tasks: List[str]) -> Any:
        """
        执行单个Agent
        """
        agent = self.agents[agent_name]

        # 记录开始时间
        start_time = time.time()

        # 执行任务
        result = await agent.execute(tasks)

        # 记录执行时间
        execution_time = time.time() - start_time

        # 更新状态
        self.workflow_state[agent_name] = {
            "status": "completed",
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat()
        }

        return result

    async def _handle_error(self, stage: str, agent: str, error: Exception) -> bool:
        """
        自动错误恢复
        """
        print(f"[Master] Error in {stage}: {error}")

        # 获取重试配置
        retry_count = self.workflow_state.get(agent, {}).get("retry_count", 0)

        if retry_count < self.retry_config["max_retries"]:
            # 指数退避重试
            delay = self.retry_config["initial_delay"] * (
                self.retry_config["backoff_factor"] ** retry_count
            )

            print(f"[Master] Retrying {agent} in {delay}s...")
            await asyncio.sleep(delay)

            # 更新重试计数
            self.workflow_state[agent] = self.workflow_state.get(agent, {})
            self.workflow_state[agent]["retry_count"] = retry_count + 1

            # 重新执行
            return True

        return False
```

### 2.2 Content Agent (内容生成专家)

**职责**: AI内容生成、Prompt优化、内容多样化

```python
# agents/content_agent.py
from typing import List, Dict
import random
from datetime import datetime

class ContentAgent:
    """
    内容生成Agent - 负责所有AI内容生成
    """

    def __init__(self):
        self.prompt_variants = self._load_prompt_variants()
        self.style_templates = self._load_style_templates()
        self.localization_db = self._load_localization_data()

    async def execute(self, tasks: List[str]) -> Dict:
        """
        执行内容生成任务
        """
        results = {}

        for task in tasks:
            if task == "generate_articles":
                results["articles"] = await self._generate_all_articles()
            elif task == "generate_legal_pages":
                results["legal"] = await self._generate_legal_pages()
            elif task == "create_variants":
                results["variants"] = await self._create_content_variants()

        return results

    async def _generate_all_articles(self) -> List[Dict]:
        """
        生成所有文章（自动多样化）
        """
        articles = []

        # 加载数据
        cities = self._load_cities()
        services = self._load_services()

        for city in cities:
            for service in services:
                # 自动选择Prompt变体（增加多样性）
                prompt_variant = self._select_prompt_variant(
                    city, service
                )

                # 自动选择写作风格
                style = self._select_style(city)

                # 生成内容
                article = await self._generate_with_fallbacks(
                    city=city,
                    service=service,
                    prompt=prompt_variant,
                    style=style
                )

                articles.append({
                    "city": city["name"],
                    "service": service["name"],
                    "content": article,
                    "variant": prompt_variant["id"],
                    "style": style["id"]
                })

        return articles

    def _select_prompt_variant(self, city: Dict, service: Dict) -> Dict:
        """
        智能选择Prompt变体（基于城市特征）
        """
        # 城市分层策略
        population = city.get("population", 0)

        if population > 500000:
            # 大城市：使用详细Prompt
            return self.prompt_variants["detailed"]
        elif population > 100000:
            # 中城市：使用标准Prompt
            return self.prompt_variants["standard"]
        else:
            # 小城市：使用简洁Prompt
            return self.prompt_variants["concise"]

    def _select_style(self, city: Dict) -> Dict:
        """
        智能选择写作风格
        """
        # 根据城市特征选择风格
        state = city.get("state", "")

        if state in ["Berlin", "Hamburg", "Bremen"]:
            # 城市州：更现代的风格
            return self.style_templates["modern"]
        elif state in ["Bayern", "Baden-Württemberg"]:
            # 南部：更传统的风格
            return self.style_templates["traditional"]
        else:
            # 默认：平衡风格
            return self.style_templates["balanced"]

    async def _generate_with_fallbacks(
        self, city: Dict, service: Dict,
        prompt: Dict, style: Dict
    ) -> str:
        """
        带降级策略的内容生成
        """
        # 尝试主AI服务
        try:
            content = await self._call_ai_service(
                city=city,
                service=service,
                prompt=prompt,
                style=style,
                provider=os.getenv("AI_PROVIDER", "openai")
            )

            # 质量检查
            if self._quick_quality_check(content):
                return content

        except Exception as e:
            print(f"[Content Agent] Primary AI failed: {e}")

        # 降级到备用AI服务
        try:
            content = await self._call_ai_service(
                city=city,
                service=service,
                prompt=prompt,
                style=style,
                provider="fallback"  # 配置的备用服务
            )
            return content

        except Exception as e:
            print(f"[Content Agent] Fallback AI failed: {e}")

        # 最后的降级：使用模板
        return self._generate_template_content(city, service)

    def _load_prompt_variants(self) -> Dict:
        """
        加载多个Prompt变体（增加内容多样性）
        """
        return {
            "detailed": {
                "id": "detailed",
                "word_count": "1000-1200",
                "sections": 6,
                "localization": "high",
                "template": self._get_detailed_prompt()
            },
            "standard": {
                "id": "standard",
                "word_count": "800-1000",
                "sections": 5,
                "localization": "medium",
                "template": self._get_standard_prompt()
            },
            "concise": {
                "id": "concise",
                "word_count": "600-800",
                "sections": 4,
                "localization": "basic",
                "template": self._get_concise_prompt()
            }
        }

    def _get_detailed_prompt(self) -> str:
        """
        详细版Prompt（用于大城市）
        """
        return """
Du bist ein erfahrener deutscher SEO-Redakteur mit Fachwissen im Handwerksbereich.

AUFGABE: Schreibe einen umfassenden, lokalbezogenen Artikel über: {service} in {city}.

ANFORDERUNGEN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. UMFANG & STRUKTUR (1000-1200 Wörter)

   <h3>Warum {service} in {city} unverzichtbar ist</h3>
   <p>...Einleitung mit lokalen Bezug (min. 150 Wörter)...</p>

   <h3>Preisübersicht 2026: Was kosten {service} Leistungen in {city}?</h3>
   <p>...detaillierte Preisaufschlüsselung nach Dienstleistungen...</p>
   <p>...Einflussfaktoren auf den Preis...</p>

   <h3> {city} im Fokus: Besonderheiten der Region</h3>
   <p>...lokale Gegebenheiten, {city_districts_example}...</p>
   <p>...regionale Herausforderungen...</p>

   <h3>Auswahlkriterien: Finden Sie den besten {service} in {city}</h3>
   <ul>
     <li>Meisterbrief und Zertifizierungen</li>
     <li>Referenzen aus {city} und Umgebung</li>
     <li>Reaktionszeit und Verfügbarkeit</li>
     <li>Preis-Leistungs-Verhältnis</li>
     <li>Kundenservice und Garantien</li>
   </ul>

   <h3>Typische Projekte in {city}</h3>
   <p>...真实世界 Beispiele...</p>

   <h3>Tipps von Experten: Kosten sparen bei {service} Aufträgen</h3>
   <p>...praktische Ratschläge...</p>

2. SEO-OPTIMIERUNG
   - Hauptkeyword: "{service} {city}" – im ersten Absatz
   - Sekundäre: "{service} Preise {city}", "{service} {city} Kosten"
   - LSI Keywords: "Notdienst", "Wartung", "Reparatur", "Instanzhaltung"
   - Keyword-Dichte: 1.5-2%

3. LOKALISIERUNG (STRICT)
   - Mindestens 5 konkrete Erwähnungen von {city}
   - 2-3 Stadtteile/Regionen nennen
   - Lokale Besonderheiten einbeziehen

4. QUALITÄT
   - Fachkorrekte Terminologie
   - Verweise auf DIN-Normen/VDI-Richtlinien
   - Vermeidung von Floskeln
"""

    def _get_standard_prompt(self) -> str:
        """
        标准版Prompt（用于中城市）
        """
        return """
Du bist ein erfahrener deutscher SEO-Redakteur.

AUFGABE: Schreibe einen informativen Artikel über: {service} in {city}.

ANFORDERUNGEN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. UMFANG: 800-1000 Wörter

2. STRUKTUR:
   <h3>Warum {service} in {city} wichtig ist</h3>
   <p>...Einleitung mit lokalem Bezug...</p>

   <h3>Preise für {service} in {city}</h3>
   <p>...Preisspanne €{price_low}-€{price_high}/h...</p>

   <h3>Worauf bei der Auswahl achten</h3>
   <ul>
     <li>Zertifizierungen</li>
     <li>Kundenbewertungen aus {city}</li>
     <li>Reaktionszeit</li>
   </ul>

   <h3>Einsatzgebiete in {city}</h3>
   <p>...lokale Bezüge...</p>

   <h3>Kostenspar-Tipps</h3>
   <p>...praktische Ratschläge...</p>

3. SEO: Hauptkeyword "{service} {city}" im ersten Absatz
4. LOKALISIERUNG: Mindestens 3 Erwähnungen von {city}
"""

    def _get_concise_prompt(self) -> str:
        """
        简洁版Prompt（用于小城市）
        """
        return """
Du bist ein deutscher SEO-Redakteur.

AUFGABE: Schreibe einen Artikel über: {service} in {city}.

ANFORDERUNGEN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. UMFANG: 600-800 Wörter

2. STRUKTUR:
   <h3>{service} in {city}</h3>
   <p>...Einleitung...</p>

   <h3>Preise & Leistungen</h3>
   <p>€{price_low}-€{price_high}/h...</p>

   <h3>Auswahlkriterien</h3>
   <p>...Zertifizierungen, Bewertungen...</p>

   <h3>Tipps für {city}</h3>
   <p>...lokale Ratschläge...</p>

3. SEO: "{service} {city}" im ersten Absatz
4. LOKALISIERUNG: Mindestens 2 Erwähnungen von {city}
"""

    def _load_style_templates(self) -> Dict:
        """
        加载写作风格模板
        """
        return {
            "modern": {
                "id": "modern",
                "tone": "freundlich, direkt",
                "sentence_length": "kurz",
                "vocabulary": "aktuell"
            },
            "traditional": {
                "id": "traditional",
                "tone": "seriös, sachlich",
                "sentence_length": "mittel",
                "vocabulary": "klassisch"
            },
            "balanced": {
                "id": "balanced",
                "tone": "professionell, verständlich",
                "sentence_length": "variiert",
                "vocabulary": "allgemeinverständlich"
            }
        }
```

### 2.3 Legal Agent (法律合规专家)

**职责**: 自动生成法律页面、GDPR检查

```python
# agents/legal_agent.py
from typing import Dict, List
import json

class LegalAgent:
    """
    法律合规Agent - 自动生成德国法律要求页面
    """

    def __init__(self):
        self.company_info = self._load_company_info()
        self.legal_templates = self._load_legal_templates()

    async def execute(self, tasks: List[str]) -> Dict:
        """
        执行法律合规任务
        """
        results = {}

        for task in tasks:
            if task == "generate_impressum":
                results["impressum"] = await self._generate_impressum()
            elif task == "generate_datenschutz":
                results["datenschutz"] = await self._generate_datenschutz()
            elif task == "check_gdpr":
                results["gdpr_check"] = await self._check_gdpr_compliance()

        return results

    async def _generate_impressum(self) -> str:
        """
        自动生成Impressum页面（德国法律强制要求）
        """
        # 使用AI生成个性化内容
        prompt = f"""
        Erstelle ein professionelles Impressum für eine deutsche Website.

        Angaben:
        - Website: handwerker-ratgeber.de
        - Zweck: Informationsplattform für Handwerkerdienste
        - Inhalt: Preisvergleich, Tipps, Empfehlungen

        Gemäß § 5 TMG (Telemediengesetz) muss das Impressum enthalten:
        1. Name der Firma
        2. Anschrift der Firma
        3. Kontaktmöglichkeiten (E-Mail)
        4. Ggf. Umsatzsteuer-ID
        5. Ggf. Registereintrag
        6. Ggf. Verantwortlicher i.S.d. § 18 MStV

        Erstelle ein komplettes, rechtssicheres Impressum.
        Verwende Platzhalter [PLATZHALTER] für noch nicht bekannte Angaben.
        """

        impressum = await self._call_ai(prompt)
        return impressum

    async def _generate_datenschutz(self) -> str:
        """
        自动生成Datenschutz页面（GDPR合规）
        """
        prompt = f"""
        Erstelle eine vollständige Datenschutzseite für eine deutsche Website.

        Website: handwerker-ratgeber.de
        Zweck: Informationsplattform mit Google AdSense Werbung

        Die Datenschutzseite muss gemäß DSGVO (GDPR) enthalten:
        1. Name und Kontaktdaten des Verantwortlichen
        2. Zwecke der Datenverarbeitung
        3. Kategorien von betroffenen Personen
        4. Kategorien von Empfängern
        5. Geplante Speicherdauer
        6. Betroffenenrechte (Auskunft, Berichtigung, Löschung, etc.)
        7. Widerrufsrecht bei Einwilligung
        8. Beschwerderecht bei Aufsichtsbehörde
        9. Pflicht zur Bereitstellung der Daten
        10. Automatisierte Entscheidungsfindung (falls zutreffend)
        11. Cookies und Google AdSense
        12. Google Analytics (falls verwendet)
        13. Server-Log-Files

        Erstelle eine vollständige, rechtssichere Datenschutzerklärung.
        """

        datenschutz = await self._call_ai(prompt)
        return datenschutz

    async def _check_gdpr_compliance(self) -> Dict:
        """
        自动检查GDPR合规性
        """
        checks = {
            "impressum_exists": False,
            "datenschutz_exists": False,
            "cookie_consent": False,
            "data_minimization": False,
            "right_withdrawal": False
        }

        # 检查Impressum
        if Path("output/impressum.html").exists():
            checks["impressum_exists"] = True
            content = Path("output/impressum.html").read_text()
            # AI检查内容完整性
            checks["impressum_complete"] = await self._ai_check_impressum(content)

        # 检查Datenschutz
        if Path("output/datenschutz.html").exists():
            checks["datenschutz_exists"] = True
            content = Path("output/datenschutz.html").read_text()
            # AI检查GDPR要素
            checks["gdpr_complete"] = await self._ai_check_gdpr_elements(content)

        return checks

    async def _ai_check_impressum(self, content: str) -> bool:
        """
        使用AI检查Impressum完整性
        """
        prompt = f"""
        Prüfe folgendes Impressum auf Vollständigkeit gemäß § 5 TMG:

        {content}

        Prüfpunkte:
        1. Name der Firma ✓/✗
        2. Anschrift ✓/✗
        3. Kontakt (E-Mail/Telefon) ✓/✗
        4. Umsatzsteuer-ID (falls vorhanden) ✓/✗
        5. Registereintrag (falls vorhanden) ✓/✗

        Gib als Ergebnis nur "COMPLETE" oder "INCOMPLETE" zurück,
        gefolgt von einer kurzen Liste der fehlenden Elemente.
        """

        result = await self._call_ai(prompt)
        return "COMPLETE" in result

    async def _ai_check_gdpr_elements(self, content: str) -> bool:
        """
        使用AI检查GDPR要素
        """
        prompt = f"""
        Prüfe folgende Datenschutzerklärung auf alle erforderlichen DSGVO-Elemente:

        {content}

        Erforderliche Elemente:
        1. Verantwortlicher
        2. Kontakt
        3. Zwecke der Verarbeitung
        4. Empfänger
        5. Speicherdauer
        6. Betroffenenrechte
        7. Widerrufsrecht
        8. Beschwerderecht
        9. Cookies
        10. Google AdSense

        Gib als Ergebnis nur "COMPLETE" oder "INCOMPLETE" zurück,
        gefolgt von einer kurzen Liste der fehlenden Elemente.
        """

        result = await self._call_ai(prompt)
        return "COMPLETE" in result
```

### 2.4 Quality Agent (质量检查专家)

**职责**: 自动内容评估、SEO评分、相似度检测

```python
# agents/quality_agent.py
from typing import Dict, List
from difflib import SequenceMatcher
import re

class QualityAgent:
    """
    质量检查Agent - 自动评估生成内容
    """

    def __init__(self):
        self.quality_thresholds = {
            "word_count_min": 600,
            "word_count_max": 1500,
            "keyword_density_min": 0.008,
            "keyword_density_max": 0.02,
            "local_mentions_min": 2,
            "readability_min": 30,  # Flesch Reading Ease
            "similarity_max": 0.7
        }

    async def execute(self, tasks: List[str]) -> Dict:
        """
        执行质量检查任务
        """
        results = {}

        for task in tasks:
            if task == "check_seo_score":
                results["seo_scores"] = await self._check_all_seo_scores()
            elif task == "detect_duplicates":
                results["duplicates"] = await self._detect_duplicates()
            elif task == "validate_localization":
                results["localization"] = await self._validate_localization()

        return results

    async def _check_all_seo_scores(self) -> List[Dict]:
        """
        检查所有页面的SEO评分
        """
        scores = []

        articles_path = Path("content/ai_articles")
        for article_file in articles_path.glob("*.html"):
            content = article_file.read_text(encoding="utf-8")

            # 计算SEO评分
            score = await self._calculate_seo_score(content)

            scores.append({
                "file": article_file.name,
                "score": score["total"],
                "details": score["details"]
            })

            # 自动标记低分页面
            if score["total"] < 70:
                await self._mark_for_regeneration(article_file)

        return scores

    async def _calculate_seo_score(self, content: str) -> Dict:
        """
        计算SEO评分（0-100）
        """
        scores = {}

        # 1. 字数检查 (20分)
        word_count = len(content.split())
        if self.quality_thresholds["word_count_min"] <= word_count <= self.quality_thresholds["word_count_max"]:
            scores["word_count"] = (20, word_count)
        else:
            scores["word_count"] = (0, word_count)

        # 2. 关键词密度 (20分)
        # 提取城市和服务名称（从文件名）
        density = self._calculate_keyword_density(content)
        if self.quality_thresholds["keyword_density_min"] <= density <= self.quality_thresholds["keyword_density_max"]:
            scores["keyword_density"] = (20, density)
        else:
            scores["keyword_density"] = (0, density)

        # 3. 本地化 (20分)
        local_mentions = self._count_local_mentions(content)
        local_score = min(20, local_mentions * 5)
        scores["localization"] = (local_score, local_mentions)

        # 4. 可读性 (20分)
        readability = self._calculate_readability(content)
        readability_score = max(0, min(20, readability))
        scores["readability"] = (readability_score, readability)

        # 5. HTML结构 (20分)
        structure_score = self._check_html_structure(content)
        scores["structure"] = (structure_score, structure_score)

        # 计算总分
        total = sum(score[0] for score in scores.values())

        return {
            "total": total,
            "details": scores
        }

    def _calculate_keyword_density(self, content: str) -> float:
        """
        计算关键词密度
        """
        # 从内容中提取关键词（需要改进）
        words = content.lower().split()
        total_words = len(words)

        # 简化：这里应该是从元数据提取
        # 实际实现需要更复杂的逻辑
        return 0.015  # 示例值

    def _count_local_mentions(self, content: str) -> int:
        """
        统计本地化提及次数
        """
        # 检查德语本地化关键词
        local_keywords = [
            "in dieser Region",
            "vor Ort",
            "in Ihrer Nähe",
            "aus",
            "bei"
        ]

        count = 0
        for keyword in local_keywords:
            count += content.lower().count(keyword)

        return count

    def _calculate_readability(self, content: str) -> float:
        """
        计算可读性分数（简化版Flesch Reading Ease）
        """
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', content)

        # 计算平均句子长度
        sentences = text.split('.')
        avg_sentence_length = len(text.split()) / max(1, len(sentences))

        # 简化评分
        if avg_sentence_length < 15:
            return 20  # 易读
        elif avg_sentence_length < 20:
            return 15  # 中等
        else:
            return 10  # 难读

    def _check_html_structure(self, content: str) -> int:
        """
        检查HTML结构
        """
        score = 0

        # 检查必要元素
        if "<h1>" in content or "<h1 " in content:
            score += 5
        if "<h2>" in content or "<h2 " in content:
            score += 3
        if "<h3>" in content or "<h3 " in content:
            score += 2
        if "<ul>" in content or "<ol>" in content:
            score += 5
        if "<p>" in content or "<p " in content:
            score += 5

        return score

    async def _detect_duplicates(self) -> List[Dict]:
        """
        检测相似内容
        """
        duplicates = []

        articles_path = Path("content/ai_articles")
        articles = list(articles_path.glob("*.html"))

        # 两两比较
        for i, article1 in enumerate(articles):
            for article2 in articles[i+1:]:
                content1 = article1.read_text(encoding="utf-8")
                content2 = article2.read_text(encoding="utf-8")

                similarity = SequenceMatcher(None, content1, content2).ratio()

                if similarity > self.quality_thresholds["similarity_max"]:
                    duplicates.append({
                        "file1": article1.name,
                        "file2": article2.name,
                        "similarity": similarity
                    })

                    # 自动标记重新生成
                    await self._mark_for_regeneration(article2)

        return duplicates

    async def _mark_for_regeneration(self, file_path: Path):
        """
        标记需要重新生成的文件
        """
        # 移动到待重新生成目录
        regen_dir = Path("content/to_regenerate")
        regen_dir.mkdir(exist_ok=True)

        new_path = regen_dir / file_path.name
        file_path.rename(new_path)

        print(f"[Quality Agent] Marked for regeneration: {file_path.name}")

    async def _validate_localization(self) -> Dict:
        """
        验证本地化程度
        """
        results = {
            "valid": [],
            "invalid": [],
            "needs_improvement": []
        }

        articles_path = Path("content/ai_articles")
        for article_file in articles_path.glob("*.html"):
            content = article_file.read_text(encoding="utf-8")

            # 提取城市名称
            city_match = re.search(r'(\w+)\.html', article_file.name)
            if city_match:
                city_slug = city_match.group(1)
                city_name = self._slug_to_city_name(city_slug)

                # 统计城市提及次数
                mentions = content.lower().count(city_name.lower())

                if mentions >= self.quality_thresholds["local_mentions_min"]:
                    results["valid"].append(article_file.name)
                elif mentions >= 1:
                    results["needs_improvement"].append(article_file.name)
                else:
                    results["invalid"].append(article_file.name)

        return results

    def _slug_to_city_name(self, slug: str) -> str:
        """
        将slug转换回城市名称
        """
        return slug.replace("-", " ").title()
```

### 2.5 SEO Agent (SEO优化专家)

**职责**: 自动SEO优化、Sitemap生成、结构化数据

```python
# agents/seo_agent.py
from typing import Dict, List
from datetime import datetime
import json

class SEOAgent:
    """
    SEO优化Agent - 自动SEO优化
    """

    def __init__(self):
        self.base_url = "https://handwerker-ratgeber.de"

    async def execute(self, tasks: List[str]) -> Dict:
        """
        执行SEO优化任务
        """
        results = {}

        for task in tasks:
            if task == "generate_sitemap":
                results["sitemap"] = await self._generate_sitemap()
            elif task == "optimize_metadata":
                results["metadata"] = await self._optimize_all_metadata()
            elif task == "create_structured_data":
                results["structured_data"] = await self._create_all_structured_data()

        return results

    async def _generate_sitemap(self) -> str:
        """
        自动生成sitemap.xml
        """
        # 获取所有HTML文件
        output_path = Path("output")
        html_files = list(output_path.glob("*.html"))

        # 构建sitemap
        urls = []

        for html_file in html_files:
            # 从文件名提取URL
            url = f"{self.base_url}/{html_file.stem}"

            # 获取文件修改时间
            mtime = html_file.stat().st_mtime
            lastmod = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

            urls.append(f"""
    <url>
        <loc>{url}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>""")

        # 生成完整sitemap
        sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{self.base_url}/</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
{''.join(urls)}
</urlset>"""

        # 保存sitemap
        sitemap_path = Path("output/sitemap.xml")
        sitemap_path.write_text(sitemap, encoding="utf-8")

        return f"Generated sitemap with {len(urls) + 1} URLs"

    async def _optimize_all_metadata(self) -> List[Dict]:
        """
        自动优化所有页面的metadata
        """
        results = []

        output_path = Path("output")
        for html_file in output_path.glob("*.html"):
            content = html_file.read_text(encoding="utf-8")

            # AI生成优化的metadata
            optimized = await self._ai_generate_metadata(content)

            # 更新HTML
            updated_content = self._update_metadata(content, optimized)

            # 保存
            html_file.write_text(updated_content, encoding="utf-8")

            results.append({
                "file": html_file.name,
                "optimized": True
            })

        return results

    async def _ai_generate_metadata(self, content: str) -> Dict:
        """
        使用AI生成优化的metadata
        """
        prompt = f"""
        Analysiere folgenden HTML-Inhalt und erstelle optimierte SEO-Metadata.

        Inhalt:
        {content[:1000]}  <!-- 前1000字符 -->

        Erstelle:
        1. Title (max 60 Zeichen,.keyword am Anfang)
        2. Meta Description (max 160 Zeichen, CTA am Ende)
        3. 3-5 Keywords (als JSON-Array)

        Format als JSON:
        {{
          "title": "...",
          "description": "...",
          "keywords": ["..."]
        }}
        """

        result = await self._call_ai(prompt)

        try:
            return json.loads(result)
        except:
            # 降级到基本metadata
            return {
                "title": "Handwerker Ratgeber",
                "description": "Finden Sie den besten Handwerker in Ihrer Nähe.",
                "keywords": []
            }

    def _update_metadata(self, content: str, metadata: Dict) -> str:
        """
        更新HTML中的metadata
        """
        # 替换title
        content = re.sub(
            r'<title>.*?</title>',
            f'<title>{metadata["title"]}</title>',
            content
        )

        # 替换meta description
        content = re.sub(
            r'<meta name="description"[^>]*content="[^"]*"',
            f'<meta name="description" content="{metadata["description"]}"',
            content
        )

        return content

    async def _create_all_structured_data(self) -> Dict:
        """
        自动为所有页面创建结构化数据
        """
        results = {}

        output_path = Path("output")
        for html_file in output_path.glob("*.html"):
            content = html_file.read_text(encoding="utf-8")

            # 检查是否已有结构化数据
            if "application/ld+json" not in content:
                # 生成结构化数据
                structured_data = await self._generate_structured_data(content)

                # 插入到HTML
                updated_content = self._insert_structured_data(content, structured_data)

                # 保存
                html_file.write_text(updated_content, encoding="utf-8")

                results[html_file.name] = "added"

        return results

    async def _generate_structured_data(self, content: str) -> str:
        """
        生成Schema.org结构化数据
        """
        # 从内容提取信息
        # 实际实现需要解析HTML

        # 生成ProfessionalService schema
        schema = {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "name": "Handwerker Ratgeber",
            "description": "Informationsplattform für Handwerkerdienste"
        }

        return json.dumps(schema)
```

### 2.6 Analytics Agent (数据分析专家)

**职责**: 自动A/B测试、性能监控、自动报告

```python
# agents/analytics_agent.py
from typing import Dict, List
from datetime import datetime, timedelta
import json

class AnalyticsAgent:
    """
    数据分析Agent - 自动监控和优化
    """

    def __init__(self):
        self.metrics_db = {}
        self.ab_test_results = []

    async def execute(self, tasks: List[str]) -> Dict:
        """
        执行数据分析任务
        """
        results = {}

        for task in tasks:
            if task == "run_ab_tests":
                results["ab_tests"] = await self._run_ab_tests()
            elif task == "generate_reports":
                results["reports"] = await self._generate_weekly_report()
            elif task == "update_prompts":
                results["prompts"] = await self._auto_optimize_prompts()

        return results

    async def _run_ab_tests(self) -> Dict:
        """
        自动运行A/B测试
        """
        # 创建测试变体
        variants = await self._create_test_variants()

        # 部署变体
        for variant in variants:
            await self._deploy_variant(variant)

        # 收集数据（需要实际API集成）
        results = await self._collect_test_data(variants)

        # 分析结果
        winner = await self._analyze_results(results)

        return {
            "winner": winner,
            "improvement": results[winner]["improvement"]
        }

    async def _create_test_variants(self) -> List[Dict]:
        """
        创建测试变体
        """
        variants = []

        # Prompt变体测试
        prompt_variants = [
            {"id": "current", "name": "当前Prompt"},
            {"id": "more_local", "name": "更多本地化"},
            {"id": "more_benefits", "name": "更多利益点"},
            {"id": "questions_first", "name": "问题优先"}
        ]

        for variant in prompt_variants:
            variants.append({
                "type": "prompt",
                "variant": variant,
                "traffic_split": 0.25  # 25%流量
            })

        return variants

    async def _generate_weekly_report(self) -> Dict:
        """
        自动生成周报告
        """
        report = {
            "period": {
                "start": (datetime.now() - timedelta(days=7)).isoformat(),
                "end": datetime.now().isoformat()
            },
            "metrics": {},
            "insights": [],
            "recommendations": []
        }

        # 收集指标
        report["metrics"] = await self._collect_metrics()

        # AI生成洞察
        insights = await self._ai_generate_insights(report["metrics"])
        report["insights"] = insights

        # AI生成建议
        recommendations = await self._ai_generate_recommendations(report)
        report["recommendations"] = recommendations

        # 保存报告
        report_path = Path(f"reports/weekly_{datetime.now().strftime('%Y%m%d')}.json")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2))

        return report

    async def _ai_generate_insights(self, metrics: Dict) -> List[str]:
        """
        使用AI生成数据洞察
        """
        prompt = f"""
        Analysiere folgende SEO-Metriken und generiere 3-5 wichtige Erkenntnisse:

        {json.dumps(metrics, indent=2)}

        Konzentriere dich auf:
        1. Verkehrstrends
        2. Ranking-Verbesserungen
        3. Content-Performance
        4. Auffällige Veränderungen

        Gib 3-5 prägnante Erkenntnisse zurück.
        """

        result = await self._call_ai(prompt)
        return result.split("\n")

    async def _ai_generate_recommendations(self, report: Dict) -> List[str]:
        """
        使用AI生成优化建议
        """
        prompt = f"""
        Basierend auf folgendem Report, generiere 3-5 konkrete Handlungsempfehlungen:

        {json.dumps(report, indent=2)}

        Empfehlungen sollten:
        - Konkret und umsetzbar sein
        - Prioritäten haben
        - SEO-Fokus haben

        Gib 3-5 Empfehlungen zurück.
        """

        result = await self._call_ai(prompt)
        return result.split("\n")

    async def _auto_optimize_prompts(self) -> Dict:
        """
        自动优化Prompt（基于A/B测试结果）
        """
        # 获取最佳变体
        best_variant = await self._get_best_ab_test_variant()

        if best_variant["improvement"] > 0.1:  # 10%以上改进
            # 更新默认Prompt
            await self._update_default_prompt(best_variant)

            return {
                "updated": True,
                "variant": best_variant["id"],
                "improvement": best_variant["improvement"]
            }

        return {
            "updated": False,
            "reason": "No significant improvement"
        }
```

---

## 三、自动化工作流

### 3.1 完整自动化流程

```python
# automation/workflow.py
from agents.master_agent import MasterAgent

class FullyAutomatedWorkflow:
    """
    全自动化PSEO工作流
    """

    def __init__(self):
        self.master = MasterAgent()
        self.config = self._load_workflow_config()

    async def run_full_automation(self):
        """
        执行完整自动化流程
        """
        print("🚀 Starting Full PSEO Automation...")

        # 执行工作流
        results = await self.master.execute_workflow(self.config)

        # 生成报告
        report = await self._generate_automation_report(results)

        # 通知结果
        await self._notify_completion(report)

        return report

    def _load_workflow_config(self) -> Dict:
        """
        加载工作流配置
        """
        return {
            "name": "pseo_full_automation",
            "stages": [
                {
                    "stage": "Data Preparation",
                    "agent": "data",
                    "tasks": ["fetch_cities", "validate_services", "enrich_metadata"]
                },
                {
                    "stage": "Legal Pages",
                    "agent": "legal",
                    "tasks": ["generate_impressum", "generate_datenschutz", "check_gdpr"]
                },
                {
                    "stage": "Content Generation",
                    "agent": "content",
                    "parallel": True,
                    "tasks": ["generate_articles", "create_variants"]
                },
                {
                    "stage": "Quality Assurance",
                    "agent": "quality",
                    "tasks": ["check_seo_score", "detect_duplicates", "validate_localization"]
                },
                {
                    "stage": "SEO Optimization",
                    "agent": "seo",
                    "tasks": ["generate_sitemap", "optimize_metadata", "create_structured_data"]
                },
                {
                    "stage": "Analytics",
                    "agent": "analytics",
                    "tasks": ["generate_reports", "run_ab_tests"]
                }
            ]
        }

if __name__ == "__main__":
    workflow = FullyAutomatedWorkflow()
    results = asyncio.run(workflow.run_full_automation())
```

---

## 四、部署与运行

### 4.1 GitHub Actions完全自动化

```yaml
# .github/workflows/full_automation.yml
name: Full PSEO Automation

on:
  schedule:
    - cron: '0 0 * * 0'  # 每周日
  workflow_dispatch:
  push:
    branches: [main]

jobs:
  automate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run Full Automation
        env:
          AI_PROVIDER: ${{ secrets.AI_PROVIDER }}
          AI_API_KEY: ${{ secrets.AI_API_KEY }}
          AI_MODEL: ${{ secrets.AI_MODEL }}
          AI_BASE_URL: ${{ secrets.AI_BASE_URL }}
        run: |
          python automation/workflow.py

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}

      - name: Notify Completion
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'PSEO Automation completed!'
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### 4.2 监控Dashboard

```python
# automation/dashboard.py
from fastapi import FastAPI
from typing import Dict

app = FastAPI()

@app.get("/api/status")
async def get_automation_status() -> Dict:
    """
    获取自动化状态
    """
    return {
        "last_run": "2026-03-10T00:00:00Z",
        "status": "completed",
        "pages_generated": 16000,
        "quality_score": 85.3,
        "errors": []
    }

@app.get("/api/metrics")
async def get_metrics() -> Dict:
    """
    获取SEO指标
    """
    return {
        "indexed_pages": 15234,
        "avg_position": 28.5,
        "total_clicks": 4521,
        "total_impressions": 125430
    }
```

---

## 五、关键优势

### 5.1 全自动化的优势

| 传统方式 | Multi-Agent自动化 |
|---------|-------------------|
| 需要人工编辑法律页面 | Legal Agent自动生成 |
| 人工检查内容质量 | Quality Agent自动评估 |
| 手动调整Prompt | Analytics Agent自动优化 |
| 定期人工审查 | 全自动A/B测试 |
| 手动生成报告 | 自动生成洞察和建议 |

### 5.2 实现零人工的目标

```
传统PSEO流程:
数据获取 → 人工编辑 → AI生成 → 人工审核 → 部署

Multi-Agent自动化:
数据获取 → AI生成 → AI审核 → AI优化 → 部署
    ↑         ↑        ↑        ↑
Data Agent  Content  Quality  SEO Agent
```

### 5.3 自我进化能力

```
第1周: 基础Prompt生成内容
   ↓
Analytics Agent检测到低CTR
   ↓
自动创建3个Prompt变体
   ↓
A/B测试找出最佳变体
   ↓
第2周: 使用优化后的Prompt
   ↓
持续迭代优化...
```

---

## 六、成本与时间预估

### 6.1 一次性投入

| 项目 | 时间 | 成本 |
|------|------|------|
| Agent框架开发 | 2-3天 | 开发时间 |
| Prompt模板开发 | 1天 | 开发时间 |
| 测试与调优 | 2-3天 | ~$50-100 |
| **总计** | **1周** | **~$50-100** |

### 6.2 每月运营成本

| 项目 | 成本 |
|------|------|
| AI生成(16K页) | $80-120 (或 ¥200-500) |
| Vercel托管 | $0 |
| GitHub Actions | $0 |
| 监控与优化 | ~$20 |
| **总计** | **$100-150/月** |

### 6.3 自动化节省

| 任务 | 手动时间 | 自动化时间 |
|------|---------|-----------|
| 内容生成审核 | 40小时 | 0 |
| SEO优化 | 10小时 | 0 |
| 报告生成 | 2小时 | 0 |
| Prompt优化 | 5小时 | 0 |
| **总计** | **57小时/月** | **0** |

---

## 七、下一步实施

1. **创建Agent框架** (Day 1-2)
2. **实现Content Agent** (Day 3)
3. **实现Quality Agent** (Day 4)
4. **实现Legal Agent** (Day 5)
5. **集成测试** (Day 6)
6. **部署上线** (Day 7)

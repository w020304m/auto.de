# PSEO Germany Handwerker - 项目概述

> **文档版本**: v2.0 Professional Edition
> **最后更新**: 2025-01-10
> **状态**: 部分内容已过时，请参考 [README.md](./README.md) 获取最新参数

---

## ⚠️ 重要提示

本文档包含一些**过时的规划信息**。项目已根据专业反馈优化为更实际的策略。

**最新的权威配置请查看**: [README.md](./README.md)

### 主要变更对比

| 项目 | 本文档（过时） | 正确配置（README.md） |
|------|---------------|---------------------|
| Phase 1 规模 | 16,000页 | 360页 |
| 服务类型 | 8个 | 4个（Phase 1） |
| Modifier | 3个 | 6个（完整策略） |
| Phase 1 方法 | AI生成 | 零AI（模板+数据） |

---

## 项目目标

构建一个面向德国工匠服务（Handwerker）的全自动化SEO网站，通过程序化SEO（PSEO）结合地理位置（GEO）策略和Multi-Agent协同，大规模生成城市×服务的着陆页面。

### 核心目标（更新后）

- **页面规模**：Phase 1 = 30城市 × 4服务 × 3 Modifier = **360页**
- **自动化程度**：100%全自动化（Multi-Agent协同）
- **人工干预**：接近零（仅初始配置和最终验证）
- **变现方式**：Google AdSense广告（德国CPM: $18-$25）
- **流量预期**：100K月访问 ≈ $1,000-$3,000月收入（Phase 3目标）

### Multi-Agent自动化策略

```
传统PSEO: 人工编辑 → AI生成 → 人工审核 → 部署
        ↓
本项目:   Data → Content → Quality → SEO → 自动部署
          ↓      ↓       ↓       ↓
      Agent  Agent   Agent   Agent
```

**六大Agent协同**:
1. **Master Agent**: 任务编排与状态管理
2. **Data Agent**: 自动数据获取与验证（OpenPLZ）
3. **Content Agent**: AI内容生成（Phase 2+可选）
4. **Quality Agent**: 自动质量评估与去重
5. **Legal Agent**: 自动生成法律页面（免费方案）
6. **SEO Agent**: 自动SEO优化与Sitemap

---

## 6个Modifier策略（完整覆盖）

```
旧策略: 3个Modifier → 收入$100-300/月
新策略: 6个Modifier → 收入$500-3000/月
```

| Modifier | URL示例 | 搜索意图 | CPC权重 |
|----------|---------|----------|---------|
| 主词 | klempner-berlin | 导航型 | 基准 |
| kosten | klempner-berlin-kosten | 信息型 | 1.5x |
| preis | klempner-berlin-preis | 信息型 | 1.5x |
| **notdienst** | klempner-berlin-notdienst | **交易型** | **3-5x** ⭐ |
| empfehlung | klempner-berlin-empfehlung | 调研型 | 1.2x |
| in-der-naehe | klempner-berlin-in-der-naehe | 交易型 | 2x |

---

## 网站结构示例

```
# Phase 1 (360页)
https://handwerker-ratgeber.de/klempner-berlin
https://handwerker-ratgeber.de/klempner-berlin-kosten
https://handwerker-ratgeber.de/klempner-berlin-notdienst

# Phase 2+ (扩展Modifier)
https://handwerker-ratgeber.de/klempner-berlin-empfehlung
https://handwerker-ratgeber.de/klempner-berlin-preis
https://handwerker-ratgeber.de/klempner-berlin-in-der-naehe
```

### 页面标题格式

```
{{modifier_title}}{{service}} in {{city}} 2026 – {{focus}}
```

示例：
- 主词: `Klempner in Berlin 2026 – Preise & Notdienst`
- kosten: `Klempner Berlin Kosten | Was Sie erwarten müssen`
- notdienst: `Klempner Notdienst Berlin | 24/7 Verfügbar`

---

## 核心逻辑

**城市 × 服务 × Modifier = 页面**

- 城市数据来源：OpenPLZ API（德国全部城市）
- 服务类型：Phase 1 = 4种核心服务
- Modifier：Phase 1 = 3个，Phase 2+ = 6个
- 自动化：全流程数据获取→内容生成→页面构建→部署

## 服务类型与价格区间（Phase 1）

| 服务 | 最低价(€/h) | 最高价(€/h) | 说明 |
|------|------------|------------|------|
| Klempner (管道工) | 80 | 160 | 高CPC |
| Elektriker (电工) | 70 | 150 | 高CPC |
| Schlüsseldienst (锁匠) | 60 | 120 | 紧急高CPC |
| Rohrreinigung (管道清理) | 70 | 130 | 长尾词 |

*价格数据来源：Destatis德国联邦统计局*

### Phase 2 扩展服务

| 服务 | 最低价(€/h) | 最高价(€/h) |
|------|------------|------------|
| Dachdecker (屋顶工) | 90 | 170 |
| Maler (油漆工) | 60 | 120 |
| Fliesenleger (瓷砖工) | 70 | 130 |
| Gärtner (园丁) | 50 | 100 |

---

## 技术选型原则

- **简单稳定**：避免过度工程化
- **静态优先**：生成静态HTML，CDN分发
- **自动化**：CI/CD定时更新
- **零成本起步**：Cloudflare Pages免费托管

---

## 三阶段扩展路径（现实版）

### Phase 1（MVP）- Month 1-2
- 目标: 30城市 × 4服务 × 3 Modifier = **360页**
- 方法: **零AI**（模板 + OpenPLZ数据）
- 重点: 验证SEO效果，建立Google信任
- 成本: $0-10（仅域名）
- 里程碑: 获得首批Google索引

### Phase 2（扩展）- Month 3-6
- 目标: 100城市 × 8服务 × 4 Modifier = **3,200页**
- 重点: 扩展高CPC关键词，AI内容增强
- 成本: $10-30/月
- 里程碑: 获得10K+月流量

### Phase 3（规模化）- Month 7+
- 目标: 500城市 × 8服务 × 6 Modifier = **24,000页**
- 重点: 完整Modifier覆盖，多语言扩展
- 里程碑: 实现€1,000+月收入

---

## 预期时间表（全自动化版本）

| 阶段 | 内容 | 时间 | 人工参与 |
|------|------|------|----------|
| Week 1 | 基础框架开发、零AI模板 | 2-3天 | 初始配置 |
| Week 2 | 生成360页、部署 | 自动化 | 监控 |
| Month 2+ | 扩展到3200页、可选AI增强 | 自动化 | 零 |

**完全自动化后**:
- 每周日00:00: 自动触发
- 30分钟内: 完成所有更新
- 自动生成报告: Slack/Email通知
- 自动部署: Cloudflare Pages更新

---

## 成功关键因素

1. **关键词规模**：覆盖大量长尾关键词组合（6个Modifier）
2. **真实数据**：OpenPLZ官方数据（避免thin content惩罚）
3. **结构化数据**：FAQ Schema + LocalBusiness Schema
4. **分阶段扩展**：避免触发Google爬虫限制
5. **持续更新**：定期更新内容保持活跃度

---

## 相关文档

| 文档 | 用途 |
|------|------|
| [README.md](./README.md) | ⭐ 项目索引和核心参数（权威） |
| [blueprint.md](./blueprint.md) | ⭐⭐ 完整执行指南（实施权威） |
| [CLAUDE.md](./CLAUDE.md) | 开发者规范 |
| [implementation.md](./implementation.md) | 技术架构说明 |
| [strategy.md](./strategy.md) | 策略和风险分析 |
| [tasks.md](./tasks.md) | 详细任务清单 |

---

**文档所有权**: 本项目遵循PSEO最佳实践，核心参数以 [README.md](./README.md) 为准，实施以 [blueprint.md](./blueprint.md) 为准。

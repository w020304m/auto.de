# Phase 1 部署指南

## 已完成的任务 ✅

| 任务 | 状态 |
|------|------|
| 372个服务页面生成 | ✅ 完成 |
| Clean URL结构 (/klempner-berlin/) | ✅ 完成 |
| Canonical URLs | ✅ 完成 |
| LocalBusiness Schema | ✅ 完成 |
| FAQ Schema | ✅ 完成 |
| "Wann brauchen Sie"模块 (200字) | ✅ 完成 |
| "Servicegebiete"模块 (200字) | ✅ 完成 |
| 城市内链 (7个城市/页面) | ✅ 完成 |
| 首页SEO文本 (180+词) | ✅ 完成 |
| Sitemap.xml (375 URLs) | ✅ 完成 |
| Robots.txt | ✅ 完成 |
| 法律页面 (Impressum, Datenschutz) | ✅ 完成 |

## 下一步操作（需要手动完成）

### 1. 本地测试（推荐）

```bash
# 启动本地服务器
cd output
python -m http.server 8080

# 在浏览器打开
# http://localhost:8080
```

**测试清单：**
- [ ] 首页显示正常，服务卡片可点击
- [ ] 随机打开5个服务页面，验证内容完整
- [ ] 点击城市内链，确认无404错误
- [ ] 移动端显示正常（Chrome DevTools切换设备）

---

### 2. GitHub 仓库初始化

```bash
# 在项目根目录执行
cd D:\code\pseo-germany-handwerker

# 初始化Git仓库
git init

# 添加文件
git add output/ .gitignore

# 提交
git commit -m "Phase 1: Deploy 375 pages"
```

然后在 GitHub 创建新仓库：
1. 访问 https://github.com/new
2. 仓库名: `handwerker-ratgeber`
3. 设为 Public（SEO需要）
4. 不要初始化README
5. 点击 "Create repository"

```bash
# 添加远程并推送
git remote add origin https://github.com/YOUR_USERNAME/handwerker-ratgeber.git
git branch -M main
git push -u origin main
```

---

### 3. Cloudflare Pages 部署

1. 访问 https://dash.cloudflare.com/
2. 左侧菜单 → Pages → Create a project
3. Connect to Git → 选择你的仓库
4. **构建设置：**
   - Build command: (留空)
   - Build output directory: `output`
   - Root directory: (留空)
5. 点击 "Save and Deploy"

部署完成后你会获得临时URL：`https://handwerker-ratgeber.pages.dev`

---

### 4. 更新 Sitemap 域名

如果使用 Cloudflare Pages 临时URL，需要更新sitemap.xml：

```bash
# 编辑 output/sitemap.xml
# 将 handwerker-ratgeber.de 替换为 handwerker-ratgeber.pages.dev
```

然后重新部署：
```bash
git add output/sitemap.xml
git commit -m "Update sitemap domain"
git push
```

---

### 5. Google Search Console 设置

1. 访问 https://search.google.com/search-console
2. 添加属性 → URL前缀
3. 输入你的URL (如 `https://handwerker-ratgeber.pages.dev/`)
4. 验证域名所有权：
   - 上传HTML文件到 `output/` 目录
   - 重新部署到 Cloudflare Pages

5. **提交Sitemap：**
   - 左侧菜单 → Sitemaps
   - 输入: `https://你的域名/sitemap.xml`
   - 点击 "提交"

---

### 6. ⚠️ 部署前必须完成：更新 Impressum 页面

只有 **Impressum（版权声明）** 需要修改个人占位符信息：
- `output/impressum/index.html`

**必须替换的信息：**
```
[Ihr Name] → 你的真实姓名
[Ihre Straße] → 你的真实地址
[PLZ] [Ort] → 你的邮编和城市
[Verantwortlicher Name] → 负责人姓名
```

**Datenschutz（隐私政策）文件不需要修改** - 它是通用模板，适用于静态网站。

---

### 7. 部署后检查清单

| 检查项 | 方法 |
|--------|------|
| Robots.txt可访问 | 访问 `域名/robots.txt` |
| Sitemap.xml可访问 | 访问 `域名/sitemap.xml` |
| 首页可访问 | 访问 `域名/` |
| 服务页可访问 | 访问 `域名/klempner-berlin/` |
| 法律页可访问 | 访问 `域名/impressum/` |

---

### 8. Phase 1 观察期（2-4周）

**不做广告，只观察：**

每周检查：
- [ ] Google Search Console → 索引状态
- [ ] Google Search Console → 覆盖范围报告
- [ ] Google Search Console → 效果报告（展示次数、排名）

**观察目标：**
- 有多少页面被索引（目标: 300+/372）
- 哪些关键词开始获得展示
- 平均排名位置

---

## 文件结构确认

部署前确认以下文件存在：

```
output/
├── index.html                    # 首页 ✅
├── sitemap.xml                   # 站点地图 ✅
├── robots.txt                    # 爬虫规则 ✅
├── impressum/
│   └── index.html               # 法律页 ⚠️ 需要更新
├── datenschutz/
│   └── index.html               # 隐私页 ⚠️ 需要更新
├── klempner-berlin/
│   └── index.html
├── klempner-berlin-kosten/
│   └── index.html
├── ... (372 个服务页面目录)
```

---

## 常见问题

**Q: Cloudflare Pages 部署后URL是什么？**
A: `your-project-name.pages.dev`，可以在设置中绑定自定义域名。

**Q: 需要购买域名吗？**
A: Phase 1 不需要，使用 pages.dev 临时URL即可。

**Q: 如何验证Google索引？**
A: 在Google搜索 `site:handwerker-ratgeber.pages.dev`

**Q: 多久能看到索引结果？**
A: 通常2-4周，新网站可能需要更长时间。

---

## 联系与支持

如有问题，请检查：
1. Cloudflare Pages 部署日志
2. Google Search Console 覆盖范围报告
3. 浏览器开发者工具Console错误

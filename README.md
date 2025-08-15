# 雅典娜 (Project Athena)

![Athena Icon](https://raw.githubusercontent.com/user-attachments/assets/cb3c6a49-3543-4556-946d-9788f6153350) 
<!-- 这是一个临时的Logo URL，我建议您将赛博朋克版的图标保存下来，放到项目的一个`assets`文件夹中，然后在这里使用相对路径 -->

**一个为您打造的个人AI信息中枢，自动抓取、总结并推送您关心的核心信息，将您从信息过载中解放出来。**

---

## 🚀 项目使命

在信息爆炸的时代，我们每天都被海量的、低信噪比的信息所淹没。在多个App之间无休止地刷新，不仅消耗了我们宝贵的时间，更带来了无尽的焦虑。

“雅典娜”项目因此而生。它的核心使命是，成为您的专属智慧女神，用AI的力量，为您在信息的迷雾中点亮火炬，将浩瀚的原始数据，提炼成每日一份的、精炼、优雅、且高度个人化的智慧简报。

## ✨ 特性 (V1.0)

*   **多源信息聚合**: 自动从您指定的RSS源列表抓取最新文章。
*   **智能正文提取**: 借助 `trafilatura`，精准地从混乱的网页中提取出核心内容，自动过滤广告、导航栏和评论。
*   **AI驱动的摘要**: 由大型语言模型（兼容OpenAI API，支持自定义服务商）驱动，为每篇文章生成高质量的核心摘要。
*   **自动化数据管道**: 实现了从数据采集、处理、AI增强到数据库持久化的全自动化后台流程。
*   **精美邮件交付**: 每日定时将摘要简报以设计精美的、完全响应式的HTML邮件推送到您的邮箱。
*   **高度健壮性**: 内置了针对网络波动和API错误的自动重试机制，并拥有专业的日志系统。
*   **完全可定制**:
    *   通过 `.env` 文件安全管理所有敏感配置。
    *   通过 `config.py` 轻松增删RSS源、调整参数。
    *   通过 `prompts/` 目录，您可以像修改配置文件一样，轻松迭代和优化AI的指令。

## 🛠️ 技术栈

*   **语言**: Python 3.12
*   **核心框架**: SQLAlchemy (ORM)
*   **核心库**: `openai`, `feedparser`, `trafilatura`, `yagmail`, `tenacity`, `python-dotenv`
*   **数据库**: SQLite

## 🚀 如何开始

### 1. 克隆仓库
```bash
git clone https://github.com/YourUsername/athena-ai-briefings.git
cd athena-ai-briefings
```

### 2. 创建并激活Conda环境
```bash
conda create -n athena python=3.12
conda activate athena
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置您的环境
*   将 `.env.example` 文件复制一份，并重命名为 `.env`。
*   打开 `.env` 文件，填入您自己的API密钥、邮箱凭据和服务器信息。**这是项目运行的关键！**

### 5. 初始化数据库
这是您第一次运行项目时**必须**执行的步骤。
```bash
python database.py
```

### 6. 运行！
现在，您可以通过以下两个核心脚本来驱动“雅典娜”：

*   **处理数据 (抓取、总结、入库)**:
    ```bash
    python data_pipeline.py
    ```
*   **发送今日简报**:
    ```bash
    python delivery_pipeline.py
    ```

建议将这两个脚本配置为您操作系统的定时任务，以实现完全自动化。

## 🏛️ 项目结构

```
/
|-- /prompts/              # AI Prompt 模板
|-- .env.example           # 环境变量模板
|-- config.py              # 常规配置
|-- data_pipeline.py       # 数据处理主流程
|-- delivery_pipeline.py   # 邮件交付主流程
|-- ai_core.py             # AI 核心模块
|-- data_collector.py      # 数据采集模块
|-- email_sender.py        # 邮件发送工具
|-- templating.py          # HTML 模板生成器
|-- database.py            # 数据库初始化脚本
|-- models.py              # 数据库模型
|-- ...
```

## 🤝 如何贡献

我们欢迎任何形式的贡献！如果您发现了Bug或有任何绝佳的功能建议，请随时提交 [Issue](https://github.com/YourUsername/athena-ai-briefings/issues)。如果您希望贡献代码，请Fork本仓库并提交Pull Request。

## 📜 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。
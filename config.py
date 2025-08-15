# config.py

# ==============================================================================
# 项目配置中心 (Project Configuration Center)
# ==============================================================================

# --- 数据源配置 (Data Source Configuration) ---
# 在这里管理您所有想关注的RSS源
RSS_FEEDS = [
    "http://www.ruanyifeng.com/blog/atom.xml",
    # 您可以在这里继续添加更多RSS链接...
    # "https://36kr.com/feed",
    # "https://www.infoq.cn/feed.xml",
]

# --- 数据处理配置 (Data Processing Configuration) ---
# 每次运行时，从每个RSS源最多处理的文章数量
# 这是一个重要的成本和性能控制器
MAX_ARTICLES_PER_FEED = 5

# 内容健全性检查的最小长度阈值（字符数）
MIN_CONTENT_LENGTH = 200


# --- 邮件配置 (Email Configuration) ---
# 邮件主题模板，{date} 将被替换为当前日期
EMAIL_SUBJECT_TEMPLATE = "您的雅典娜每日简报 - {date}"
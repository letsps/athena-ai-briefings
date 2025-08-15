# templating.py (Version 4.0 - Grouped & Branded Final Edition)

from datetime import datetime, timezone
from models import BriefingItem
from collections import defaultdict

# --- 雅典娜品牌图标 (Base64 编码的SVG) ---
# 这是一个嵌入式的猫头鹰图标，无需外部网络请求，兼容性极佳。
# 您未来可以替换成任何您喜欢的图标的Base64编码。
ATHENA_ICON_BASE64 = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM1NTUiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLW93bCI+PHBhdGggZD0iTTIyIDggYy0uODYtMi4zMy00LjE2LTMtNy0zLTMuNjMgMC02Ljc1IDEuMjQtNyA1Ljg3QTYuODcgNi44NyAwIDAgMCA4LjUgMjEuNUg5YTYgNiAwIDAgMCA2LTZWMjEiLz48cGF0aCBkPSJNNyAxM2gyIi8+PHBhdGggZD0iTTIwIDEzYTQgNCAwIDAgMC04IDBaIi8+PC9zdmc+"


def create_html_content(briefing_items: list[BriefingItem]) -> str:
    """
    生成一份带品牌标识、按来源分组、设计优雅的HTML邮件。
    """
    today_str = datetime.now(timezone.utc).strftime('%Y年%m月%d日')

    # ======================================================================
    # --- 核心升级：按来源对文章进行分组 ---
    # ======================================================================
    grouped_items = defaultdict(list)
    for item in briefing_items:
        grouped_items[item.source_name].append(item)

    # --- 动态生成每个分组的HTML片段 ---
    groups_html = ""
    for source_name, items in grouped_items.items():
        items_html = ""
        for item in items:
            sanitized_summary = " ".join(str(item.summary_text).split())
            items_html += f'''
            <!-- 单个摘要 -->
            <div style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #f0f0f0;">
                <p style="margin: 0; font-family: 'Georgia', 'Times New Roman', serif; font-size: 16px; line-height: 1.7; color: #34495e;">
                    {sanitized_summary}
                </p>
                <div style="padding-top: 10px; text-align: right;">
                    <a href="{item.source_url}" target="_blank" style="font-family: Arial, sans-serif; font-size: 13px; color: #3498db; text-decoration: none;">
                        阅读原文 &rarr;
                    </a>
                </div>
            </div>
            '''
        
        # 移除最后一个条目的底部分隔线，更美观
        if items_html.endswith('</div>'):
            last_div_pos = items_html.rfind('<div style="margin-bottom: 15px;')
            items_html = items_html[:last_div_pos] + items_html[last_div_pos:].replace('border-bottom: 1px solid #f0f0f0;', '')

        groups_html += f'''
        <!-- 单个来源分组 -->
        <tr>
            <td style="padding: 20px 0;">
                <h2 style="margin: 0 0 15px 0; font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px;">
                    {source_name}
                </h2>
                {items_html}
            </td>
        </tr>
        '''

    # --- 完整的HTML文档结构 ---
    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>雅典娜每日简报</title>
        <style>
            @media screen and (max-width: 600px) {{
                .container {{ padding: 0 !important; width: 100% !important; }}
                .header, .footer, .content-cell {{ padding-left: 15px !important; padding-right: 15px !important; }}
                h1 {{ font-size: 24px !important; }}
                h2 {{ font-size: 16px !important; }}
            }}
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f6f8fa; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td style="padding: 20px 0;">
                    <table class="container" align="center" border="0" cellpadding="0" cellspacing="0" width="680" style="max-width: 680px; margin: 0 auto; background-color: #ffffff; border-collapse: collapse; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                        <!-- 页眉 -->
                        <tr>
                            <td class="header" style="padding: 30px; text-align: center;">
                                <img src="{ATHENA_ICON_BASE64}" alt="Athena Icon" width="36" height="36" style="margin-bottom: 10px;">
                                <h1 style="margin: 0; font-size: 28px; font-weight: 600; color: #121212;">每日简报</h1>
                                <p style="margin: 4px 0 0; font-size: 14px; color: #888888;">{today_str}</p>
                            </td>
                        </tr>
                        <!-- 主要内容 -->
                        <tr>
                            <td class="content-cell" style="padding: 10px 30px;">
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                                    {groups_html}
                                </table>
                            </td>
                        </tr>
                        <!-- 页脚 -->
                        <tr>
                            <td class="footer" style="padding: 30px; text-align: center; font-size: 12px; color: #999999; border-top: 1px solid #eaeaea;">
                                <p style="margin: 0;">由 '雅典娜' 为您精心呈现</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    return "".join(full_html.splitlines())
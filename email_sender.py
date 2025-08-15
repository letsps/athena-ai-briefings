# email_sender.py (Version 3.2 - Bypassing Parser Final Edition)

import os
import yagmail
from dotenv import load_dotenv
from logger_config import logger

load_dotenv(override=True)

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT_STR = os.getenv("SMTP_PORT")
SMTP_SSL_STR = os.getenv("SMTP_SSL")

required_configs = {
    "SENDER_EMAIL": SENDER_EMAIL,
    "SENDER_PASSWORD": SENDER_PASSWORD,
    "SMTP_HOST": SMTP_HOST,
    "SMTP_PORT": SMTP_PORT_STR
}
for name, value in required_configs.items():
    if not value:
        raise ValueError(f"错误: 配置项 '{name}' 未在 .env 文件中找到。")

yag = None
try:
    smtp_port = int(SMTP_PORT_STR)
    smtp_ssl = SMTP_SSL_STR.lower() == 'true' if SMTP_SSL_STR else False
    yag = yagmail.SMTP(
        user=SENDER_EMAIL,
        password=SENDER_PASSWORD,
        host=SMTP_HOST,
        port=smtp_port,
        smtp_ssl=smtp_ssl
    )
    logger.info(f"邮件客户端初始化成功，连接到 {SMTP_HOST}:{smtp_port}，发件人: {SENDER_EMAIL}")
except ValueError:
    logger.error(f"错误: .env 文件中的 SMTP_PORT ('{SMTP_PORT_STR}') 不是一个有效的数字。")
except Exception as e:
    logger.error(f"邮件客户端初始化失败: {e}")

def send_briefing_email(receiver_email: str, subject: str, html_content: str):
    """
    发送一封包含简报内容的HTML邮件。(V3.2)
    现在接收一个单一的HTML字符串作为内容。
    """
    if not yag:
        logger.error("邮件客户端未成功初始化，无法发送邮件。")
        return False
    
    logger.info(f"正在向 {receiver_email} 发送邮件，主题: '{subject}'...")
    try:
        yag.send(
            to=receiver_email,
            subject=subject,
            contents=html_content # 直接发送字符串，绕过内部解析
        )
        logger.info("邮件发送成功。")
        return True
    except Exception as e:
        logger.error(f"发送邮件时发生错误: {e}")
        return False

if __name__ == '__main__':
    if not RECEIVER_EMAIL:
        logger.error("错误: 请在 .env 文件中配置 RECEIVER_EMAIL 以进行测试。")
    else:
        logger.info(f"--- 开始独立测试 email_sender (绕过解析器) ---")
        test_subject = "雅典娜项目 - 邮件模块(v3.2)测试"
        # 将HTML片段连接成一个单一的字符串
        test_html_body = "".join([
            "<h1>雅典娜项目通用邮件测试 (v3.2)</h1>",
            "<p>这个版本旨在绕过yagmail的CSS解析器问题。</p>",
            f"<p>已成功连接到服务器: <b>{SMTP_HOST}</b></p>"
        ])
        success = send_briefing_email(RECEIVER_EMAIL, test_subject, test_html_body)
        if success:
            logger.info("\n测试邮件已成功发送。")
        else:
            logger.error("\n测试邮件发送失败。请检查终端日志。")
        logger.info("\n--- 测试 email_sender 结束 ---")
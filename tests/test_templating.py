# tests/test_templating.py

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock # 我们将使用Mock来创建“假的”数据库对象

# 导入我们需要测试的目标函数
from templating import create_html_content

# ==============================================================================
# 我们的第一个单元测试函数 (Unit Test Function)
# 函数名也必须以 test_ 开头
# ==============================================================================
def test_create_html_content_with_data():
    """
    测试: 当有摘要数据时，create_html_content函数是否能生成包含关键信息的HTML。
    """
    # --- 1. 准备 (Arrange) ---
    # 我们不依赖真实数据库，而是手动创建“假的”BriefingItem对象。
    # Mock对象是一个强大的工具，它可以模拟任何Python对象的行为。
    
    mock_item_1 = Mock()
    mock_item_1.source_name = "科技前沿"
    mock_item_1.summary_text = "这是第一条摘要，关于人工智能。"
    mock_item_1.source_url = "http://example.com/ai"

    mock_item_2 = Mock()
    mock_item_2.source_name = "商业观察"
    mock_item_2.summary_text = "这是第二条摘要，关于市场动态。"
    mock_item_2.source_url = "http://example.com/business"

    test_data = [mock_item_1, mock_item_2]

    # --- 2. 行动 (Act) ---
    # 调用我们想要测试的函数
    html_output = create_html_content(test_data)

    # --- 3. 断言 (Assert) ---
    # 这是测试的核心。我们断言（声明并检查）输出结果必须满足某些条件。
    # 如果任何一个 assert 失败，Pytest就会报告测试失败。

    # 断言：返回的必须是字符串
    assert isinstance(html_output, str)
    
    # 断言：HTML中必须包含我们传入的摘要内容
    assert "这是第一条摘要，关于人工智能。" in html_output
    assert "这是第二条摘要，关于市场动态。" in html_output
    
    # 断言：HTML中必须包含信源名称
    assert "科技前沿" in html_output
    assert "商业观察" in html_output

    # 断言：HTML中必须包含原文链接
    assert "http://example.com/ai" in html_output
    assert "http://example.com/business" in html_output

def test_create_html_content_with_no_data():
    """
    测试: 当摘要数据列表为空时，函数是否能优雅地处理。
    """
    # 1. 准备：一个空列表
    test_data = []

    # 2. 行动
    html_output = create_html_content(test_data)

    # 3. 断言
    assert isinstance(html_output, str)
    # 我们可以断言它不应该包含某些通常会有的内容
    assert "阅读原文" not in html_output
    # 或者断言它应该包含“空状态”的提示（如果我们的模板里有的话）
    # 例如：assert "今日没有新的简报" in html_output
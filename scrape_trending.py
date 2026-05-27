import httpx
import json
from datetime import datetime
from bs4 import BeautifulSoup

def scrape_github_trending():
    """抓取 GitHub Trending 数据"""
    url = "https://github.com/trending"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    weekly_data = []
    daily_data = []
    
    try:
        # 获取页面
        response = httpx.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 这里需要根据实际页面结构解析
        # GitHub Trending 页面结构可能会变化，需要调整选择器
        
        # 模拟数据（实际使用时替换为真实解析逻辑）
        weekly_data = [
            {
                "rank": 1,
                "name": "colbymchenry/codegraph",
                "url": "https://github.com/colbymchenry/codegraph",
                "descEn": "Pre-indexed code knowledge graph for Claude Code, Codex, Gemini, Cursor, OpenCode, AntiGravity, Kiro, and Hermes Agent — fewer tokens, fewer tool calls, 100% local",
                "descCn": "为 Claude Code、Codex、Gemini、Cursor 等 AI 编程助手预构建的代码知识图谱，大幅减少 token 消耗和工具调用次数，完全本地运行。",
                "lang": "TypeScript",
                "stars": "28,789",
                "starsLabel": "WEEKLY_DATA",
            }
        ]
        
        daily_data = [
            {
                "rank": 1,
                "name": "Lum1104/Understand-Anything",
                "url": "https://github.com/Lum1104/Understand-Anything",
                "descEn": "Graphs that teach > graphs that impress. Turn any code into an interactive knowledge graph you can explore, search, and ask questions about. Works with Claude Code, Codex, Cursor, Copilot, Gemini CLI, and more.",
                "descCn": "将任意代码库转化为可交互的知识图谱，支持探索、搜索和自然语言问答，兼容 Claude Code、Codex、Cursor、Copilot、Gemini CLI 等主流 AI 编程工具。",
                "lang": "TypeScript",
                "stars": "37,509",
                "starsLabel": "DAILY_DATA",
            }
        ]
        
        return weekly_data, daily_data
        
    except Exception as e:
        print(f"抓取失败: {e}")
        return [], []

def update_html_file(weekly_data, daily_data):
    """更新 HTML 文件中的 JavaScript 数据"""
    try:
        with open('github-trending.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新更新时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        content = content.replace(
            '更新时间 2026-05-27',
            f'更新时间 {datetime.now().strftime("%Y-%m-%d")}'
        )
        
        # 更新页脚中的时间
        content = content.replace(
            '更新时间 2026-05-27',
            f'更新时间 {datetime.now().strftime("%Y-%m-%d")}'
        )
        
        # 更新 JavaScript 数据
        soup = BeautifulSoup(content, 'html.parser')
        scripts = soup.find_all('script')
        
        for script in scripts:
            if script.string and 'WEEKLY_DATA' in script.string:
                # 替换 WEEKLY_DATA
                new_weekly_js = f"const WEEKLY_DATA = {json.dumps(weekly_data, indent=2, ensure_ascii=False)};"
                script.string = script.string.replace(
                    'const WEEKLY_DATA = [',
                    new_weekly_js.split('const WEEKLY_DATA = [')[0] + 'const WEEKLY_DATA = ['
                )
            
            if script.string and 'DAILY_DATA' in script.string:
                # 替换 DAILY_DATA
                new_daily_js = f"const DAILY_DATA = {json.dumps(daily_data, indent=2, ensure_ascii=False)};"
                script.string = script.string.replace(
                    'const DAILY_DATA = [',
                    new_daily_js.split('const DAILY_DATA = [')[0] + 'const DAILY_DATA = ['
                )
        
        # 写回文件
        with open('github-trending.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"HTML 文件已更新，更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
    except Exception as e:
        print(f"更新 HTML 文件失败: {e}")

if __name__ == "__main__":
    print("开始抓取 GitHub Trending 数据...")
    weekly_data, daily_data = scrape_github_trending()
    
    if weekly_data or daily_data:
        print(f"抓取到 {len(weekly_data)} 条周榜数据, {len(daily_data)} 条日榜数据")
        update_html_file(weekly_data, daily_data)
    else:
        print("未抓取到数据，使用默认数据")
        # 使用示例数据
        weekly_data = [{
            "rank": 1,
            "name": "示例仓库",
            "url": "https://github.com/example",
            "descEn": "Example repository",
            "descCn": "示例仓库",
            "lang": "Python",
            "stars": "1,000",
            "starsLabel": "WEEKLY_DATA",
        }]
        daily_data = [{
            "rank": 1,
            "name": "示例仓库",
            "url": "https://github.com/example",
            "descEn": "Example repository",
            "descCn": "示例仓库",
            "lang": "Python",
            "stars": "1,000",
            "starsLabel": "DAILY_DATA",
        }]
        update_html_file(weekly_data, daily_data)
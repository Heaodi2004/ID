from flask import Flask, render_template, request, jsonify
import requests
import re
import webbrowser
import threading
import time
import sys
import os
from urllib.parse import urlparse, parse_qs, unquote

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

app = Flask(__name__, template_folder=resource_path('templates'))

def extract_url_from_text(text):
    url_pattern = r'https?://[^\s]+'
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None

def parse_from_short_url(url):
    match = re.search(r'v\.douyin\.com/([a-zA-Z0-9_-]+)', url)
    if match:
        short_code = match.group(1)
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }
            session = requests.Session()
            response = session.get(url, headers=headers, allow_redirects=True, timeout=20)
            
            if response.url != url:
                return parse_douyin_url(response.url)
            
            html_content = response.text
            video_match = re.search(r'video/(\d+)', html_content)
            user_match = re.search(r'sec_user_id=([^&]+)', html_content)
            
            result = {
                'short_code': short_code,
                'video_id': video_match.group(1) if video_match else None,
                'user_id': unquote(user_match.group(1)) if user_match else None,
                'full_url': url
            }
            
            if result['video_id'] or result['user_id']:
                return result
            
        except Exception as e:
            print(f"网络请求失败: {e}")
        
        return {
            'short_code': short_code,
            'video_id': None,
            'user_id': None,
            'full_url': url,
            'note': '需要重定向获取完整信息，请尝试在浏览器中打开链接查看'
        }
    return None

def parse_douyin_url(url):
    if not url:
        return None
    
    url = extract_url_from_text(url)
    if not url:
        return None
    
    video_id = None
    user_id = None
    sec_user_id = None
    
    full_url = url
    
    parsed = urlparse(url)
    
    if '/video/' in parsed.path:
        match = re.search(r'/video/(\d+)', parsed.path)
        if match:
            video_id = match.group(1)
    
    if '/note/' in parsed.path:
        match = re.search(r'/note/(\d+)', parsed.path)
        if match:
            video_id = match.group(1)
    
    query_params = parse_qs(parsed.query)
    if 'user_id' in query_params:
        user_id = query_params['user_id'][0]
    
    if 'sec_user_id' in query_params:
        sec_user_id = query_params['sec_user_id'][0]
        if not user_id:
            user_id = sec_user_id
    
    if not video_id and 'mid' in query_params:
        video_id = query_params['mid'][0]
    
    if not video_id and 'item_id' in query_params:
        video_id = query_params['item_id'][0]
    
    if not user_id and 'social_author_id' in query_params:
        user_id = query_params['social_author_id'][0]
    
    if not user_id and 'activity_info' in query_params:
        activity_info = query_params['activity_info'][0]
        try:
            activity_info_decoded = unquote(activity_info)
            author_match = re.search(r'"social_author_id":"([^"]+)"', activity_info_decoded)
            if author_match:
                user_id = author_match.group(1)
        except:
            pass
    
    match = re.search(r'/user/([a-zA-Z0-9_-]+)', parsed.path)
    if match and not user_id:
        user_id = match.group(1)
    
    match = re.search(r'/v/([a-zA-Z0-9_-]+)', parsed.path)
    if match and not video_id:
        video_id = match.group(1)
    
    if 'v.douyin.com' in url and not video_id:
        short_parse = parse_from_short_url(url)
        if short_parse:
            return short_parse
    
    return {
        'video_id': video_id,
        'user_id': user_id,
        'sec_user_id': sec_user_id,
        'full_url': full_url
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/parse', methods=['POST'])
def api_parse():
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        result = parse_douyin_url(url)
        
        if result:
            return jsonify({
                'success': True,
                'result': result
            })
        else:
            return jsonify({
                'success': False,
                'message': '解析失败，请检查链接是否有效'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        })

def open_browser():
    """延迟打开浏览器"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("=" * 50)
    print("       抖音链接解析器")
    print("=" * 50)
    print()
    print("正在启动服务...")
    print("服务地址: http://127.0.0.1:5000")
    print("按 Ctrl+C 停止服务")
    print()
    print("=" * 50)
    print()
    
    # 在新线程中打开浏览器
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(debug=False, host='0.0.0.0', port=5000)

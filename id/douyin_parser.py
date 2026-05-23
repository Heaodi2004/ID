import requests
import re
import json
from urllib.parse import urlparse, parse_qs, unquote

def extract_url_from_text(text):
    url_pattern = r'https?://[^\s]+'
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None

def get_redirect_url(short_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        }
        session = requests.Session()
        response = session.get(short_url, headers=headers, allow_redirects=True, timeout=15)
        return response.url
    except Exception as e:
        print(f"重定向获取失败: {e}")
        return None

def parse_from_short_url(url):
    match = re.search(r'v\.douyin\.com/([a-zA-Z0-9_-]+)', url)
    if match:
        short_code = match.group(1)
        print(f"正在尝试获取完整信息，短链接码: {short_code}...")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }
            session = requests.Session()
            response = session.get(url, headers=headers, allow_redirects=True, timeout=20)
            
            if response.url != url:
                print(f"重定向成功，获取到完整链接")
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

def main():
    print("抖音视频链接解析器")
    print("=" * 40)
    print("支持的链接格式:")
    print("- v.douyin.com/xxxxx")
    print("- www.douyin.com/video/xxxxxx")
    print("- www.douyin.com/note/xxxxxx")
    print("=" * 40)
    
    while True:
        input_text = input("\n请输入抖音视频链接 (输入 q 退出): ").strip()
        
        if input_text.lower() == 'q':
            print("程序退出")
            break
        
        if not input_text:
            print("请输入有效的链接")
            continue
        
        result = parse_douyin_url(input_text)
        
        if result:
            print("\n解析结果:")
            print(f"完整链接: {result['full_url']}")
            if 'short_code' in result:
                print(f"短链接码: {result['short_code']}")
                print(f"提示: {result.get('note', '')}")
            else:
                print(f"视频ID: {result['video_id'] if result['video_id'] else '未找到'}")
                print(f"用户ID: {result['user_id'] if result['user_id'] else '未找到'}")
                if result.get('sec_user_id'):
                    print(f"加密用户ID: {result['sec_user_id']}")
        else:
            print("解析失败，请检查链接是否有效")

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

taipei_tz = pytz.timezone('Asia/Taipei')
cal = Calendar()

def get_headers():
    return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def scrape_taipei_arena():
    """抓取台北小巨蛋活動"""
    print("開始偵測台北小巨蛋...")
    url = "https://www.arena.taipei/News.aspx?n=8A9D937AE7AF5691&sms=E4C6D82A2EAA2CEB"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        events = soup.find_all('div', class_='event-item') 
        
        for item in events:
            title = item.find('h3').text.strip()
            date_str = item.find('span', class_='date').text.strip()
            start_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            end_time = start_time + timedelta(hours=3) 
            
            e = Event()
            e.name = f"🚕 [肥單預警] 小巨蛋散場：{title}"
            e.begin = end_time.replace(tzinfo=taipei_tz)
            e.description = "小巨蛋演唱會散場！建議提早排班。"
            cal.events.add(e)
    except Exception as e:
        print(f"小巨蛋抓取失敗，原因：{e}")

def inject_test_event():
    """💡 強迫灌入一筆明天的測試肥單，用來檢查行事曆連線"""
    print("正在灌入測試資料...")
    tomorrow = datetime.now(taipei_tz) + timedelta(days=1)
    # 設定在明天晚上 9 點散場
    test_time = tomorrow.replace(hour=21, minute=0, second=0, microsecond=0)
    
    e = Event()
    e.name = "🚕 [測試成功] 大巨蛋周杰倫演唱會散場測試"
    e.begin = test_time
    e.description = "恭喜！看到這個代表你的 GitHub 自動化雷達與 Google 行事曆完全接通了！連線測試成功！"
    cal.events.add(e)

def create_calendar():
    # 1. 抓官網資料（目前可能是空的）
    scrape_taipei_arena()
    # 2. 強制塞入測試行程（保證有東西）
    inject_test_event()
    
    with open('taipei_surge_events.ics', 'w', encoding='utf-8') as f:
        f.writelines(cal.serialize_iter())
    print("🎉 行事曆雷達更新完成！")

if __name__ == "__main__":
    create_calendar()

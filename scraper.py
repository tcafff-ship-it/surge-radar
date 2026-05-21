import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

# 設定台北時區
taipei_tz = pytz.timezone('Asia/Taipei')
cal = Calendar()

def get_headers():
    # 💡 為什麼要偽裝 Header？因為如果直接裸奔過去，伺服器會發現你是機器人並把你踢掉
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

def scrape_taipei_arena():
    """抓取台北小巨蛋活動"""
    print("開始偵測台北小巨蛋...")
    # 小巨蛋官網活動列表網址 (此為示意結構，實際需依當下官網 HTML 為準)
    url = "https://www.arena.taipei/News.aspx?n=8A9D937AE7AF5691&sms=E4C6D82A2EAA2CEB"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 假設我們抓取表格中的活動 (實際 CSS Class 需以官網為準)
        events = soup.find_all('div', class_='event-item') 
        
        for item in events:
            title = item.find('h3').text.strip()
            date_str = item.find('span', class_='date').text.strip() # 假設格式: 2026-06-15 19:30
            
            # 💡 為什麼要手動加 3 小時？因為演唱會通常抓 3 小時散場最準
            start_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            end_time = start_time + timedelta(hours=3) 
            
            e = Event()
            e.name = f"🚕 [肥單預警] 小巨蛋散場：{title}"
            e.begin = end_time.replace(tzinfo=taipei_tz)
            e.description = "小巨蛋演唱會散場！建議提早至八德路或南京東路外圍排班，避開敦化北路主幹道。"
            cal.events.add(e)
    except Exception as e:
        print(f"小巨蛋抓取失敗，原因：{e}")

def create_calendar():
    # 執行所有抓取任務
    scrape_taipei_arena()
    # 這裡可以繼續擴充 scrape_nangang() 等函式...
    
    # 💡 為什麼要寫出這個檔案？因為你的手機只能讀取標準的 .ics 格式
    with open('taipei_surge_events.ics', 'w', encoding='utf-8') as f:
        f.writelines(cal.serialize_iter())
    print("🎉 行事曆雷達更新完成！")

if __name__ == "__main__":
    create_calendar()

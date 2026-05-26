import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_scraper():
    # מספר המעקב של HFD (שנה למספר האמיתי שלך)
    tracking_number = "88297724" 
    courier_slug = "hfd" # חברת HFD
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # פנייה ישירה לדף המעקב של HFD
        url = f"https://www.aftership.com/track/{courier_slug}/{tracking_number}"
        print(f"ניגש לכתובת: {url}")
        driver.get(url)
        
        # המתנה לטעינת הסטטוס (עד 20 שניות)
        wait = WebDriverWait(driver, 20)
        
        # מחפש את הסטטוס המרכזי
        status_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "status-tag")))
        status = status_element.text
        
        # שליפת היסטוריית המשלוח
        checkpoints = driver.find_elements(By.CLASS_NAME, "checkpoint-item")
        history = [cp.text.replace('\n', ' ') for cp in checkpoints]
        
        if not history:
            history = ["אין עדכונים זמינים כרגע"]

        output = {
            "tracking_number": tracking_number,
            "courier": "HFD",
            "status": status,
            "history": history,
            "last_update": time.strftime("%d/%m/%Y %H:%M")
        }

        # שמירה לקובץ
        with open('tracking_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
        print(f"!!! SUCCESS: Data for {tracking_number} saved !!!")

    except Exception as e:
        print(f"!!! ERROR: {e}")
        # יצירת קובץ שגיאה בסיסי כדי שהאתר לא יציג "טוען..." לנצח
        with open('tracking_data.json', 'w', encoding='utf-8') as f:
            json.dump({
                "tracking_number": tracking_number,
                "status": "בבדיקה / לא נמצא",
                "history": ["לא הצלחנו למשוך נתונים מ-AfterShip. וודא שמספר המעקב תקין."],
                "last_update": time.strftime("%d/%m/%Y %H:%M")
            }, f, ensure_ascii=False)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()

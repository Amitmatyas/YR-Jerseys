import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_scraper():
    tracking_number = "כאן_שים_מספר_מעקב" 
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # שורה קריטית: גורמת לשרתים של AfterShip לחשוב שזה דפדפן רגיל
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"Starting search for: {tracking_number}")
        driver.get(f"https://www.aftership.com/track/{tracking_number}")
        
        # מחכה עד 20 שניות שהסטטוס יופיע
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "status-tag")))
        
        status = driver.find_element(By.CLASS_NAME, "status-tag").text
        checkpoints = driver.find_elements(By.CLASS_NAME, "checkpoint-item")
        history = [cp.text.replace('\n', ' ') for cp in checkpoints]

        output = {
            "tracking_number": tracking_number,
            "status": status,
            "history": history,
            "last_update": time.strftime("%d/%m/%Y %H:%M")
        }

        # שמירה בתיקייה הנוכחית
        with open('tracking_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
        print("!!! SUCCESS: tracking_data.json created !!!")

    except Exception as e:
        print(f"!!! ERROR: {e}")
        # יצירת קובץ שגיאה קטן כדי שה-Action לא יקרוס
        with open('tracking_data.json', 'w', encoding='utf-8') as f:
            json.dump({"status": "Error", "message": str(e)}, f)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()

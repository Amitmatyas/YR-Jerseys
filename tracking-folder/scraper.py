import json
import time
import requests
import os

def get_tracking_api():
    # שליפת המפתח והמספר מהגדרות המערכת
    api_key = os.getenv('AFTERSHIP_KEY')
    tracking_number = "88297724" # שים פה את המספר שלך
    slug = "hfd"

    url = "https://api.aftership.com/tracking/v202601/trackings"
    headers = {
        "as-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "tracking": {
            "tracking_number": tracking_number,
            "slug": slug
        }
    }

    try:
        # שליחת הבקשה ל-AfterShip
        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()
        
        # גם אם זה כבר קיים (4003) או נוצר (201), אנחנו רוצים את הנתונים
        tracking_info = res_data.get("data", {}).get("tracking", {})
        
        # אם אין נתונים ב-POST, נבצע GET קטן כדי למשוך אותם
        if not tracking_info:
            get_url = f"{url}/{slug}/{tracking_number}"
            tracking_info = requests.get(get_url, headers=headers).json().get("data", {}).get("tracking", {})

        history = [f"[{cp.get('checkpoint_time')}] {cp.get('message')}" for cp in tracking_info.get("checkpoints", [])]
        
        output = {
            "tracking_number": tracking_number,
            "status": tracking_info.get("tag", "בתהליך"),
            "history": history if history else ["ממתין לעדכון ראשון מ-HFD"],
            "last_update": time.strftime("%d/%m/%Y %H:%M")
        }

        with open('tracking_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
        print("Success: API data saved to JSON")

    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    get_tracking_api()

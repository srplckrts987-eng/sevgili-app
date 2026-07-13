import requests
from datetime import datetime
import json
import random

def get_prayer_times(city="Tokat", country="Turkey"):
    """
    Fetches daily prayer times using Aladhan API.
    """
    try:
        # 1. Yöntem: Şehir ve Ülke ile günlük vakit çekmek
        url = f"http://api.aladhan.com/v1/timingsByCity"
        params = {
            "city": city,
            "country": country,
            "method": 13 # Diyanet İşleri Başkanlığı methodu
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["code"] == 200:
            timings = data["data"]["timings"]
            # Sadece temel vakitleri alalım
            return {
                "İmsak": timings.get("Imsak", ""),
                "Güneş": timings.get("Sunrise", ""),
                "Öğle": timings.get("Dhuhr", ""),
                "İkindi": timings.get("Asr", ""),
                "Akşam": timings.get("Maghrib", ""),
                "Yatsı": timings.get("Isha", "")
            }
        return None
    except Exception as e:
        print(f"Error fetching prayer times: {e}")
        return None

def get_daily_content():
    """
    Returns a daily verse (Ayet) and Hadith based on the current day.
    For now, uses a static list but rotates based on the day of the year.
    """
    contents = [
        {"ayet": "Şüphesiz ki Allah, adaleti, iyiliği, akrabaya yardım etmeyi emreder... (Nahl, 90)", 
         "hadis": "Kolaylaştırın, zorlaştırmayın; müjdeleyin, nefret ettirmeyin. (Buhari)"},
        {"ayet": "Sizin içinizde öyle bir topluluk bulunsun ki, onlar hayra çağırsın... (Âl-i İmrân, 104)", 
         "hadis": "Sizin en hayırlınız, ahlakı en güzel olanınızdır. (Buhari)"},
        {"ayet": "Rabbiniz şöyle buyurdu: Bana dua edin, duanıza cevap vereyim. (Mü'min, 60)", 
         "hadis": "Dua, ibadetin özüdür. (Tirmizi)"},
        {"ayet": "İyilikle kötülük bir olmaz. Sen kötülüğü en güzel bir şekilde önle... (Fussilet, 34)", 
         "hadis": "İnsanlara merhamet etmeyene Allah da merhamet etmez. (Müslim)"},
        {"ayet": "Gevşemeyin, hüzünlenmeyin. Eğer gerçekten iman etmişseniz üstün olan sizsiniz. (Âl-i İmrân, 139)", 
         "hadis": "Müminin durumu ne gariptir! Onun her işi kendisi için hayırdır... (Müslim)"}
    ]
    
    # Use the day of the year to pick a consistent index
    day_of_year = datetime.now().timetuple().tm_yday
    index = day_of_year % len(contents)
    
    return contents[index]

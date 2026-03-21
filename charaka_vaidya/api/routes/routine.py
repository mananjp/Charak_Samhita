
from fastapi import APIRouter, Query
from datetime import datetime

router = APIRouter()

ROUTINES = {
    "spring":  {"season": "Vasanta (Spring)", "wake": "Sunrise", "exercise": "Moderate",
                "diet_focus": "Light, bitter, astringent foods; reduce Kapha",
                "herbs": ["Triphala", "Neem", "Turmeric"],
                "avoid": ["Heavy, oily foods", "Daytime sleep", "Cold drinks"]},
    "summer":  {"season": "Grishma (Summer)", "wake": "Before sunrise",
                "exercise": "Light in cooler hours",
                "diet_focus": "Cooling, sweet foods; ghee, milk, coconut water",
                "herbs": ["Shatavari", "Amla", "Brahmi"],
                "avoid": ["Spicy foods", "Excessive sun exposure", "Strenuous exercise"]},
    "monsoon": {"season": "Varsha (Monsoon)", "wake": "Sunrise",
                "exercise": "Very light indoor",
                "diet_focus": "Light, easily digestible warm foods; Panchakarma ideal",
                "herbs": ["Giloy", "Tulsi", "Ginger"],
                "avoid": ["River water", "Heavy meals", "Street food"]},
    "autumn":  {"season": "Sharad (Autumn)", "wake": "Before sunrise",
                "exercise": "Moderate morning",
                "diet_focus": "Sweet, bitter, astringent; Pitta pacifying",
                "herbs": ["Amla", "Haritaki", "Turmeric"],
                "avoid": ["Sour, salty, pungent foods", "Midday sun", "Anger"]},
    "winter":  {"season": "Hemanta/Shishira (Winter)", "wake": "Before sunrise",
                "exercise": "Vigorous allowed",
                "diet_focus": "Nourishing, warm, unctuous; build Ojas",
                "herbs": ["Ashwagandha", "Shatavari", "Triphala"],
                "avoid": ["Cold, dry foods", "Exposure to cold winds", "Suppressing appetites"]},
}

def get_current_season():
    month = datetime.now().month
    if month in [3, 4]:    return "spring"
    elif month in [5, 6]:  return "summer"
    elif month in [7, 8, 9]: return "monsoon"
    elif month in [10, 11]: return "autumn"
    else:                   return "winter"

@router.get("")
def daily_routine(season: str = Query(None)):
    s = (season or get_current_season()).lower()
    routine = ROUTINES.get(s, ROUTINES["winter"])
    return {"season_key": s, **routine,
            "dinacharya": [
                "Wake up at Brahma Muhurta (96 min before sunrise)",
                "Tongue scraping (Jihwa Nirlekhana)",
                "Oil pulling (Kavala Graha) with sesame oil — 5 min",
                "Warm water on empty stomach",
                "Abhyanga (self-massage with warm sesame oil)",
                "Exercise / Yoga / Pranayama — 30 min",
                "Warm bath",
                "Light nutritious breakfast after sunrise",
                "Main meal at midday (digestive fire peaks)",
                "Evening walk or light activity",
                "Dinner 2-3 hours before sleep",
                "Sleep by 10 PM",
            ]}

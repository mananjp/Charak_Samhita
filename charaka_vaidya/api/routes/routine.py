
from fastapi import APIRouter, Query
from datetime import datetime

router = APIRouter()

ROUTINES = {
    "spring":  {"season": "Vasanta (Spring)", "wake": "Sunrise", "exercise": "Moderate",
                "diet_focus": "Light, bitter, astringent foods; reduce Kapha",
                "herbs": ["Triphala", "Neem", "Turmeric"],
                "avoid": ["Heavy, oily foods", "Daytime sleep", "Cold drinks"],
                "dinacharya": [
                    "Wake at Brahma Muhurta (sunrise) — Kapha time ends",
                    "Tongue scraping (Jihwa Nirlekhana) — removes Ama",
                    "Oil pulling with sesame oil (Kavala Graha) — 5 min",
                    "Drink warm water with honey and lemon — dissolves Kapha",
                    "Dry powder massage (Udvartana) with chickpea flour — reduces fat",
                    "Vigorous Surya Namaskar + Kapalabhati Pranayama — 30 min",
                    "Warm bath with neem leaves",
                    "Light breakfast: barley porridge, warm mung soup, honey",
                    "Main meal at midday — favour bitter greens, barley, light grains",
                    "Afternoon: avoid napping (aggravates Kapha in spring)",
                    "Evening walk followed by ginger-tulsi tea",
                    "Light dinner by 7 PM — warm soups, steamed vegetables",
                    "Apply Triphala-infused eye wash before bed",
                    "Sleep by 10 PM — avoid late nights",
                ]},
    "summer":  {"season": "Grishma (Summer)", "wake": "Before sunrise (cooler hours)",
                "exercise": "Light exercise in cooler hours only",
                "diet_focus": "Cooling, sweet foods; ghee, milk, coconut water",
                "herbs": ["Shatavari", "Amla", "Brahmi"],
                "avoid": ["Spicy foods", "Excessive sun exposure", "Strenuous exercise", "Alcohol"],
                "dinacharya": [
                    "Wake before sunrise to avoid heat — early Brahma Muhurta",
                    "Tongue scraping and gentle oil pulling with coconut oil",
                    "Drink room-temperature water infused with fennel seeds",
                    "Abhyanga with cooling coconut oil or sandalwood oil",
                    "Light Yoga — Shitali/Shitkari Pranayama (cooling breath)",
                    "Cool bath with rose water or sandalwood paste",
                    "Breakfast: sweet fruits, milk with mishri (rock sugar), soaked raisins",
                    "Main meal at midday — rice, sweet lassi, ghee, cucumber raita",
                    "Afternoon rest allowed (Charaka permits daytime sleep in Grishma)",
                    "Apply sandalwood paste on forehead and temples to cool Pitta",
                    "Evening: moonlit walk, fragrant gardens — Chandanadi activities",
                    "Dinner: light khichdi with ghee, buttermilk with roasted cumin",
                    "Drink cold milk with saffron before bed",
                    "Sleep on terrace/cool area, apply camphor on soles",
                ]},
    "monsoon": {"season": "Varsha (Monsoon)", "wake": "Sunrise",
                "exercise": "Very light indoor exercise only",
                "diet_focus": "Light, easily digestible warm foods; ideal for Panchakarma",
                "herbs": ["Giloy", "Tulsi", "Ginger"],
                "avoid": ["River/pond water", "Heavy meals", "Street food", "Raw salads"],
                "dinacharya": [
                    "Wake at sunrise — do not oversleep (weakens Agni)",
                    "Tongue scraping, oil pulling with warm sesame oil",
                    "Drink warm water with dry ginger powder — stokes Agni",
                    "Abhyanga with warm sesame oil — counters Vata aggravation",
                    "Light indoor exercise — gentle yoga, joint rotations",
                    "Warm bath with neem-turmeric water — antifungal protection",
                    "Breakfast: warm porridge with ginger, roasted mung dal",
                    "Use rock salt instead of regular salt — aids digestion",
                    "Main meal: freshly cooked warm food with ghee, aged rice, lentils",
                    "Avoid daytime sleep — aggravates Kapha in monsoon",
                    "Drink boiled and cooled water throughout the day",
                    "Evening: light tulsi-ginger-pepper tea (Trikatu kashaya)",
                    "Light warm dinner: khichdi, vegetable soups with cumin",
                    "Fumigate rooms with guggulu/neem dhoop — purifies air",
                    "Sleep by 10 PM on dry, elevated bed",
                ]},
    "autumn":  {"season": "Sharad (Autumn)", "wake": "Before sunrise",
                "exercise": "Moderate morning exercise",
                "diet_focus": "Sweet, bitter, astringent foods; Pitta pacifying",
                "herbs": ["Amla", "Haritaki", "Turmeric"],
                "avoid": ["Sour, salty, pungent foods", "Midday sun", "Anger", "Curd"],
                "dinacharya": [
                    "Wake before sunrise — Pitta is naturally high in Sharad",
                    "Tongue scraping, oil pulling with cooling coconut oil",
                    "Drink water stored overnight in silver vessel (Charaka method)",
                    "Abhyanga with sandalwood or vetiver oil — cools aggravated Pitta",
                    "Moderate exercise — swimming, walking in cool morning air",
                    "Bath with cooling herbs (chandana, usheera/vetiver)",
                    "Breakfast: sweet pomegranate, amla juice, rice flakes with milk",
                    "Virechana (therapeutic purgation) recommended in this season",
                    "Main meal: bitter-gourd sabzi, wheat, green gram, ghee-rice",
                    "Moonlit walks in evening — 'Sharad Chandrika' healing light",
                    "Apply sandalwood + camphor paste on body — Pitta relief",
                    "Dinner: light warm food, avoid fermented/sour items",
                    "Drink warm milk with turmeric and mishri before bed",
                    "Sleep in moonlit/open area with fragrant flowers (per Charaka)",
                ]},
    "winter":  {"season": "Hemanta/Shishira (Winter)", "wake": "Before sunrise",
                "exercise": "Vigorous exercise allowed — Agni is strongest",
                "diet_focus": "Nourishing, warm, unctuous foods; build Ojas",
                "herbs": ["Ashwagandha", "Shatavari", "Triphala"],
                "avoid": ["Cold, dry foods", "Exposure to cold winds", "Fasting", "Suppressing appetite"],
                "dinacharya": [
                    "Wake at Brahma Muhurta — body is strongest in Hemanta",
                    "Tongue scraping, warm sesame oil pulling",
                    "Drink warm water with tulsi and black pepper",
                    "Full-body Abhyanga with warm sesame/mustard oil — essential",
                    "Vigorous exercise: Surya Namaskar, wrestling, running (Charaka allows)",
                    "Hot water bath with sesame oil massage beforehand",
                    "Breakfast: heavy, nourishing — wheat halwa, warm milk with ghee",
                    "Apply agaru (aloewood) paste on body for warmth",
                    "Main meal: meat soups (for non-vegetarians), sugarcane juice, ghee-rich foods",
                    "Afternoon sun exposure — absorb vitamin D, counter cold",
                    "Evening: warm spiced milk, dry fruit ladoo, chyawanprash",
                    "Dinner: warm, heavy — urad dal, wheat rotis, ghee",
                    "Apply warm sesame oil on soles of feet and scalp before sleep",
                    "Sleep well-covered in warm room, early by 9:30 PM",
                ]},
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
    return {"season_key": s, **routine}

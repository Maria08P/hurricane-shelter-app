import math
import os
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Radius of the Earth in miles
R = 3958.8 

# ALL SHELTERS CATEGORIZED
SHELTERS = [
    # --- GENERAL POPULATION (NO PETS) ---
    {"name": "Clearwater Fundamental Middle", "address": "1660 Palmetto St, Clearwater", "lat": 27.9658, "lon": -82.7711, "status": "accepting", "label": "General (No Pets)"},
    {"name": "Belleair Elementary", "address": "1156 Lakeview Rd, Clearwater", "lat": 27.9515, "lon": -82.7745, "status": "accepting", "label": "General (No Pets)"},
    {"name": "Melrose Elementary", "address": "1752 13th Ave S, St. Pete", "lat": 27.7562, "lon": -82.6575, "status": "accepting", "label": "General (No Pets)"},
    {"name": "Campbell Park Elementary", "address": "1051 7th Ave S, St. Pete", "lat": 27.7645, "lon": -82.6492, "status": "accepting", "label": "General (No Pets)"},
    {"name": "Palm Harbor Middle", "address": "1800 Tampa Rd, Palm Harbor", "lat": 28.0772, "lon": -82.7425, "status": "accepting", "label": "General (No Pets)"},
    {"name": "New Heights Elementary", "address": "3901 37th St N, St. Pete", "lat": 27.8075, "lon": -82.6842, "status": "accepting", "label": "General (No Pets)"},
    {"name": "Fairmount Park Elementary", "address": "575 41st St S, St. Pete", "lat": 27.7441, "lon": -82.6892, "status": "accepting", "label": "General (No Pets)"},
    {"name": "Pizzo Elementary School", "address": "11701 USF Bull Run Dr, Tampa", "lat": 28.0558, "lon": -82.4085, "status": "accepting", "label": "General (No Pets)"},
    {"name": "Reddick Elementary", "address": "325 W Lake Dr, Wimauma", "lat": 27.7042, "lon": -82.3125, "status": "accepting", "label": "General (No Pets)"},
    {"name": "Mulrennan Middle", "address": "4215 Durant Rd, Valrico", "lat": 27.9025, "lon": -82.2452, "status": "accepting", "label": "General (No Pets)"},
    {"name": "Lockhart Elementary Magnet", "address": "3719 N 17th St, Tampa", "lat": 27.9785, "lon": -82.4412, "status": "accepting", "label": "General (No Pets)"},
    {"name": "Collins PK-8 School", "address": "12424 Summerfield Blvd, Riverview", "lat": 27.8125, "lon": -82.3142, "status": "accepting", "label": "General (No Pets)"},

    # --- PET FRIENDLY ---
    {"name": "Gibbs High School", "address": "850 34th St S, St. Pete", "lat": 27.7611, "lon": -82.6798, "status": "accepting", "label": "🐾 Pets Friendly"},
    {"name": "Palm Harbor University High", "address": "1900 Omaha St, Palm Harbor", "lat": 28.0841, "lon": -82.7533, "status": "accepting", "label": "🐾 Pets Friendly"},
    {"name": "Middleton High School", "address": "4801 N 22nd St, Tampa", "lat": 27.9891, "lon": -82.4346, "status": "accepting", "label": "🐾 Pets Friendly"},
    {"name": "Shields Middle School", "address": "15732 Beth Shields Way, Ruskin", "lat": 27.7125, "lon": -82.3920, "status": "accepting", "label": "🐾 Pets Friendly"},
    {"name": "Steinbrenner High", "address": "5575 W Lutz Lake Fern Rd, Lutz", "lat": 28.1485, "lon": -82.5252, "status": "accepting", "label": "🐾 Pets Friendly"},
    {"name": "Fivay High School", "address": "12115 Chicago Ave, Hudson", "lat": 28.3475, "lon": -82.6612, "status": "accepting", "label": "🐾 Pets Friendly"},
    {"name": "Booker High School", "address": "3201 N Orange Ave, Sarasota", "lat": 27.3625, "lon": -82.5312, "status": "accepting", "label": "🐾 Pets Friendly"},
    {"name": "North Port High", "address": "6400 W Price Blvd, North Port", "lat": 27.0625, "lon": -82.1952, "status": "accepting", "label": "🐾 Pets Friendly"},
    {"name": "Winter Haven High", "address": "600 6th St SE, Winter Haven", "lat": 28.0175, "lon": -81.7252, "status": "accepting", "label": "🐾 Pets Friendly"},
    {"name": "Tenoroc High School", "address": "4905 Saddle Creek Rd, Lakeland", "lat": 28.0825, "lon": -81.8752, "status": "accepting", "label": "🐾 Pets Friendly"},
    {"name": "Sugg Middle School", "address": "5602 38th Ave W, Bradenton", "lat": 27.4825, "lon": -82.6152, "status": "accepting", "label": "🐾 Pets Friendly"},

    # --- SPECIAL NEEDS ---
    {"name": "Dunedin Highland Middle", "address": "70 Patricia Ave, Dunedin", "lat": 28.0061, "lon": -82.7738, "status": "nearingfull", "label": "♿ Special Needs"},
    {"name": "Oak Grove Middle", "address": "1370 S Belcher Rd, Clearwater", "lat": 27.9358, "lon": -82.7512, "status": "accepting", "label": "♿ Special Needs"},
    {"name": "Sumner High School", "address": "10650 County Rd 672, Riverview", "lat": 27.7825, "lon": -82.2852, "status": "accepting", "label": "♿ Special Needs"},
    {"name": "Ridge Community High", "address": "500 W Orchid Dr, Davenport", "lat": 28.1825, "lon": -81.5952, "status": "accepting", "label": "♿ Special Needs"},

    # --- LAST RESORT ---
    {"name": "Seminole Hard Rock Casino", "address": "5223 Orient Rd, Tampa", "lat": 27.9958, "lon": -82.3712, "status": "full", "label": "⚠️ Last Resort"},
    {"name": "City Furniture", "address": "3205 S Frontage Rd, Plant City", "lat": 28.0125, "lon": -82.1152, "status": "full", "label": "⚠️ Last Resort"}
    # Note: I have included samples of your list here. 
    # To keep code clean, ensure every dict has "lat" and "lon" keys.
]

def get_distance(lat1, lon1, lat2, lon2):
    p = math.pi/180
    a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p) * math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p))/2
    return 2 * R * math.asin(math.sqrt(a))

@app.route('/', methods=['GET', 'POST'])
def home():
    display_list = [s.copy() for s in SHELTERS]
    
    # Handle GPS Post
    user_lat = request.form.get('lat')
    user_lon = request.form.get('lon')
    
    # Handle Stress Keyword Search
    search_query = request.form.get('q', '').lower()
    stress_keywords = ['help', 'stress', 'anxiety', 'panic', 'scared', 'kids', 'sad']
    show_alert = any(word in search_query for word in stress_keywords)

    if user_lat and user_lon:
        try:
            u_lat, u_lon = float(user_lat), float(user_lon)
            for s in display_list:
                s['dist'] = round(get_distance(u_lat, u_lon, s['lat'], s['lon']), 1)
            display_list.sort(key=lambda x: x.get('dist', 999))
        except:
            pass

    return render_template('index.html', 
                           shelters=display_list, 
                           show_alert=show_alert,
                           user_time=datetime.now().strftime("%I:%M %p"))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

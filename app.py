import math
import os
import qrcode
import io
from flask import Flask, render_template, send_file, request
from datetime import datetime

app = Flask(__name__)

R = 3958.8 # Earth Radius in Miles

# ALL 66 SHELTERS INCLUDED
SHELTERS = [
    # --- 🏠 GENERAL POPULATION ---
    {"name": "Clearwater Fundamental Middle", "address": "1660 Palmetto St., Clearwater", "lat": 27.9658, "lon": -82.7711, "label": "🏠 General"},
    {"name": "Belleair Elementary School", "address": "1156 Lakeview Rd., Clearwater", "lat": 27.9515, "lon": -82.7745, "label": "🏠 General"},
    {"name": "Melrose Elementary School", "address": "1752 13th Ave. S., St. Petersburg", "lat": 27.7562, "lon": -82.6575, "label": "🏠 General"},
    {"name": "Campbell Park Elementary", "address": "1051 7th Ave. S., St. Petersburg", "lat": 27.7645, "lon": -82.6492, "label": "🏠 General"},
    {"name": "Palm Harbor Middle School", "address": "1800 Tampa Rd., Palm Harbor", "lat": 28.0772, "lon": -82.7425, "label": "🏠 General"},
    {"name": "New Heights Elementary", "address": "3901 37th St. N., St. Petersburg", "lat": 27.8075, "lon": -82.6842, "label": "🏠 General"},
    {"name": "Fairmount Park Elementary", "address": "575 41st St. S., St. Petersburg", "lat": 27.7441, "lon": -82.6892, "label": "🏠 General"},
    {"name": "Pizzo Elementary School", "address": "11701 USF Bull Run Dr., Tampa", "lat": 28.0558, "lon": -82.4085, "label": "🏠 General"},
    {"name": "Reddick Elementary School", "address": "325 W. Lake Dr., Wimauma", "lat": 27.7042, "lon": -82.3125, "label": "🏠 General"},
    {"name": "Mulrennan Middle School", "address": "4215 Durant Rd., Valrico", "lat": 27.9025, "lon": -82.2452, "label": "🏠 General"},
    {"name": "Lockhart Elementary Magnet", "address": "3719 N. 17th St., Tampa", "lat": 27.9785, "lon": -82.4412, "label": "🏠 General"},
    {"name": "Collins PK-8 School", "address": "12424 Summerfield Blvd., Riverview", "lat": 27.8125, "lon": -82.3142, "label": "🏠 General"},

    # --- 🐾 PET-FRIENDLY ---
    {"name": "Gibbs High School", "address": "850 34th St. S., St. Petersburg", "lat": 27.7611, "lon": -82.6798, "label": "🐾 Pet Friendly"},
    {"name": "Palm Harbor University High", "address": "1900 Omaha St., Palm Harbor", "lat": 28.0841, "lon": -82.7533, "label": "🐾 Pet Friendly"},
    {"name": "Burnett Middle School", "address": "1010 N. Kingsway Rd., Seffner", "lat": 27.9625, "lon": -82.2852, "label": "🐾 Pet Friendly"},
    {"name": "Durant High School", "address": "4748 Cougar Path, Plant City", "lat": 27.8925, "lon": -82.1652, "label": "🐾 Pet Friendly"},
    {"name": "Middleton High School", "address": "4801 N. 22nd St., Tampa", "lat": 27.9891, "lon": -82.4346, "label": "🐾 Pet Friendly"},
    {"name": "Shields Middle School", "address": "15732 Beth Shields Way, Ruskin", "lat": 27.7125, "lon": -82.3920, "label": "🐾 Pet Friendly"},
    {"name": "Steinbrenner High School", "address": "5575 W. Lutz Lake Fern Rd., Lutz", "lat": 28.1485, "lon": -82.5252, "label": "🐾 Pet Friendly"},
    {"name": "Centennial Middle School", "address": "38505 Centennial Rd., Dade City", "lat": 28.3125, "lon": -82.1752, "label": "🐾 Pet Friendly"},
    {"name": "Fivay High School", "address": "12115 Chicago Ave., Hudson", "lat": 28.3475, "lon": -82.6612, "label": "🐾 Pet Friendly"},
    {"name": "Wesley Chapel High School", "address": "30651 Wells Rd., Wesley Chapel", "lat": 28.2325, "lon": -82.3252, "label": "🐾 Pet Friendly"},
    {"name": "River Ridge Middle/High", "address": "11646 Town Center Rd., New Port Richey", "lat": 28.2625, "lon": -82.6452, "label": "🐾 Pet Friendly"},
    {"name": "Sunlake High School", "address": "3023 Sunlake Blvd., Land O’ Lakes", "lat": 28.1925, "lon": -82.5052, "label": "🐾 Pet Friendly"},
    {"name": "Atwater Elementary School", "address": "4701 Huntsville Ave., North Port", "lat": 27.0825, "lon": -82.2152, "label": "🐾 Pet Friendly"},
    {"name": "Booker High School", "address": "3201 N. Orange Ave., Sarasota", "lat": 27.3625, "lon": -82.5312, "label": "🐾 Pet Friendly"},
    {"name": "Brookside Middle School", "address": "3636 South Shade Ave., Sarasota", "lat": 27.3125, "lon": -82.5152, "label": "🐾 Pet Friendly"},
    {"name": "Gulf Gate Elementary", "address": "6500 S. Lockwood Ridge Rd., Sarasota", "lat": 27.2625, "lon": -82.4952, "label": "🐾 Pet Friendly"},
    {"name": "Heron Creek Middle School", "address": "6501 W. Price Blvd., North Port", "lat": 27.0525, "lon": -82.1652, "label": "🐾 Pet Friendly"},
    {"name": "North Port High School", "address": "6400 W. Price Blvd., North Port", "lat": 27.0625, "lon": -82.1952, "label": "🐾 Pet Friendly"},
    {"name": "Phillippi Shores Elementary", "address": "4747 S. Tamiami Trail, Sarasota", "lat": 27.2725, "lon": -82.5352, "label": "🐾 Pet Friendly"},
    {"name": "Southside Elementary School", "address": "1901 Webber St., Sarasota", "lat": 27.3125, "lon": -82.5252, "label": "🐾 Pet Friendly"},
    {"name": "Woodland Middle School", "address": "2700 Panacea Blvd., North Port", "lat": 27.0925, "lon": -82.2452, "label": "🐾 Pet Friendly"},
    {"name": "West Hernando Middle", "address": "14325 Ken Austin Pkwy., Brooksville", "lat": 28.5525, "lon": -82.4952, "label": "🐾 Pet Friendly"},
    {"name": "Enrichment Center", "address": "800 John Gary Grubbs Blvd., Brooksville", "lat": 28.5425, "lon": -82.3952, "label": "🐾 Pet Friendly"},
    {"name": "Challenger K-8", "address": "13400 Elgin Blvd., Spring Hill", "lat": 28.4825, "lon": -82.5352, "label": "🐾 Pet Friendly"},
    {"name": "Auburndale High School", "address": "1 Bloodhound Trail, Auburndale", "lat": 28.0625, "lon": -81.7952, "label": "🐾 Pet Friendly"},
    {"name": "Spessard Holland Elementary", "address": "2432 E.F. Griffin Rd., Bartow", "lat": 27.9125, "lon": -81.8252, "label": "🐾 Pet Friendly"},
    {"name": "Citrus Ridge Academy", "address": "1775 Sand Mine Rd., Davenport", "lat": 28.3225, "lon": -81.6552, "label": "🐾 Pet Friendly"},
    {"name": "Horizons Elementary School", "address": "1700 Forest Lake Dr., Davenport", "lat": 28.2125, "lon": -81.6052, "label": "🐾 Pet Friendly"},
    {"name": "George Jenkins High School", "address": "6000 Lakeland Highlands Rd., Lakeland", "lat": 27.9525, "lon": -81.9152, "label": "🐾 Pet Friendly"},
    {"name": "Highlands Grove Elementary", "address": "4510 Lakeland Highlands Rd., Lakeland", "lat": 27.9725, "lon": -81.9252, "label": "🐾 Pet Friendly"},
    {"name": "Kathleen High School", "address": "1100 Red Devil Way, Lakeland", "lat": 28.0625, "lon": -81.9852, "label": "🐾 Pet Friendly"},
    {"name": "R. Bruce Wagner Elementary", "address": "5500 Yates Rd., Lakeland", "lat": 28.0025, "lon": -82.0152, "label": "🐾 Pet Friendly"},
    {"name": "Sleepy Hill Elementary", "address": "2285 Sleepy Hill Rd., Lakeland", "lat": 28.0825, "lon": -81.9952, "label": "🐾 Pet Friendly"},
    {"name": "Mulberry Middle School", "address": "500 S.E. MLK Jr. Ave., Mulberry", "lat": 27.8925, "lon": -81.9752, "label": "🐾 Pet Friendly"},
    {"name": "Lake Marion Creek Middle", "address": "3055 Lake Marion Creek Dr., Poinciana", "lat": 28.1125, "lon": -81.4952, "label": "🐾 Pet Friendly"},
    {"name": "Chain of Lakes Elementary", "address": "7001 Hwy. 653, Winter Haven", "lat": 27.9625, "lon": -81.6852, "label": "🐾 Pet Friendly"},
    {"name": "Winter Haven High School", "address": "600 6th St. S.E., Winter Haven", "lat": 28.0175, "lon": -81.7252, "label": "🐾 Pet Friendly"},
    {"name": "Haines City High School", "address": "2800 Hornet Dr., Haines City", "lat": 28.1225, "lon": -81.6052, "label": "🐾 Pet Friendly"},
    {"name": "Lake Region High School", "address": "1995 Thunder Rd., Eagle Lake", "lat": 27.9725, "lon": -81.7552, "label": "🐾 Pet Friendly"},
    {"name": "Tenoroc High School", "address": "4905 Saddle Creek Rd., Lakeland", "lat": 28.0825, "lon": -81.8752, "label": "🐾 Pet Friendly"},
    {"name": "Gullett Elementary School", "address": "12125 44th Ave. E., Bradenton", "lat": 27.4425, "lon": -82.4152, "label": "🐾 Pet Friendly"},
    {"name": "Harvey Elementary School", "address": "8610 115th Ave. E., Parrish", "lat": 27.5925, "lon": -82.3952, "label": "🐾 Pet Friendly"},
    {"name": "McNeal Elementary School", "address": "6325 Lorraine Rd., Bradenton", "lat": 27.4225, "lon": -82.4152, "label": "🐾 Pet Friendly"},
    {"name": "Miller Elementary School", "address": "601 43rd St. W., Bradenton", "lat": 27.4925, "lon": -82.6052, "label": "🐾 Pet Friendly"},
    {"name": "Mills Elementary School", "address": "7200 69th St. E., Palmetto", "lat": 27.5625, "lon": -82.4852, "label": "🐾 Pet Friendly"},
    {"name": "Mona Jain Middle School", "address": "12205 44th Ave. E., Bradenton", "lat": 27.4425, "lon": -82.4052, "label": "🐾 Pet Friendly"},
    {"name": "Myakka Elementary School", "address": "37205 Manatee Ave., Myakka City", "lat": 27.3425, "lon": -82.1452, "label": "🐾 Pet Friendly"},
    {"name": "Sugg Middle School", "address": "5602 38th Ave. W., Bradenton", "lat": 27.4825, "lon": -82.6152, "label": "🐾 Pet Friendly"},
    {"name": "Robert H. Prine Elementary", "address": "3801 Southern Pkwy. W., Bradenton", "lat": 27.4625, "lon": -82.5952, "label": "🐾 Pet Friendly"},
    {"name": "Virgil Mills Elementary", "address": "7200 69th St. E., Palmetto", "lat": 27.5625, "lon": -82.4852, "label": "🐾 Pet Friendly"},
    {"name": "Buffalo Creek Middle", "address": "7320 69th St. E., Palmetto", "lat": 27.5725, "lon": -82.4752, "label": "🐾 Pet Friendly"},

    # --- ♿ SPECIAL NEEDS ---
    {"name": "Dunedin Highland Middle", "address": "70 Patricia Ave., Dunedin", "lat": 28.0061, "lon": -82.7738, "label": "♿ Special Needs"},
    {"name": "Oak Grove Middle School", "address": "1370 S. Belcher Rd., Clearwater", "lat": 27.9358, "lon": -82.7512, "label": "♿ Special Needs"},
    {"name": "Sumner High School", "address": "10650 County Rd. 672, Riverview", "lat": 27.7825, "lon": -82.2852, "label": "♿ Special Needs"},
    {"name": "Strawberry Crest High", "address": "4691 Gallagher Rd., Dover", "lat": 28.0225, "lon": -82.2352, "label": "♿ Special Needs"},
    {"name": "Fasano Hurricane Center", "address": "11611 Denton Ave., Hudson", "lat": 28.3425, "lon": -82.6752, "label": "♿ Special Needs"},
    {"name": "FDOH Polk Specialty Unit", "address": "1255 Brice Blvd., Bartow", "lat": 27.8825, "lon": -81.8352, "label": "♿ Special Needs"},
    {"name": "Ridge Community High", "address": "500 W. Orchid Dr., Davenport", "lat": 28.1825, "lon": -81.5952, "label": "♿ Special Needs"},
    {"name": "McKeel Academy", "address": "1810 W. Parker St., Lakeland", "lat": 28.0325, "lon": -81.9852, "label": "♿ Special Needs"},

    # --- ⚠️ LAST RESORT ---
    {"name": "City Furniture", "address": "3205 S. Frontage Rd., Plant City", "lat": 28.0125, "lon": -82.1152, "label": "⚠️ Last Resort"},
    {"name": "Seminole Hard Rock Casino", "address": "5223 Orient Rd., Tampa", "lat": 27.9958, "lon": -82.3712, "label": "⚠️ Last Resort"},
    {"name": "BayCare (Old B&N)", "address": "11802 N. Dale Mabry Hwy., Tampa", "lat": 28.0525, "lon": -82.5012, "label": "⚠️ Last Resort"}
]
@app.route('/qr_code')
def qr_code():
    # THIS MUST BE THE GOOGLE FORM LINK, NOT THE RENDER LINK
    survey_url = "https://hss-ppcu.onrender.com"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(survey_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')
def calculate_distance(lat1, lon1, lat2, lon2):
    p = math.pi/180
    a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p) * math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p))/2
    return 2 * R * math.asin(math.sqrt(a))

@app.route('/', methods=['GET', 'POST'])
def home():
    display_list = [s.copy() for s in SHELTERS]
    user_lat = request.form.get('lat')
    user_lon = request.form.get('lon')
    search_query = request.form.get('q', '').lower()
    
    # Tool Trigger: FEMA/Stress Detection
    trigger_words = ['fema', 'money', 'help', 'stress', 'sad', 'scared', 'apply']
    show_alert = any(word in search_query for word in trigger_words)

    if user_lat and user_lon:
        try:
            u_lat, u_lon = float(user_lat), float(user_lon)
            for s in display_list:
                s['dist'] = round(calculate_distance(u_lat, u_lon, s['lat'], s['lon']), 1)
            display_list.sort(key=lambda x: x.get('dist', 999))
        except: pass

    return render_template('index.html', shelters=display_list, show_alert=show_alert, user_time=datetime.now().strftime("%I:%M %p"))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

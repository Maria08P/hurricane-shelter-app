from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    shelters = [
        # --- GENERAL POPULATION ---
        {"name": "Clearwater Fundamental Middle School", "address": "1660 Palmetto St., Clearwater", "status": "accepting", "label": "Accepting"},
        {"name": "Belleair Elementary School", "address": "1156 Lakeview Rd., Clearwater", "status": "accepting", "label": "Accepting"},
        {"name": "Melrose Elementary School", "address": "1752 13th Ave. S., St. Petersburg", "status": "accepting", "label": "Accepting"},
        {"name": "Campbell Park Elementary School", "address": "1051 7th Ave. S., St. Petersburg", "status": "accepting", "label": "Accepting"},
        {"name": "Palm Harbor Middle School", "address": "1800 Tampa Rd., Palm Harbor", "status": "accepting", "label": "Accepting"},
        {"name": "New Heights Elementary School", "address": "3901 37th St. N., St. Petersburg", "status": "accepting", "label": "Accepting"},
        {"name": "Fairmount Park Elementary School", "address": "575 41st St. S., St. Petersburg", "status": "accepting", "label": "Accepting"},
        {"name": "Pizzo Elementary School", "address": "11701 USF Bull Run Dr., Tampa", "status": "accepting", "label": "Accepting"},
        {"name": "Reddick Elementary School", "address": "325 W. Lake Dr., Wimauma", "status": "accepting", "label": "Accepting"},
        {"name": "Mulrennan Middle School", "address": "4215 Durant Rd., Valrico", "status": "accepting", "label": "Accepting"},
        {"name": "Lockhart Elementary Magnet School", "address": "3719 N. 17th St., Tampa", "status": "accepting", "label": "Accepting"},
        {"name": "Collins PK-8 School", "address": "12424 Summerfield Blvd., Riverview", "status": "accepting", "label": "Accepting"},

        # --- PET FRIENDLY ---
        {"name": "Gibbs High School", "address": "850 34th St. S., St. Petersburg", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Palm Harbor University High School", "address": "1900 Omaha St., Palm Harbor", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Burnett Middle School", "address": "1010 N. Kingsway Rd., Seffner", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Durant High School", "address": "4748 Cougar Path, Plant City", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Middleton High School", "address": "4801 N. 22th St., Tampa", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Shields Middle School", "address": "15732 Beth Shields Way, Ruskin", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Steinbrenner High School", "address": "5575 W. Lutz Lake Fern Rd., Lutz", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Centennial Middle School", "address": "38505 Centennial Rd., Dade City", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Fivay High School", "address": "12115 Chicago Ave., Hudson", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Wesley Chapel High School", "address": "30651 Wells Rd., Wesley Chapel", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "River Ridge Middle/High School", "address": "11646 Town Center Rd., New Port Richey", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Sunlake High School", "address": "3023 Sunlake Blvd., Land O’ Lakes", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Atwater Elementary School", "address": "4701 Huntsville Ave., North Port", "status": "accepting", "label": "🐾 Pets OK"},
        {"name": "Booker High School", "address": "3201 N. Orange Ave., Sarasota", "status": "accepting", "label": "🐾 Pets OK"},

        # --- SPECIAL NEEDS ---
        {"name": "Dunedin Highland Middle School", "address": "70 Patricia Ave., Dunedin", "status": "nearingfull", "label": "♿ Special Needs"},
        {"name": "Oak Grove Middle School", "address": "1370 S. Belcher Rd., Clearwater", "status": "nearingfull", "label": "♿ Special Needs"},
        {"name": "Sumner High School", "address": "10650 County Rd. 672, Riverview", "status": "accepting", "label": "♿ Special Needs"},
        {"name": "Fasano Regional Hurricane Center", "address": "11611 Denton Ave., Hudson", "status": "accepting", "label": "♿ Special Needs"},

        # --- LAST RESORT ---
        {"name": "City Furniture", "address": "3205 S. Frontage Rd., Plant City", "status": "full", "label": "Last Resort"},
        {"name": "Seminole Hard Rock Casino", "address": "5223 Orient Rd., Tampa", "status": "accepting", "label": "Last Resort"},
        {"name": "BayCare (Old Barnes & Noble)", "address": "11802 N. Dale Mabry Hwy., Tampa", "status": "accepting", "label": "Last Resort"}
    ]
    
    now = datetime.now().strftime("%I:%M %p")
    return render_template('index.html', user_time=now, shelters=shelters)

if __name__ == '__main__':
    app.run(debug=True)
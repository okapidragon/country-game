import os
import random
import requests
from flask import Flask, request, render_template, redirect, url_for # Combined imports

random_country = ""
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/submit', methods=['GET', 'POST'])
def home():
    output_message = ""
    
    if request.method == 'POST':
        def isindependent():
            global reresponse, recountries, independent
            reresponse = requests.get(f"https://restcountries.com/v3.1/name/{random_country}")
            recountries = reresponse.json()
            independent = [recountry["independent"] for recountry in recountries][0]
        
        def countrypicker():
            global random_country, response, countries, country_names
            response = requests.get("https://restcountries.com/v3.1/all?fields=name")
            countries = response.json()
            country_names = [country["name"]["common"] for country in countries]
            random_country = random.choice(country_names)
            isindependent()

        def go():
            nonlocal output_message # Added to let 'go' update the variable above
            countrypicker()
            if independent == True:
                global pop, continent, capital, flag
                pop = (((str([recountry["population"] for recountry in recountries][0]).replace("[", "")).replace("]", "")).replace("'", ""))
                continent = (((str([recountry["continents"] for recountry in recountries][0]).replace("[", "")).replace("]", "")).replace("'", ""))
                capital = (((str([recountry["capital"] for recountry in recountries][0]).replace("[", "")).replace("]", "")).replace("'", ""))
                flag = (((str([recountry["flag"] for recountry in recountries][0]).replace("[", "")).replace("]", "")).replace("'", ""))
                level = request.form.get("difficulty")
                if level == "Easy":
                    output_message = (f"Pop: {pop}, Continent: {continent}, Cap: {capital}, Flag: {flag}")
                
                guessedcountry = request.form.get("guess")
                if guessedcountry.lower() == random_country.lower():
                    output_message = "Correct!"
                else:
                    output_message = f"Sorry, the country was {random_country}"
            else:
                go()
        
        go()
    return render_template("index.html", result=output_message)

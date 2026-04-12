import os
import random
import requests
from flask import Flask, request, render_template, redirect, url_for

# 1. Fix pathing for /api folder
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

# 2. Define these at the top level so 'global' has something to find
random_country = ""
independent = False
recountries = []
re_response = None

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/submit', methods=['GET', 'POST'])
def home():
    output_message = ""
    
    # We must declare these as global inside the route to use your logic
    global random_country, independent, recountries, pop, continent, capital, flag

    if request.method == 'POST':
        def isindependent():
            global re_response, recountries, independent
            re_response = requests.get(f"https://restcountries.com/v3.1/name/{random_country}")
            recountries = re_response.json()
            # Safety check to prevent crash if API returns error
            if isinstance(recountries, list) and len(recountries) > 0:
                independent = recountries[0].get("independent", False)
            else:
                independent = False
        
        def countrypicker():
            global random_country, response, countries, country_names
            response = requests.get("https://restcountries.com/v3.1/all?fields=name")
            countries = response.json()
            country_names = [country["name"]["common"] for country in countries]
            random_country = random.choice(country_names)
            isindependent()

        def go():
            nonlocal output_message 
            countrypicker()
            if independent == True:
                # Using .get() prevents 500 errors if a key is missing
                data = recountries[0]
                pop = str(data.get("population", "Unknown"))
                continent = str(data.get("continents", ["Unknown"])[0])
                capital = str(data.get("capital", ["Unknown"])[0])
                flag = str(data.get("flag", ""))
                
                level = request.form.get("difficulty")
                if level == "Easy":
                    output_message = (f"Pop: {pop}, Continent: {continent}, Cap: {capital}, Flag: {flag}")
                
                guessedcountry = request.form.get("guess", "")
                if guessedcountry.lower() == random_country.lower():
                    output_message = "Correct!"
                else:
                    # If it's not Easy, we just show the name
                    if level != "Easy":
                        output_message = f"Sorry, the country was {random_country}"
                    else:
                        output_message = f"Sorry, it was {random_country}. {output_message}"
            else:
                go() 
        
        go()
        
    return render_template("index.html", result=output_message)

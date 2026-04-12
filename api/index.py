import os
import random
import requests
from flask import Flask, request, render_template

# 1. Setup pathing for Vercel /api folder structure
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

def get_random_independent_country():
    """
    Fetches the full list from the API once and picks an independent country.
    This replaces the 'go()' recursion to prevent 500 errors/timeouts.
    """
    try:
        response = requests.get("https://restcountries.com/v3.1/all?fields=name,independent,population,continents,capital,flag")
        all_countries = response.json()
        
        # Filter the list first so we only pick valid countries
        independent_list = [c for c in all_countries if c.get("independent")]
        
        if not independent_list:
            return None
            
        country = random.choice(independent_list)
        
        # Format the data into a clean dictionary for the HTML
        return {
            "name": country['name']['common'],
            "pop": f"{country.get('population', 0):,}", # Formats 1000000 as 1,000,000
            "continent": country.get('continents', ['Unknown'])[0],
            "capital": country.get('capital', ['None'])[0],
            "flag": country.get('flag', '🏳️')
        }
    except Exception as e:
        print(f"API Error: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    output_message = ""
    
    if request.method == 'POST':
        # CHECK THE GUESS
        # We get the 'correct_country' from the hidden input field in your HTML
        user_guess = request.form.get("guess", "").strip().lower()
        correct_answer = request.form.get("correct_country", "").strip().lower()
        
        if user_guess == correct_answer:
            output_message = f"Correct! It was indeed {correct_answer.title()}."
        else:
            output_message = f"Sorry, the country was {correct_answer.title()}."
            
        # When showing the result, we don't pick a new country yet 
        # (The HTML will provide a 'Play Again' link)
        return render_template("index.html", result=output_message)

    # INITIAL LOAD (GET REQUEST)
    # Pick the country and pass the data to the template
    target_country = get_random_independent_country()
    return render_template("index.html", country=target_country)

# Vercel needs the 'app' variable at the top level

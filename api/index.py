import os
import random
import requests
from flask import Flask, request, render_template

# 1. Setup pathing for Vercel /api folder structure
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

def get_random_independent_country():
    try:
        response = requests.get("https://restcountries.com/v3.1/all?fields=name,independent,population,continents,capital,flag")
        all_countries = response.json()
        
        # Filter for independent countries
        independent_list = [c for c in all_countries if c.get("independent")]
        
        if not independent_list:
            return None
            
        choice = random.choice(independent_list)
        
        # FIX: We use ['population'] or .get('population') 
        # specifically to avoid the .pop() function name collision.
        return {
            "name": choice['name']['common'],
            "pop": f"{choice.get('population', 0):,}", # The value, formatted with commas
            "continent": choice.get('continents', ['Unknown'])[0],
            "capital": choice.get('capital', ['None'])[0],
            "flag": choice.get('flag', '🏳️')
        }
    except Exception as e:
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

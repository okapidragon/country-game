import random
import requests
global random_country
random_country = ""
def isindependent():
        global reresponse
        global recountries
        global independent
        reresponse = requests.get(f"https://restcountries.com/v3.1/name/{random_country}")
        recountries = reresponse.json()
        independent = [recountry["independent"] for recountry in recountries][0]
def countrypicker():
        global random_country
        global response
        global countries
        global country_names
        response = requests.get("https://restcountries.com/v3.1/all?fields=name")
        countries = response.json()
        country_names = [country["name"]["common"] for country in countries]
        random_country = random.choice(country_names)
        isindependent()
def go():
    countrypicker()
    isindependent()
    if independent == True:
        global pop
        global continent
        global capital
        global flag
        pop = (((str([recountry["population"] for recountry in recountries][0]).replace("[", "")).replace("]", "")).replace("'", ""))
        continent = (((str([recountry["continents"] for recountry in recountries][0]).replace("[", "")).replace("]", "")).replace("'", ""))
        capital = (((str([recountry["capital"] for recountry in recountries][0]).replace("[", "")).replace("]", "")).replace("'", ""))
        flag = (((str([recountry["flag"] for recountry in recountries][0]).replace("[", "")).replace("]", "")).replace("'", ""))
        level = input("Level: Easy, Medium, or Hard ")
        if level.lower() == "easy":
                guessedcountry = input(f"""Guess the country:
Population: {pop}
Continent: {continent}
Capital: {capital}
Flag: {flag}
""")
                if guessedcountry.lower() == random_country.lower():
                        print("Correct!")
                else:
                        print(f"Sorry, the country was {random_country}")
    else:
        go()
go()

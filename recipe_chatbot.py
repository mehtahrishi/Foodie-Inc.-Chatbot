import aiml
import requests

# Initialize AIML kernel
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("LOAD AIML B")

# Replace with your actual API keys
SPOONACULAR_API_KEY = 'bdf93e0f01ea4e8e88713289d1c79abf'
WEATHER_API_KEY = 'f7efff2c055cf4815a2b09b14dea96af'

BASE_URL_SPOONACULAR = 'https://api.spoonacular.com/recipes'
BASE_URL_WEATHER = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    try:
        response = requests.get(BASE_URL_WEATHER, params={
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        })
        data = response.json()
        if data.get('cod') == 200:
            temp = data['main']['temp']
            weather = data['weather'][0]['description']
            return temp, weather
        else:
            return None, "Sorry, I couldn't fetch the weather information."
    except Exception as e:
        return None, f"An error occurred: {e}"

def get_recipe(query):
    try:
        response = requests.get(f"{BASE_URL_SPOONACULAR}/search", params={
            'query': query,
            'apiKey': SPOONACULAR_API_KEY,
            'number': 1
        })
        data = response.json()
        if data['results']:
            recipe = data['results'][0]
            recipe_id = recipe['id']
            recipe_details = get_recipe_details(recipe_id)
            return (f"Here's a recipe for {query}: {recipe['title']}. More details: {recipe['sourceUrl']}\n\n"
                    f"Ingredients:\n{recipe_details}")
        else:
            return "Sorry, I couldn't find any recipes for that query."
    except Exception as e:
        return f"An error occurred: {e}"

def get_recipe_details(recipe_id):
    try:
        response = requests.get(f"{BASE_URL_SPOONACULAR}/{recipe_id}/information", params={
            'apiKey': SPOONACULAR_API_KEY
        })
        data = response.json()
        ingredients = data.get('extendedIngredients', [])
        ingredient_list = [f"{ingredient['amount']} {ingredient['unit']} {ingredient['name']}" for ingredient in ingredients]
        ingredients_text = "\n".join(ingredient_list)
        return ingredients_text
    except Exception as e:
        return f"An error occurred: {e}"
    
def suggest_food_based_on_weather(temp):
    if temp < 15:
        return "It's quite cold! How about some hot soup or spicy food to warm you up?"
    elif 15 <= temp < 25:
        return "The weather is mild. A nice pasta or sandwich might be just right."
    elif 25 <= temp < 35:
        return "It's getting warm! Maybe a fresh salad or cold beverage would be refreshing."
    else:
        return "It's really hot outside! A cold dessert or something light would be perfect."

while True:
    input_text = input(">Human: ").strip().lower()
    
    if input_text == "what should i eat":
        print(">Bot: Hmm! Lemme see... Give me your location.")
        city = input(">Human: ").strip()
        temp, weather = get_weather(city)
        if temp is not None:
            food_suggestion = suggest_food_based_on_weather(temp)
            print(f">Bot: According to your location, {city}, where the weather is {temp}°C ({weather}), you should eat something like: {food_suggestion}")
        else:
            print(f">Bot: {weather}")
    elif 'recipe' in input_text:
        query = input_text.replace('recipe', '').strip()
        recipe_info = get_recipe(query)
        print(f">Bot: {recipe_info}")
    elif 'how to cook' in input_text:
        query = input_text.replace('how to cook', '').strip()
        recipe_info = get_recipe(query)
        print(f">Bot: {recipe_info}")
    else:
        response = kernel.respond(input_text)
        print(f">Bot: {response}")
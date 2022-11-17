from flask import Flask, request, render_template
import random
import json
import requests

server = Flask(__name__)

@server.route('/')
def homepage():
    #please note I use @server instead of @app
    return render_template('index.html')

@server.route('/starwars')
def chuck():
    return render_template('starwars.html')

@server.route('/sw_results')
def chuck_results():
    # CHARACTER DATA #
    character_id = request.args.get('id')
    if (int(character_id) == 17) or (int(character_id) > 88) or (int(character_id) <= 0):
        return render_template('error.html')
    api_call = requests.get(f'https://swapi.py4e.com/api/people/{character_id}')
    data_json = api_call.json()
    name = data_json['name']
    height = data_json['height']
    mass = data_json['mass']
    hair_colour = data_json['hair_color']
    eye_colour = data_json['eye_color']
    homeworld = data_json['homeworld']
    films = data_json['films']
    # HOMEWORLD DATA #
    homeworld_api_call = requests.get(homeworld)
    homeworld_data_json = homeworld_api_call.json()
    homeworld_data = homeworld_data_json['name']
    # FILM DATA # 
    film_list = []
    for film in films:
        film_api_call = requests.get(film)
        film_data_json = film_api_call.json()
        film_data_title = film_data_json['title']
        print('Test:', film_data_title)
        film_list.append(film_data_title)
    print(film_list)
    # DATA TO SEND FOR RESULTS#
    context = {
        'name' : name,
        'height': height,
        'mass': mass,
        'eye_colour': eye_colour,
        'hair_colour': hair_colour,
        'films': film_list,
        'world': homeworld_data,
    }
    
    return render_template('sw_results.html', **context)


if __name__ == '__main__':
    server.config['ENV'] = 'development'
    server.run(debug = True, port = 5000)
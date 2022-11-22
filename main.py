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
def sw():
    return render_template('starwars.html')

@server.route('/sw_results', methods=['GET', 'POST'])
def sw_results():
    API = 'https://swapi.py4e.com/api/people/'
    if request.method == 'POST':
        character = request.form.get("id")
        API = 'https://swapi.py4e.com/api/people/' + character  
        try:            
            response = requests.get(API)
        except KeyError:
            return render_template('error.html')
        if json.loads(response.content).get('detail') == 'Not found':        
            # give 'no data exists' API repsonse to render 404
            return render_template('error.html')           
        else:
            # give 'data exists' API response to render received details 
            # print(json.loads(response.content))
            context = {
                'name': json.loads(response.content).get('name'),
                'height': json.loads(response.content).get('height'),
                'mass': json.loads(response.content).get('mass'),
                'hair_colour': json.loads(response.content).get('hair_color'),
                'eye_colour': json.loads(response.content).get('eye_color'),
            }
            films_list = json.loads(response.content).get('films')
            print(films_list)
            # homeworld search 
            try:
                homeworld_response = requests.get(json.loads(response.content).get('homeworld'))
                homeworld = json.loads(homeworld_response.content).get('name')
                context['world'] = homeworld
            except KeyError:
                context['world'] = ''           
            # movie search
            movie_titles = []
            try:
                for film in films_list:
                    film_response = requests.get(film)
                    print(json.loads(film_response.content).get('title'))
                    movie_titles.append(json.loads(film_response.content).get('title'))
                context['films'] = movie_titles
            except KeyError:
                context['films'] = ''
        return render_template('sw_results.html', **context)
    else:
        return render_template('sw_results.html')
    
    return render_template('sw_results.html', **context)


if __name__ == '__main__':
    server.config['ENV'] = 'development'
    server.run(debug = True, port = 5000)
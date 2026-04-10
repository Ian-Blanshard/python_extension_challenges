# == EXERCISES ==
from urllib.request import urlopen
import json
# Purpose: Use Python libraries to request the provided URL, convert the
#          response data to JSON, and return the data.
def load_data_from_url(url):
    return json.loads(urlopen(url).read().decode('UTF-8'))
    
# Purpose: Use Python libraries to open the specified file, convert the
#          data to JSON, and return the data.
def load_data_from_file(filename):
    with open(filename) as file:
        return json.load(file)
    
# Purpose: Load the sample JSON from file, and returns a list of films 
#           directed by the named person.
def get_films_by_director(filename, director):    
    return [x['name'] for x in load_data_from_file(filename) if x['director'] == director]

# Purpose: Load the sample JSON from file, and returns a list of films 
#           starring the named person.
def get_films_by_actor(filename, desired_actor):
    return [x['name'] for x in load_data_from_file(filename) if desired_actor in x['stars']]

# Purpose: Load the sample JSON from file, and returns a list of films 
#           with a rating which is AT LEAST the value specified.
def get_films_with_minimum_rating(filename, rating):
    return [x['name'] for x in load_data_from_file(filename) if x['imdb_rating'] >= rating]

# Purpose: Load the sample JSON from file, and returns a list of films 
#           which were released during the specified years.
def get_films_within_year_range(filename, start_year, end_year):
    return [x['name'] for x in load_data_from_file(filename) if x['year'] >= start_year and x['year'] <= end_year]

# Purpose: Load the sample JSON from file, and returns a list of films 
#           in order of the year that they were released.
def order_films_chronologically(filename):
    return [x['name'] for x in sorted(load_data_from_file(filename), key=lambda x: x['year'])]

# Purpose: Load the sample JSON from file, and returns a list of films 
#           starting with the most recent.
def order_films_most_recent_first(filename):
    return [x['name'] for x in sorted(load_data_from_file(filename), key=lambda x: x['year'], reverse=True)]

# Purpose: Load the sample JSON from file, and returns a deduplicated list 
#           of all the actors whose name begins with that letter,
#           in alphabetical order.
def all_actors_starting_with_letter(filename, letter):
    
    stars = [star for film in load_data_from_file(filename) for star in film['stars'] if star[0].lower() == letter]
    stars = list(set(stars))
    stars.sort()    
    return (stars)

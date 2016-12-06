import json
import pickle
import time

MOVIES_PICKLE_FILE = 'movies.model'

class MoviesParser:

    def __init__(self):
        self.dictDirector = {} # {director : [movieID]}
        self.dictActor = {} # {actor : [movieID]}
        self.dictGenre = {} # {genre : [movieID]}
    
    def returnMovieID(self, movieObject):
         return movieObject['movie_id']

    #method that checks if ID of dict contains directors: if not, create one dict with dir as ID and movieID as value                                
    def updateDictOfDirectors(self, movieObject):
        director = movieObject['director']
        if director not in self.dictDirector:
            self.dictDirector[director] = set()
        self.dictDirector[director].add(self.returnMovieID(movieObject))
        
    #method that checks if ID of dict contains actors: if not, create one dict with actor as ID and set of movieIDs as value    
    def updateDictOfActors(self, movieObject):
        listOfActors = movieObject['actors']
        for actor in listOfActors:
            if actor not in self.dictActor:
                self.dictActor[actor] = set()
            self.dictActor[actor].add(self.returnMovieID(movieObject))
        
    #method that checks if ID of dict contains genres: if not, create one dict with genre as ID and set of movieIDs as value        
    def updateDictOfGeneres(self, movieObject):
        genre = movieObject['genre']
        if genre not in self.dictGenre:
            self.dictGenre[genre] = set()  
        self.dictGenre[genre].add(self.returnMovieID(movieObject))

    def parseMoviesObjects(self, filename,  parse = True):
        start_time = time.time()
        if parse:
            json_data =  open(filename, 'r').read() 
            jsonData = json.loads(json_data) 
                                  
            for movieObject in jsonData: 
                self.updateDictOfDirectors(movieObject)
                self.updateDictOfActors(movieObject)
                self.updateDictOfGeneres(movieObject)
            print("Parsed movies.json in %f seconds" % (time.time() - start_time))
            s = pickle.dumps(self)
            with open(MOVIES_PICKLE_FILE, 'w') as f:
                f.write(s)
        else:
            with open(MOVIES_PICKLE_FILE, 'r') as f:
                s = f.read()
                mov = pickle.loads(s)
                self.dictActor = mov.dictActor
                self.dictDirector = mov.dictDirector
                self.dictGenre = mov.dictDirector
            print("Loaded pickled movies model in %f seconds" % (time.time() - start_time))
        return self


#main function to parse a json file of movies:
def main(moviesJson):  
    mov = MoviesParser()
    mov.parseMoviesObjects(moviesJson, parse = True)
    print(len(mov.dictActor))
    print(len(mov.dictDirector))
    print(len(mov.dictGenre))

if __name__ == "__main__":
    moviesJson = 'json/movies.json'
    main(moviesJson)
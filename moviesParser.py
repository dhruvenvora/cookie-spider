import json

class Movies:
    dictDirector = {}
    dictActor = {}
    dictGenre = {}
    def __init__(self):
        self.movieID = 0
    
    def returnMovieID(self, objFromJson):                
         self.movieID = objFromJson['movie_id'] 
         return self.movieID                           

    #method that checks if ID of dict contains directors: if not, create one dict with dir as ID and movieID as value                                
    def dictOfDirectors(self, objFromJson, movieID, dictDirector):
        director = objFromJson['director']       
        if director not in self.dictDirector.keys():
            self.dictDirector[director] = set()
        self.dictDirector[director].add(self.movieID)    
        
    #method that checks if ID of dict contains actors: if not, create one dict with actor as ID and set of movieIDs as value    
    def dictOfActors(self, objFromJson, movieID, dictActor):
        listOfActors = objFromJson['actors']        
        for actor in listOfActors:       
            if actor not in self.dictActor.keys():
                self.dictActor[actor] = set() 
            self.dictActor[actor].add(self.movieID)    
        
    #method that checks if ID of dict contains genres: if not, create one dict with genre as ID and set of movieIDs as value        
    def dictOfGeneres(self, objFromJson, movieID, dictGenre):      
        genre = objFromJson['genre']     
        if genre not in self.dictGenre.keys():
            self.dictGenre[genre] = set()  
        self.dictGenre[genre].add(self.movieID)   
        

#main function to parse a json file of movies:                
def main(moviesJson):  
    json_data =  open(moviesJson, 'r').read() 
    jsonData = json.loads(json_data) 
    
    mov = Movies()
                  
    for movieObject in jsonData: 
        mov.dictOfDirectors(movieObject, mov.returnMovieID, mov.dictDirector)
        mov.dictOfActors(movieObject, mov.returnMovieID, mov.dictActor)
        mov.dictOfGeneres(movieObject, mov.returnMovieID, mov.dictGenre)
                        
if __name__ == "__main__":
    moviesJson = 'movies.json'
    main(moviesJson)
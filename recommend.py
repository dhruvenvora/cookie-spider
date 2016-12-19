import itertools
import numpy as np
from functools import reduce
import heapq

class PotentialMovie:
    
    def __init__(self, movie, score):
        self.movie = movie
        self.score = score
        
    def __cmp__(self, other):
        return cmp(self.score, other.score) 

class Recommender:
    
    graph = None

    def __init__(self, graph):
        self.graph = graph

    def recommend(self, likesModel, moviesModel, user):
        self.likesModel = likesModel
        self.moviesModel = moviesModel
        self.user = user
        
        (watchedMovies, likedMovies) = likesModel[user]
        
        allDirs = self.graph.UD[user]
        allActs = self.graph.UA[user]
        allGens = self.graph.UG[user]
        
        #go by actors
        favAct = allActs.argsort()[-30:][::-1]
        favDir = allDirs.argsort()[-30:][::-1]
        favGen = allGens.argsort()[-30:][::-1]
        
        self.findRecommendedMovies(favDir, favAct, favGen, watchedMovies)  
        
        #while i in range(MAX_LEVEL):
        #    favs = graph.getKHighestAffinityValues(favs)
            
    def findRecommendedMovies(self, favDirs, favActs, favGens, watchedMovies):
        
        movies = []
        count = 0
        
        #level one
        for i in itertools.product(favDirs, favActs, favGens):
            
            score = 0
            score += self.graph.DA[i[0]][i[1]]
            score += self.graph.DG[i[0]][i[2]]
            score += self.graph.AG[i[1]][i[2]]
            
            dMovies = list(self.moviesModel.dictDirector[i[0]])
            aMovies = list(self.moviesModel.dictActor[i[1]])
            gMovies = list(self.moviesModel.dictGenre[i[2]])
            
            potentialMovies = np.intersect1d(dMovies, aMovies)
            
            potentialMovies = set(np.setdiff1d(potentialMovies, watchedMovies))
            
            for i in potentialMovies:
                if(count > 20):
                    heapq.heappushpop(movies, PotentialMovie(i, score))
                else:
                    heapq.heappush(movies, PotentialMovie(i, score))
                    count += 1
                    
        for obj in movies:
            print obj.movie
                
            
            
            
            
            
            
            
                

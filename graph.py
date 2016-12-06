import numpy as np
from scipy.sparse import csr_matrix

class Graph:
    
    def __init__(self, usersCount, actorsCount, directorsCount, genreCount):
        #Storing weights as matrix
        self.usersCount = usersCount
        self.actorsCount = actorsCount
        self.directorsCount = directorsCount
        self.genreCount = genreCount
        self.UD = np.ndarray((usersCount, directorsCount))
        # self.UD.fill(0)
        self.UG = np.ndarray((usersCount, genreCount))
        self.UA = np.ndarray((usersCount, actorsCount))
        self.DA = np.ndarray((directorsCount, actorsCount))
        self.DG = np.ndarray((directorsCount, genreCount))
        self.AG = np.ndarray((actorsCount, genreCount))
        self.DD = np.ndarray((directorsCount, directorsCount))
        self.GG = np.ndarray((genreCount, genreCount))
        self.AA = np.ndarray((usersCount, actorsCount))
        
           
    """
    all lists are represented as sets
    
    dirMap = {dir -> list of movies}
    actorMap = similar
    genreMap = similar
    
    likesMap = {user -> ([all movies], [liked movies])}
    
    """
    def calculateUserAffinity(self, dirMap, actorMap, genreMap, likesMap):
        for user_id, ratedMovies in likesMap.items():
            
            for dir_id, movies in dirMap.items():
                dirLike = len(movies.intersection(ratedMovies[1])) / float(len(movies.intersection(ratedMovies[0]))+1)
                print("%s:%s  = %f" %(user_id, dir_id, dirLike))
                print(self.UD)
                self.UD[user_id][dir_id] = dirLike
                
            for act_id, movies in actorMap.items():
                actLike = len(movies.intersection(ratedMovies[1])) / (len(movies.intersection(ratedMovies[0]))+1)
                self.UA[user_id][act_id] = actLike
                
            for genre_id, movies in genreMap.items():
                genreLike = len(movies.intersection(ratedMovies[1])) / (len(movies.intersection(ratedMovies[0]))+1)
                self.UA[user_id][genre_id] = genreLike
    
    """
    Calculate affinity between DxA, DxG and AxG
    """
    def calculateAffinityBetweenEntities(self):
        
        # affinity between directors and actors
        self.DA = numpy.dot(self.UD.T, self.UA)
        
        # affinity between directors and genre
        self.DG = numpy.dot(self.UD.T, self.UG)
        
        # affinity between actors and genre 
        self.AG = numpy.dot(self.UA.T, self.UG)
        
    """
    Calculate affinity between DxD, AxA and GxG
    """    
    def calculateSelfAffinity(self):
        
        # affinity between directors
        self.DD = numpy.dot(numpy.dot(self.DA, self.AG), self.DG.T)
        
        # affinity between actors
        self.AA = numpy.dot(numpy.dot(self.AG, self.DG.T), self.DA)
        
        # affinity between genres
        self.GG = numpy.dot(numpy.dot(self.DG.T, self.DA), self.AG)
        
    

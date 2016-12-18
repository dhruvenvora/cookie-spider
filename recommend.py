import itertools

class Recommender:

    def __init__(self):
        pass

    def recommend(self, graph, likesModel, moviesModel, user):
        (watchedMovies, likedMovies) = likesModel[user]
        
        print likedMovies
        
        """
        favDirs = []
        favActs = []
        favGens = []
        
        recommendedMovies = heap(10)
        
        for movie in likedMovies:
            movieDetails = moviesModel.movieMap[movie]
            favDirs.append(movieDetails.directors)
            favActs.append(movieDetails.actors)
            favGens.append(movieDetails.genres)
            
        favs = [favDirs, favActs, favGens]  
        
        findAllCombinations(favDirs, favActs, favGens)  
        """
        #while i in range(MAX_LEVEL):
        #    favs = graph.getKHighestAffinityValues(favs)
            
    def findAllCombinations(favDirs, favActs, favGens):
        for i in itertools.product(favDirs, favActs, favGens):
            print i
            
            
                

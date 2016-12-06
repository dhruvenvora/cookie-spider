
class Recommender:

    def __init__(self):
        pass

    def recommend(self, graph, likesModel, moviesModel, user):
        (watchedMovies, likedMovies) = likesModel[user]
        
        for movie in likedMovies:
            movieDetails = moviesModel.movieMap[movie]
            directors = movieDetails.directors
            actors = movieDetails.actors
            genres = movieDetails.genres

            md = []
            ad = []
            gd = []

            for d in directors:
                md = h_dfs(d)
            for a in actors:
                ad = h_dfs(a)
            for g in genres:
                gd = h_dfs(g)

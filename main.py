from likes_parser import LikesParser
from moviesParser import Movies
from graph import Graph

def main(likesJson, moviesJson):
    likesParser = LikesParser(likeThreshold=3) #out of 5
    likesMap = likesParser.getUserDict(likesJson, build = False, count = None)
    
    moviesParser = Movies()
    moviesParser.parseMoviesObjects(moviesJson, parse = False)

    userCount = len(likesMap)
    actorsCount = len(moviesParser.dictActor)
    directorsCount = len(moviesParser.dictDirector)
    genreCount = len(moviesParser.dictGenre)

    graph = Graph(userCount, actorsCount, directorsCount, genreCount)
    graph.calculateUserAffinity(moviesParser.dictDirector, moviesParser.dictActor, moviesParser.dictGenre, likesMap)



if __name__ == "__main__":
    main('json/likes.json', 'json/movies.json')
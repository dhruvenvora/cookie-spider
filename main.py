from likes_parser import LikesParser
from moviesParser import MoviesParser
from graph import Graph
from entity_index import ChannelIndex, Channels
from recommend import Recommender, PotentialMovie

def creatingTrainingData(likesMap):
    #print likesMap
    print "Exit"


moviesParser = None
likesMap = None

def main(likesJson, moviesJson):
    global moviesParser
    global likesMap
    channelIndex = ChannelIndex(Channels.CHANNELS)
    likesParser = LikesParser(channelIndex, likeThreshold=3) #out of 5
    likesMap = likesParser.getUserDict(likesJson, build = True, count = None)
    
    creatingTrainingData(likesMap)
    
    moviesParser = MoviesParser(channelIndex)
    moviesParser.parseMoviesObjects(moviesJson, parse = True)

    userCount = len(likesMap)
    actorsCount = len(moviesParser.dictActor)
    directorsCount = len(moviesParser.dictDirector)
    genreCount = len(moviesParser.dictGenre)
    print("%d,%d,%d,%d" % (userCount, actorsCount, directorsCount, genreCount))
    graph = Graph(userCount, actorsCount, directorsCount, genreCount)
    graph.calculateUserAffinity(moviesParser.dictDirector, moviesParser.dictActor, moviesParser.dictGenre, likesMap)
    graph.calculateAffinityBetweenEntities()
    graph.calculateSelfAffinity()

    reco = Recommender(graph)
    movies = reco.recommend(likesParser.model, moviesParser, 0)
    print(movies)
    print("Recommendations: ")
    for m in movies:
        movieObj = moviesParser.movies[m.movie]
        movieName = movieObj['name']
        print(movieName)

if __name__ == "__main__":
    main('json/test/likes.json', 'json/test/movies.json')
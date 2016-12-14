from likes_parser import LikesParser
from moviesParser import MoviesParser
from graph import Graph
from entity_index import ChannelIndex, Channels

def creatingTrainingData(likesMap):
    #print likesMap
    print "Exit"



def main(likesJson, moviesJson):
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
    
    print "Calculating user affinities"
    graph.calculateUserAffinity(moviesParser.dictDirector, moviesParser.dictActor, moviesParser.dictGenre, likesMap)
    
    print "Calculating affinites between entities"
    graph.calculateAffinityBetweenEntities()
    
    print "Calculating self affinity"
    graph.calculateSelfAffinity()



if __name__ == "__main__":
    main('json/likes.json', 'json/movies.json')

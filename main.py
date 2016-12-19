from likes_parser import LikesParser
from moviesParser import MoviesParser
from graph import Graph
from entity_index import ChannelIndex, Channels
import gc
from recommend import Recommender

def main(likesJson, moviesJson, fromFile):
    channelIndex = ChannelIndex(Channels.CHANNELS)
    likesParser = LikesParser(channelIndex, likeThreshold=3) #out of 5
    likesMap = likesParser.getUserDict(likesJson, build = True, count = None)
        
    moviesParser = MoviesParser(channelIndex)
    moviesParser.parseMoviesObjects(moviesJson, parse = True)

    userCount = len(likesMap)
    actorsCount = len(moviesParser.dictActor)
    directorsCount = len(moviesParser.dictDirector)
    genreCount = len(moviesParser.dictGenre)
    print("%d,%d,%d,%d" % (userCount, actorsCount, directorsCount, genreCount))
    graph = Graph(userCount, actorsCount, directorsCount, genreCount)
    
    if fromFile:
        graph.UG = graph.readFile("model/ug.h5")
        graph.UA = graph.readFile("model/ua.h5")
        graph.UD = graph.readFile("model/ud.h5")
        graph.DA = graph.readFile("model/da.h5")
        graph.DG = graph.readFile("model/dg.h5")
        graph.AG = graph.readFile("model/ag.h5")
        graph.DD = graph.readFile("model/dd.h5")
        graph.AA = graph.readFile("model/aa.h5")
        graph.GG = graph.readFile("model/gg.h5")
        
    else:
        print "Calculating user affinities"
        graph.calculateUserAffinity(moviesParser.dictDirector, moviesParser.dictActor, moviesParser.dictGenre, likesMap)
        
        print "Calculating affinites between entities"
        graph.calculateAffinityBetweenEntities()
        
        gc.collect()
        
        print "Calculating self affinity"
        graph.calculateSelfAffinity()
    
    rec = Recommender(graph)
    
    rec.recommend(likesMap, moviesParser, userCount-1)


if __name__ == "__main__":
    main('json/likes.json', 'json/movies.json', False)

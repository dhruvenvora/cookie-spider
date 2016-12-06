from likes_parser import LikesParser
from moviesParser import MoviesParser
from graph import Graph
from entity_index import EntityIndex

def creatingTrainingData(likesMap):
    #print likesMap
    print "Exit"



def main(likesJson, moviesJson):
    entityIndex = EntityIndex()
    likesParser = LikesParser(entityIndex, likeThreshold=3) #out of 5
    likesMap = likesParser.getUserDict(likesJson, build = True, count = None)
    
    creatingTrainingData(likesMap)
    
    moviesParser = MoviesParser(entityIndex)
    moviesParser.parseMoviesObjects(moviesJson, parse = True)

    userCount = len(likesMap)
    actorsCount = len(moviesParser.dictActor)
    directorsCount = len(moviesParser.dictDirector)
    genreCount = len(moviesParser.dictGenre)
    print("%d,%d,%d,%d" % (userCount, actorsCount, directorsCount, genreCount))
    graph = Graph(userCount, actorsCount, directorsCount, genreCount)
    graph.calculateUserAffinity(moviesParser.dictDirector, moviesParser.dictActor, moviesParser.dictGenre, likesMap)



if __name__ == "__main__":
    main('json/likes.json', 'json/movies.json')
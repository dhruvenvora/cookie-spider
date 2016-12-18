import pickle
from likes_parser import LikesParser
from moviesParser import MoviesParser
from graph import Graph
from entity_index import ChannelIndex, Channels

def main(likesJson, moviesJson):

    with open('test_data.model') as f:
         s = f.read()
         modelDict = pickle.loads(s)

    # modelDict
    # {'moviesParser': <moviesParser.MoviesParser instance at 0x7f56b0fbaa28>, 'likesParser': <likes_parser.LikesParser instance at 0x7f56abe03a70>}

    moviesParser = modelDict['moviesParser']
    likesParser = modelDict['likesParser']

    likesMap = likesParser._model
    watched = likesMap[likesMap.keys()[0]][0]
    userCount = len(likesMap)
    actorsCount = len(moviesParser.dictActor)
    directorsCount = len(moviesParser.dictDirector)
    genreCount = len(moviesParser.dictGenre)
    print("movies:%d" % len(watched))
    print("users:%d, actors:%d, dirs:%d, genres:%d" % (userCount, actorsCount, directorsCount, genreCount))
    graph = Graph(userCount, actorsCount, directorsCount, genreCount)
    graph.calculateUserAffinity(moviesParser.dictDirector, moviesParser.dictActor, moviesParser.dictGenre, likesMap)



if __name__ == "__main__":
    main('json/likes.json', 'json/movies.json')


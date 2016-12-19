from likes_parser import LikesParser
from moviesParser import MoviesParser
from graph import Graph
from entity_index import ChannelIndex, Channels
WATCH_THRESHOLD = 200

def main(likesJson, moviesJson):
    channelIndex = ChannelIndex(Channels.CHANNELS)
    likesParser = LikesParser(channelIndex, likeThreshold=3) #out of 5
    likesMap = likesParser.getUserDict(likesJson, build = True, count = None)
    
    moviesParser = MoviesParser(channelIndex)
    moviesParser.parseMoviesObjects(moviesJson, parse = True)

    # find user with most likes
    # find movies liked by the user - create new likesParser with single user
    # create moviesParser: 
    # collect directors, actors and genre - update moviesParser
    # pickle the parsers
    histo = dict([(user, len(mTuple[0])) for (user, mTuple) in likesMap.items()])
    from operator import itemgetter
    sortedHisto = sorted(histo.items(), key=itemgetter(1))
    sortedHisto.reverse()
    selectedUsers = None
    idx = 0
    userCount = 3
    while(True and idx < len(sortedHisto)):
        (selectedUser, count) = sortedHisto[idx]
        if count <= WATCH_THRESHOLD:
            break
        idx += 1


    watched = likesMap[selectedUser][0]

    newLikesParser = LikesParser(channelIndex, likeThreshold=3) #out of 5
    newLikesParser._likeThreshold = likesParser._likeThreshold
    newLikesParser._model = {selectedUser: likesMap[selectedUser]} # userID: ([watched movieID], [liked movieID])
    newLikesParser._userMoviesDict = {selectedUser: likesParser._userMoviesDict[selectedUser]} # userID: [movieObject]
    newLikesParser._indexProvider = likesParser._indexProvider

    newMoviesParser = MoviesParser(channelIndex)
    newMoviesParser.dictDirector = {} # {director : [movieID]}
    newMoviesParser.dictActor = {} # {actor : [movieID]}
    newMoviesParser.dictGenre = {} # {genre : [movieID]}
    newMoviesParser.movies = {} # movieID: movieObject
    newMoviesParser._indexProvider = moviesParser._indexProvider

    watched = newLikesParser._model[selectedUser][0]
    for m in watched:
        if m in moviesParser.movies:
            print m
            mObj = moviesParser.movies[m]
            print(mObj)
            newMoviesParser.movies[m] = mObj
            
            g = mObj['genre']
            if g not in newMoviesParser.dictGenre:
                newMoviesParser.dictGenre[g] = set()
            newMoviesParser.dictGenre[g].add(m)

            d = mObj['director']
            if d not in newMoviesParser.dictDirector:
                newMoviesParser.dictDirector[d] = set()
            newMoviesParser.dictDirector[d].add(m)

            for a in mObj['actors']:
                if a not in newMoviesParser.dictActor:
                    newMoviesParser.dictActor[a] = set()
                newMoviesParser.dictActor[a].add(m)

    print("Selected User: %s" % str(selectedUser))

    # picle test models
    import pickle
    with open('test_data.model', 'w') as f:
        s = pickle.dumps({'likesParser': newLikesParser, 'moviesParser': newMoviesParser})
        f.write(s)


if __name__ == "__main__":
    main('json/likes.json', 'json/movies.json')
'''
1. likesParser.userMoviesDict.keys()
2. testUsers = select 20% randomly
3. testUserLikes = extract 20% likes for each user in testUsers
4. Create graph
5. Invoke recommend for testUsers
6. Intersect recommends with testUserLikes for each user.
7. accuracy the no of users that had one or more hits
'''

from likes_parser import LikesParser
from moviesParser import MoviesParser
from graph import Graph
from entity_index import ChannelIndex, Channels
from recommend import Recommender, PotentialMovie
import numpy as np

moviesParser = None
likesMap = None

def partitionTrainTest(likesMap):

    count = len(likesMap)
    trainCount = int(0.8 * count)
    indices = np.random.permutation(count)

    training_idx, test_idx = indices[:trainCount], indices[trainCount:]
    
    users = likesMap.keys()
    testLikesMap = {}
    for idx in test_idx:
        # select user by random index
        testUser = users[idx]

        # extract user's watched and liked movies
        (watched, liked) = likesMap[testUser]
        watched = watched.copy()
        # generate random indices from liked movies
        likedCount = len(liked)
        likedSubCount = int(0.8 * likedCount)
        likedIndices = np.random.permutation(likedCount)
        training_liked_idx, test_liked_idx = likedIndices[:likedSubCount], likedIndices[likedSubCount:]

        print(liked, training_liked_idx)
        # extract training data from liked movies
        training_liked = np.take(list(liked), training_liked_idx)
        
        print(liked, test_liked_idx)
        # extract test data from liked movies
        test_liked = np.take(list(liked), test_liked_idx)
        
        # remove test data liked movies from watched movies
        print(test_liked)
        for m in test_liked:
            watched.remove(m)

        # update the user in the likesMap
        likesMap[testUser] = (watched, set(training_liked))
        testLikesMap[testUser] = test_liked

    return (likesMap, testLikesMap)

def createParsers(likesJson, moviesJson):
    global moviesParser
    global likesMap
    channelIndex = ChannelIndex(Channels.CHANNELS)
    likesParser = LikesParser(channelIndex, likeThreshold=3) #out of 5
    likesMap = likesParser.getUserDict(likesJson, build = True, count = None)
    moviesParser = MoviesParser(channelIndex)
    moviesParser.parseMoviesObjects(moviesJson, parse = True)

    # partition 80-20
    # testLikesMap : keys are the users selected as test users, values are the  liked movies removed from the test users' likes 
    (trainLikesMap, testLikesMap) = partitionTrainTest(likesMap)

    return (moviesParser, likesParser, trainLikesMap, testLikesMap)

def createGraph(moviesParser, trainLikesMap):
    userCount = len(trainLikesMap)
    actorsCount = len(moviesParser.dictActor)
    directorsCount = len(moviesParser.dictDirector)
    genreCount = len(moviesParser.dictGenre)
    print("%d,%d,%d,%d" % (userCount, actorsCount, directorsCount, genreCount))
    
    # create graph from training data
    graph = Graph(userCount, actorsCount, directorsCount, genreCount)
    graph.calculateUserAffinity(moviesParser.dictDirector, moviesParser.dictActor, moviesParser.dictGenre, trainLikesMap)
    graph.calculateAffinityBetweenEntities()
    graph.calculateSelfAffinity()
    return graph

def createRecommendations(likesParser, recommender, users):
    ret = {}
    for user in users:
        movies = recommender.recommend(likesParser.model, moviesParser, user)
        ret[user] = movies
    return ret

def main(likesJson, moviesJson):
    (moviesParser, likesParser, trainLikesMap, testLikesMap) = createParsers(likesJson, moviesJson)
    # print(trainLikesMap)
    # print(testLikesMap)
    graph = createGraph(moviesParser, trainLikesMap)

    # Generate recommendations for testLikesMap
    # Count if recommended movies match any of the movies in value testLikesMap
    reco = Recommender(graph)
    movies = reco.recommend(likesParser.model, moviesParser, 0)
    # print(movies)
    # print("Recommendations: ")
    # for m in movies:
    #     movieObj = moviesParser.movies[m.movie]
    #     movieName = movieObj['name']
    #     print(movieName)

    recoMap = createRecommendations(likesParser, reco, testLikesMap.keys())
    # print(recoMap)
    likesMap = likesParser.model
    accuracy = 0
    for user, movies in recoMap.items():
        (watched, liked) = likesMap[user]
        hits = liked.intersection(set(movies))
        if len(hits) > 0:
            accuracy += 1

    accuracy = accuracy / float(len(recoMap))
    print(accuracy)


if __name__ == "__main__":
    main('json/test/likes.json', 'json/test/movies.json')    
    main('json/likes.json', 'json/movies.json')
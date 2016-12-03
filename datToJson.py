import numpy as np
import csv
import json


#
class Movie(object):
    ID = ""
    age = 0
    major = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, ID, age, major):
        self.ID = ID
        self.age = age
        self.major = major

def make_student(ID, age, major):
    movie = Movie(ID, age, major)
    return movie



#this function returns the 
def read_data(filename):
    newLines = []
    with open(filename, 'r') as input_file: 
            heading = input_file.readline().split("\t")
            for line in input_file.readlines()[0:]:
                read_data = line.split("\t")
                newLines.append(read_data)
    header = np.asarray(heading, dtype=np.str_)            
    dataNumpy =  np.asarray(newLines, dtype=np.str_)  
    return header, dataNumpy
    
    
def dataFromFiles(heading_mov, dataNumpy_mov, heading_act, dataNumpy_act, heading_dir, dataNumpy_dir, heading_gen, dataNumpy_gen, heading_rat, dataNumpy_rat): 
    #create a JSON file of likes(user, movie):        
    with open('likes.json', 'w') as outfile:
        userID_r = dataNumpy_rat[:,0].tolist()
        movieID_r = dataNumpy_rat[:,1].tolist()
        rating_r = dataNumpy_rat[:,2].tolist()
        for i in range(len(userID_r)):
            data = {heading_rat[0]: userID_r[i], heading_rat[1]: movieID_r[i], heading_rat[2]: rating_r[i]}
            json.dump(data, outfile)

    #create a JSON file of likes(user, movie):        
    with open('movies.json', 'w') as outfile:
        userID_r = dataNumpy_rat[:,0].tolist()
        movieID_r = dataNumpy_rat[:,1].tolist()
        rating_r = dataNumpy_rat[:,2].tolist()
        for i in range(len(userID_r)):
            if(movieID_r[i]):
                data = {"Movie":{heading_rat[1]: movieID_r[i]}}
                json.dump(data, outfile)        
      
        
#if ID is in the numpy array then write the row to the file  
                        
#function to write the entire data to a csv file
def writeDataToCSV(csvFile, data):
    csvReviewFile = open(csvFile, 'a+')
    csvFileWriter = csv.writer(csvReviewFile)
    csvFileWriter.writerow(data)
    print "bye"    
       
#aList = [1,2,3]        
#writeDataToCSV("data.csv", aList)
                                                              
    
########################################################################################################    
    
if __name__=="__main__":
    print "Reading the data...\n"
    head_mov, data_mov = read_data('hetrecMovielens/movies.dat')
    head_act, data_act = read_data('hetrecMovielens/movie_actors.dat')
    head_dir, data_dir = read_data('hetrecMovielens/movie_directors.dat')
    head_gen, data_gen = read_data('hetrecMovielens/movie_genres.dat')
    head_rat, data_rat = read_data('hetrecMovielens/user_ratedmovies.dat')
    
    dataFromFiles(head_mov, data_mov, head_act, data_act, head_dir, data_dir, head_gen, data_gen, head_rat, data_rat)
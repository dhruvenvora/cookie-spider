class Graph:
    
    __init__(self):
        #Storing weights as matrix
        self.usersCount = 0
        self.actorsCount = 0
        self.directorsCount = 0
        self.genreCount = 0
        self.affinity_AD = []
        self.affinity_GD = []
        self.affinity_AG = []
        
    _add_count(self, usersCount, actorsCount, directorsCount, genreCount):
        self.usersCount = usersCount
        self.actorsCount = actorsCount
        self.directorsCount = directorsCount
        self.genreCount = genreCount
        
    _add_matrix(self, movies) 
    
    _calculate_affinity_between_AD(self):
        
        
    _calculate_affinity_between_GD(self):
        
        
    _calculate_affinity_between_AG(self):
        

    _train(self):
        

import json
import pickle

MAX_COUNT = 1000000

class PositionWeightMatrix:

    def __init__(self):
        self._pwmFreqs = {}
        self._pwm = {}
        # self._indices = {}
        self._newIndex = 0

    def addFactRelation(self, e1, e2, weight=None, increment=False):
        if e1 not in self._pwmFreqs:
            self._pwmFreqs[e1] = {}
        dim1 = self._pwmFreqs[e1]

        if e2 not in dim1:
            dim1[e2] = 0

        if not weight:
            dim1[e2] = dim1[e2] + 1
        else:
            val = dim1[e2]
            if increment:
                val += weight
            else:
                val = weight
            dim1[e2] = val

    def addDBObj(self, fObj, parser):
            (fromEntity, toEntity, weight) = parser(fObj)
            self.addFactRelation(fromEntity, toEntity, weight)
            

    def addDBObjArr(self, fObjArr, parser):
        global MAX_COUNT
        for fObj in fObjArr:
            self.addDBObj(fObj, parser)
            MAX_COUNT -= 1
            if not MAX_COUNT:
                break

    def parseLike(self, fObj):
        fromObj = fObj['userID']
        toObj = fObj['movieID']
        weight = float(fObj['rating'])
        return (fromObj, toObj, weight)

    def finalizePWM(self):
        for dim1, dim2Dict in self._pwmFreqs.items():
            sumWt = 0
            for dim2,wt in dim2Dict.items():
                sumWt += wt
            for dim2,wt in dim2Dict.items():
                newWt = wt / float(sumWt)
                if dim1 not in self._pwm:
                    self._pwm[dim1] = {}
                self._pwm[dim1][dim2] = newWt
            
        for dim1, dim2Dict in self._pwm.items():
            sumWt = 0
            for dim2,wt in dim2Dict.items():
                sumWt += wt
            print("DIM-%s : %f" % (dim1, sumWt))

def main(jsonFiles):
    pwm = PositionWeightMatrix()
    for fname in jsonFiles:
        with open(fname, 'r') as f:
            fObjArr = json.loads(f.read())
            pwm.addDBObjArr(fObjArr, pwm.parseLike)
    print(len(pwm._pwmFreqs))
    pwm.finalizePWM()
    
    s = pickle.dumps(pwm)
    with open('model', 'w') as f:
        f.write(s)

    return pwm

if __name__ == "__main__":
    jsonFiles = ['likes.json']
    main(jsonFiles)

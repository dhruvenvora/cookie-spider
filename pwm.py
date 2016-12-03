import json
import pickle

MAX_COUNT = 1000000

class PositionWeightMatrix:

    def __init__(self):
        self._pwm = {}
        # self._indices = {}
        self._newIndex = 0

    def addFactRelation(self, e1, e2, weight=None, increment=False):
        if e1 not in self._pwm:
            self._pwm[e1] = {}
        dim1 = self._pwm[e1]

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
        weight = fObj['rating']
        return (fromObj, toObj, weight)

def main(jsonFiles):
    pwm = PositionWeightMatrix()
    for fname in jsonFiles:
        with open(fname, 'r') as f:
            fObjArr = json.loads(f.read())
            pwm.addDBObjArr(fObjArr, pwm.parseLike)
    print(len(pwm._pwm))
    
    s = pickle.dumps(pwm)
    with open('model', 'w') as f:
        f.write(s)

    return pwm

if __name__ == "__main__":
    jsonFiles = ['likes.json']
    main(jsonFiles)

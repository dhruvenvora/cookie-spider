
class EntityIndex:

    def __init__(self):
        self._index = {}
        self._indexCounter = 0
        self._reverseIndex = {}

    def getEntityIndex(self, name):
        entityIndex = None
        if name:
            if name not in self._index:
                entityIndex = self._indexCounter
                self._indexCounter += 1
                self._index[name] = entityIndex
                self._reverseIndex[entityIndex] = name
            else:
                entityIndex = self._index[name]
        return entityIndex

    def getEntityByIndex(self, entityIndex):
        ret = None
        if entityIndex in self._reverseIndex:
            ret = self._reverseIndex[entityIndex]
        return ret
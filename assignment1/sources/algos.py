from abc import ABC, abstractmethod
from typing import List

# Interface Algorithme
class IAlgo(ABC) :
    @abstractmethod
    def solve(self, buildings: List[List[int]]) -> List[List[int]] :
        pass

# Algorithme naif
class NaiveAlgo(IAlgo) :
    def solve(self, buildings: List[List[int]]) -> List[List[int]] :
        # TODO : Ajouter algorithme naif
        return []

# Interface Algorithme Diviser pour Regner (Divide and Conquer)
class IDCAlgo(IAlgo) :
    def __init__(self, threshold: int) -> None: 
        self._threshold = threshold
    
    @property
    def threshold(self) -> int :
        return self._threshold
        
    @threshold.setter
    def threshold(self, threshold: int) -> None :
        self._threshold = threshold
        
    @abstractmethod
    def conquer(self, buildings: List[List[int]]) -> List[List[int]] :
        pass
     
    def merge(self, halves: List[List[List[int]]]) -> List[List[int]]:
        merge_lst = list()
        heights = [0]*2
        idxs = [0]*2
        sizes = len(halves[0]), len(halves[1])
        critical = None
        
        while idxs[0] != sizes[0] or idxs[1] != sizes[1]:
            # test pour determiner la moitie qui a le point critique d'abscisse minimum
            tst = idxs[1] != sizes[1] and \
                    (idxs[0] == sizes[0] or halves[0][idxs[0]][0] > halves[1][idxs[1]][0])
            
            # retirer le point critique
            critical = halves[tst][idxs[tst]]
            idxs[tst] += 1
            heights[tst] = critical[1]
            
            # surelever le point critique au maximum des hauteurs
            critical[1] = max(heights)
            
            # ajouter le point critique ou non selon qu'il est redondant
            if merge_lst and merge_lst[-1][0] == critical[0] :
                merge_lst.pop()
            if not merge_lst or merge_lst[-1][1] != critical[1] :
                merge_lst.append(critical)
        
        return merge_lst
    
    def solve(self, buildings: List[List[int]]) -> List[List[int]]:
        n = len(buildings)
        if n <= self._threshold :
            return self.conquer(buildings)
        else:
            halves = (self.solve(buildings[:(n+1)//2]), self.solve(buildings[(n+1)//2:]))
            return self.merge(halves)
            

# Algorithme Diviser pour Regner (Divide and Conquer)
class DCAlgo(IDCAlgo) :
    def __init__(self) -> None:
        super().__init__(1)

    def conquer(self, buildings: List[List[int]]) -> List[List[int]] :
        return [[buildings[0][0], buildings[0][2]], [buildings[0][1], 0]]

# Algorithme Diviser pour Regner avec Seuil (Divide and Conquer with Threshold)
class DCThresAlgo(IDCAlgo) :
    naive_algo = NaiveAlgo()
    def conquer(self, buildings: List[List[int]]) -> List[List[int]] :
        return self.naive_algo.solve(buildings)
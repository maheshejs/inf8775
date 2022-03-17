from abc import ABC, abstractmethod
from typing import List

# Interface for algorithm
class IAlgo(ABC) :
    @abstractmethod
    def solve(self, buildings: List[List[int]]) -> List[List[int]] :
        pass

# Naive algorithm
class NaiveAlgo(IAlgo) :
    def solve(self, buildings: List[List[int]]) -> List[List[int]] :
        # Naive algo
        solution = []
        critical_points = self.get_critical_points(buildings)
        # Loop through critical points
        for critical_point in critical_points :
            critical_x, critical_y = critical_point

            # Loop through buildings
            for building in buildings :
                x1, x2, height = building

                if critical_x < x1 :
                  break
                # Check to see if a point is contained in a building
                if critical_x < x2 :
                    # If the height is superior to the current height of 
                    # the critical point, update the critical_y
                    if height > critical_y : 
                        critical_y = height
            
            # If the solution is not empty, verify redundancy with last point of solution
            # Else, add the point to the solution
            if not solution or solution[-1][1] != critical_y : 
                solution.append([critical_x, critical_y])
        return solution
    
    def get_critical_points(self, buildings: List[List[int]]) -> List[List[int]] :
        critical_points = []
        # For each building, we mark its critical points
        for building in buildings : 
            x1, x2, height = building
            critical_points.append([x1, height])
            critical_points.append([x2, 0])
        return sorted(critical_points)

# Interface for Divide and Conquer algorithm
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
            # boolean which tells which half has the critical point of minimal abscissa
            tst = idxs[1] != sizes[1] and \
                    (idxs[0] == sizes[0] or halves[0][idxs[0]][0] > halves[1][idxs[1]][0])
            
            # remove critical point from the half given by the boolean tst
            critical = halves[tst][idxs[tst]]
            idxs[tst] += 1
            heights[tst] = critical[1]
            
            # update the critical point to the maximum of heights
            critical[1] = max(heights)
            
            # verify redundancy before adding the critical point to the solution
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
            

# Divide and Conquer algorithm
class DCAlgo(IDCAlgo) :
    def __init__(self) -> None:
        super().__init__(1)

    def conquer(self, buildings: List[List[int]]) -> List[List[int]] :
        return [[buildings[0][0], buildings[0][2]], [buildings[0][1], 0]]

# Divide and Conquer algorithm with threshold
class DCThresAlgo(IDCAlgo) :
    naive_algo = NaiveAlgo()
    def conquer(self, buildings: List[List[int]]) -> List[List[int]] :
        return self.naive_algo.solve(buildings)
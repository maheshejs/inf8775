from abc import ABC, abstractmethod
from typing import List
from collections import deque
import utils
import random
import copy

# Interface for algorithm
class IAlgo(ABC) :
    @abstractmethod
    def solve(self, buildings: List[List[int]]) -> List[List[int]] :
        pass

# Greedy algorithm
class GreedyAlgo(IAlgo):
    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        # Greedy choice : width * depth + height
        blocks.sort(key = lambda x : x[0] + x[1] * x[2], reverse = True)
        greedy_blocks = [blocks[0]]
        last_idx = 0
        idx = 1
        
        # Construct the greedy solution
        while idx < len(blocks):
            if blocks[last_idx][1] > blocks[idx][1] and blocks[last_idx][2] > blocks[idx][2] :
                greedy_blocks.append(blocks[idx])
                last_idx = idx
            idx += 1
        return greedy_blocks

# Dynamic programming algorithm
class DynProgAlgo(IAlgo):
    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        # Sort blocks by decreasing area (width * height)
        blocks.sort(key = lambda x : x[1] * x[2], reverse = True)
        heights, widths, depths = zip(*blocks)

        # Compute in table the value of an optimal solution
        #   in a bottom-up fashion and keep track with dependency (list)
        n = len(blocks)
        dependency = [-1]*n
        table = [0]*n
        j = 0
        while j < n:
            i = 0
            running_max = 0
            while i < j :
                if widths[i] > widths[j] and depths[i] > depths[j] :
                    if table[i] > running_max :
                        running_max = table[i]
                        dependency[j] = i
                i += 1
            table[j] = running_max + heights[j]
            j += 1

        # Reconstruct the optimal solution from computed information 
        #   in dependency and track of indices
        track = deque([max(range(n), key = table.__getitem__)])
        while dependency[track[0]] != -1:
            track.appendleft(dependency[track[0]])

        return [blocks[idx] for idx in track]


# Tabu search algorithm
class TabuAlgo(IAlgo):
    def __init__(self, max_iter: int) -> None: 
        self._max_iter = max_iter
    
    @property
    def max_iter(self) -> int :
        return self._max_iter
        
    @max_iter.setter
    def max_iter(self, max_iter: int) -> None :
        self._max_iter = max_iter


    def solve(self, blocks: List[List[int]]) -> List[List[int]] :
        # Compute the initial solution with greedy algorithm
        greedy_blocks = GreedyAlgo().solve(blocks)
        best_candidate = utils.Candidate(greedy_blocks, utils.compute_height(greedy_blocks))
        candidate = copy.deepcopy(best_candidate)
        
        # Different tabu lists with sizes 7 to 10
        # A tabu list is defined with a deque with a fixed size
        #   when the deque is full, the older block is popped and 
        #   is no longer tabu
        tabus = tuple(deque(maxlen = size) for size in range(7, 10+1))
        random.seed(0)

        count = self._max_iter

        while count :
            count -= 1
            neighbours = {*blocks} - {*candidate.blocks} - \
                         {block for tabu in tabus for blocks in tabu for block in blocks}

            # Find the best neighbour
            best_height = 0
            best_neighbour = ()
            for neighbour in neighbours :
                height = candidate.push(neighbour, update = False)
                if height > best_height :
                    best_height = height
                    best_neighbour = neighbour
            
            # If the set of neighbours is empty, pop older tabu blocks
            #   and continue the loop
            if not neighbours:
                for tabu in tabus :
                    tabu.popleft()
                pass

            # The best neighbour becomes the candidate solution
            candidate.push(best_neighbour, update = True)

            # If the candidate solution is better than the current best solution,
            #   the candidate becomes the current best solution and
            #   the counter is resetted
            if candidate.height > best_candidate.height :
                best_candidate = copy.deepcopy(candidate)
                count = self._max_iter
        
            # update tabu list with blocks removed in candidate
            random.choice(tabus).append(candidate.tabu)
        
        return best_candidate.blocks

from typing import List, Callable

def compute_height(blocks: List[List[int]]) -> int:
    if blocks :
        heights, *_ = zip(*blocks)
        return sum(heights)
    return 0

def bisect(lst: List[List[int]], value: List[int], key: Callable[[List[int]], int]) -> int:
    lo = 0
    hi = len(lst)
    while lo < hi:
        mid = (lo + hi) // 2
        if key(lst[mid]) > key(value):
            lo = mid + 1
        else:
            hi = mid
    return lo

class Candidate:
    def __init__(self, blocks: List[List[int]], height: int) -> None:
        self._blocks  = blocks
        self._height  = height
        self._tabu    = []

    @property
    def height(self) -> int :
        return self._height
    
    @property
    def blocks(self) -> List[List[int]] :
        return self._blocks
    
    @property
    def tabu(self) -> List[List[int]] :
        return self._tabu
    
    def push(self, block: List[int], update: bool) -> int:
        n = len(self._blocks)
        start = min([bisect(self._blocks, block,
                              key = lambda x: x[idx+1]) for idx in range(2)])
        end = start
        height = self._height + block[0]
        while end < n :
            if self._blocks[end][1] < block[1] and self._blocks[end][2] < block[2] :
                break
            height -= self._blocks[end][0]
            end += 1

        if update:
            self._tabu   = self._blocks[start:end]
            self._blocks = self._blocks[:start] + [block] + self._blocks[end:]
            self._height = height
  
        return height
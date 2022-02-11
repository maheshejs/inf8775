import time
import argparse
from algos import IAlgo, NaiveAlgo, DCAlgo, DCThresAlgo
from typing import List, Dict

class Skyline:
    def __init__(self, algo: IAlgo) -> None:
        self._algo = algo

    @property
    def algo(self) -> int :
        return self._algo

    @algo.setter
    def algo(self, algo: int) -> None :
        self._algo = algo
    
    def execute_algo(self, buildings: List[List[int]], options: Dict[str, bool]) -> None :
        start_time = time.perf_counter()
        solution = self._algo.solve(buildings)
        end_time = time.perf_counter()

        if options['print'] :
            for critical in solution :
                print(*critical)

        if options['time'] :
            elapsed_time_ms = (end_time - start_time) * 1000
            print(elapsed_time_ms)

if __name__ == "__main__" :
    # analyser arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", \
                        help="algorithm to use", \
                        dest="algo", \
                        action='store', required=True)
    parser.add_argument("-e", \
                        help="example file with buildings", \
                        dest="example_file", \
                        action='store', required=True, metavar = 'FILE_EXAMPLE')
    parser.add_argument("-t", \
                        help="prints elapsed time", \
                        dest="time", \
                        action='store_true')
    parser.add_argument("-p", \
                        help="print solution", \
                        dest="print", \
                        action='store_true')
    args = parser.parse_args()

    with open(args.example_file, 'r') as f :
        next(f)
        buildings = list()
        for line in f :
            buildings.append([int(x) for x in line.rstrip().split()])

    options = {'print': args.print, 'time': args.time}

    threshold = 20
    algo = {'brute':    NaiveAlgo(),
            'recursif': DCAlgo(),
            'seuil':    DCThresAlgo(threshold)}[args.algo]

    # resoudre probleme
    skyline = Skyline(algo)
    skyline.execute_algo(buildings, options)
/**
 ******************************************************************************
 * @file    main.cpp
 * @brief   Résolution d'une variante du problème QAP (Quadratic Assignment Problem)
 *          L'approche utilisée est une recherche taboue suivi d'une méthode d'escalade
 *          La recherche tabou utilisée est fortement basée de celui de David Gasquez
 *          Voir lien suivant : https://github.com/davidgasquez/qap 
 * @author  -
 ******************************************************************************
 */
#include "common.h"
#include "input.h"
#include "tabuSearch.h"
#include <cstdlib>

using namespace std;

int main(int argc, char *argv[])
{
  bool printSol;
  if (argc == 3)
  {
    printSol = atoi(argv[2]);
  }
  else
  {
    cerr << "ERROR: Invalid number of argurments" << endl;
    return -1;
  }

  // Read file
  Input input(argv[1]);
  if (!input.read())
  {
    cerr << "ERROR: Not file found";
    return -1;
  }

  // Tabu Search - neighbourhoodSize : 10000 - maxFails : 2500
  TabuSearch ts(input, printSol, 10000, 2500);

  return 0;
}
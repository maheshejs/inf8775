#ifndef INPUT_H__
#define INPUT_H__

#include "common.h"

class Input
{
public:
    Input(const string &filename);
    Input(int dimension, vector< vector<int> > distances, vector< vector<int> > flow);

    bool read();

    string getFilename() const;
    int getDimension() const;
    int getType() const;

    vector< vector<int> > getFlow() const;
    vector< int > getFrequencies() const;
    map< int, vector<int> > getAdjacency() const;



private:
    string filename_;
    int dimension_;
    int type_;
    vector< vector<int> > flow_;
    map< int, vector<int> > adjacency_;
    vector< int > frequencies_;
};

#endif
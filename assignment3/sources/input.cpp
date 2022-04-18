#include "input.h"

Input::Input(const string &filename)
    : filename_(filename), dimension_(0)
{

}

bool Input::read()
{
    ifstream data(filename_.c_str());

    if (!data)
    {
        cerr << "ERROR: Can not open input data file: " << filename_ << endl;
        return false;
    }

    // Obtain dimension
    data >> dimension_;
    
    // 
    int K, edges;
    data >> K >> edges;
    
    type_ = K;
    frequencies_.resize(type_);
    data >> frequencies_[0]; 
    for (int i = 1; i < K; ++i)
    {
      int a;
      data >> a;
      frequencies_[i] = a + frequencies_[i-1]; 
    }


    int energies[K][K] = {{0}};
    for (int i = 0; i < K; ++i)
      for (int j = 0; j < K; ++j)
        data >> energies[i][j];
    
    // Initialize flow matrix

    flow_.resize(dimension_);
    for (int i = 0; i < dimension_; ++i)
        flow_[i].resize(dimension_);

    //Fill flows
    int r = 0;
    for (int i = 0; i < dimension_; ++i)
    {
        if (i == frequencies_[r])
          r++;

        int s = 0;
        for (int j = 0; j < dimension_; ++j)
        {
            if (j == frequencies_[s])
              s++;
            flow_[i][j] = energies[r][s];
        }
    }

    // Fill adjacency list
    int a, b;
    while (data >> a >> b)
    {
        adjacency_[a].push_back(b);
        adjacency_[b].push_back(a);
    }

    return true;
}

int Input::getDimension() const
{
    return dimension_;
}

int Input::getType() const
{
    return type_;
}

vector< vector<int> > Input::getFlow() const
{
    return flow_;
}

vector< int > Input::getFrequencies() const
{
    return frequencies_;
}

map< int, vector<int> > Input::getAdjacency() const
{
    return adjacency_;
}
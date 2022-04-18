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
    int K, E;
    data >> K >> E;
    
    int frequencies[K] = {0};
    data >> frequencies[0]; 
    for (int i = 1; i < K; ++i)
    {
      int a;
      data >> a;
      frequencies[i] = a + frequencies[i-1]; 
    }

    int energies[K][K] = {{0}};
    for (int i = 0; i < K; ++i)
      for (int j = 0; j < K; ++j)
        data >> energies[i][j];
    
    // Initialize distance and flow matrix
    distances_.resize(dimension_);
    for (int i = 0; i < dimension_; ++i)
    {
        distances_[i].resize(dimension_);
    }

    flow_.resize(dimension_);
    for (int i = 0; i < dimension_; ++i)
    {
        flow_[i].resize(dimension_);
    }

    //Fill flows
    int r = 0;
    for (int i = 0; i < dimension_; ++i)
    {
        if (i == frequencies[r])
        {
          r++;
        }

        int s = 0;
        for (int j = 0; j < dimension_; ++j)
        {
            if (j == frequencies[s])
            {
              s++;
            }
            flow_[i][j] = energies[r][s];
        }
    }

    // Fill distances
    for (int i = 0; i < dimension_; i++)
    {
        for (int j = 0; j < dimension_; ++j)
        {
            distances_[i][j] = 0;
        }
    }

    int a, b;
    while (data >> a >> b)
    {
        adjacencies_[a].push_back(b);
        adjacencies_[b].push_back(a);
        distances_[a][b] = 1;
        distances_[b][a] = 1;
    }

    return true;
}

int Input::getDimension() const
{
    return dimension_;
}

vector< vector<int> > Input::getDistances() const
{
    return distances_;
}

vector< vector<int> > Input::getFlow() const
{
    return flow_;
}

map< int, vector<int> > Input::getAdjacencies() const
{
    return adjacencies_;
}
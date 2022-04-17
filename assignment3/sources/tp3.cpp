#include <iostream>

int main(int argc, char* argv[]) {

    // If more than 4 arguments are passed, return 
    if (argc > 4) {
        std::cerr << "Invalid number of arguments\n";
        return 1;
    }

    for(int i = 0; i < argc; i++) { 
        std::cout << argv[i] << std::endl;
    }
    return 0;
}
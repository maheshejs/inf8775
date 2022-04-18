#Makefile TP3 INF8775

all: folders
	g++ -o obj/input.o -c -Werror -std=c++0x -Ofast -Iincludes sources/input.cpp
	g++ -o obj/main.o -c -Werror -std=c++0x -Ofast -Iincludes sources/main.cpp
	g++ -o obj/tabuSearch.o -c -Werror -std=c++0x -Ofast -Iincludes sources/tabuSearch.cpp
	g++ -o bin/tp3 obj/input.o obj/main.o  obj/tabuSearch.o

folders:
	mkdir bin obj

clean:
	rm -rf bin obj

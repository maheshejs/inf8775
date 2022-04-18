#Makefile

all: folders
	g++ -o obj/input.o -c -Werror -std=c++0x -Ofast -Iinclude src/input.cc
	g++ -o obj/main.o -c -Werror -std=c++0x -Ofast -Iinclude src/main.cc
	g++ -o obj/ILS.o -c -Werror -std=c++0x -Ofast -Iinclude src/ILS.cc
	g++ -o obj/tabuSearch.o -c -Werror -std=c++0x -Ofast -Iinclude src/tabuSearch.cc
	g++ -o bin/qap_ils obj/input.o obj/ILS.o
	g++ -o bin/qap obj/input.o obj/main.o  obj/tabuSearch.o

folders:
	mkdir bin obj

clear:
	rm -rf bin obj

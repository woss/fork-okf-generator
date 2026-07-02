CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

all: calc_test

calc_test: calc.cpp calc.h
	$(CXX) $(CXXFLAGS) -c calc.cpp -o calc.o

clean:
	rm -f *.o

#include "containers/vector.h"
#include <iostream>
#include <cassert>

int main() {
    okfgen::Vector<int> vec;
    assert(vec.empty());
    assert(vec.size() == 0);

    vec.push_back(10);
    vec.push_back(20);
    vec.push_back(30);
    assert(vec.size() == 3);
    assert(vec.at(1) == 20);

    vec.pop_back();
    assert(vec.size() == 2);

    okfgen::Vector<int> copy(vec);
    assert(copy.size() == 2);
    assert(copy[0] == 10);

    vec.clear();
    assert(vec.empty());

    std::cout << "All Vector tests passed." << std::endl;
    return 0;
}

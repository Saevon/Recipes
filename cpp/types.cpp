// ----------------------------------------------------------------------------
// Basic Types




void;
// c++11
auto;


bool;
int;   // ~64bit
char;  // 8bit

// Rare types (C)
union
struct

// Pointers & const
//   Treat the * or & as commas
//   OR just read it backwards (saying pointer/reference when you hit the symbol)
//

// int, const ptr, ptr, const ptr, ptr
//  .: ptr -> const* -> * -> const* -> int
int * const * * const *val

// volatile int, const reference
//  .: &const -> volatile int
volatile int & const val

x->method() == (*x).method()



// ----------------------------------------------------------------------------
#include <string>

string text("raw string for input goes here");
text += "more text";


// Output / printing / input
#include <iostream>

cout << text << int_value << "suffix" << endl;
cin >> my_type_var;


// Regular Expressions
#include <regex>


regex ip_re("[0-9]{3}(\\.[0-9]{3}){3})");
smatch match;

// Returns 1/0
if (regex_search(input_str, match, ip_re)) {
    // Read Group
    match[1]
}

// regex_match()
// regex_replace()



// ----------------------------------------------------------------------------
#include <vector>

// Initialize
vector <val_t> list;
vector <val_t> list = {1, 2, 3, 4};

// Insert
list.push_back(val)

// Get size
list.size()

// Remove last
list.pop_back()
// Remove index 5
list.erase(list.begin() + 5)

// Editing
list[5] = val

// Read
list.at(5)

// Looping
// (c++11)
for (val_t const &val : vector) {

}
// Pre c++11
for (vector <val_t>::iterator iter = list.begin(); iter != list.end(); ++iter) {
    val_t val = *iter;
}


// Merge
vector<val_t> result;
std::merge(
    left.begin(), left.end(),
    right.begin(), right.end(),
    std::inserter(result, result.begin()
));


// Constant length vector (doesn't resize)
#include <array>

array <val_t, 3> = {1, 2, 3};


// Double ended queue
#include <deque>
// Linked List
#include <list>

#include <stack>
#include <queue>

// Not implemented
// #include <circular_buffer>



// ----------------------------------------------------------------------------
#include <map>

// Hashmap
unordered_map hash_map;


map <key_t, value_t> dict;

// Get
dict[key]
dict.at(key)
// Set
dict[key] = val
// delete
dict.erase(key)

// Has / contains
dict.count(key) == true/false

// Looping
// c++11
for (auto const &pair : dict) {
    pair->first == key;
    pair->second == val;
}

// Pre c++11
for (map<key_t, val_t>::iterator pair = dict.begin(); pair != dict.end(); ++pair) {
    pair->first   // == key;
    pair->second  // == val;
}

// Merge
dict.insert(other.begin(), other.end())



// Sets
#include <set>

set <val> my_set;

// Add
set.insert(val)
// Remove
set.erase(val)

// has / contains
set.count(val)

// Set Math
#include <algorithm>
set <val> result;

// Subtraction
std::set_difference(
    left.begin(), left.end(),
    right.begin(), right.end(),
    std::inserter(result, result.end()
));

// Addition (Union OR)
std::set_union(
    left.begin(), left.end(),
    right.begin(), right.end(),
    std::inserter(result, result.begin()
));

// intersection (AND)
std::set_intersection(
    left.begin(), left.end(),
    right.begin(), right.end(),
    std::inserter(result, result.begin()
));




// ----------------------------------------------------------------------------
enum Choices {
    red,        // default 0
    green,      // 1
    blue,       // 2
    orange = 12,
    purple,     // 13
    white  = 3,
    yellow,     // 4
};  // Int type

input_choice == Choices::red










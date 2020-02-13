// ----------------------------------------------------------------------------
#include <iterator>

InputIterator
OutputIterator
ForwardIterators
BidirectionalIterator
RandomAccessIterator


// ----------------------------------------------------------------------------
#include <algorithm>

// usually accept a Begin/End pair for iterator inputs

bool all_of(InIter, InIter, Pred)
bool any_of(InIter, InIter, Pred)
bool none_of(InIter, InIter, Pred)
bool is_sorted(FwdIter, FwdIter, Comp?)

// Container Algorithms
// * _copy versions will return a pair of OutputIterators to create the new container

// Sort in place
void sort(RandIter, RandIter, Comp?)
void reverse(BiIter, BiIter, Comp?)
void remove_if(FwdIter, FwdIter, Comp?)
// GroupBy (sorts items into two parts (before the return iter and after))
BiIter partition(BiIter, BiIter, Pred)




// Returns iterator to min,max
pair<FwdIter, FwdIter> minmax_element(FwdIter, FwdIter, Comp?)



// ----------------------------------------------------------------------------
#include <functional>

// Partials
std::bind

// Also contains: Operators





// ----------------------------------------------------------------------------
// Lambda
[capture_block](parameters) mutable exception_specification -> return_type { body }


// Captures
[ ]          // DO NOT Capture
[=]          // Capture by value
[&]          // Capture by reference
[&x]         // Capture JUST x by ref
[x]          // Capture JUST x by value
[=, &x, &y]  // Capture by value, except x,y
[&, x, y]    // Capture by reference, except x,y

// Mutable
// variables captured by-value are const, mutable makes them non-const

// exception_specification
noexcept


















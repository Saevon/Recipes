#pragma once
#ifndef __MY_HEADER_H__
#define __MY_HEADER_H__

// NEVER!!!!!
// Do not do this
using namespace std;


// Some headers are autogenerate
// see the `Makeheaders` binary



// Minimize header includes
// This includes all the functions too!
// but if you just need the type...
#include <map>

// Always include things you need
// Don't rely on include chains
#include <string>
#include <iostream> // This already includes string... but better be explicit


// Split your headers into class declarations
//  and full declarations

// Forward Declaration
class A;
// FULL
class A {
    int m;
    int j;

    int count();
}

// Use forward declarations instead of includes if you can
// The following are all equivalent if you just need string
#include <iostream>
#include <iosfwd>
class string;




// System headers
#include <string>
// System: old-c headers (without std:: namespace)
#include <string.h>
// System: old-c headers (with automatic std:: namespace)
#include <cstring>

// User headers
#include "my_string.h"
#include "path/my_string.h"






#endif /* !__MY_HEADER_H__ */

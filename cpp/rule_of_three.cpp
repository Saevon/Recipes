




// Make a class NonCopyable
class NonCopyable {
    NonCopyable(const NonCopyable&) = delete;
    void operator = (const NonCopyable&) = delete;
}


// pre c++11
class NonCopyable {
 private:
    NonCopyable(const NonCopyable&);
    void operator = (const NonCopyable&);
}


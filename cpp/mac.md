
# Setup

1. Ensure you have commandline tools
2. For memory leaks, you might need this symlink

```bash
ln -s /Applications/Xcode.app//Contents/Developer/usr/lib/libLeaksAtExit.dylib /usr/local/lib/
```


# Memory Leaks
```bash
g++ -fsanitize=address -std=c++98 -Wall ${file_name} -o ${file_base_name} && ASAN_OPTIONS=detect_leaks=1 ./${file_base_name}

# Or using "leaks"
g++ ${file_name} -o ${file_base_name} && leaks --atExit -- ./${file_base_name}
```

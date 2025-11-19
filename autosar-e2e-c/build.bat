@echo on

if exist build rmdir /s /q build

pause

mkdir build && cd build

cmake -DCMAKE_BUILD_TYPE=Debug -G "MinGW Makefiles" ..

mingw32-make -j4
pause

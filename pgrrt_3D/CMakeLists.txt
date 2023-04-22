cmake_minimum_required(VERSION 3.10)
project(pgrrt)

set(CMAKE_CXX_STANDARD 17)

include_directories(/usr/local/include/eigen3)
find_package(PythonLibs 3)
include_directories(include ${PYTHON_INCLUDE_DIRS})

add_executable(pgrrt main.cpp Tree.cpp Tree.h GMM.cpp GMM.h Canvas.cpp Canvas.h Utils.cpp Utils.h config.h matplotlibcpp.h)

target_link_libraries(pgrrt python3.8)

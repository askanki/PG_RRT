cmake_minimum_required(VERSION 3.10)
project(pgrrt)

set(CMAKE_CXX_STANDARD 17)

include_directories(C:\\Users\\Paras\\CLionProjects\\PG_RRT\\eigen3\\eigen3)

add_executable(pgrrt main.cpp Tree.cpp Tree.h GMM.cpp GMM.h Canvas.cpp Canvas.h Utils.cpp Utils.h config.h matplotlibcpp.h)

cmake_minimum_required(VERSION 3.10)
project(pgrrt)

set(CMAKE_CXX_STANDARD 17)

include_directories(/usr/local/include/eigen3)
find_package(PythonLibs 3)
include_directories(include ${PYTHON_INCLUDE_DIRS})

find_package(octomap REQUIRED)
include_directories(${OCTOMAP_INCLUDE_DIRS})
link_directories(${OCTOMAP_LIBRARY_DIRS})
link_libraries(${OCTOMAP_LIBRARIES})

find_package(dynamicEDT3D REQUIRED )
include_directories(${DYNAMICEDT3D_INCLUDE_DIRS})
link_directories(${DYNAMICEDT3D_LIBRARY_DIRS})
link_libraries(${DYNAMICEDT3D_LIBRARIES})

add_executable(pgrrt main.cpp Tree.cpp Tree.h GMM.cpp GMM.h Canvas.cpp Canvas.h Utils.cpp Utils.h config.h matplotlibcpp.h)

target_link_libraries(pgrrt python3.8)

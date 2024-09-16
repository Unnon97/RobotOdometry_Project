cmake_minimum_required(VERSION 3.1)
project(carMotion_project)

# Find OpenCV package
find_package(OpenCV REQUIRED)

# Set the source directory
set(SOURCE_DIR src)

# Add the executable
add_executable(orb_feature ${SOURCE_DIR}/orb_featurematch.cpp)
add_executable(trajectory ${SOURCE_DIR}/trajectory.cpp)

# Link OpenCV to the executable
target_link_libraries(orb_feature ${OpenCV_LIBS})
target_link_libraries(trajectory ${OpenCV_LIBS})

# Include OpenCV headers
include_directories(${OpenCV_INCLUDE_DIRS})

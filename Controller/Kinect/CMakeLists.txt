cmake_minimum_required(VERSION 2.8.12.1)
project("My Project")

set(CMAKE_CXX_FLAGS "-std=c++11")

find_package(freenect2 REQUIRED)

include_directories("/usr/include/libusb-1.0/")

INCLUDE_DIRECTORIES(
        ${freenect2_INCLUDE_DIR}
)


add_executable(main ImageCapture.cpp SharedMemWrite.cpp ./main.cpp)

target_link_libraries(main ${freenect2_LIBRARIES})

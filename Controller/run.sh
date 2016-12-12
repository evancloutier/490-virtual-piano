#!/bin/bash

cd Kinect/build
cmake -Dfreenect2_DIR=$HOME/freenect2/lib/cmake/freenect2 .. && make
./main
cd ../..

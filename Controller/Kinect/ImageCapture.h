#include <libfreenect2/libfreenect2.hpp>
#include <libfreenect2/frame_listener_impl.h>
#include <libfreenect2/packet_pipeline.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

using namespace std;

class Kinect {
  public:
    libfreenect2::Freenect2 freenect2;
    libfreenect2::Freenect2Device *dev;
    libfreenect2::PacketPipeline *pipeline;
    libfreenect2::FrameMap *frames;
    libfreenect2::SyncMultiFrameListener *listener;
    string serial;
    libfreenect2::Frame *rgbFrame;
    libfreenect2::Frame *depthFrame;

  public:
    bool openKinect();
    bool configureKinect(bool enableRGB, bool enableDepth);
    bool startKinect(bool enableRGB, bool enableDepth);
    bool getKinectFrames();
    bool stopKinect();
    bool releaseFrames();
};

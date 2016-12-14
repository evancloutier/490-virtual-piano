#include <libfreenect2/libfreenect2.hpp>
#include <libfreenect2/frame_listener_impl.h>
#include <libfreenect2/packet_pipeline.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>
#include <cstring>

using namespace std;

struct bgrx {
  unsigned char b;
  unsigned char g;
  unsigned char r;
  unsigned char x;
};

struct bgr {
  unsigned char b;
  unsigned char g;
  unsigned char r;
  bgr& operator=(bgrx& other) {
    memcpy(&b, &other, 3);
  }
};

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
    libfreenect2::Frame *irFrame;

  public:
    bool openKinect();
    bool configureKinect(bool enableRGB, bool enableDepth, bool enableIr);
    bool startKinect(bool enableRGB, bool enableDepth, bool enableIr);
    bool getKinectFrames();
    bool stopKinect();
    bool releaseFrames();
    void getFramesInfo();
};

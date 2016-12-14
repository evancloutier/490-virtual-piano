#include "ImageCapture.h"

using namespace std;

void Kinect::getFramesInfo() {
  cout << "frames coming from kinect:" << endl;
  cout << "rgb: height - " << rgbFrame->height << " width - " <<
  rgbFrame->width << " bytes per pixel - " << rgbFrame->bytes_per_pixel << endl;

  cout << "depth: height - " << depthFrame->height << " width - " <<
  depthFrame->width << " bytes per pixel - " << depthFrame->bytes_per_pixel << endl;

  cout << "IR: height - " << irFrame->height << " width - " <<
  irFrame->width << " bytes per pixel - " << irFrame->bytes_per_pixel << endl;
}

bool Kinect::releaseFrames() {
  listener->release(*frames);
}

bool Kinect::stopKinect() {
  dev->stop();
}

bool Kinect::getKinectFrames() {
  listener->waitForNewFrame(*frames);
  rgbFrame = frames->at(libfreenect2::Frame::Color);
  depthFrame = frames->at(libfreenect2::Frame::Depth);
  irFrame = frames->at(libfreenect2::Frame::Ir);
  return true;
}

bool Kinect::startKinect(bool enableRGB, bool enableDepth, bool enableIr) {
  if(enableRGB && enableDepth) {

    if(!dev->start()) {
      cout << endl << endl << dev->getSerialNumber() << endl << endl;
      return false;
    }
  }
  else {
    if(!dev->startStreams(enableRGB, enableDepth)) {
      return false;
    }
  }
  return true;

}

bool Kinect::configureKinect(bool enableRGB, bool enableDepth, bool enableIr) {
  int types = 0;
  if(enableRGB) {
    types = types | libfreenect2::Frame::Color;
  }

  if(enableDepth) {
    types = types | libfreenect2::Frame::Ir | libfreenect2::Frame::Depth;
  }
  listener = new libfreenect2::SyncMultiFrameListener(types);
  frames = new libfreenect2::FrameMap;
  dev->setColorFrameListener(listener);
  dev->setIrAndDepthFrameListener(listener);
  return true;
}

bool Kinect::openKinect() {
  dev = 0;
  pipeline = 0;
  if(freenect2.enumerateDevices() == 0) {
    cout << "no devices connected" << endl;
    return false;
  }

  if(serial == "") {
    serial = freenect2.getDefaultDeviceSerialNumber();
  }
  dev = freenect2.openDevice(serial);

  return true;
}

#include "ImageCapture.h"

using namespace std;

/*int main() {
  bool enableRGB = true;
  bool enableDepth = true;
  Kinect kinect;
  kinect.openKinect();
  kinect.configureKinect(enableRGB, enableDepth);
  kinect.startKinect(enableRGB, enableDepth);
  //for(int i = 0; i < 2; i++) {
    kinect.getKinectFrames();

    //unsigned char blue = kinect.rgbFrame->data[1];
    cout << endl << endl <<  "width: " << kinect.rgbFrame->width << " height: " << kinect.rgbFrame->height << " format: " << kinect.rgbFrame->format << " bytes per pixel: " << kinect.rgbFrame->bytes_per_pixel << endl << endl << endl;
    //cout << endl << endl << kinect.rgbFrame->data << endl << endl;
    kinect.releaseFrames();
  //}

  kinect.stopKinect();
  cout << endl << endl << "program done!" << endl << endl;
  return 0;
}*/

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
  return true;
}

bool Kinect::startKinect(bool enableRGB, bool enableDepth) {
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

bool Kinect::configureKinect(bool enableRGB, bool enableDepth) {
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

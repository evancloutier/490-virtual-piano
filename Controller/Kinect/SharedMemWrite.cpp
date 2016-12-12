#include "ImageCapture.h"
#include "SharedMemWrite.h"

using namespace std;

int rgbShmid;
int depthShmid;

int main() {
  //setup kinect
  bool enableRGB = true;
  bool enableDepth = true;
  Kinect kinect;
  kinect.openKinect();
  kinect.configureKinect(enableRGB, enableDepth);
  kinect.startKinect(enableRGB, enableDepth);
  kinect.getKinectFrames();

  //setup shared memory
  //get RGB frame shared memory
  key_t keyRgb = getMemKey(false);
  int rgbPayloadSize = kinect.rgbFrame->width * kinect.rgbFrame->height * kinect.rgbFrame->bytes_per_pixel + 1;
  void* sharedRgbMem = setupMem(false, keyRgb, rgbPayloadSize);
  unsigned char* rgbPayload;

  //get Depth frame shared memory
  key_t keyDepth = getMemKey(true);
  int depthPayloadSize = kinect.depthFrame->width * kinect.depthFrame->height * kinect.rgbFrame->bytes_per_pixel + 1;
  void* sharedDepthMem = setupMem(true, keyDepth, depthPayloadSize);
  unsigned char* depthPayload;

  kinect.releaseFrames();


  //get frames from kinect
  //for(int i = 0; i < 2; i++) {
    kinect.getKinectFrames();

    rgbPayload = (unsigned char*)kinect.rgbFrame->data;
    depthPayload = (unsigned char*)kinect.depthFrame->data;
    writeToMem(sharedRgbMem, rgbPayload, rgbPayloadSize);
    writeToMem(sharedDepthMem, depthPayload, depthPayloadSize);
    while(1){};
    kinect.releaseFrames();
  //}

  //destroy shared memory
  destoryMem(sharedRgbMem, rgbShmid);
  destoryMem(sharedDepthMem, depthShmid);

  //stop kinect
  kinect.stopKinect();
  cout << endl << endl << "program done!" << endl << endl;
  return 0;
}

void writeToMem(void* sharedMem, unsigned char* payload, int payloadSize) {
  memcpy(sharedMem, payload, payloadSize);
}

void destoryMem(void* shared_memory, int shmid) {
  shmdt(shared_memory);
  shmctl(shmid, IPC_RMID, NULL);
}

void* setupMem(bool isDepth, key_t key, int payloadSize) {
  // give your shared memory an id, anything will do
  void *shared_memory;
  int* shmid;

  if(isDepth)
    shmid = &rgbShmid;
  else
    shmid = &depthShmid;

  if ((*shmid = shmget(key, payloadSize, IPC_CREAT | 0666)) < 0)
  {
     printf("Error getting shared memory id");
     exit(1);
  }
  // Attached shared memory
 shared_memory = shmat(*shmid, NULL, 0);
  if ((char *)(shared_memory) == (char *) -1)
  {
     printf("Error attaching shared memory id");
     exit(1);
  }
  return shared_memory;
}

int getMemKey(bool isDepthBuff) {
  ifstream infile("../memkey.txt");
  int key;
  infile >> key;
  if(isDepthBuff)
    infile >> key;
  return key;
}

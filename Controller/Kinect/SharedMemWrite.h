#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <math.h>

using namespace std;

class ImageWrite {

  public:
    ImageWrite();
    void* getMemory(int imageType);;
    int getMemKey(int memType);
    int getSemKey();
    void writeToMem(void* sharedMem, unsigned char* payload, int payloadSize);
    void* createMem(int memType, key_t key, int payloadSize);
    void destoryMem(void* shared_memory, int shmid);
    void endSession();
    void getFramesAndWriteToBuff(bool enableRGB, bool enableDepth, bool enableIr);
    unsigned char* scaleDownImage(bgrx* originalPayload);
    void* createSemaphore();


  public:
    enum ImageType {
      RGB = 0,
      Depth = 1,
      IR = 2,
      Semaphore = 3,
    };

    enum SemaphoreVals {
      Writing = 0,
      Reading = 1,
      BuffSize = sizeof(int),
    };

    Kinect kinect;


    int rgbWidth = 1920;
    int rgbHeight = 1080;
    int desiredRgbWidth = 1000;
    int desiredRgbHeight = 500;
    int desiredRgbBytesPerPixel = 3;
    int depthWidth = 512;
    int depthHeight = 424;
    int rgbBytesPerPixel = 3;
    int depthBytesPerPixel = 4;

    int semId;
    void* semaphore;

    int rgbShmid;
    int depthShmid;
    int irShmid;

    void* rgbMem;
    void* depthMem;
    void* irMem;

    int rgbMemSize;
    int depthMemSize;
    int irMemSize;

};

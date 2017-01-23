#include "ImageCapture.h"
#include "SharedMemWrite.h"

using namespace std;


ImageWrite::ImageWrite() {
  bool enableRGB = true;
  bool enableDepth = true;
  bool enableIR = true;

  kinect.openKinect();
  kinect.configureKinect(enableRGB, enableDepth, enableIR);
  kinect.startKinect(enableRGB, enableDepth, enableIR);
  kinect.getKinectFrames();

  rgbMem = getMemory(ImageWrite::RGB);
  depthMem = getMemory(ImageWrite::Depth);
  irMem = getMemory(ImageWrite::IR);

  semaphore = createSemaphore();

  kinect.releaseFrames();
}

void* ImageWrite::createSemaphore() {
  key_t key = getSemKey();
  cout << "Sem key: " << key << endl;

  void* mem = createMem(ImageWrite::Semaphore, key, ImageWrite::BuffSize);

  return mem;
}

unsigned char* ImageWrite::scaleDownImage(bgrx* originalPayload) {
  //original image is 1920 * 1080
  //scaled down new image is 1024 * 848

  bgr* newPayload = (bgr*)malloc(desiredRgbWidth * desiredRgbHeight * sizeof(bgr));

  int baseIdx;
  float height = 0;
  float width = 0;

  for(int newIdx = 0; newIdx < desiredRgbWidth * desiredRgbHeight; newIdx += 1) {
    baseIdx = round(width) + rgbWidth * round(height);

    newPayload[newIdx] = originalPayload[baseIdx];

    width += ((float)rgbWidth/desiredRgbWidth);
    if(width >= rgbWidth) {
      width = 0;
      height += ((float)rgbHeight/desiredRgbHeight);
    }

  }

  return (unsigned char*)newPayload;
}

void ImageWrite::getFramesAndWriteToBuff(bool enableRGB, bool enableDepth, bool enableIr) {
  //get frames from kinect
  int writing = ImageWrite::Writing;
  int reading = ImageWrite::Reading;

  memcpy(semaphore, &writing, ImageWrite::BuffSize);

  while(true) {

    //get semaphore
    while(*(int*)semaphore == ImageWrite::Reading) {
      kinect.getKinectFrames();

    }

    unsigned char* rgbPayload = (unsigned char*)kinect.rgbFrame->data;
    rgbPayload = scaleDownImage((bgrx*)rgbPayload);
    //unsigned char* depthPayload = (unsigned char*)kinect.depthFrame->data;
    //unsigned char* irPayload = (unsigned char*)kinect.irFrame->data;
    //copy values to shared mem

    writeToMem(rgbMem, rgbPayload, rgbMemSize);
    //writeToMem(depthMem, depthPayload, depthMemSize);
    //writeToMem(irMem, irPayload, irMemSize);

    //release semaphore
    memcpy(semaphore, &reading, ImageWrite::BuffSize);

    //free(rgbMem);

  }

}

void ImageWrite::endSession() {
  destoryMem(rgbMem, rgbShmid);
  destoryMem(depthMem, depthShmid);
  destoryMem(irMem, depthShmid);
  kinect.stopKinect();
  cout << endl << endl << "program done!" << endl << endl;
}

void* ImageWrite::getMemory(int imageType) {
  key_t key = getMemKey(imageType);
  cout << "mem type: " << imageType << " key: " << key << endl;
  libfreenect2::Frame *frame;
  int bufferSize;

  if(imageType == ImageWrite::RGB) {
    frame = kinect.rgbFrame;
    bufferSize = desiredRgbWidth * desiredRgbHeight * desiredRgbBytesPerPixel;
    rgbMemSize = bufferSize;
  }

  else if(imageType == ImageWrite::Depth) {
    frame = kinect.depthFrame;
    bufferSize = frame->width * frame->height * frame->bytes_per_pixel;
    depthMemSize = bufferSize;
  }

  else if(imageType == ImageWrite::IR) {
    frame = kinect.depthFrame;
    bufferSize = frame->width * frame->height * frame->bytes_per_pixel;
    irMemSize = bufferSize;
  }

  void* mem = createMem(imageType, key, bufferSize);
  return mem;
}

void ImageWrite::writeToMem(void* sharedMem, unsigned char* payload, int payloadSize) {
  memcpy(sharedMem, payload, payloadSize);
}

void ImageWrite::destoryMem(void* shared_memory, int shmid) {
  shmdt(shared_memory);
  shmctl(shmid, IPC_RMID, NULL);
}

void* ImageWrite::createMem(int imageType, key_t key, int payloadSize) {
  void *shared_memory;
  int* shmid;

  if(imageType == ImageWrite::RGB) {
    shmid = &rgbShmid;
  }
  else if(imageType == ImageWrite::Depth)
    shmid = &depthShmid;
  else if(imageType == ImageWrite::IR)
    shmid = &irShmid;
  else if(imageType == ImageWrite::Semaphore)
    shmid = &semId;

  if ((*shmid = shmget(key, payloadSize, IPC_CREAT | 0666)) < 0)
  {
     printf("Error getting shared memory id");
     exit(1);
  }

 shared_memory = shmat(*shmid, NULL, 0);
  if ((char *)(shared_memory) == (char *) -1)
  {
     printf("Error attaching shared memory id");
     exit(1);
  }
  return shared_memory;
}

int ImageWrite::getMemKey(int imageType) {
  ifstream infile("../memkey.txt");
  int n = imageType + 1;
  int key;
  for(int i = 0; i < n; i++)
    infile >> key;
  return key;
}

int ImageWrite::getSemKey() {
  ifstream infile("../semkey.txt");
  int key;
  infile >> key;
  return key;
}

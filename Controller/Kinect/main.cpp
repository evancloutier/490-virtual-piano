#include "ImageCapture.h"
#include "SharedMemWrite.h"

using namespace std;

int main() {
  ImageWrite imageWriter;

  bool enableRGB = true;
  bool enableDepth = true;
  bool enableIR = true;
  imageWriter.getFramesAndWriteToBuff(enableRGB, enableDepth, enableIR);

  imageWriter.endSession();
  return 0;
}

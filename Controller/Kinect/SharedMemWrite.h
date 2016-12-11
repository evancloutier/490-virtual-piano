#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

void writeToMem(void* sharedMem, unsigned char* payload, int payloadSize);
int getMemKey(bool isDepthBuff);
void* setupMem(bool isDepth, key_t key, int payloadSize);
void destoryMem(void* shared_memory, int shmid);

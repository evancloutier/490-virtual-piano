from PIL import Image
import sysv_ipc
import struct

rgbMem = sysv_ipc.SharedMemory(29837423)
rgbMemVal = rgbMem.read()
rgbUnorderedBytes = bytearray(rgbMemVal)

depthMem = sysv_ipc.SharedMemory(23938294)
depthMemVal = depthMem.read()
depthUnorderedBytes = bytearray(depthMemVal)


rgbImageData = ""
depthImageStr = ""
depthImageFlt = []

rgbImage = True
depthImage = True

if rgbImage:
    rgbImgHeight = 1080
    rgbImgWidth = 1920
if depthImage:
    depthImgHeight = 424
    depthImgWidth = 512



if rgbImage:
    idx = 0
    while idx < rgbImgHeight * rgbImgWidth * 4:
        rgbImageData += chr(rgbUnorderedBytes[idx + 2])
        rgbImageData += chr(rgbUnorderedBytes[idx + 1])
        rgbImageData += chr(rgbUnorderedBytes[idx + 0])
        idx += 4

    image = Image.frombytes("RGB", (rgbImgWidth, rgbImgHeight), rgbImageData)
    image.save("/home/evan/test3.png", "PNG")

if depthImage:
    idx = 0
    while idx < depthImgHeight * depthImgWidth * 4:

        depthImageStr += chr(depthUnorderedBytes[idx + 2])
        depthImageStr += chr(depthUnorderedBytes[idx + 1])
        depthImageStr += chr(depthUnorderedBytes[idx + 0])
        depthImageFlt.append(chr(depthUnorderedBytes[idx])
        + chr(depthUnorderedBytes[idx + 1])
        + chr(depthUnorderedBytes[idx + 2])
        + chr(depthUnorderedBytes[idx + 3]))
        idx += 4

    depthImageFlt = [struct.unpack('>f', b) for b in depthImageFlt]


    image = Image.frombytes("RGB", (depthImgWidth, depthImgHeight), depthImageStr)
    image.save("/home/evan/test4.png", "PNG")

    f = open("/home/evan/depthVals.txt", 'w')

    idx = 0
    while idx < depthImgHeight * depthImgWidth:

        f.write('{:30s} '.format(str(depthImageFlt[idx][0])))

        if idx % depthImgWidth == 0:
            f.write('\n')
        idx += 1


    f.close()

from PIL import Image
import sysv_ipc
import struct

rgbMem = sysv_ipc.SharedMemory(29837423)
rgbMemVal = rgbMem.read()
rgbUnorderedBytes = bytearray(rgbMemVal)

depthMem = sysv_ipc.SharedMemory(23938294)
depthMemVal = depthMem.read()
depthUnorderedBytes = bytearray(depthMemVal)

irMem = sysv_ipc.SharedMemory(89239843)
irMemVal = irMem.read()
irUnorderedBytes = bytearray(irMemVal)


rgbImageData = ""
depthImageStr = ""
depthImageFlt = []
irImageStr = ""
irImageFlt = []

rgbImage = True
depthImage = True
irImage = False

if rgbImage:
    rgbImgHeight = 424
    rgbImgWidth = 512
if depthImage:
    depthImgHeight = 424
    depthImgWidth = 512
if irImage:
    irImageHeight = 512
    irImageWidth = 424




if rgbImage:
    idx = 0
    while idx < rgbImgHeight * rgbImgWidth * 3:
        rgbImageData += chr(rgbUnorderedBytes[idx + 2])
        rgbImageData += chr(rgbUnorderedBytes[idx + 1])
        rgbImageData += chr(rgbUnorderedBytes[idx])
        idx += 3


    image = Image.frombytes("RGB", (rgbImgWidth, rgbImgHeight), rgbImageData)

    image.save("/home/evan/rgb.png", "PNG")

if irImage:
    idx = 0
    while idx < irImageWidth * irImageHeight * 4:

        irImageStr += chr(irUnorderedBytes[idx + 2])
        irImageStr += chr(irUnorderedBytes[idx + 1])
        irImageStr += chr(irUnorderedBytes[idx + 0])
        irImageFlt.append(chr(irUnorderedBytes[idx])
        + chr(irUnorderedBytes[idx + 1])
        + chr(irUnorderedBytes[idx + 2])
        + chr(irUnorderedBytes[idx + 3]))
        idx += 4

    irImageFlt = [struct.unpack('>f', b) for b in irImageFlt]


    image = Image.frombytes("RGB", (irImageWidth, irImageHeight), irImageStr)
    image.save("/home/evan/ir.png", "PNG")

    f = open("/home/evan/irVals.txt", 'w')

    idx = 0
    while idx < irImageHeight * irImageWidth:

        f.write('{:30s} '.format(str(irImageFlt[idx][0])))

        if idx % irImageWidth == 0:
            f.write('\n')
        idx += 1


    f.close()

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
    image.save("/home/evan/depth.png", "PNG")

    f = open("/home/evan/depthVals.txt", 'w')

    idx = 0
    while idx < depthImgHeight * depthImgWidth:

        f.write('{:30s} '.format(str(depthImageFlt[idx][0])))

        if idx % depthImgWidth == 0:
            f.write('\n')
        idx += 1


    f.close()

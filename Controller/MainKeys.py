
# coding: utf-8

import numpy as np
import cv2
import sys
import KeyDetector
import PyKinect

# Initialize the PyKinect class for streaming
pk = PyKinect.PyKinect()

# Want to re-write the KeyDetector class to accept a frame when detecting keys
kd = KeyDetector.KeyDetector(pk)

# When we are finished with the Kinect
pk.exit()

# # Now we display the key contours
# xoffset = 0
# yoffset = 100
# minusBool = 1
# while True:
#     frames = listener.waitForNewFrame()
#     color = frames["color"]
#     keyDetector.receiveFrame(color)
#
#     for contour in keyDetector.transmitKeyContours():
#         c = contour[0]
#         cv2.drawContours(color.asarray(), [c], -1, (0, 0, 0), 5)
#         cv2.circle(color.asarray(), (contour[1], contour[2]), 7, (0, 0, 0), -1)
#
#
#     # for contour in keyDetector.transmitBounds():
#     #     #epsilon marks accuracy of square
#     #     epsilon = 0.1*cv2.arcLength(contour, True)
#     #     approx = cv2.approxPolyDP(contour, epsilon, True)
#     #     x, y, w, h = cv2.boundingRect(approx)
#     #
#     #     cv2.rectangle(color.asarray(), (x, y), (x + w + xoffset, y + h + yoffset), (255, 0, 0), 2)
#
    # cv2.imshow("Contours", cv2.resize(color.asarray(), (int(1920 / 3), int(1080 / 3))))
#
#     listener.release(frames)
#
#     k = cv2.waitKey(10)
#
#     # if k == ord('-'):
#     #     print("toggled subtraction mode")
#     #     minusBool = -1 * minusBool
#     # if k == ord('x'):
#     #     xoffset += 5 * minusBool
#     # if k == ord('y'):
#     #     yoffset += 5 * minusBool
#     if k == 27:
#         break
#
#
# device.stop()
# device.close()
#
# sys.exit(0)
#
# # octave = ["B", "Bb", "A", "Ab", "G", "Gb", "F", "E", "Eb", "D", "Db", "C"]
# # index = 0
#
# # for contour in contours:
# #     c = contour[1]
# #     cv2.drawContours(frame.asarray(), [c], -1, (0, 255, 0), 2)
# #     cv2.circle(frame.asarray(), (contour[2], contour[3]), 7, (0, 0, 0), -1)
# #     # cv2.putText(frame.asarray(), octave[index], (contour[2], contour[3] + 20),
# #         # cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 2)
# #     # index += 1

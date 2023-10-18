# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 11:41:28 2023

@author: user
"""
import argparse
import cv2
from pathlib import Path
import sys
import os
 
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0] 
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT)) 
ROOT = Path(os.path.relpath(ROOT, Path.cwd())) 

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str, default=ROOT / 'source.mp4', help="video or 0 for webcam")
args = parser.parse_args()

source = Path(args.source)

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(str(source))
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
else:
  ret, frame = cap.read()
  if ret == True:
    cv2.imwrite("out.jpg", frame) 
    print("successfull")
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()


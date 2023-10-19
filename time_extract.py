import argparse
import sys
import cv2
import pytesseract
import os
from pathlib import Path

from utils.general import print_args

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0] 
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT)) 
ROOT = Path(os.path.relpath(ROOT, Path.cwd())) 

def downscaleResize(img, scale_percent):
    ''' input: image object, scale_percent or ratio
        output: image object with resized ratio'''
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation= cv2.INTER_AREA)
    return resized

# def extract_time_rescale(img, scale_percent=50, custom_config = r'-c tessedit_char_whitelist=1234567890Oo --psm 6'):
def extract_time_rescale(img, scale_percent=50, custom_config = r'-c tessedit_char_whitelist=1234567890 --psm 6'):
    '''take path of image and return the extracted text on top right'''
    height, width, _ = img.shape
    img_time = img[int(0.026*height) : int(0.064*height), int(0.907*width) : int(0.983*width)] #only time hour:min:sec

    # grayscale
    img_time = cv2.cvtColor(img_time, cv2.COLOR_BGR2GRAY)
    # thresholding (>127 = white, else black)
    _, img_time = cv2.threshold(img_time, 160, 255, cv2.THRESH_BINARY_INV )
    img_time = cv2.bitwise_not(img_time)

    cv2.imwrite("check_processed_text.png", img_time)

    str_time = pytesseract.image_to_string(img_time, config=custom_config)
    print(str_time)
    return str(str_time)

def detectTime(im):
    time = extract_time_rescale(im)
    time = f"{time[0:2]}:{time[2:4]}:{time[4:6]}"
    return time

def extract(source = ROOT / 'source/out.jpg'):
    i = cv2.imread(source)
    height, width, _ = i.shape
    print(height, width)

    # Create a window with the same dimensions as the image
    cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Original Image', width, height)
    cv2.imshow('Original Image',i)
    time = detectTime(i)
    cv2.imwrite("test.png", i)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(time)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default=ROOT / 'source/out.jpg', help='image to extract the time')
    opt = parser.parse_args()

    return opt
  
def main(opt):

    extract(opt.source)

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
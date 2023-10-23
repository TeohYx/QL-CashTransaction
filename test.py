import cv2
import pytesseract
import numpy as np

def main():
    img = cv2.imread("time.png")
    height, width, _ = img.shape
    cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Original Image', width, height)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    black_background = np.zeros_like(img)

    # Copy the original image to the black background using the binary mask
    img = cv2.bitwise_and(black_background, img, mask=np.ones((3, 3), np.uint8))
    # _, img = cv2.threshold(img, 165, 255, cv2.THRESH_BINARY_INV )
    # img = cv2.bitwise_not(img)

    # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    # img = cv2.dilate(img, np.ones((3, 3), np.uint8), iterations=2)
    # img = cv2.erode(img, np.ones((3, 3), np.uint8), iterations=1)
    cv2.imshow("Original Image", img)


    str_time = pytesseract.image_to_string(img, config=r'-c tessedit_char_whitelist=1234567890 --psm 6')
    print(str_time)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()
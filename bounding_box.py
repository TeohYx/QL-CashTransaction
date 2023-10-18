import cv2
import sys
import keyboard

class Bounding_box:
    def __init__(self, path=None, frame=None):
        self.path = path                    # Path of the video
        self.frame = frame                  # The first frame captured as image
        self.roi_value = []                 # The temporary roi value
        self.roi_value_all = []             # All roi value 
        self.height = None
        self.width = None
        """
        0 - Cashier
        1 - Customer
        """
        self.class_label = ["0", "1"]
        self.labeling = {"0": "Cashier",
                        "1": "Customer"
                        }     

    #  Extract the first frame as image
    def screenshot(self):
        video_path = self.path
        cap = cv2.VideoCapture(video_path)

        ret, frame = cap.read()
        if not ret:
            return

        cv2.imwrite('screenshot.jpg', frame)

        # Get the image of the frame
        self.frame = cv2.imread('screenshot.jpg')
        # print("width is: ", self.frame.Width)
        height, width, channels = self.frame.shape
        self.height = height
        self.width = width
        print(f"Image size: Width = {width}, Height = {height}, Channels = {channels}")

        cap.release()
        cv2.destroyAllWindows()

    # Define a ROI
    """
    Format: 
    [x, y, w, h]
    x - Top left x coordinate
    y - Top left y coordinate
    w - Width
    h - Height
    """
    def region_of_interest(self):
        roi = cv2.selectROI("Select ROIs", self.frame, showCrosshair=False)
        self.roi_value = list(roi)

        # print(roi)
        cv2.destroyAllWindows()

def on_key_event(e, bb):
    if e.name == bb.class_label[0]:
        print(f"----{bb.labeling[bb.class_label[0]]}----")
        extract_roi_cashier(bb, bb.class_label[0])
    elif e.name == bb.class_label[1]:
        print(f"----{bb.labeling[bb.class_label[1]]}----")
        extract_roi_cashier(bb, bb.class_label[1])
    elif e.name == "q":
        print(f"the roi are as follow: \n {bb.roi_value_all}")

def extract_roi_cashier(bb, label):
    """
    0 - Set the box for cashier
    1 - Set the box for customer
    """
    bb.region_of_interest()
    roi_temp = bb.roi_value
    # print(roi_temp)
    roi_temp.insert(0, label)
    # print(roi_temp)
    bb.roi_value_all.append(roi_temp)
    # print(bb.roi_value_all)

    print(f"Done setting ROI for {bb.labeling[label]}")

# Do a normalization so that it fits on the video
def resize(value, bb):
    result = []
    for c, x, y, w, h in value:
        xn = round(x/bb.width, 4)
        yn = round(y/bb.height, 4)
        wn = round(w /bb.width, 4)
        hn = round(h/bb.height, 4)

        result.append((c, xn, yn, wn, hn))

    return result

def get_roi(source):
    bb = Bounding_box(source)
# def get_roi():
#     bb = Bounding_box("test.mp4")
    print("You may start drawing the bounding box.")
    for key, value in bb.labeling.items():
        print(key, ":", value)
    print("q : quit")

    keyboard.on_press(lambda e: on_key_event(e, bb))
    bb.screenshot()     # Get the image of the video
    keyboard.wait("q")

    result = resize(bb.roi_value_all, bb)
    print("result: ", result)
    return result

# def main():
#     get_roi()

# if __name__ == "__main__":
#     main()
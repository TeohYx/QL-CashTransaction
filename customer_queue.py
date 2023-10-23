import cv2
from txt_extractor import text_extractor
from time_extract import detectTime as dT 
import threading
import time

class Queue:
    def __init__(self, queue_class=2, roi=None, box_info=None):
        # c, x1, y1, x2, y2
        self.roi = roi
        # xa, ya, xb, yb, cate, iden
        self.box_info = box_info
        self.queue_roi = []
        self.queue_customer = []
        self.queue_class = queue_class
        self.count = 0
        self.notification = []
        self.is_notification_sent = False
        self.cooldown = 0
        self.remaining = 0

    def set_roi(self, roi):
        self.roi = roi

    def set_box_info(self, box_info):
        self.box_info = box_info

    def check_queue(self):
        """
        Check if there is more than 5 customer in the queue ROI
        """
        # ROIs = text_extractor("source/out.txt")
        # print(ROIs)
        self.queue_roi = [row for row in self.roi if int(row[0]) == self.queue_class]
        print("Queue roi: ",self.queue_roi)

    def check_customer(self):
        """
        Check if there is more than 5 customer in the queue ROI
        """
        self.queue_customer = [row for row in self.box_info if int(row[4]) == 0]
        print("Customer box: ",self.queue_customer)
    
    def allow_notification(self):
        self.is_notification_sent = False

    def get_notification(self):
        return self.notification

    def set_fps(self, fps):
        self.cooldown = fps * 5

    def count_customers(self, img):
        self.count = 0
        self.check_queue()
        self.check_customer()

        for _, x1, y1, x2, y2 in self.queue_roi:    # ROI
            for xa, ya, xb, yb, _, id in self.queue_customer:   # Person
                inter_x1 = max(x1, xa)
                inter_y1 = max(y1, ya)
                inter_x2 = min(x2, xb)
                inter_y2 = min(y2, yb)

                w = max(0., (inter_x2 - inter_x1))
                h = max(0., (inter_y2 - inter_y1))

                inter_area = (w * h)
                roi_area = ((xb - xa) * (yb - ya))

                intersection = inter_area / roi_area
                print("Intersection: ", intersection, " and id is : ", id, " iter_area = ", inter_area, " and roi_area = ", roi_area)
                if intersection > 0.3:
                    self.count += 1
                # if xb < x1 or yb < y1 or xa > x2 or ya > y2:
                #     print(f"{xb} and {x1}\n {yb} and {y1} \n {xa} and {x2}\n {ya} and {y2}")
                #     print("id for outside is: ", id)
                #     continue
                # else:
                #     print("id is: ", id)
                #     self.count += 1
        print("count:", self.count)

        if self.count >= 5 and self.is_notification_sent == False:
            print("Notification sent")

            print(self.is_notification_sent)
            current = dT(img)
            self.notification.append([current, self.count])

            self.remaining = self.cooldown
            self.is_notification_sent = True

        if self.remaining != 0 and self.is_notification_sent == True:  
            self.remaining -= 1 
        elif self.remaining == 0:
            self.is_notification_sent = False

def main():
    queue = Queue()
    queue.check_queue()

if __name__ == "__main__":
    main()
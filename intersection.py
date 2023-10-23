import datetime
import cv2
from time_extract import detectTime as dT 

class Intersection:
    def __init__(self, roi=None, box_info=None, stop_track=3):
        self.roi = roi
        self.box_info = box_info
        self.stop_track = stop_track
        self.time_database = []
        self.is_transaction_sent = False
        self.cashier_id = -1
        self.customer_id = -1
        self.cash_id = -1
        self.tracked_id = -1
        self.intersect = []

    def set_roi(self, roi):
        self.roi = roi
    
    def set_box_info(self, box_info):
        self.box_info = box_info

    def get_time_database(self):
        return self.time_database

# """Check cash transaction"""
# time_database = []                      # Store all cash transaction
# is_transaction_sent = False             # Check if there is any transaction by cash

# # Store the existing frame that tracking cashier, customer and cash id
# cas_id = -1
# cus_id = -1
# cash_id = -1

# # Deal with the scenario when id disappear unexpectedly
# tracked_id = -1
# # Counter to drop the customer id after defined frames
# stop_track = 3

    def check_intersect(self):
        print("transaction happening: ", self.is_transaction_sent)

        inters = []
        counter = 0
        for c, x1, y1, x2, y2 in self.roi:
                # x1, y1, x2, y2, category, identity
            for xa, ya, xb, yb, cate, iden  in self.box_info:
                counter+=1
                # Calculate the coordinate of the intersection quad
                inter_x1 = max(x1, xa)
                inter_y1 = max(y1, ya)
                inter_x2 = min(x2, xb)
                inter_y2 = min(y2, yb)
                w = max(0., (inter_x2 - inter_x1))
                h = max(0., (inter_y2 - inter_y1))
            
                inter_area = (w * h)
                roi_area = ((x2 - x1) * (y2 - y1))

                intersection = inter_area / roi_area
                inters.append([c, cate, iden, intersection])

        """"
        inters list now have all the box information visible in every frame

        c - category of ROI (0 = cashier, 1 = customer)
        cate - category of detected object (0 = person, 1 = cash)
        iden - unique ID of detected object
        intersection - the intersection ratio of the ROI on detected object (c/cate)
        """    
        
        # print("Iteration: ", counter)
        # print(f"Intersection is: {inters}")

        # Sorted so that the arrangement is in descending order
        inters.sort(key=lambda x: x[3], reverse=True)

        return inters

    def cash_transaction(self, img):
        self.intersect = self.check_intersect()

        haveCashier = False
        haveCustomer = False
        haveCash = False

        # Store the value of intersection of 0 so that: it can easily detected the dropped unique id and remove it.
        all_iden = [row[2] for row in self.intersect if float(row[3]) == 0 ]

        for c, cate, iden, intersection in self.intersect:
            # print(f"{c}, {cate}, {iden}, {intersection}")
            # Deal with the box where detected object have no intersection with ROIs
            if intersection == float(0):
                """
                Case 1: Customer leaving the ROI and the cas_id need to be cleared (-1)
                Case 2: Customer leaving the ROI but its unique_id changed due to poor object detection 
                Case 3: Person in the background (can be customer or cashier) which will be ignored
                """
                # print(all_iden)

                # Case 1 (Drop the track when it is not visible after stop_track frame)
                if int(self.tracked_id) != -1 and int(self.tracked_id) not in all_iden:
                    print("deduce1 left: ", self.stop_track)
                    self.stop_track -= 1

                # Customer leaving
                    """
                    isPersonCustomerTemp to get the last frame of customer leaving the customer box. This make the detection of 
                        customer leaving the box to be one frame later.
                    int(c) == 1 to ensure the taken value is the customer box
                    int(iden) == int(customer_id) to get the specific customer that leaves the customer box
                    """
                # Case 1 (When it reaches stop_track frames)
                if self.stop_track == 0:
                    print("Tracked id dropped")
                    # Reset tracked_id, this prevent this tracked_id on tracking disappeared id which cause the prevention of turning
                    #   is_transaction_sent to False, and to start tracking the new customer id
                    # Reset the stop_trck 
                    self.tracked_id = -1 
                    self.stop_track = 3

                # Case 2 (When the tracked_id as customer is move out of ROI, that is happen exactly when their intersection is 0)
                if int(c) == 1 and int(iden) == int(self.tracked_id):  
                    print("Customer leaving")  
                    cv2.waitKey(2000)

                    # Customer leaving indicating end of transaction, therefore
                    # Stop track the id --> tracked_id = -1
                    # Turn is_transaction_sent to False
                    # Reset the cash_id to start get new id
                    self.tracked_id = -1
                    self.is_transaction_sent = False
                    self.cash_id = -1
                    self.stop_track = 3
            else:
                # print("there is intersection")
                # The first encounter that meet these 3 requirements is the one with the highest intersection value
                # This is because the list is sorted in descending in respect to the intersection. 
                if int(c) == 0 and int(cate) == 0:
                    # Start tracking cashier id
                    if not haveCashier:
                        # print(iden)
                        self.cashier_id = iden
                        haveCashier = True

                # The first encounter that meet these 3 requirements is the one with the highest intersection value
                elif int(c) == 1 and int(cate) == 0:
                    # Start tracking customer id
                    if not haveCustomer:
                        # print(iden)
                        self.customer_id = iden
                        haveCustomer = True
                        # Assign new id if havent 
                        if int(self.tracked_id) == -1:
                            self.tracked_id = self.customer_id

                # The first encounter that meet these 3 requirements is the one with the highest intersection value
                # int(cash_id) == -1 is to make sure it track only the frame where cash is visible in the customer ROI 
                elif int(c) == 1 and int(cate) == 1 and int(self.cash_id) == -1:
                    if not haveCash:
                        # print(iden)
                        self.cash_id = iden
                        haveCash = True

        # print("tracked_id: ", tracked_id)
        # print("cashier id: ", cas_id)
        # print("customer id: ", cus_id)
        # print("cashier_id: ", cash_id)

        # When all the haveCashier, haveCustomer and haveCash is True, indicating cashier in cashier ROI, customer in customer ROI ,
            # and cash in customer ROI (customer paying by cash)
        if(self.cashier_id != -1 and self.customer_id != -1 and self.cash_id != -1):
            # If the transaction not happening yet
            if not self.is_transaction_sent:
                print("Payment happening, sending data")

                # Send the time
                # current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                current = dT(img)
                self.time_database.append(current)

                cv2.waitKey(1000)  
                # Set the is_transaction_sent to True to prevent this if statement from running and causing duplicate result
                self.is_transaction_sent = True   

        

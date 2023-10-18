# QL-CashTransaction
An object detection and tracking model to tracked for possible cash transaction

To get the code, clone the git:

``` 
git clone https://github.com/TeohYx/QL-CashTransaction.git
```

Before using the application, please follow the setup in the YoloDeepSort folder. 

**Note that in Step 5, to get the video, click on the link provided, and download the video in the folder Video.

Some important argument:
```
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default=ROOT / 'data/images', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--roi', type=str, default=ROOT / 'source/out.txt', help='get the txt file containing location of ROIs')
```

To run the obj_det_and_trk.py file, the format is as follow:
```
python obj_det_and_trk.py --weight best.pt --source <video directory> --roi <txt directory>
```
By default, the location of the 
  custom model is set at current working directory
  video is set at data/images folder
  annotation txt is set at source folder

After input the code, let the script run, and eventually it will come out an output containing all the cash transaction of the given video input.

The transaction is saved in current working directory, and named as 'transaction.xlsx'

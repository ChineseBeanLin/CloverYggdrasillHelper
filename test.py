import cv2
from config import SCREEN_SHOOT_SAVE_PATH
import baidu_ocr




def box_to_rectangle(src, box):
    print (box[0],(box[0][0]+box[1][0], box[0][1]+box[1][0]), box[1])
    cv2.rectangle(src, box[0], (box[0][0]+box[1][0], box[0][1]+box[1][1]), (0, 255, 255))
    cv2.imshow("t", src)
    cv2.waitKey(0)


print( baidu_ocr.image2text(SCREEN_SHOOT_SAVE_PATH + "event_title1.png"))
#AshenArms.choose_event_opt(client)
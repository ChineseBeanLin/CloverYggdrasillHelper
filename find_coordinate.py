import ADBShell
import cv2
from config import SCREEN_SHOOT_SAVE_PATH,RES_PATH
import img_utils

a = ADBShell.ADBShell()
a.get_screen_shoot()
loc = img_utils.match_tpl_loc(SCREEN_SHOOT_SAVE_PATH + "screenshoot.png", RES_PATH + "shop_end.png")
print(loc)
a.get_screen_shoot(screen_range=((981, 265), (210, 210)))
#print (img_utils.image_compare("screen_shoot/item.png", RES_PATH + "super_boss.png"))

def box_to_rectangle(src, box):
    cv2.rectangle(src, box[0], (box[0][0]+box[1][0], box[0][1]+box[1][0]), (0, 255, 255))
    cv2.imshow(src)
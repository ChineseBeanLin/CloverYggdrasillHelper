import ADBShell
import cv2
import numpy as np
from config import SCREEN_SHOOT_SAVE_PATH
import AshenArms

# ADBShell.ADBShell().get_screen_shoot(AshenArms.box)
ADBShell.ADBShell.get_sub_screen("2star.png", [[0,0],[102,30]])

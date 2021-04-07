# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 10:52:21 2021

@author: hasee
"""
import cv2
import numpy as np
from skimage.metrics import structural_similarity
import math
def match_tpl_loc(target, tpl, threshold = 0.9):
    img_target = cv2.imread(target, 0)
    img_tpl = cv2.imread(tpl, 0)
    methods = [cv2.TM_CCOEFF_NORMED]
    for md in methods:
        result = cv2.matchTemplate(img_target, img_tpl, md)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if (max_val < threshold) : 
            return [-1, -1]
        return max_loc
    
    
def image_compare(img1_path,img2_path, threshold = 0.83):
    img1 = cv2.imread(img1_path, 0)
    img2 = cv2.imread(img2_path, 0)
    (score, diff) = structural_similarity(img1, img2, full=True)
    print(score)
    return score > threshold


def image_compare_RGB(img1_path,img2_path, threshold = 0.83):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    (score, diff) = structural_similarity(img1, img2, full=True, multichannel=True)
    return score > threshold


def match_tpl_loc_multi(target, tpl, threshold = 0.95):
    all_loc = []
    img_target = cv2.imread(target, 0)
    img_tpl = cv2.imread(tpl, 0)
    methods = [cv2.TM_CCOEFF_NORMED]
    for md in methods:
        result = cv2.matchTemplate(img_target, img_tpl, md)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if (max_val < threshold) : 
        return [-1, -1]
    loc = np.where(result >= threshold)
    temp_point = [-1, -1]
    for pt in zip(*loc[::-1]):
        if (temp_point == [-1, -1]):
            temp_point = [pt[0], pt[1]]
            all_loc.append((pt[0], pt[1]))
        dx = temp_point[0] - pt[0]
        dy = temp_point[1] - pt[1]
        dl = math.sqrt(dx ** 2 + dy ** 2)
        if (dl > 20):
            all_loc.append((pt[0], pt[1]))
            temp_point = [pt[0], pt[1]]
    return all_loc


def shadow_detect(target):
    img = cv2.imread(target)
    img_sum = np.sum(img,axis=2)
    std_img = np.std(img)
    std_img = np.where(img_sum<250,std_img,255)
    cv2.imshow("gray", std_img)
    
import ADBShell
import cv2
import math
import random
from config import SCREEN_SHOOT_SAVE_PATH,RES_PATH,ADB_ROOT
import time
import img_utils
import baidu_ocr
import json
import codecs


packet_name = "com.moefantasy.clover"
state = ""
floor_cnt = 0
template = [RES_PATH + "normal_battle.png",
            RES_PATH + "elite_battle.png",  RES_PATH + "normal_boss.png",
            RES_PATH + "super_boss.png",RES_PATH + "special_boss.png", 
            RES_PATH + "loot.png", RES_PATH + "event.png",
            RES_PATH + "shop.png"]
template_size = []
for tpl_path in template: #读各个点的大小
    tpl_img = cv2.imread(tpl_path)
    template_size.append(tpl_img.shape[1::-1])
path_tangle = 28
START_PERFORM_BOX = ((1154, 706), (227, 70))
SKIP_LOOT_BOX = ((622, 644), (200, 46))
BOTTOM_BOX = ((30, 735), (1300, 40))
CONFIRM_BOX = ((631, 689), (190, 58))
PERFORM_END_BOX = ((629, 532), (220, 55))
HP_UP_BOX = ((1031, 166), (259,441))
PORTAL_BOX = ((765, 355), (100, 150))
EVENT_TITLE_BOX = ((754, 123), (381, 34))
EVENT_OPT_BOX = ((1068, 243), (108, 40))
END_SHOP_BOX = ((1006, 688), (142, 46))
OPT_SPACE = 120
default_screenshoot = SCREEN_SHOOT_SAVE_PATH+"screenshoot.png"
res_map = {"start_perform": RES_PATH + "start_perform.png",
           "skip_loot": RES_PATH + "skip_loot.png",
           "end_perform": RES_PATH + "perform_end.png",
           "end_shop": RES_PATH + "shop_end.png"}
box_map = {"start_perform": START_PERFORM_BOX,
           "skip_loot": SKIP_LOOT_BOX,
           "event_opt": EVENT_OPT_BOX,
           "end_perform": PERFORM_END_BOX,
           "confirm": CONFIRM_BOX,
           "end_shop": END_SHOP_BOX}
file = codecs.open("config\\event_opt.json","r","utf-8")
EVENT_CHOOSE = json.loads(file.readline())
GIFT_BOX = (((234, 265), (210, 210)), ((607, 265), (210, 210)), ((981, 265), (210, 210)))
gift_template = (RES_PATH + "gift_hp_up.png", RES_PATH + "gift_lv_up.png", 
            RES_PATH + "gift_artifact.png")

def find_clickable_item(client):# TODO:重启游戏没做好
    find_cnt = 0
    up_flag = 1
    while (True):
        if (find_cnt > 10):
            restart_game(client)
            up_flag = -1
        client.get_screen_shoot()
        for i in range(0, 7) :
            loc = img_utils.match_tpl_loc(default_screenshoot, template[i])
            if (loc != [-1, -1]):
                return i, loc
        find_cnt += 1
        swipe_screen_angle(client, up_flag * random.randint(200, 220), path_tangle)
    
    
def find_all_clickable_item(client):#找下一层（模板匹配找可疑位置，结构化匹配确认）
    print("寻找下一关")
    find_max_time = 10
    all_items = []
    find_cnt = 0
    up_flag = 1
    while (True):
        if (find_cnt > find_max_time):
            restart_game(client)
            find_cnt = 0
            up_flag = -1
        if (up_flag == -1 and find_cnt > find_max_time):
            exit("未找到可点击对象")
        client.get_screen_shoot()
        for i in range(0, len(template)) :
        #for i in range(5, 6):
            locs = img_utils.match_tpl_loc_multi(default_screenshoot, template[i], 0.9)
            if (locs != [-1, -1]):
                for loc in locs:
                    client.get_screen_shoot("item.png",
                                            screen_range = (loc, tuple(template_size[i])))
                    if (img_utils.image_compare("screen_shoot\\item.png", template[i])):
                        #模板匹配无法识别出来不能点的点，得用结构化匹配再来一次
                        if (i == 1 or i == 2):
                            if (not img_utils.image_compare_RGB("screen_shoot\\item.png"
                                                            , template[i])):
                                continue
                        all_items.append((i, locs))
        if (all_items != []):
            return all_items
        find_cnt += 1
        swipe_screen_angle(client, up_flag * random.randint(300, 320), path_tangle)
    
    
def restart_game(client):#重启游戏
    print("重启游戏中")
    client.stop_app(packet_name)
    time.sleep(2)
    client.start_app(packet_name+"/com.hm.proj212.UnityPlayerActivity")
    time.sleep(30)
    client.get_mouse_click_random(((10, 10), (710, 395)))
    time.sleep(10)
    
    
    
def swipe_screen_angle(client, x, path_tangle):#斜向滑动屏幕
    y = int(x * math.tan(math.pi/180.0*path_tangle))
    point_o = (client.resolution[0]/2, client.resolution[1]/2)
    client.get_mouse_swipe(point_o, ([point_o[0]+x, point_o[1]+y]))
    

def choose_event_opt(client):#事件选择
    time.sleep(5)
    client.get_screen_shoot("event_title.png", EVENT_TITLE_BOX)
    title = baidu_ocr.image2text(SCREEN_SHOOT_SAVE_PATH + "event_title.png")
    if (title in EVENT_CHOOSE.keys()):
        for opt in EVENT_CHOOSE.get(title):
            BOX = ((EVENT_OPT_BOX[0][0], EVENT_OPT_BOX[0][1] + (int(opt)-1)*OPT_SPACE), 
                   EVENT_OPT_BOX[1])
            client.get_mouse_click_random(BOX)
            time.sleep(1)
            if (title == "未知晶体"):
                skip_loot(client)
        return True
    else:
        print("遭遇未识别事件：" + title)
        exit(0)

    
def skip_loot(client):
    print("寻找跳过按钮")
    if (block_until_img_exist(client, "skip_loot")):
        client.get_mouse_click_random(SKIP_LOOT_BOX)
        client.get_mouse_click_random(SKIP_LOOT_BOX)
        client.get_mouse_click_random(SKIP_LOOT_BOX)
        return True
    return False


def do_noting(client):
    time.sleep(0)


def block_until_img_exist(client, template_name, block_max_time = 6):#阻塞直到屏幕上出现对应图片
    wait_time = 0
    client.get_screen_shoot(screen_range=box_map.get(template_name))
    while(not img_utils.image_compare(default_screenshoot, res_map.get(template_name))):
        time.sleep(0.75)
        client.get_screen_shoot(screen_range=box_map.get(template_name))
        if (wait_time >= block_max_time):
            print("等待时间过长")
            return False
        wait_time += 1
    return True


def choose_gift(client):
    for i in range(0, 3):
        client.get_screen_shoot("gift.png", screen_range=GIFT_BOX[i])
        for j in range(0, 3):
            if (img_utils.image_compare("screen_shoot/gift.png", gift_template[j])):
                client.get_mouse_click_random(GIFT_BOX[i])
                time.sleep(0.5)
                client.get_mouse_click_random(box_map.get("confirm"))
                if (j == 2):
                    skip_loot(client)
                return True
    
    
    
def enter_portal(client):
    client.get_mouse_click_random(PORTAL_BOX)
    client.get_mouse_click_random(PORTAL_BOX)
    time.sleep(3)


def clickable_box_fix(box):
    box_prefix = (0, 125)
    box_size = (93, 33)
    return ((box[0], box[1]+box_prefix[1]), box_size)


def process_item(a, point_type, loc, state): 
    #point_type, loc = find_clickable_item(a)
    print("点击"+template[point_type])
    for i in range(0, 3):
        a.get_mouse_click_random(clickable_box_fix(loc))
    time.sleep(2)
    if (point_type >= 0 and point_type < 5): # 表演处理
        print("waiting....")
        a.get_screen_shoot(screen_range=START_PERFORM_BOX)
        if (block_until_img_exist(a, "start_perform")):
            state = "开始表演"
            a.get_mouse_click_random(START_PERFORM_BOX)
            a.get_mouse_click_random(START_PERFORM_BOX)
            time.sleep(5)
            if (block_until_img_exist(a, "end_perform", 20)):
                state = "表演结束"
                a.get_mouse_click_random(PERFORM_END_BOX)
                time.sleep(2)
                a.get_mouse_click_random(BOTTOM_BOX)
                a.get_mouse_click_random(BOTTOM_BOX)
                if (point_type > 0):
                    time.sleep(3)
                    skip_loot(a)   
                if (point_type > 2):
                    time.sleep(3)
                    choose_gift(a)
                time.sleep(3)
                a.get_mouse_click_random(HP_UP_BOX)
                time.sleep(0.5)
                a.get_mouse_click_random(CONFIRM_BOX)
                if (point_type == 2 or point_type == 3):
                    time.sleep(3)
                    enter_portal(a)
            return True
                
        
    if (point_type == 6): # 事件处理
        #开始事件
        state = "遭遇事件"
        if (not choose_event_opt(a)):
            exit(1)
        return True
    if (point_type == 5): # 宝箱处理
        state = "捡到宝箱"
        return skip_loot(a)
    if (point_type == 7): # 商店
        if (block_until_img_exist(a, "end_shop")):
             a.get_mouse_click_random(END_SHOP_BOX)
             a.get_mouse_click_random(END_SHOP_BOX)
             enter_portal(a)
             return True

if __name__ == '__main__' :
    state = "在大地图"
    next_flag = False
    a = ADBShell.ADBShell()
    while(True):
        next_flag = False
        a.get_screen_shoot()
        all_items = find_all_clickable_item(a)
        for item in all_items:
            for loc in item[1]:
                if (process_item(a, item[0], loc, state) == True):
                    next_flag = True
                    break
            if (next_flag == True):
                break
        
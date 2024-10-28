import math
import random
import sys
import time
import cv2
import cv
import yolov5 as yolo
import HID as keyboard
import signal
import threading


def handle_interrupt(signal, frame):
    print("程序被中断...")
    keyboard.press("stop")
    raise KeyboardInterrupt


map_coordinates = []
room_coordinates = []
huodong_coordinates = []
role_coordinate = (0, 0)

stop_drop = 0
role_num = ""
role_height = 0
map = ""
row_index = 0
col_index = 0

count = 0
pl_count = 0
door_count = 0
bug_count = 0
room_count = 0
ctrl_count = 0

roles = {
    "role_0": {
        "name": "召唤",
        "image": "static/npc/npc0.png",
        "height": 142,
        "speed_x": 680,
        "speed_y": 840,
        "skills": "s",
        "boss": "s",
    },
    "role_1": {
        "name": "气功",
        "image": "static/npc/npc1.png",
        "height": 158,
        "speed_x": 700,
        "speed_y": 835,
        "skills": "z",
        "boss": "w",
    },
    "role_2": {
        "name": "战法",
        "image": "static/npc/npc2.png",
        "height": 142,
        "speed_x": 700,
        "speed_y": 790,
        "skills": "weh",
        "boss": "f",
    },
    "role_3": {
        "name": "奶萝",
        "image": "static/npc/npc3.png",
        "height": 142,
        "speed_x": 720,
        "speed_y": 875,
        "skills": "w",
        "boss": "s",
    },
    "role_4": {
        "name": "剑魔",
        "image": "static/npc/npc4.png",
        "height": 168,
        "speed_x": 680,
        "speed_y": 830,
        "skills": "dy",
        "boss": "r",
    },
    "role_5": {
        "name": "气功2",
        "image": "static/npc/npc5.png",
        "height": 158,
        "speed_x": 650,
        "speed_y": 850,
        "skills": "sqx",
        "boss": "w",
    },
    "role_6": {
        "name": "四姨",
        "image": "static/npc/npc6.png",
        "height": 170,
        "speed_x": 635,
        "speed_y": 780,
        "skills": "whyx",
        "boss": "e",
    },
    "role_7": {
        "name": "刃影",
        "image": "static/npc/npc7.png",
        "height": 164,
        "speed_x": 635,
        "speed_y": 780,
        "skills": "th",
        "boss": "w",
    },
    "role_8": {
        "name": "女漫游",
        "image": "static/npc/npc8.png",
        "height": 178,
        "speed_x": 630,
        "speed_y": 770,
        "skills": "x",
        "boss": "e",
    },
    "role_9": {
        "name": "红眼",
        "image": "static/npc/npc9.png",
        "height": 180,
        "speed_x": 630,
        "speed_y": 780,
        "skills": "sh",
        "boss": "e",
    },
    "role_10": {
        "name": "审判",
        "image": "static/npc/npc10.png",
        "height": 180,
        "speed_x": 650,
        "speed_y": 760,
        "skills": "t",
        "boss": "d",
    },
    "role_11": {
        "name": "奶妈",
        "image": "static/npc/npc11.png",
        "height": 173,
        "speed_x": 740,
        "speed_y": 870,
        "skills": "r",
        "boss": "d",
    },
}


def yolov5():
    global stop_drop, room_count, ctrl_count
    time.sleep(0.3)
    data = yolo.find(0.6)
    if room_count % 2 == 0:
        which_room()
        room_count += 1

    drop_list = []
    monster_list = []
    door_list = []

    for item in data:
        if "boss" in item:
            skills = roles[role_num]["boss"]
            keyboard.press("right")
            time.sleep(0.3)
            keyboard.release("right")
            time.sleep(0.1)
            keyboard.press(skills)
            time.sleep(0.1)
            keyboard.release(skills)
            time.sleep(0.3)
        elif "monster" in item:
            if 50 < item["monster"][0] < 1080:
                if ctrl_count % 2 == 0:
                    monster_list.append(item["monster"])
                    ctrl_count += 1
        elif "drop" in item:
            drop_coordinates = (item["drop"][0], item["drop"][1] - 20)
            if drop_coordinates[1] > 350:
                drop_list.append(drop_coordinates)
        elif "door" in item:
            door_coordinates = (item["door"][0] + 20, item["door"][1] - 25)
            door_list.append(door_coordinates)

    if monster_list:
        ctrl(monster_list)
    elif drop_list:
        drop(drop_list)
    elif door_list:
        door(door_list)
    else:
        if again():
            door()


# 确定当前角色
def choose_role():
    global role_num, role_height
    cv_role = [cv2.imread(path["image"]) for key, path in roles.items()]
    role_data = cv.find(cv_role, list(roles.keys()), 0.8)

    role_num = list(role_data.keys())[0]
    role_name = roles[list(role_data.keys())[0]]["name"]
    role_height = roles[list(role_data.keys())[0]]["height"]
    print(f"当前角色：{role_name}, 身高：{role_height}")

    return True


# 翻牌，再次挑战
def again():
    global map, stop_drop, pl_count
    cv_card = [cv2.imread("static/card.png")]
    cv_again = [cv2.imread("static/again.png")]
    data_card = cv.find(cv_card, ["card"])

    if data_card:
        print("翻牌")
        stop_drop = 1
        keyboard.press("esc")
        time.sleep(0.1)
        keyboard.release("esc")
        again()
    else:
        data_again = cv.find(cv_again, ["again"])
        if data_again:
            keyboard.move(980, 713)
            cv_pl = [cv2.imread("static/pl.png")]
            data_pl = cv.find(cv_pl, ["pl"], 0.97)

            keyboard.press("0")
            time.sleep(0.1)
            keyboard.release("0")
            time.sleep(0.1)
            keyboard.press("/")
            time.sleep(0.1)
            keyboard.release("/")
            time.sleep(0.1)
            keyboard.press("x")
            time.sleep(0.1)
            keyboard.release("x")
            time.sleep(0.1)
            keyboard.press("x")
            time.sleep(0.1)
            keyboard.release("x")
            time.sleep(0.1)
            keyboard.press("x")
            time.sleep(0.1)
            keyboard.release("x")
            time.sleep(0.1)
            keyboard.press("x")
            time.sleep(0.1)
            keyboard.release("x")
            time.sleep(0.1)
            keyboard.press("x")
            time.sleep(0.1)
            keyboard.release("x")
            time.sleep(0.1)

            if data_pl:
                pl_count += 1
                if pl_count >= 5:
                    print("疲劳为0，切换角色")
                    map = ""
                    pl_count = 0
                    change_role()
            else:
                print("再次挑战")
                map = ""
                stop_drop = 0
                pl_count = 0
                return True

        else:
            return True


# 选择角色
def change_role():
    global role_num, role_height, speed_x, speed_y, map_coordinates, room_coordinates, huodong_coordinates, role_coordinate, stop_drop, map, row_index, col_index, count, pl_count, door_count, bug_count, room_count, ctrl_count
    cv_esc = [cv2.imread("static/esc.png")]
    time.sleep(0.5)
    keyboard.press("=")
    time.sleep(0.1)
    keyboard.release("=")
    time.sleep(0.1)
    keyboard.press("esc")
    time.sleep(0.1)
    keyboard.release("esc")
    time.sleep(8)
    if cv.find(cv_esc, ["esc"]):
        keyboard.press("esc")
        time.sleep(0.1)
        keyboard.release("esc")
    keyboard.press("esc")
    keyboard.move(608, 500)
    time.sleep(0.1)
    keyboard.release("esc")
    time.sleep(1)
    keyboard.click()
    time.sleep(3)
    keyboard.press("right")
    time.sleep(0.1)
    keyboard.release("right")
    time.sleep(0.1)
    keyboard.press("space")
    time.sleep(0.1)
    keyboard.release("space")
    time.sleep(0.1)
    role_num = ""
    speed_x = 0
    speed_y = 0
    map_coordinates = []
    room_coordinates = []
    huodong_coordinates = []
    role_coordinate = (0, 0)

    stop_drop = 0
    role_height = 0
    map = ""
    row_index = 0
    col_index = 0

    count = 0
    pl_count = 0
    door_count = 0
    bug_count = 0
    room_count = 0
    ctrl_count = 0
    go_to_fb()


# 进入风暴幽城
def go_to_fb():
    cv_sly = [cv2.imread("static/sly.png")]
    data_sly = cv.find(cv_sly, ["sly"])
    if data_sly:
        print("进入风暴幽城")
        keyboard.move(560, 211)
        time.sleep(0.3)
        keyboard.click()
        keyboard.move(625, 240)
        time.sleep(0.3)
        keyboard.click()
        time.sleep(0.3)
        keyboard.move(433, 608)
        time.sleep(0.3)
        keyboard.click()
        time.sleep(0.3)
        keyboard.move(431, 298)
        time.sleep(0.3)
        keyboard.click()
        time.sleep(0.3)
        keyboard.move(496, 489)
        time.sleep(0.3)
        keyboard.click()
        time.sleep(0.3)
        keyboard.move(466, 480)
        time.sleep(0.3)
        keyboard.click()
        time.sleep(0.3)
        keyboard.move(639, 418)
        time.sleep(0.3)
        keyboard.click()
        time.sleep(0.3)
        keyboard.press("right")
        time.sleep(2)
        keyboard.release("right")
        time.sleep(1)
        keyboard.move(335, 320)
        time.sleep(1)
        keyboard.click()
        time.sleep(1)
        keyboard.press("right")
        time.sleep(2)
        keyboard.release("right")
        time.sleep(1)
        keyboard.press("up")
        time.sleep(0.1)
        keyboard.release("up")
        time.sleep(1)
        keyboard.move(680, 470)
        time.sleep(1)
        keyboard.click()
        time.sleep(0.5)
        keyboard.press("right")
        time.sleep(0.1)
        keyboard.release("right")
        time.sleep(0.1)
        keyboard.press("right")
        time.sleep(0.1)
        keyboard.release("right")
        time.sleep(0.1)
        keyboard.press("space")
        time.sleep(0.1)
        keyboard.release("space")
        time.sleep(0.1)
        main()
    else:
        go_to_fb()


# 识别材料
def drop(drop_data):
    global stop_drop, map, row_index, col_index

    if drop_data and stop_drop == 0:
        drop_coordinates = drop_data[0]
        print(f"发现材料：{drop_coordinates}")
        if go(drop_coordinates):
            yolov5()
        else:
            return True
    else:
        if again():
            yolov5()


# 控制角色
def ctrl(monster_coordinates):
    global role_num

    skills = roles[role_num]["skills"]
    skill = skills[random.randint(0, len(skills) - 1)]

    if monster_coordinates:
        go(monster_coordinates[0])

        time.sleep(0.1)
        keyboard.press(skill)
        time.sleep(0.1)
        keyboard.release(skill)
        time.sleep(0.3)
        yolov5()
    else:
        yolov5()


# 确定地图
def which_map():
    global role_num, map, map_coordinates, room_coordinates, huodong_coordinates
    cv_map = [cv2.imread("static/map.png")]
    data_map = cv.find(cv_map, ["map"])
    map_coordinate = data_map.get("map", [])

    if 1243 <= map_coordinate[0] <= 1261 and 71 <= map_coordinate[1] <= 89:
        map = "map1"
        room_coordinates = (1162, 80)
    elif 1228 <= map_coordinate[0] <= 1246 and 53 <= map_coordinate[1] <= 71:
        map = "map2"
        room_coordinates = (1183, 62)
    elif 1246 <= map_coordinate[0] <= 1264 and 89 <= map_coordinate[1] <= 107:
        map = "map3"
        room_coordinates = (1183, 80)

    map_coordinates = map_coordinate

    if role_num != "role_3":
        keyboard.press("space")
        time.sleep(0.1)
        keyboard.release("space")
        time.sleep(0.5)
    keyboard.press("down")
    time.sleep(0.3)
    keyboard.release("down")
    time.sleep(0.1)

    return True


# 确定房间
def which_room():
    global map, map_coordinates, room_coordinates, huodong_coordinates, row_index, col_index, boss_ctrl
    cv_room = [cv2.imread("static/room.png")]
    data_room = cv.find(cv_room, ["room"])

    if data_room:
        room_coordinates = data_room.get("room", [])
    else:
        cv_room2 = [cv2.imread("static/room2.png")]
        data_room2 = cv.find(cv_room2, ["room2"])
        if data_room2:
            boss_ctrl = ""
            room_coordinates = data_room2.get("room2", [])
        else:
            cv_room3 = [cv2.imread("static/room3.png")]
            data_room3 = cv.find(cv_room3, ["room3"])
            if data_room3:
                room_coordinates = data_room3.get("room3", [])
            else:
                cv_huodong = [cv2.imread("static/huodong.png")]
                data_huodong = cv.find(cv_huodong, ["huodong"])
                if data_huodong:
                    room_coordinates = data_huodong.get("huodong", [])
                elif map == "map2":
                    row_index = 2
                    col_index = 2

    if map == "map1":
        map_top_left = (1155, 53)
        num_rows = 3
        num_cols = 6
        map_height = 18 * num_rows
        map_width = 18 * num_cols

    elif map == "map2" or map == "map3":
        map_top_left = (1174, 53)
        num_rows = 4
        num_cols = 5
        map_height = 18 * num_rows
        map_width = 18 * num_cols

    block_width = map_width / num_cols
    block_height = map_height / num_rows

    point_x = room_coordinates[0]
    point_y = room_coordinates[1]

    row_index = math.floor((point_y - map_top_left[1]) / block_height) + 1
    col_index = math.floor((point_x - map_top_left[0]) / block_width) + 1

    print(f"角色当前位于图 {map} 的第 {row_index} 行，第 {col_index} 列的房间中。")

    if room_bug():
        return True


def room_bug():
    global map, row_index, col_index, bug_count
    if (
        (
            map == "map1"
            and (row_index == 1 or row_index == 3)
            and (col_index == 2 or col_index == 3 or col_index == 4)
        )
        or (
            map == "map2"
            and row_index == 2
            and (col_index == 3 or col_index == 4 or col_index == 5)
        )
        or (map == "map3" and row_index == 2 and (col_index == 2 or col_index == 4))
    ):
        bug_count += 1
        if bug_count > 3:
            keyboard.press("esc")
            time.sleep(0.1)
            keyboard.release("esc")
            keyboard.move(730, 505)
            time.sleep(0.5)
            keyboard.click()
            time.sleep(0.1)
            keyboard.move(607, 419)
            time.sleep(0.5)
            keyboard.click()
            time.sleep(1)
            keyboard.press("right")
            time.sleep(3)
            keyboard.release("right")
            time.sleep(1)
            keyboard.press("up")
            time.sleep(0.1)
            keyboard.release("up")
            time.sleep(1)
            keyboard.move(680, 470)
            time.sleep(1)
            keyboard.click()
            time.sleep(0.5)
            keyboard.press("right")
            time.sleep(0.1)
            keyboard.release("right")
            time.sleep(0.1)
            keyboard.press("right")
            time.sleep(0.1)
            keyboard.release("right")
            time.sleep(0.1)
            keyboard.press("space")
            time.sleep(0.1)
            keyboard.release("space")
            time.sleep(0.1)
            map = ""
            row_index = 0
            col_index = 0
            main()
    else:
        bug_count = 0
        return True


# 找门
def door(door_coordinates=[]):
    global row_index, col_index, map, door_count, role_height

    if door_coordinates and door_coordinates[0][1] < 300:
        door_coordinates.remove(door_coordinates[0])

    if door_coordinates and door_coordinates[0][1] > 300:
        door_coordinate = ()
        for coordinate in door_coordinates:
            if map == "map2" and row_index == 2 and col_index == 2:
                if 200 < coordinate[0] < 1000:
                    door_coordinate = coordinate
                else:
                    continue
            else:
                if coordinate[0] > 950:
                    door_coordinate = coordinate
                else:
                    continue

        if door_coordinate:
            if go(door_coordinate):
                print("找到门")
                door_count = 0
                return True
        else:
            if door_count > 1:
                keyboard.press("up")
                time.sleep(0.5)
                keyboard.release("up")
                door_count = 0
                yolov5()
            else:
                time_count = 1
                if map == "map2" and row_index == 2 and col_index == 2:
                    time_count = 0.2
                keyboard.press("right")
                time.sleep(time_count)
                keyboard.release("right")
                door_count += 1
                door_coordinates = []

                yolov5()
    else:
        if door_count > 1:
            keyboard.press("up")
            time.sleep(0.5)
            keyboard.release("up")
            door_count = 0
            yolov5()
        else:
            time_count = 1
            if map == "map2" and row_index == 2 and col_index == 2:
                time_count = 0.2
            keyboard.press("right")
            time.sleep(time_count)
            keyboard.release("right")
            door_count += 1
            door_coordinates = []

            yolov5()


# 移动到指定坐标
def go(coordinates_2):
    global role_coordinate, role_height

    cv_role = [cv2.imread("static/role.png")]
    data_role = cv.find(cv_role, ["role"], height=role_height)
    coordinates_1 = data_role.get("role", [])

    if coordinates_1 == []:
        count = random.randint(0, 1)
        if count == 0:
            keyboard.press("left")
            time.sleep(0.2)
            keyboard.release("left")
        else:
            keyboard.press("right")
            time.sleep(0.2)
            keyboard.release("right")
        return True

    if (
        abs(role_coordinate[0] - coordinates_1[0]) < 10
        and abs(role_coordinate[1] - coordinates_1[1]) < 10
    ):
        keyboard.press("left")
        time.sleep(0.3)
        keyboard.release("left")
        return True

    role_coordinate = coordinates_1

    if coordinates_1 == [] or coordinates_2 == []:
        return

    x = coordinates_1[0] - coordinates_2[0]
    y = coordinates_1[1] - coordinates_2[1]

    speed_x = roles[role_num]["speed_x"]
    speed_y = roles[role_num]["speed_y"]

    thread_y = threading.Thread(target=go_y, args=(y, speed_y))
    thread_x = threading.Thread(target=go_x, args=(x, speed_x))
    thread_y.start()
    thread_x.start()

    time_x = abs(x) / speed_x
    time_y = abs(y) / speed_y

    if time_x > time_y:
        time.sleep(time_x)
    else:
        time.sleep(time_y)

    return True


def go_x(x, role_speed_x):
    time_ = abs(x) / role_speed_x if abs(x) / role_speed_x > 0 else 0.1
    if x > 0:
        keyboard.press("left")
        time.sleep(time_)
        keyboard.release("left")
    elif x < 0:
        keyboard.press("right")
        time.sleep(time_)
        keyboard.release("right")


def go_y(y, role_speed_y):
    time_ = abs(y) / role_speed_y if abs(y) / role_speed_y > 0 else 0.1
    time.sleep(0.2)
    if y > 0:
        keyboard.press("up")
        time.sleep(time_)
        keyboard.release("up")
    elif y < 0:
        keyboard.press("down")
        time.sleep(time_)
        keyboard.release("down")


def main():
    global role_num, map
    while True:
        try:
            if role_num == "":
                if choose_role():
                    pass
            if again():
                pass
            if len(map) == 0:
                if which_map():
                    pass
            yolov5()
        except KeyboardInterrupt as e:
            print(e)
            sys.exit()
        except:
            main()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    keyboard.press("stop")
    main()

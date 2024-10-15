import math
import time
import cv2
from cv import find
import keyboard
from ctrl import ctrl_

import signal


def handle_interrupt(signal, frame):
    print("程序被中断...")
    keyboard.press("stop")
    raise KeyboardInterrupt


room_coordinates = []
huodong_coordinates = []

drop_count = 0

boss_ctrl = ""
role_num = ""
map = ""
row_index = 0
col_index = 0

count = 0

roles = {
    "role_0": {
        "name": "召唤",
        "speed": 174,
        "image": "static/npc/npc0.png",
        "skill": {
            "boss": "s",
            "bug": "a",
            "map1": "ssss",
            "map2": "ssss",
            "map3": "ssss",
        },
    },
    "role_1": {
        "name": "气功",
        "speed": 133,
        "image": "static/npc/npc1.png",
        "skill": {
            "boss": "t",
            "bug": "a",
            "map1": "fwer",
            "map2": "rdwe",
            "map3": "fwer",
        },
    },
    "role_2": {
        "name": "战法",
        "speed": 151,
        "image": "static/npc/npc2.png",
        "skill": {
            "boss": "f",
            "bug": "a",
            "map1": "fffd",
            "map2": "dfdf",
            "map3": "dffd",
        },
    },
    "role_3": {
        "name": "奶萝",
        "speed": 178,
        "image": "static/npc/npc3.png",
        "skill": {
            "boss": "a",
            "bug": "a",
            "map1": "sses",
            "map2": "sess",
            "map3": "sess",
        },
    },
    "role_4": {
        "name": "剑魔",
        "speed": 125,
        "image": "static/npc/npc4.png",
        "skill": {
            "boss": "g",
            "bug": "s",
            "map1": "dfed",
            "map2": "rdwd",
            "map3": "dded",
        },
    },
    "role_5": {
        "name": "气功2",
        "speed": 117,
        "image": "static/npc/npc5.png",
        "skill": {
            "boss": "d",
            "bug": "a",
            "map1": "fweq",
            "map2": "rqwe",
            "map3": "fweq",
        },
    },
    "role_6": {
        "name": "四姨",
        "speed": 193,
        "image": "static/npc/npc6.png",
        "skill": {
            "boss": "t",
            "bug": "w",
            "map1": "werq",
            "map2": "rwqe",
            "map3": "werq",
        },
    },
    "role_7": {
        "name": "刃影",
        "speed": 142,
        "image": "static/npc/npc7.png",
        "skill": {
            "boss": "f",
            "bug": "s",
            "map1": "weda",
            "map2": "dwea",
            "map3": "awde",
        },
    },
    "role_8": {
        "name": "漫游",
        "speed": 135,
        "image": "static/npc/npc8.png",
        "skill": {
            "boss": "h",
            "bug": "s",
            "map1": "dwse",
            "map2": "wdse",
            "map3": "wdse",
        },
    },
    "role_9": {
        "name": "红眼",
        "speed": 131,
        "image": "static/npc/npc9.png",
        "skill": {
            "boss": "f",
            "bug": "a",
            "map1": "qwer",
            "map2": "wqer",
            "map3": "qrwa",
        },
    },
    "role_10": {
        "name": "奶爸",
        "speed": 151,
        "image": "static/npc/npc10.png",
        "skill": {
            "boss": "f",
            "bug": "a",
            "map1": "wdww",
            "map2": "awwd",
            "map3": "wdww",
        },
    },
    "role_11": {
        "name": "奶妈",
        "speed": 171,
        "image": "static/npc/npc11.png",
        "skill": {
            "boss": "a",
            "bug": "a",
            "map1": "qesd",
            "map2": "dqse",
            "map3": "dqes",
        },
    },
}


# 识别材料
def drop():
    global drop_count, boss_ctrl
    images_drop = {
        "G": "static/G.png",
        "suipian": "static/suipian.png",
        "wuhe": "static/wuhe.png",
        "equip": "static/equip.png",
    }
    cv_drop = [cv2.imread(path) for key, path in images_drop.items()]
    drop_data = find(cv_drop, list(images_drop.keys()))

    if drop_data and boss_ctrl == "":
        key = next(iter(drop_data))
        drop_coordinates = drop_data[key]
        print(f"发现{key}")

        if go(drop_coordinates):
            drop_count = 1
            drop()
        else:
            return True
    else:
        if drop_count == 1:
            keyboard.press("right")
            time.sleep(0.1)
            keyboard.release("right")
            time.sleep(0.1)
            keyboard.press("right")
            time.sleep(0.3)
            keyboard.release("right")
            drop_count = 0
        return True


# 控制角色
def ctrl():
    global role_num, map, row_index, col_index
    skill = roles[role_num]["skill"][map]
    if ctrl_(role_num, map, row_index, col_index, skill):
        if door():
            pass


# 确定当前角色
def choose_role():
    global role_num
    cv_role = [cv2.imread(path["image"]) for key, path in roles.items()]
    role_data = find(cv_role, list(roles.keys()))

    role_num = list(role_data.keys())[0]
    role_name = roles[list(role_data.keys())[0]]["name"]
    print(f"当前角色：{role_name}")


# 确定地图
def which_map():
    global map, room_coordinates, huodong_coordinates
    cv_map = [cv2.imread("static/map.png")]
    cv_huodong = [cv2.imread("static/huodong.png")]
    data_map = find(cv_map, ["map"])
    data_huodong = find(cv_huodong, ["huodong"])
    map_coordinates = data_map.get("map", [])
    huodong_coordinates = data_huodong.get("huodong", [])

    if 1243 <= map_coordinates[0] <= 1261 and 71 <= map_coordinates[1] <= 89:
        map = "map1"
        room_coordinates = (1162, 80)
    elif 1228 <= map_coordinates[0] <= 1246 and 53 <= map_coordinates[1] <= 71:
        map = "map2"
        room_coordinates = (1183, 62)
    elif 1246 <= map_coordinates[0] <= 1264 and 89 <= map_coordinates[1] <= 107:
        map = "map3"
        room_coordinates = (1183, 80)

    print(f"当前地图：{map}")
    return True


# 确定房间
def which_room():
    global map, room_coordinates, huodong_coordinates, row_index, col_index, boss_ctrl
    cv_room = [cv2.imread("static/room.png")]
    cv_room2 = [cv2.imread("static/room2.png")]
    data_room2 = find(cv_room2, ["room2"])
    data_room = find(cv_room, ["room"])

    if data_room:
        room_coordinates = data_room.get("room", [])
    elif data_room2:
        boss_ctrl = ""
        room_coordinates = data_room2.get("room2", [])
    else:
        room_coordinates = huodong_coordinates

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

    return True


# 找门
def door():
    cv_door = [cv2.imread("static/door.png")]
    if (
        (map == "map1" and row_index == 2 and col_index == 1)
        or (map == "map2" and row_index == 1 and col_index == 1)
        or (map == "map3" and row_index == 2 and col_index == 1)
    ):
        keyboard.press("left")
        time.sleep(0.3)
        keyboard.release("left")
    else:
        keyboard.press("left")
        time.sleep(0.5)
        keyboard.release("left")
        keyboard.press("up")
        time.sleep(0.2)
        keyboard.release("up")
    time.sleep(0.2)
    data_door = find(cv_door, ["door"])
    door_coordinates = data_door.get("door", [])
    if door_coordinates:
        if go(door_coordinates):
            return True


# 移动到指定坐标
def go(coordinates_2):
    try:
        cv_role = [cv2.imread("static/role.png")]
        data_role = find(cv_role, ["role"])
        coordinates_1 = data_role.get("role", [])

        if coordinates_1 == "" or coordinates_2 == "":
            return
        x = coordinates_1[0] - coordinates_2[0]
        y = coordinates_1[1] - coordinates_2[1]
        role_speed_x = 800
        role_speed_y = 310
        ctrl_x = []

        if y > 2:
            keyboard.press("up")
            time.sleep(0.1)
            keyboard.release("up")
            time.sleep(0.1)
            keyboard.press("up")
            time.sleep(abs(y) / role_speed_y)
            keyboard.release("up")
        elif y < -2:
            keyboard.press("down")
            time.sleep(0.1)
            keyboard.release("down")
            time.sleep(0.1)
            keyboard.press("down")
            time.sleep(abs(y) / role_speed_y)
            keyboard.release("down")

        if x > 2:
            keyboard.press("left")
            time.sleep(0.1)
            keyboard.release("left")
            time.sleep(0.1)
            keyboard.press("left")
            time.sleep(abs(x) / role_speed_x)
            keyboard.release("left")
            ctrl_x.append("left")
        elif x < -2:
            keyboard.press("right")
            time.sleep(0.1)
            keyboard.release("right")
            time.sleep(0.1)
            keyboard.press("right")
            time.sleep(abs(x) / role_speed_x)
            keyboard.release("right")
            ctrl_x.append("right")

        time.sleep(0.5)

        if ctrl_x[0] == "left":
            keyboard.press("right")
            time.sleep(0.1)
            keyboard.release("right")
            time.sleep(0.1)
            keyboard.press("right")
            time.sleep(abs(x) / role_speed_x)
            keyboard.release("right")

        return True

    except IndexError as e:
        print(e)
        door()


# 找boss
def boss():
    global role_num, boss_ctrl
    cv_boss = [cv2.imread("static/boss.png")]
    boss_data = find(cv_boss, ["boss"])
    boss_coordinates = boss_data.get("boss", [])
    if boss_coordinates:
        print("发现Boss")
        boss_ctrl = "boss"
        keyboard.press("right")
        time.sleep(0.3)
        keyboard.release("right")
        time.sleep(0.1)
        skill = roles[role_num]["skill"]["boss"]
        keyboard.press(skill)
        time.sleep(0.1)
        keyboard.release(skill)
        boss_coordinates = []
        return True
    else:
        return True


# 翻牌，再次挑战
def again():
    global map
    cv_card = [cv2.imread("static/card.png")]
    cv_again = [cv2.imread("static/again.png")]
    data_card = find(cv_card, ["card"])

    if data_card:
        print("翻牌")
        keyboard.press("esc")
        time.sleep(0.1)
        keyboard.release("esc")
        again()
    else:
        data_again = find(cv_again, ["again"])
        if data_again:
            keyboard.move(980, 713)

            print("再次挑战")
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
            map = ""

            cv_pl = [cv2.imread("static/pl.png")]
            data_pl = find(cv_pl, ["pl"], 0.97)

            if data_pl:
                print("疲劳为0，切换角色")
                change_role()
            else:
                return True
        else:
            return True


# 选择角色
def change_role():
    global role_num
    time.sleep(0.5)
    keyboard.press("=")
    time.sleep(0.1)
    keyboard.release("=")
    time.sleep(3)
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
    go_to_fb()


# 进入风暴幽城
def go_to_fb():
    cv_sly = [cv2.imread("static/sly.png")]
    data_sly = find(cv_sly, ["sly"])
    if data_sly:
        keyboard.press("right")
        time.sleep(1)
        keyboard.release("right")
        time.sleep(1)
        keyboard.move(335, 320)
        time.sleep(1)
        keyboard.click()
        time.sleep(1)
        keyboard.press("right")
        time.sleep(1)
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


def main():
    global role_num, map
    while True:
        try:
            if role_num == "":
                if choose_role():
                    pass
            if boss():
                pass
            if again():
                pass
            if len(map) == 0:
                if which_map():
                    pass
            if which_room():
                ctrl()
        except IndexError as e:
            print(e)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    keyboard.press("stop")
    main()

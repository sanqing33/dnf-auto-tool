import math
import random
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
map = ""
row_index = 0
col_index = 0

count = 0
door_count = 0

roles = {
    "role_0": {
        "name": "召唤",
        "image": "E:/Code/yolov5/dnf/static/npc/npc0.png",
        "skills": "s",
    },
    "role_1": {
        "name": "气功",
        "image": "E:/Code/yolov5/dnf/static/npc/npc1.png",
        "skills": "adfwer",
    },
    "role_2": {
        "name": "战法",
        "image": "E:/Code/yolov5/dnf/static/npc/npc2.png",
        "skills": "qwdwfwq",
    },
    "role_3": {
        "name": "奶萝",
        "image": "E:/Code/yolov5/dnf/static/npc/npc3.png",
        "skills": "ase",
    },
    "role_4": {
        "name": "剑魔",
        "image": "E:/Code/yolov5/dnf/static/npc/npc4.png",
        "skills": "asdfrew",
    },
    "role_5": {
        "name": "气功2",
        "image": "E:/Code/yolov5/dnf/static/npc/npc5.png",
        "skills": "qasf",
    },
    "role_6": {
        "name": "四姨",
        "image": "E:/Code/yolov5/dnf/static/npc/npc6.png",
        "skills": "qwerafgh",
    },
}


def yolov5():
    global stop_drop

    data = yolo.find(0.6)
    drop_list = []
    monster_list = []
    door_list = []

    for item in data:
        if "monster" in item:
            monster_list.append(item["monster"])
        elif "drop" in item:
            drop_coordinates = (item["drop"][0], item["drop"][1] - 20)
            if drop_coordinates[1] > 350:
                drop_list.append(drop_coordinates)
        elif "door" in item:
            door_coordinates = (item["door"][0] - 20, item["door"][1] - 25)
            door_list.append(door_coordinates)

    print(f"怪物：{monster_list}, 门：{door_list}, 掉落：{drop_list}")

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
    global role_num
    cv_role = [cv2.imread(path["image"]) for key, path in roles.items()]
    role_data = cv.find(cv_role, list(roles.keys()))

    role_num = list(role_data.keys())[0]
    role_name = roles[list(role_data.keys())[0]]["name"]
    print(f"当前角色：{role_name}")


# 翻牌，再次挑战
def again():
    global map, stop_drop
    cv_card = [cv2.imread("E:/Code/yolov5/dnf/static/card.png")]
    cv_again = [cv2.imread("E:/Code/yolov5/dnf/static/again.png")]
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
            stop_drop = 0

            cv_pl = [cv2.imread("E:/Code/yolov5/dnf/static/pl.png")]
            data_pl = cv.find(cv_pl, ["pl"], 0.97)

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
    cv_esc = [cv2.imread("E:/Code/yolov5/dnf/static/esc.png")]
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
    go_to_fb()


# 进入风暴幽城
def go_to_fb():
    cv_sly = [cv2.imread("E:/Code/yolov5/dnf/static/sly.png")]
    data_sly = cv.find(cv_sly, ["sly"])
    if data_sly:
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
        if go(drop_coordinates):
            yolov5()
        else:
            return True
    else:
        if again():
            yolov5()


# 控制角色
def ctrl(monster_coordinates):
    global role_num, map, row_index, col_index, boss_ctrl

    cv_role = [cv2.imread("E:/Code/yolov5/dnf/static/role.png")]
    data_role = cv.find(cv_role, ["role"])
    role_coordinates = data_role.get("role", [])

    skills = roles[role_num]["skills"]
    skill = skills[random.randint(0, len(skills) - 1)]

    if role_coordinates == []:
        keyboard.press(skill)
        time.sleep(0.1)
        keyboard.release(skill)
        time.sleep(0.1)
        keyboard.press("left")
        time.sleep(0.3)
        keyboard.release("left")

    if monster_coordinates:
        if monster_coordinates[0][0] > role_coordinates[0]:
            keyboard.press("right")
            time.sleep(0.3)
            keyboard.release("right")
        elif monster_coordinates[0][0] < role_coordinates[0]:
            keyboard.press("left")
            time.sleep(0.1)
            keyboard.release("left")

        if monster_coordinates[0][1] - role_coordinates[1] > 100:
            keyboard.press("down")
            time.sleep(0.3)
            keyboard.release("down")
        elif monster_coordinates[0][1] - role_coordinates[1] < -100:
            keyboard.press("up")
            time.sleep(0.3)
            keyboard.release("up")

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
    cv_map = [cv2.imread("E:/Code/yolov5/dnf/static/map.png")]
    cv_huodong = [cv2.imread("E:/Code/yolov5/dnf/static/huodong.png")]
    data_map = cv.find(cv_map, ["map"])
    data_huodong = cv.find(cv_huodong, ["huodong"])
    map_coordinate = data_map.get("map", [])
    huodong_coordinates = data_huodong.get("huodong", [])

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

    keyboard.press("space")
    time.sleep(0.1)
    keyboard.release("space")
    time.sleep(1)

    print(role_num)

    if role_num == "role_0":
        keyboard.press("down")
        time.sleep(0.1)
        keyboard.press("space")
        time.sleep(0.1)
        keyboard.release("down")
        keyboard.release("space")
        time.sleep(0.5)

    print(f"当前地图：{map}")
    return True


# 确定房间
def which_room():
    global map, map_coordinates, room_coordinates, huodong_coordinates, row_index, col_index, boss_ctrl
    cv_room = [cv2.imread("E:/Code/yolov5/dnf/static/room.png")]
    cv_room2 = [cv2.imread("E:/Code/yolov5/dnf/static/room2.png")]
    data_room2 = cv.find(cv_room2, ["room2"])
    data_room = cv.find(cv_room, ["room"])

    if data_room:
        room_coordinates = data_room.get("room", [])
    elif data_room2:
        boss_ctrl = ""
        room_coordinates = data_room2.get("room2", [])
    elif huodong_coordinates:
        room_coordinates = huodong_coordinates
    elif map == "map2":
        row_index = 2
        col_index = 2
    else:
        room_coordinates = map_coordinates

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
def door(door_coordinates=[]):
    global row_index, col_index, map, door_count

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
            print(f"发现门 {door_coordinate}")
            if go(door_coordinate):
                door_count = 0
                return True
        else:
            if door_count > 3:
                keyboard.press("left")
                time.sleep(0.7)
                keyboard.release("left")
                door_count = 0
                time.sleep(0.5)
                yolov5()
            else:
                keyboard.press("right")
                time.sleep(0.1)
                keyboard.release("right")
                time.sleep(0.1)
                keyboard.press("right")
                time.sleep(0.7)
                keyboard.release("right")

                door_count += 1
                door_coordinates = []

                if which_room():
                    yolov5()
    else:
        if door_count > 3:
            keyboard.press("left")
            time.sleep(0.7)
            keyboard.release("left")
            door_count = 0
            time.sleep(0.5)
            yolov5()
        else:
            keyboard.press("right")
            time.sleep(0.1)
            keyboard.release("right")
            time.sleep(0.1)
            keyboard.press("right")
            time.sleep(0.7)
            keyboard.release("right")

            door_count += 1
            door_coordinates = []

            if which_room():
                yolov5()


# 移动到指定坐标
def go(coordinates_2):
    global role_coordinate

    cv_role = [cv2.imread("E:/Code/yolov5/dnf/static/role.png")]
    data_role = cv.find(cv_role, ["role"])
    coordinates_1 = data_role.get("role", [])

    if (
        abs(role_coordinate[0] - coordinates_1[0]) < 10
        and abs(role_coordinate[1] - coordinates_1[1]) < 10
    ):
        keyboard.press("left")
        time.sleep(0.5)
        keyboard.release("left")
        return True

    role_coordinate = coordinates_1

    print(f"角色坐标 {coordinates_1}，移动到坐标 {coordinates_2}")

    if coordinates_1 == []:
        keyboard.press("left")
        time.sleep(0.5)
        keyboard.release("left")

    if coordinates_1 == [] or coordinates_2 == []:
        return

    x = coordinates_1[0] - coordinates_2[0]
    y = coordinates_1[1] - coordinates_2[1]
    role_speed_x = 800
    role_speed_y = 310

    if -20 < x < 20 and -10 < y < 10:
        keyboard.press("left")
        time.sleep(0.3)
        keyboard.release("left")

    thread_x = threading.Thread(target=go_x, args=(x, role_speed_x))
    thread_y = threading.Thread(target=go_y, args=(y, role_speed_y))
    thread_x.start()
    thread_y.start()

    time_x = abs(x) / role_speed_x
    time_y = abs(y) / role_speed_y

    if time_x > time_y:
        time.sleep(time_x)
    else:
        time.sleep(time_y)

    return True


def go_x(x, role_speed_x):
    if x > 2:
        keyboard.press("left")
        time.sleep(0.1)
        keyboard.release("left")
        time.sleep(0.1)
        keyboard.press("left")
        time.sleep(abs(x) / role_speed_x)
        keyboard.release("left")
    elif x < -2:
        keyboard.press("right")
        time.sleep(0.1)
        keyboard.release("right")
        time.sleep(0.1)
        keyboard.press("right")
        time.sleep(abs(x) / role_speed_x)
        keyboard.release("right")


def go_y(y, role_speed_y):
    time.sleep(0.2)
    if y > 2:
        keyboard.press("up")
        time.sleep(0.1)
        keyboard.release("up")
        time.sleep(0.1)
        keyboard.press("up")
        time.sleep(abs(y) / role_speed_y * 0.8)
        keyboard.release("up")
    elif y < -2:
        keyboard.press("down")
        time.sleep(0.1)
        keyboard.release("down")
        time.sleep(0.1)
        keyboard.press("down")
        time.sleep(abs(y) / role_speed_y)
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
            if which_room():
                yolov5()
        except:
            pass


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    keyboard.press("stop")
    main()

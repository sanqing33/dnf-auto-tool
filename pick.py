import time
import cv2
from cv import find
from keyboard import key_press

role_speed = 0

goods_images = {
    "role": "static/role.png",
    "G": "static/G.png",
    "suipian": "static/suipian.png",
    "wuhe": "static/wuhe.png",
    "wuhe2": "static/wuhe2.png",
    "equip": "static/equip.png",
    "equip2": "static/equip2.png",
}


# 获取角色移速
def get_role_speed(speed):
    global role_speed
    role_speed = speed


def pick(role, goods, key):
    operation_list = []

    x = role[0] - goods[0]
    y = role[1] - goods[1]

    print(f"发现{key}，与角色距离", x, y)

    if abs(role[0] - goods[0]) < 3:
        pass
    elif role[0] > goods[0]:
        key_press('left', abs(x) / role_speed / 5.5, 2)
        operation_list.append("left")
    elif role[0] < goods[0]:
        key_press('right', abs(x) / role_speed / 5.5, 2)
        operation_list.append("right")

    if role[1] > goods[1]:
        key_press('up', abs(y) / role_speed / 1.5)
        operation_list.append("up")
    elif role[1] < goods[1]:
        key_press('down', abs(y) / role_speed / 2.5)
        operation_list.append("down")

    time.sleep(0.1)
    key_press("x")
    time.sleep(0.1)

    # 倒序执行操作
    for op in operation_list[::-1]:
        if op == "left":
            key_press('right', abs(x) / role_speed / 5.5, 2)
        elif op == "right":
            key_press('left', abs(x) / role_speed / 5.5, 2)
        elif op == "up":
            key_press('down', abs(y) / role_speed / 1.5)
        elif op == "down":
            key_press('up', abs(y) / role_speed / 2.5)

    return True


def do_pick():
    time.sleep(0.2)
    cv_goods = [cv2.imread(path) for key, path in goods_images.items()]
    pick_data = find(cv_goods, list(goods_images.keys()), 0.8)

    keys = list(pick_data.keys())
    if len(keys) >= 2:
        role = pick_data.get("role", [])
        if not role:
            key_press('left')
            do_pick()
        goods = pick_data[keys[1]]
        if pick(role, goods, keys[1]):
            do_pick()
    return True


if __name__ == "__main__":
    get_role_speed(140)
    do_pick()

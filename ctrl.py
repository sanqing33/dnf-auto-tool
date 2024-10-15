import time
import keyboard


def key_press(key, delay=0.1, num=1):
    keyboard.press(key)
    if num > 1:
        time.sleep(0.1)
        keyboard.release(key)
        time.sleep(0.1)
        keyboard.press(key)
    time.sleep(delay)
    keyboard.release(key)


def ctrl_(role, map, row_index, col_index, skill):
    if map == "map1":
        if ctrl_map1(role, row_index, col_index, skill):
            return True
    elif map == "map2":
        if ctrl_map2(role, row_index, col_index, skill):
            return True
    elif map == "map3":
        if ctrl_map3(role, row_index, col_index, skill):
            return True


def ctrl_map1(role, row_index, col_index, skill):
    from main import drop

    if row_index == 1 and (col_index == 2 or col_index == 4):
        key_press(skill[3])
        time.sleep(0.5)
        key_press("left", 0.5, 2)
        key_press("down", 0.2)
        key_press("right", 0.5, 2)
        key_press("down", 0.2)
        if drop():
            pass

    if row_index == 2 and col_index == 1:
        if role == "role_0":
            key_press("down", num=2)
            key_press("space")
            time.sleep(2)
            key_press("s")
            time.sleep(1)
        elif role == "role_3":
            pass
        else:
            print("加buff")
            key_press("space")
            time.sleep(1)
    if row_index == 2 and col_index == 2:
        key_press("right", 0.5, 2)
        key_press("down", 0.2)
        key_press(skill[0])
        time.sleep(0.5)
        key_press("right", 0.5, 2)
        if drop():
            key_press("right", 0.5, 2)
    if row_index == 2 and col_index == 3:
        key_press("right", 0.5, 2)
        key_press(skill[1])
        time.sleep(0.5)
        key_press("right", 0.5, 2)
        if drop():
            key_press("right", 0.5, 2)
    if row_index == 2 and col_index == 4:
        key_press("right", 0.5, 2)
        key_press("down", 0.2)
        key_press(skill[2])
        time.sleep(0.5)
        key_press("right", 0.5, 2)
        if drop():
            key_press("right", 0.5, 2)
    if row_index == 2 and col_index == 5:
        key_press("right", 0.5, 2)
        key_press(skill[3])
        time.sleep(0.5)
        key_press("right", 0.5, 2)
        if drop():
            key_press("right", 0.5, 2)

    return True


def ctrl_map2(role, row_index, col_index, skill):
    from main import drop

    if row_index == 2 and col_index == 3:
        key_press(skill[3])
        time.sleep(0.5)
        key_press("down", 0.5, 2)
        key_press("left", 0.2)
        key_press("up", 0.5, 2)
        key_press("left", 0.2)
        key_press("up", 0.5, 2)
        key_press("left", 0.8, 2)
        if drop():
            pass

    if row_index == 1 and col_index == 1:
        if role == "role_0":
            key_press("down", num=2)
            key_press("space")
            time.sleep(2)
            key_press("s")
            time.sleep(1)
        elif role == "role_3":
            pass
        else:
            print("加buff")
            key_press("space")
            time.sleep(1)
    if row_index == 2 and col_index == 1:
        key_press("down", 0.5)
        key_press("left", 0.3)
        key_press(skill[0])
        time.sleep(0.5)
        if drop():
            key_press("right", 0.5, 2)
    if row_index == 2 and col_index == 2:
        key_press("right", 0.5, 2)
        key_press(skill[1])
        time.sleep(0.5)
        if drop():
            key_press("up", 0.5)
            key_press("right", 0.5, 2)
    if row_index == 1 and col_index == 2:
        key_press("up", 0.5)
        key_press("left")
        key_press(skill[2])
        time.sleep(1)
        if drop():
            key_press("right", 0.5, 2)
    if row_index == 1 and col_index == 3:
        key_press("right", 0.5, 2)
        key_press(skill[3])
        time.sleep(0.5)
        key_press("right", 0.5, 2)
        if drop():
            key_press("right", 0.5, 2)

    return True


def ctrl_map3(role, row_index, col_index, skill):
    from main import drop

    if row_index == 2 and (col_index == 2 or col_index == 4):
        key_press(skill[3])
        time.sleep(0.5)
        key_press("left", 0.5, 2)
        key_press("down", 0.3)
        key_press("right", 0.5, 2)
        key_press("down", 0.3)
        if drop():
            pass

    if row_index == 2 and col_index == 1:
        if role == "role_0":
            key_press("down", num=2)
            key_press("space")
            time.sleep(2)
            key_press("s")
            time.sleep(1)
        elif role == "role_3":
            pass
        else:
            print("加buff")
            key_press("space")
            time.sleep(1)
    if row_index == 3 and col_index == 1:
        key_press("down", 0.5)
        key_press("right", 0.3, 2)
        key_press(skill[0])
        time.sleep(0.5)
        key_press("right", 0.5, 2)
        if drop():
            key_press("right", 0.5, 2)
    if row_index == 3 and col_index == 2:
        key_press("right", 0.5, 2)
        key_press("down", 0.2)
        key_press(skill[1])
        time.sleep(0.5)
        key_press("right", 0.5, 2)
        if drop():
            key_press("right", 0.5, 2)
    if row_index == 3 and col_index == 3:
        key_press("right", 0.5, 2)
        key_press(skill[2])
        time.sleep(0.5)
        key_press("right", 0.5, 2)
        if drop():
            key_press("right", 0.5, 2)
    if row_index == 3 and col_index == 4:
        key_press("right", 0.5, 2)
        key_press(skill[3])
        time.sleep(0.5)
        key_press("right", 0.5, 2)
        if drop():
            key_press("right", 0.5, 2)

    return True

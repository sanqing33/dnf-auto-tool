import math
import time
import cv2
import numpy as np
import pyautogui


def draw_rectangle(name, top_left, bottom_right):
    if name == "role":
        bottom_right = (bottom_right[0], bottom_right[1] + 155)
    elif name == "G":
        top_left = (top_left[0] - 35, top_left[1])
        bottom_right = (bottom_right[0] + 5, bottom_right[1] + 23)
    elif name == "suipian" or name == "wuhe":
        bottom_right = (bottom_right[0], bottom_right[1] + 23)
    elif name == "room":
        bottom_right = (bottom_right[0], bottom_right[1] - 7)
    elif name == "map" or name == "huodong":
        top_left = (top_left[0] + 6, top_left[1] + 8)
        bottom_right = (bottom_right[0] - 8, bottom_right[1] - 8)

    return top_left, bottom_right


def distance(tuple1, tuple2):
    return math.sqrt((tuple2[0] - tuple1[0]) ** 2 + (tuple2[1] - tuple1[1]) ** 2)


def find(subimages, keys, threshold=0.7):
    # 存储已识别的坐标
    coordinates = []
    result_dict = {}

    screenshot = pyautogui.screenshot(region=(0, 0, 1280, 720))
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    subimage_names = keys
    subimages_with_names = list(zip(subimages, subimage_names))

    # 定义在HSV颜色空间中的范围
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    for subimage, name in subimages_with_names:
        if subimage is None:
            print(f"Error: Failed to read image for {name}. Check file path.")
            continue
        sub_gray = cv2.cvtColor(subimage, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(img_gray, sub_gray, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        h, w = subimage.shape[:2]
        for pt in zip(*locations[::-1]):
            top_left = pt
            bottom_right = (top_left[0] + w, top_left[1] + h)

            if name == "map":
                # 获取识别出的目标物体所在区域图像并转换为HSV颜色空间
                sub_image_found = frame[
                    top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]
                ]
                sub_image_hsv = cv2.cvtColor(sub_image_found, cv2.COLOR_BGR2HSV)

                # 对识别出的部分进行红色筛选
                mask1 = cv2.inRange(sub_image_hsv, lower_red1, upper_red1)
                mask2 = cv2.inRange(sub_image_hsv, lower_red2, upper_red2)
                mask = cv2.bitwise_or(mask1, mask2)
                red_count = np.count_nonzero(mask)

                if red_count <= 50:
                    continue

            # 如果不是map相关的name则直接处理（不进行颜色筛选）
            top_left_count = tuple(map(int, top_left))
            bottom_right_count = tuple(map(int, bottom_right))

            x = int(top_left_count[0] + (bottom_right_count[0] - top_left_count[0]) / 2)
            y = int(top_left_count[1] + (bottom_right_count[1] - top_left_count[1]) / 2)

            # 判断是否与已识别的坐标过于接近
            add_tuple = True
            for existing_tuple in coordinates:
                if (
                    (x - existing_tuple[0]) ** 2 + (y - existing_tuple[1]) ** 2
                ) ** 0.5 <= 50:
                    add_tuple = False
                    break

            if add_tuple:
                coordinates.append((x, y))
                top_left, bottom_right = draw_rectangle(name, top_left, bottom_right)

                if (name == "room" or name == "huodong") and not (
                    top_left[0] >= 1160
                    and top_left[1] >= 30
                    and bottom_right[0] <= 1280
                    and bottom_right[1] <= 120
                ):
                    continue

                if name == "door" and top_left[0] < 900:
                    continue

                if (name == "G" or name == "suipian" or name == "wuhe") and top_left[
                    1
                ] < 400:
                    continue

                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    name,
                    (top_left[0], top_left[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1,
                )
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))
                result_dict[name] = (
                    top_left[0] + (bottom_right[0] - top_left[0]) / 2,
                    bottom_right[1],
                )

    # cv2.imshow("Screen", frame)
    # cv2.waitKey(1)

    return result_dict


if __name__ == "__main__":
    cv_images = {
        "pl": "static/pl.png",
    }
    cv = [cv2.imread(path) for key, path in cv_images.items()]

    while True:
        find(cv, list(cv_images.keys()), 0.99)
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(date)

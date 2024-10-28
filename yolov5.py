import pyautogui
import torch
import cv2
import numpy as np
import time

model = torch.hub.load(".", "custom", path="best3.pt", source="local")
import warnings

warnings.filterwarnings("ignore")


def find(threshold=0.7):
    result_list = []

    screenshot = pyautogui.screenshot(region=(0, 0, 1280, 720))
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    results = model(frame)

    for i in range(len(results.xyxy[0])):
        x1, y1, x2, y2, conf, cls = results.xyxy[0][i]
        class_name = model.names[int(cls)]

        if conf > threshold:
            text = f"{class_name}: {int(conf * 100)}%"

            if class_name == "role":
                y2 = y2 + 150

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(
                frame,
                text,
                (int(x1), int(y1)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            center_x = int(x1 + (x2 - x1) / 2)
            center_y = int(y2)
            result = {}
            result[class_name] = (center_x, center_y)

            result_list.append(result)

    # cv2.imshow("img", frame)
    # cv2.waitKey(1)

    return result_list


if __name__ == "__main__":
    while True:
        find(0.1)

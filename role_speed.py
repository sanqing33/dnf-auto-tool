import time
import HID as keyboard
import cv2
import cv


def role_speed():
    speed_x_values = []
    speed_y_values = []

    cv_role = [cv2.imread("static/role.png")]

    for _ in range(5):
        keyboard.press("left")
        time.sleep(0.3)
        keyboard.release("left")
        time.sleep(0.1)
        keyboard.press("up")
        time.sleep(0.3)
        keyboard.release("up")
        time.sleep(0.1)
        keyboard.press("down")
        time.sleep(0.25)
        keyboard.release("down")
        time.sleep(0.5)

        data_role_start = cv.find(cv_role, ["role"])
        role_start = data_role_start.get("role", [])
        keyboard.press("right")
        time.sleep(0.2)
        keyboard.release("right")
        time.sleep(0.2)
        keyboard.press("up")
        time.sleep(0.2)
        keyboard.release("up")
        time.sleep(0.5)
        data_role_end = cv.find(cv_role, ["role"])
        role_end = data_role_end.get("role", [])

        speed_x = abs(role_end[0] - role_start[0]) / 0.2
        speed_y = abs(role_end[1] - role_start[1]) / 0.2

        speed_x_values.append(speed_x)
        speed_y_values.append(speed_y)

    speed_x_values.sort()
    speed_y_values.sort()
    speed_x_values = speed_x_values[1:-1]
    speed_y_values = speed_y_values[1:-1]

    average_speed_x = sum(speed_x_values) / len(speed_x_values)
    average_speed_y = sum(speed_y_values) / len(speed_y_values)

    print(f"平均移速：x: {average_speed_x}, y: {average_speed_y}")

    return True


if __name__ == "__main__":
    role_speed()

import socket
import time

# 创建UDP套接字
UDP_IP = "192.168.1.9"
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_message(key, state, x=0, y=0):
    x_str = str(int(x * 1.035)).zfill(4)
    y_str = str(int(y * 1.035)).zfill(4)
    message = f"{key},{state},{x_str},{y_str}"
    print("Sending message:", message)
    sock.sendto(message.encode("utf-8"), (UDP_IP, UDP_PORT))


def send(key, state):

    if key == "up":
        key = "8"
    elif key == "down":
        key = "2"
    elif key == "left":
        key = "4"
    elif key == "right":
        key = "6"
    elif key == "esc":
        key = "5"
    elif key == "space":
        key = " "

    send_message(key, state)


def press(key):
    send(key, "press")


def release(key):
    send(key, "relea")


def move(x, y):
    send_message("mouse", "move_", x, y)


def click():
    send_message("mouse", "click")


if __name__ == "__main__":
    move(608, 500)
    time.sleep(1)
    move(335, 320)

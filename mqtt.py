import time
import paho.mqtt.publish as publish

broker = "101.34.255.5"
port = 1883
topic = "mqtt/keyboard"


def key_press(key, duration=0.1, num=1):
    if key == "up":
        key = '8'
    elif key == "down":
        key = '2'
    elif key == "left":
        key = '4'
    elif key == "right":
        key = '6'
    elif key == "esc":
        key = '5'
    elif key == "space":
        key = ' '

    send_mqtt_message(key, duration, num)

    time.sleep(duration * num)


def send_mqtt_message(key, duration, num):
    message = f"{key},{duration},{num}"
    publish.single(topic, message, hostname=broker, port=port)


if __name__ == "__main__":
    key_press("up", 3, 2)
    key_press("down", 0.1, 1)
    key_press("left", 0.1, 1)
    key_press("right", 0.1, 1)

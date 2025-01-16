from gpiozero import PWMOutputDevice, Servo
from evdev import InputDevice, ecodes
import numpy as np
import csv
import time
import sys

# DCモーター設定
motor_pwm_forward = PWMOutputDevice(pin=12)  # 前進用
motor_pwm_backward = PWMOutputDevice(pin=13)  # 後進用

# サーボモーター設定
servo = Servo(12)

# コントローラー設定
device = InputDevice('/dev/input/event0')

# マッピング関数
def map_value(value, in_min, in_max, out_min, out_max):
    return np.interp(value, [in_min, in_max], [out_min, out_max])

# モーター制御関数
def forward(speed):
    motor_pwm_forward.value = speed / 100  # gpiozeroでは0.0～1.0の範囲で指定
    motor_pwm_backward.value = 0.0  # 後進ピンは停止

def backward(speed):
    motor_pwm_forward.value = 0.0  # 前進ピンは停止
    motor_pwm_backward.value = speed / 100

# サーボ制御関数
def control_servo(angle):
    normalized_angle = map_value(angle, 5.7, 10, -1, 1)  # Servo expects -1 to +1
    servo.value = normalized_angle

# 動作登録機能
def record_actions(filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'speed', 'servo_angle'])  # ヘッダーを書き込み
        start_time = time.time()

        print("動作登録を開始 (終了: Ctrl+C)")
        try:
            for event in device.read_loop():
                if event.type == ecodes.EV_ABS:
                    current_time = time.time() - start_time

                    if event.code == ecodes.ABS_GAS:
                        speed = round(map_value(event.value, 0, 1023, 0, 100))
                        forward(speed)
                        writer.writerow([current_time, speed, None])

                    elif event.code == ecodes.ABS_BRAKE:
                        speed = round(map_value(event.value, 0, 1023, 0, 100))
                        backward(speed)
                        writer.writerow([current_time, -speed, None])

                    elif event.code == ecodes.ABS_X:
                        angle = 5.7 + (event.value / 21845)
                        control_servo(angle)
                        writer.writerow([current_time, None, angle])

        except KeyboardInterrupt:
            print("動作登録を終了")

# 動作再生機能
def replay_actions(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        print("動作再生を開始")
        start_time = time.time()

        for row in reader:
            elapsed_time = float(row['time'])
            while time.time() - start_time < elapsed_time:
                pass  # タイミングを同期

            speed = row['speed']
            angle = row['servo_angle']

            if speed:
                speed = float(speed)
                if speed > 0:
                    forward(speed)
                else:
                    backward(abs(speed))

            if angle:
                control_servo(float(angle))

        print("動作再生を終了")

# メイン関数
def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <mode> <filename>")
        print("mode: record or replay")
        sys.exit(1)

    mode = sys.argv[1]
    filename = sys.argv[2]

    if mode == 'record':
        record_actions(filename)
    elif mode == 'replay':
        replay_actions(filename)
    else:
        print("Invalid mode. Use 'record' or 'replay'.")

if __name__ == '__main__':
    main()

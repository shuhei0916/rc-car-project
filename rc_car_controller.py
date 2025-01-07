from gpiozero import PWMOutputDevice, Servo
from evdev import InputDevice, ecodes
import numpy as np

# DCモーター設定
motor_pwm_forward = PWMOutputDevice(pin=29)  # 前進用
motor_pwm_backward = PWMOutputDevice(pin=31)  # 後進用

# サーボモーター設定
servo = Servo(11)

# コントローラー設定
device = InputDevice('/dev/input/event0')

# マッピング関数
def map_value(value, in_min, in_max, out_min, out_max):
    return np.interp(value, [in_min, in_max], [out_min, out_max])

# モーター制御関数
def forward(speed):
    print(f"Going Forward at {speed}%")
    motor_pwm_forward.value = speed / 100  # gpiozeroでは0.0～1.0の範囲で指定
    motor_pwm_backward.value = 0.0  # 後進ピンは停止

def backward(speed):
    print(f"Going Backward at {speed}%")
    motor_pwm_forward.value = 0.0  # 前進ピンは停止
    motor_pwm_backward.value = speed / 100

# サーボ制御関数
def control_servo(angle):
    # Servo expects values in range -1 to +1, so map to this range
    normalized_angle = map_value(angle, 5.7, 10, -1, 1)
    print(f"Servo Angle (normalized): {normalized_angle}")
    servo.value = normalized_angle

def main():
    # イベントループ
    for event in device.read_loop():
        if event.type == ecodes.EV_ABS:
            # DCモーター制御
            if event.code == ecodes.ABS_GAS:
                speed = round(map_value(event.value, 0, 1023, 0, 100))
                forward(speed)
            elif event.code == ecodes.ABS_BRAKE:
                speed = round(map_value(event.value, 0, 1023, 0, 100))
                backward(speed)
            
            # サーボ制御
            elif event.code == ecodes.ABS_X:
                angle = 5.7 + (event.value / 21845)  # 入力値を適切に変換
                control_servo(angle)
    
    
if __name__ == '__main__':
    main()
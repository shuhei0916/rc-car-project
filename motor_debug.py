from gpiozero import Servo, PWMOutputDevice
import time

# モーター設定
motor_pwm_forward = PWMOutputDevice(pin=12)  # 前進用ピン
motor_pwm_backward = PWMOutputDevice(pin=13)  # 後進用ピン

# サーボモーター設定
servo = Servo(12)  # GPIO 11 ピンに接続

def dc_motor_test():
    print("モーターを前進させます...")
    motor_pwm_forward.value = 0.5  # 50% の速度で前進
    motor_pwm_backward.value = 0.0  # 後進は停止
    time.sleep(2)  # 2秒間動作

    print("モーターを後進させます...")
    motor_pwm_forward.value = 0.0  # 前進を停止
    motor_pwm_backward.value = 0.5  # 50% の速度で後進
    time.sleep(2)  # 2秒間動作

    print("モーターを停止します...")
    motor_pwm_forward.value = 0.0
    motor_pwm_backward.value = 0.0
    print("動作確認終了")

def servo_test():
    print("サーボモーターのテストを開始します。")

    print("サーボを最左 (最小角度) に移動します...")
    servo.min()  # 最小角度（-1.0）
    time.sleep(2)

    print("サーボを中央 (中間角度) に移動します...")
    servo.mid()  # 中間角度（0.0）
    time.sleep(2)

    print("サーボを最右 (最大角度) に移動します...")
    servo.max()  # 最大角度（+1.0）
    time.sleep(2)

    print("サーボモーターの動作確認が完了しました。")


if __name__ == "__main__":
    print("DCモーターの動作確認を開始します...")
    dc_motor_test()

    print("\nサーボモーターの動作確認を開始します...")
    servo_test()

    print("\nすべての動作確認が完了しました。")
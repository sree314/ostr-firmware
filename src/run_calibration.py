import turtle
import time

v = True

# wait until button is pushed
while not turtle.isButtonPushed():
    turtle.leftLED.value = v
    turtle.rightLED.value = not v
    time.sleep(0.5)
    v = not v

turtle.leftLED.value = False
turtle.rightLED.value = False

import wheel_calibration


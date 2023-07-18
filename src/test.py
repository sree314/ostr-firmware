# circuit python
#
# test.py
#
# Tests turtle functionality. Requires the board to be powered on
# through the batteries.
#
# To run this, connect via serial console. Then, hit any key to enter the REPL. Type:
#
#    import test
#     test.test()
#
# or run individual tests.


import cpturtle as turtle
import time
import simpleio

def test_front_leds():
    print('testing front LEDs')
    for led in [turtle.leftLED, turtle.rightLED]:
        led.value = True
        time.sleep(0.5)

    for led in [turtle.leftLED, turtle.rightLED]:
        led.value = False

def test_piezo():
    print('Testing speaker')
    simpleio.tone(turtle.PIEZO_PIN, 400, duration=0.5)

def test_servo():
    # requires power to be on
    print('Testing servo -- needs board power to be switched on')
    print('Pen up')
    turtle.servo.angle = 55
    time.sleep(1)
    print('Pen down')
    turtle.servo.angle = 140
    time.sleep(1)

def test_steppers():
    # for now, just use forward/backward
    print('Testing steppers')
    print('Moving forward')
    turtle.forward(50)
    time.sleep(1)
    print('Moving backward')
    turtle.backward(50)
    time.sleep(1)

def test_emitters():
    det = [turtle.rightDetector, turtle.leftDetector]

    print('Testing emitters and detectors')
    ref1 = [d.value for d in det]
    print('Detector IR led OFF values -- Pass #1')
    print(ref1)

    print('Switching IR leds ON')
    turtle.emitter.value = True
    time.sleep(0.1)

    onv = [d.value for d in det]
    print('Detector IR led ON values')
    print(onv)

    print('Switching IR leds OFF')
    turtle.emitter.value = False
    time.sleep(0.1)

    ref2 = [d.value for d in det]
    print('Detector IR led OFF values -- Pass #2')
    print(ref2)

    print("These values should be large", [x - y for (x, y) in zip(ref1, onv)])
    print("These values should be small", [x - y for (x, y) in zip(ref1, ref2)])

def test_button():
    print('Testing button -- will execute for 5 seconds. Press and hold button during this period.')
    for i in range(5*2):
        pushed = not turtle.button.value
        print("button is", "PUSHED" if pushed else "NOT PUSHED")
        time.sleep(0.5)

def test():
    test_piezo()
    test_front_leds()
    test_emitters()

    test_servo()
    test_steppers()
    test_button()

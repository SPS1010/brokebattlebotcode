from machine import Pin, PWM
import time

# motor control pins
motor_a_forward = Pin(0, Pin.OUT)
motor_a_backward = Pin(1, Pin.OUT)
motor_b_forward = Pin(2, Pin.OUT)
motor_b_backward = Pin(3, Pin.OUT)
weapon_motor = Pin(4, Pin.OUT)

# PWM for speed control
pwm_a = PWM(motor_a_forward)
pwm_a.freq(1000)
pwm_b = PWM(motor_b_forward)
pwm_b.freq(1000)
pwm_weapon = PWM(weapon_motor)
pwm_weapon.freq(1000)

rc_ch1 = Pin(10, Pin.IN)  # forward/backward
rc_ch2 = Pin(11, Pin.IN)  # left/right
rc_ch3 = Pin(12, Pin.IN)  # weapon control
rc_ch4 = Pin(13, Pin.IN)  # spinner control
def read_pwm(pin):
    pulse_start = time.ticks_us()
    while pin.value() == 0:
        pulse_start = time.ticks_us()
    while pin.value() == 1:
        pulse_end = time.ticks_us()
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    return pulse_duration
def control_spinner():
    global spinner_on
    if spinner_on:
        pwm_weapon.duty_u16(0)
        spinner_on = False
    else:
        pwm_weapon.duty_u16(65535) 
        spinner_on = True
spinner_on = False
try:
    while True:
        ch1_pulse = read_pwm(rc_ch1)
        ch2_pulse = read_pwm(rc_ch2)
        ch3_pulse = read_pwm(rc_ch3)
        ch4_pulse = read_pwm(rc_ch4)
        ch1_value = (ch1_pulse - 1500) / 500.0
        ch2_value = (ch2_pulse - 1500) / 500.0
        ch3_value = (ch3_pulse - 1500) / 500.0
        ch4_value = (ch4_pulse - 1500) / 500.0
        if ch1_value > 0:
            pwm_a.duty_u16(int(ch1_value * 65535))
            pwm_b.duty_u16(int(ch1_value * 65535))
            motor_a_backward.low()
            motor_b_backward.low()
        elif ch1_value < 0:
            pwm_a.duty_u16(0)
            pwm_b.duty_u16(0)
            motor_a_backward.high()
            motor_b_backward.high()
        else:
            pwm_a.duty_u16(0)
            pwm_b.duty_u16(0)
            motor_a_backward.low()
            motor_b_backward.low()
        if ch2_value > 0:
            pwm_a.duty_u16(0)
            pwm_b.duty_u16(int(ch2_value * 65535))
            motor_a_backward.low()
            motor_b_backward.low()
        elif ch2_value < 0:
            pwm_a.duty_u16(int(abs(ch2_value) * 65535))
            pwm_b.duty_u16(0)
            motor_a_backward.low()
            motor_b_backward.low()
        else:
            pwm_a.duty_u16(0)
            pwm_b.duty_u16(0)
            motor_a_backward.low()
            motor_b_backward.low()
        if ch3_value > 0:
            pwm_weapon.duty_u16(int(ch3_value * 65535))
        else:
            pwm_weapon.duty_u16(0)
        if ch4_value > 0:
            control_spinner()

        time.sleep(0.02)
except KeyboardInterrupt:
    pwm_a.duty_u16(0)
    pwm_b.duty_u16(0)
    pwm_weapon.duty_u16(0)
    print("Program terminated")
  # bro this shit is not gonna work

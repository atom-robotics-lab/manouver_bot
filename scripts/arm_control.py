#!/usr/bin/env python3
import Adafruit_PCA9685
import time
import rospy
from sensor_msgs.msg import Joy

class servo_Class:
    #"Channel" is the channel for the servo motor on PCA9685
    #"ZeroOffset" is a parameter for adjusting the reference position of the servo motor
    def __init__(self, Channel, ZeroOffset):
        self.buttons = []
        self.Channel = Channel
        self.ZeroOffset = ZeroOffset

        #Initialize Adafruit_PCA9685
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40)
        self.pwm.set_pwm_freq(int(60))

    # Angle setting
    def SetPos(self,pos):
        #PCA9685 controls angles with pulses, 150~650 of pulses correspond to 0~180° of angle
        pulse = int((650-150)/180*pos+150+self.ZeroOffset)
        self.pwm.set_pwm(self.Channel, 0, pulse)

    def callback(self,data):
        global left_btn, right_btn, pick_btn, travel_btn, drop_btn
        self.buttons = data.buttons
        left_btn = self.buttons[6]
        right_btn = self.buttons[0]
        pick_btn = self.buttons[3]
        travel_btn = self.buttons[2]
        drop_btn = self.buttons[1] 

if __name__ == '__main__':
	
    pick_btn = 0
    travel_btn = 0
    drop_btn = 0
    left_btn = 0   
    right_btn = 0
 
    Servo0 = servo_Class(Channel=0, ZeroOffset=0)
    Servo1 = servo_Class(Channel=3, ZeroOffset=0)
    Servo2 = servo_Class(Channel=2, ZeroOffset=0)
    
    rospy.init_node('arm_control')
    rospy.Subscriber("/joy", Joy, Servo0.callback)

    flag = 1
    print("arm linked successfully")
    while not rospy.is_shutdown():
        if pick_btn == 1:
            Servo0.SetPos(10)
            Servo2.SetPos(55)
            print("pick")
            
        if travel_btn == 1:
            Servo0.SetPos(10)
            Servo2.SetPos(21)
            print("travel")
        if drop_btn == 1:
            Servo0.SetPos(50)
            Servo2.SetPos(50)
            print("drop")
            
        if left_btn == 1:
            print("open")
            Servo1.SetPos(100)
        if right_btn == 1:
            if flag ==1:
                print("close")
                Servo1.SetPos(30)
                flag = 0
            else:
                print("open")
                Servo1.SetPos(105)
                flag = 1
            right_btn = 0

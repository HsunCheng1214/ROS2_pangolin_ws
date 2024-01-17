#!/usr/bin/python3
# coding=utf8

import os, sys, math
sys.path.append('/home/ubuntu/pangolin_ws/src/pangolin_control/driver')

import numpy as np
import time
import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from time import sleep
from Board import setPWMServoPulse
from queue import Queue
from os import geteuid
from ServoCmd import Servo
from std_msgs.msg import String
from std_srvs.srv import SetBool
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from pangolin_interfaces.action import PangolinAction


class Pangolin_Control(Node):
    def __init__(self):
        self.servo_control = Servo()
        super().__init__('pangolin_controller')
        self.cmd_subscriber_ = self.create_subscription(Twist, 'cmd_vel', self.cmd_callback, 1)

    def cmd_callback(self, msg: Twist,):
        self.liner_x = -(msg.linear.x)
        self.angular_z = msg.angular.z


        if self.liner_x >= 0.01 and abs(self.angular_z) >= 0.01:
            self.servo_control.move_joystick(0.4, self.angular_z)
        elif self.liner_x <= -0.01 and abs(self.angular_z) >= 0.01:
            self.servo_control.move_joystick(-0.4, self.angular_z)
        elif abs(self.liner_x) >= 0.01 or abs(self.angular_z) >= 0.01:
            self.servo_control.initial_position()
            self.servo_control.move_joystick(self.liner_x, self.angular_z)
        
        self.get_logger().info('  liner_x : "%s"' % self.liner_x)
        self.get_logger().info('angular_z : "%s"' % self.angular_z)

        self.servo_control.move_joystick(self.liner_x, self.angular_z)
     
            

def main(args=None):
    rclpy.init(args=args)

    PangolinControl = Pangolin_Control()

    rclpy.spin(PangolinControl)

    PangolinControl.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

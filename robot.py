#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive


class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        self.frontLeft = wpilib.Spark(1)
        self.rearLeft = wpilib.Spark(2)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.frontRight = wpilib.Spark(3)
        self.rearRight = wpilib.Spark(4)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

        self.drive = DifferentialDrive(self.left, self.right)
        self.stick = wpilib.Joystick(0)

    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def operatorControl(self):
        timer = wpilib.Timer()
        timer.start()
        while self.isOperatorControl() and self.isEnabled():

            # Move a motor with a Joystick
            self.drive.tankDrive(self.stick.getY(), self.stick.getY())

            if timer.hasPeriodPassed(1.0):
                print("Analog 8: %s" % self.ds.getBatteryVoltage())

            wpilib.Timer.delay(0.02)

    def autonomous(self):
        timer = wpilib.Timer()
        timer.start()
        while self.isAutonomous() and self.isEnabled():
            if timer.get() < 3.0:
                self.drive.tankDrive(-1, -1)
            else:
                self.drive.tankDrive(0, 0)

            wpilib.Timer.delay(0.01)


if __name__ == '__main__':
    wpilib.run(MyRobot)

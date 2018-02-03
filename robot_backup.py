#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive


class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        self.frontLeft = wpilib.Talon(0)
        self.rearLeft = wpilib.Talon(1)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.frontRight = wpilib.Talon(2)
        self.rearRight = wpilib.Talon(3)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

        self.drive = DifferentialDrive(self.left, self.right)
        self.stick2 = wpilib.Joystick(0)
        self.stick = wpilib.Joystick(1)

    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def operatorControl(self):
        timer = wpilib.Timer()
        timer.start()
        i = -1
        while self.isOperatorControl() and self.isEnabled():
            # if self.stick.getRawButton(2):
            #     # self.drive.arcadeDrive(self.stick.getY(), self.stick.getX())
            #     self.drive.arcadeDrive(1, 0)
            #     # self.drive.tankDrive(self.stick.getY() * -0.7, self.stick2.getY() * -0.7, True)
            # else:
            #     # self.drive.arcadeDrive(self.stick.getY(), self.stick.getX())
            #     self.drive.arcadeDrive(1, 0)
            #     # self.drive.tankDrive(self.stick.getY() * 0.7, self.stick2.getY() * 0.7, True)
            # # i = i * self.stick.getRawAxis(4)
            # # Move a motor with a Joystick
            self.drive.arcadeDrive(0.4, 0)

            if timer.hasPeriodPassed(1.0):
                print("Analog 8: %s" % self.ds.getBatteryVoltage())

            wpilib.Timer.delay(0.02)

    def autonomous(self):
        timer = wpilib.Timer()
        timer.start()
        while self.isAutonomous() and self.isEnabled():
            if timer.get() < 3.0:
                self.drive.tankDrive(-0.1, -1)
            else:
                self.drive.tankDrive(0., 0)

            wpilib.Timer.delay(0.01)


if __name__ == '__main__':
    wpilib.run(MyRobot)
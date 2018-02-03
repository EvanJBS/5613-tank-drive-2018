#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive


class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        self.frontLeft = wpilib.Spark(0)
        self.rearLeft = wpilib.Spark(1)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.frontRight = wpilib.Spark(2)
        self.rearRight = wpilib.Spark(3)
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
        while self.isOperatorControl() and self.isEnabled():
            if self.stick2.getRawButton(1) and self.stick2.getRawButton(7):
                self.drive.arcadeDrive(self.stick2.getY() * 0.6, self.stick2.getX() * 0.7, True)
            elif self.stick2.getRawButton(7) and not self.stick2.getRawButton(1):
                self.drive.arcadeDrive(self.stick2.getY() * -0.6, self.stick2.getX() * 0.7, True)
            elif self.stick2.getRawButton(1) and not self.stick2.getRawButton(7):
                self.drive.arcadeDrive(self.stick2.getY() * 1, self.stick2.getX() * 1, True)
            else:
                self.drive.arcadeDrive(self.stick2.getY() * -1, self.stick2.getX() * 1, True)
            wpilib.Timer.delay(0.02)

    def autonomous(self):
        timer = wpilib.Timer()
        timer.start()
        while self.isAutonomous() and self.isEnabled():
            if timer.get() < 1.0:
                self.drive.tankDrive(0, 0)
            else:
                self.drive.tankDrive(0, 0)

            wpilib.Timer.delay(0.01)


if __name__ == '__main__':
    wpilib.run(MyRobot)

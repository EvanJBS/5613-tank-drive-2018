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
        self.stick1 = wpilib.Joystick(0)
        self.stick2 = wpilib.Joystick(1)
        self.a = -1
        self.b = 0

        self.intake = wpilib.Spark(4)
    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def operatorControl(self):
        timer = wpilib.Timer()
        timer.start()
        while self.isOperatorControl() and self.isEnabled():
            # if self.stick1.getRawButton(1) and self.stick1.getRawButton(7):
            #     self.drive.arcadeDrive(self.stick1.getY() * 0.6, self.stick1.getX() * 0.7, True)
            # elif self.stick1.getRawButton(7) and not self.stick1.getRawButton(1):
            #     self.drive.arcadeDrive(self.stick1.getY() * -0.6, self.stick1.getX() * 0.7, True)
            # elif self.stick1.getRawButton(1) and not self.stick1.getRawButton(7):
            #     self.drive.arcadeDrive(self.stick1.getY() * 1, self.stick1.getX() * 1, True)
            # else:
            #     self.drive.arcadeDrive(self.stick1.getY() * -1, self.stick1.getX() * 1, True)
            #
            # if self.stick1.getRawButton(6):
            #     self.intake.set(1)
            # elif self.stick1.getRawButton(8):
            #     self.intake.set(-1)
            # else:
            #     self.intake.set(0)
            self.drive.arcadeDrive(self.stick1.getY() * self.a, self.stick1.getX() * 0.8)
            self.intake.set(self.b)
            if self.stick1.getRawButton(7) and self.stick1.getRawButton(1):
                self.a = 0.6
            elif self.stick1.getRawButton(7):
                self.a = -0.6
            elif self.stick1.getRawButton(1):
                self.a = 1
            elif self.stick1.getRawButton(6):
                self.b = 1
            elif self.stick1.getRawButton(4):
                self.b = -1
            else:
                self.a = -1
                self.b = 0


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
#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.frontLeft = wpilib.Spark(0)
        self.rearLeft = wpilib.Spark(1)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.frontRight = wpilib.Spark(2)
        self.rearRight = wpilib.Spark(3)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

        self.intake = wpilib.Spark(4)


        self.drive = DifferentialDrive(self.left, self.right)
        self.stick1 = wpilib.Joystick(0)
        self.stick2 = wpilib.Joystick(1)
        self.a = -1
        self.b = 0

    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def operatorControl(self):
        timer = wpilib.Timer()
        timer.start()
        while self.isOperatorControl() and self.isEnabled():
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
        # timer = wpilib.Timer()
        # timer.start()
        # while self.isAutonomous() and self.isEnabled():
        #     if timer.get() < 1.0:
        #         self.drive.tankDrive(0, 0)
        #     else:
        #         self.drive.tankDrive(0, 0)
        #
        #     wpilib.Timer.delay(0.01)
        timer = wpilib.Timer()
        timer.start()
        if wpilib.DriverStation.getInstance().getGameSpecificMessage() == "RRR" or "RLR":
            while self.isAutonomous() and self.isEnabled():
                if timer.get() < 2.0:
                    self.drive.arcadeDrive(1, 0)
                else:
                    self.drive.arcadeDrive(0, 0)
        elif wpilib.DriverStation.getInstance().getGameSpecificMessage() == "LLL" or "LRL":
            while self.isAutonomous() and self.isEnabled():
                if timer.get() < 2.0:
                    self.drive.arcadeDrive(-1, 0)
                else:
                    self.drive.arcadeDrive(0, 0)
        else:
            self.drive.arcadeDrive(0, 0)


if __name__ == '__main__':
    wpilib.run(MyRobot)

#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive
from robotpy_ext.control.toggle import Toggle


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.DriveSpd = 1
        self.RotationSpd = 1
        self.IntakeSpd = 0
        self.ShooterSpd = 1
        self.Direction = 1

        self.frontLeft = wpilib.Spark(0)
        self.rearLeft = wpilib.Spark(1)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.frontRight = wpilib.Spark(2)
        self.rearRight = wpilib.Spark(3)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

        self.drive = DifferentialDrive(self.left, self.right)

        self.stick1 = wpilib.Joystick(0)
        self.stick2 = wpilib.Joystick(1)
        # self.toggle7 = Toggle(self.stick1, 7)
        # self.toggle1 = Toggle(self.stick1, 1)
        # self.toggle6 = Toggle(self.stick1, 6)
        # self.toggle4 = Toggle(self.stick1, 4)
        # self.toggle5 = Toggle(self.stick1, 5)
        # self.toggle3 = Toggle(self.stick1, 3)
        # self.toggle2 = Toggle(self.stick1, 2)

        self.Lshoot = wpilib.Spark(5)
        self.Rshoot = wpilib.Spark(6)
        self.shoot = wpilib.SpeedControllerGroup(self.Lshoot, self.Rshoot)

        self.Lintake = wpilib.Spark(4)
        self.Rintake = wpilib.Spark(8)
        self.intake = wpilib.SpeedControllerGroup(self.Lintake, self.Rintake)

    def disabled(self):
        wpilib.Timer.delay(0.01)

    def teleopInit(self):
        self.timer = wpilib.Timer()
        self.timer.start()

    def teleopPeriodic(self):
        self.drive.arcadeDrive((self.stick1.getY() * self.DriveSpd) * self.Direction, self.stick1.getX() * self.RotationSpd)
        self.intake.set(self.IntakeSpd)
        self.shoot.set(self.ShooterSpd)

        if self.stick1.getRawButton(1):
            self.Direction = -1
        else:
            self.Direction = 1
        if self.stick1.getRawButton(2):
            self.DriveSpd = 0.5
        else:
            self.DriveSpd = 1
        if self.stick1.getRawButton(6):
            self.IntakeSpd = 0.5
        elif self.stick1.getRawButton(4):
            self.IntakeSpd = -0.5
        else:
            self.IntakeSpd = 0
        if self.stick1.getRawButton(5):
            self.ShooterSpd = 0.5
        elif self.stick1.getRawButton(3):
            self.ShooterSpd = -0.5
        else:
            self.ShooterSpd = 0

        self.timer.delay(0.02)
    def autonomousInit(self):
        self.timer = wpilib.Timer()
        self.timer.start()
        self.gamedata = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        print(self.gamedata)

    def autonomousPeriodic(self):
        self.drive.arcadeDrive(self.Speed * self.Direction, self.Rotation)
        self.IntakeSpd.set(self.IntakeSpd)
        self.shoot.set(self.ShooterSpd)
        if self.gamedata is "LLL" or "LRL" and not "RRR" or "RLR":
            if self.timer.get() < 1.0:
                self.Speed = 0.5
            else:
                self.Speed = 0
        if self.gamedata is "RRR" or "RLR" and not "LLL" or "LRL":
            if self.timer.get() < 1.0:
                self.Speed = -0.5
            else:
                self.Speed = 0

        else:
            self.Speed = -1


if __name__ == '__main__':
    wpilib.run(MyRobot)

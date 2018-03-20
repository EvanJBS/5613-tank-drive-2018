#!/usr/bin/env python3

import wpilib
from wpilib.drive import DifferentialDrive
from robotpy_ext.common_drivers import navx
from robotpy_ext.control.toggle import Toggle

def run():
    raise ValueError()


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.sd = wpilib.SmartDashboard
        self.timer = wpilib.Timer()

        self.navx = navx.AHRS.create_spi()
        self.analog = wpilib.AnalogInput(navx.getNavxAnalogInChannel(0))


        self.DriveSpd = 1
        self.RotationSpd = 1
        self.IntakeSpd = 0
        self.ShooterSpd = 1
        self.Direction = -1

        self.EncoderB = wpilib.encoder.Encoder(0, 1)
        self.EncoderA = wpilib.encoder.Encoder(2, 3, True)

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
        self.logger.info("Entered disabled mode")

        self.timer.reset()
        self.timer.start()
        self.timer.reset()
        self.timer.start()

        if self.timer.hasPeriodPassed(0.5):
            self.sd.putBoolean('SupportsDisplacement', self.navx._isDisplacementSupported())
            self.sd.putBoolean('IsCalibrating', self.navx.isCalibrating())
            self.sd.putBoolean('IsConnected', self.navx.isConnected())
            self.sd.putNumber('Angle', self.navx.getAngle())
            self.sd.putNumber('Pitch', self.navx.getPitch())
            self.sd.putNumber('Yaw', self.navx.getYaw())
            self.sd.putNumber('Roll', self.navx.getRoll())
            self.sd.putNumber('Analog', self.analog.getVoltage())
            self.sd.putNumber('Timestamp', self.navx.getLastSensorTimestamp())


    def teleopInit(self):
        self.timer = wpilib.Timer()
        self.timer.start()

    def teleopPeriodic(self):
        self.drive.arcadeDrive((self.stick1.getY() * self.DriveSpd) * self.Direction,
                               self.stick1.getX())
        self.intake.set(self.IntakeSpd)
        self.shoot.set(self.ShooterSpd * ((self.stick1.getThrottle()+1)))
        print(self.stick1.getThrottle())
        if self.stick1.getRawButton(1):
            self.IntakeSpd = 1
            self.ShooterSpd = -1
        elif self.stick1.getRawButton(6):
            self.IntakeSpd = 1
        elif self.stick1.getRawButton(4):
            self.IntakeSpd = -1
        elif self.stick1.getRawButton(5):
            self.ShooterSpd = -1
        elif self.stick1.getRawButton(3):
            self.ShooterSpd = 1
        else:
            self.IntakeSpd = 0
            self.ShooterSpd = 0
        if self.stick1.getRawButton(12):
            self.Direction = 1
        else:
            self.Direction = -1
        if self.stick1.getRawButton(2):
            self.DriveSpd = 0.6
        else:
            self.DriveSpd = 1

    def autonomousInit(self):
        self.timer.start()
        self.gamedata = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        print(self.gamedata)

    def autonomousPeriodic(self):
        print("A", self.EncoderA.get())
        # print("B", self.EncoderB.get())
        if self.EncoderA.get() > -69.9 * 25:
            self.drive.arcadeDrive(-0.6, 0)
        elif
            self.drive.arcadeDrive(0, 0)

        # if self.EncoderA.get() < 1:
        #     self.drive.arcadeDrive(0.5, 0)
        # else:
        #     self.drive.arcadeDrive(0.5, 0)

        # if self.timer.get() < 3.7:
        #     self.drive.arcadeDrive(0.5,0)
        # elif self.timer.get() > 3.7:
        #     self.drive.arcadeDrive(0,0)
        # else:
        #     self.drive.arcadeDrive(0,0)+


        # if self.gamedata is "LLL" or "LRL" and not "RRR" or "RLR":
        #     if self.timer.get() < 1.0:
        #         self.DriveSpd = 0.1
        #     else:
        #         self.DriveSpd = 0
        # if self.gamedata is "RRR" or "RLR" and not "LLL" or "LRL":
        #     if self.timer.get() < 1.0:
        #         self.DriveSpd = 0.4
        #     else:
        #         self.DriveSpd = 0
        #
        # else:
        #     self.DriveSpd = 0


if __name__ == '__main__':
    wpilib.run(MyRobot)

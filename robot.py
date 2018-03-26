#!/usr/bin/env python3

import wpilib
from robotpy_ext.common_drivers.navx import AHRS
from wpilib.drive import DifferentialDrive
from robotpy_ext.common_drivers import navx
from networktables import NetworkTables

# from robotpy_ext.control.toggle import Toggle


class MyRobot(wpilib.IterativeRobot):

    """This is a demo program showing the use of the navX MXP to implement
    a "rotate to angle" feature. This demo works in the pyfrc simulator.

    This example will automatically rotate the robot to one of four
    angles (0, 90, 180 and 270 degrees).

    This rotation can occur when the robot is still, but can also occur
    when the robot is driving.  When using field-oriented control, this
    will cause the robot to drive in a straight line, in whatever direction
    is selected.

    This example also includes a feature allowing the driver to "reset"
    the "yaw" angle.  When the reset occurs, the new gyro angle will be
    0 degrees.  This can be useful in cases when the gyro drifts, which
    doesn't typically happen during a FRC match, but can occur during
    long practice sessions.

    Note that the PID Controller coefficients defined below will need to
    be tuned for your drive system.
    """

    # The following PID Controller coefficients will need to be tuned */
    # to match the dynamics of your drive system.  Note that the      */
    # SmartDashboard in Test mode has support for helping you tune    */
    # controllers by displaying a form where you can enter new P, I,  */
    # and D constants and test the mechanism.                         */

    # Often, you will find it useful to have different parameters in
    # simulation than what you use on the real robot

    if wpilib.RobotBase.isSimulation():
        # These PID parameters are used in simulation
        kP = 0.06
        kI = 0.00
        kD = 0.00
        kF = 0.00
    else:
        # These PID parameters are used on a real robot
        kP = 0.03
        kI = 0.00
        kD = 0.00
        kF = 0.00

    kToleranceDegrees = 2.0

    def robotInit(self):
        self.sd = wpilib.SmartDashboard
        self.timer = wpilib.Timer()

        self.DriveSpd = 1
        self.RotationSpd = 1
        self.IntakeSpd = 0
        self.ShooterSpd = 1
        self.Direction = -1
        self.currentRotationRate = 0
        self.SpeedAut = 0
        self.rotateToAngle = False

        self.gamedata = wpilib.DriverStation.getInstance().getGameSpecificMessage()

        self.navx = navx.AHRS.create_spi()
        self.analog = wpilib.AnalogInput(navx.getNavxAnalogInChannel(0))

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

        # For Toggling Buttons
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
        #
        # Communicate w/navX MXP via the MXP SPI Bus.
        # - Alternatively, use the i2c bus.
        # See http://navx-mxp.kauailabs.com/guidance/selecting-an-interface/ for details
        #

        self.ahrs = AHRS.create_spi()
        # self.ahrs = AHRS.create_i2c()

        turnController = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, self.ahrs, output=self)
        turnController.setInputRange(-180.0, 180.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(self.kToleranceDegrees)
        turnController.setContinuous(True)

        self.turnController = turnController
        self.rotateToAngleRate = 0

        # Add the PID Controller to the Test-mode dashboard, allowing manual  */
        # tuning of the Turn Controller's P, I and D coefficients.            */
        # Typically, only the P value needs to be modified.                   */
        wpilib.LiveWindow.addActuator("DriveSystem", "RotateController", turnController)
        print(self.sd.getTable())

    def teleopInit(self):
        self.tm = wpilib.Timer()
        self.tm.start()

    def teleopPeriodic(self):
        self.drive.arcadeDrive((self.stick1.getY() * self.DriveSpd) * self.Direction,
                               self.stick1.getX())
        self.intake.set(self.IntakeSpd)
        self.shoot.set(self.ShooterSpd * (self.stick1.getThrottle() + 1))
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

            # Use the joystick Y axis for forward movement,
            # and either the X axis for rotation or the current
            # calculated rotation rate depending upon whether
            # "rotate to angle" is active.
            #
            # This works better for mecanum drive robots, but this
            # illustrates one way you could implement this using
            # a 4 wheel drive robot

    def autonomousInit(self):
        self.timer.start()
        print(self.gamedata)

    def autonomousPeriodic(self):
        self.drive.arcadeDrive(self.SpeedAut, self.currentRotationRate)
        print("A", self.EncoderA.get())
        # print("B", self.EncoderB.get())
        if self.EncoderA.get() > -69.9 * 25:
            self.SpeedAut = -0.6
        elif self.EncoderA.get() < -69.9 * 25:
            self.turnController.setSetpoint(179.9)
            self.rotateToAngle = True
        if self.rotateToAngle:
            self.turnController.enable()
            self.currentRotationRate = self.rotateToAngleRate
        else:
            self.turnController.disable()
            self.currentRotationRate = 0.0

    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        self.rotateToAngleRate = output


if __name__ == '__main__':
    wpilib.run(MyRobot)

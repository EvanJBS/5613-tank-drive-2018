import wpilib


class MyRobot(wpilib.SampleRobot):
    '''Main robot class'''

    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        self.lstick = wpilib.Joystick(1)
        self.rstick = wpilib.Joystick(2)

        self.right_motor = wpilib.Jaguar(1)
        self.left_motor = wpilib.Jaguar(2)

        self.robot_drive = wpilib.RobotDrive(self.left_motor, self.right_motor)

        #position gets automatically updated as robot moves
        self.gyro = wpilib.AnalogGyro(1)

    def disabled(self):
        '''called when robot is disabled'''
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def autonomous(self):
        '''Called when autonomous mode is enabled'''

        timer = wpilib.Timer()
        timer.start()

        while self.isAutonomous() and self.isEnabled():

            if timer.get() <.99:
                self.robot_drive.arcadeDrive(1, -.8)

            elif timer.get() <2.3:
                self.robot_drive.arcadeDrive(1, 0)

            elif timer.get() <5.8:
                self.robot_drive.arcadeDrive(1, .6)

            elif timer.get() <6.9:
                self.robot_drive.arcadeDrive(1, 0)
            else:
                self.robot_drive.arcadeDrive(0, 0)

            wpilib.Timer.delay(0.01)

    def operatorControl(self):
        '''Called when operator control mode is enabled'''

        while self.isOperatorControl() and self.isEnabled():

            self.robot_drive.tankDrive(self.left_motor, self.right_motor)

            wpilib.Timer.delay(0.04)

if __name__ == '__main__':
    wpilib.run(MyRobot,
               physics_enabled=True)
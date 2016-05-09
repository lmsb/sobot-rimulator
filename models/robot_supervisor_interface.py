# Sobot Rimulator - A Robot Programming Tool
# Copyright (C) 2013-2014 Nicholas S. D. McCrea
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Email mccrea.engineering@gmail.com for questions, comments, or to report bugs.

from irobotcreate2control import *

ISCREATE2CONNECTED = 1

# a class representing the available interactions a supervisor may have with a robot
class RobotSupervisorInterface:

  def __init__( self, robot ):
    self.robot = robot
    if (ISCREATE2CONNECTED):
        #first get the Create2 robot object
        self.robotComm = IRobotCreate2Control()
        #then connect with it through serial
        self.robotComm.connectIRobotCreate('/dev/ttyUSB0')
        self.robotComm.sendControlKey('P')
        self.robotComm.sendControlKey('S')
        self.robotComm.sendControlKey('SPACE')  # for a beep

        #initial encoder read to turn to 0. 
        self.leftEncAt0, self.rightEncAt0 = self.robotComm.getEncoders()
    
  
  # read the proximity sensors
  def read_proximity_sensors( self ):
    return [ s.read() for s in self.robot.ir_sensors ]

  # read the wheel encoders
  def read_wheel_encoders( self ):
    if (ISCREATE2CONNECTED):
        leftEnc, rightEnc = self.robotComm.getEncoders()
        print "rob int encoder left: ", str(leftEnc), " right: ", str(rightEnc)
        return [leftEnc-self.leftEncAt0, rightEnc-self.rightEncAt0]
    else:
        return [ e.read() for e in self.robot.wheel_encoders ]

  # apply wheel drive command
  def set_wheel_drive_rates( self, v_l, v_r ):
    self.robot.set_wheel_drive_rates( v_l, v_r )
    print ">> sending command to robot!"
    print "v_l = ", v_l
    print "v_r = ", v_r
    if (ISCREATE2CONNECTED):
        self.robotComm.sendDriveCommand(v_r, v_l)


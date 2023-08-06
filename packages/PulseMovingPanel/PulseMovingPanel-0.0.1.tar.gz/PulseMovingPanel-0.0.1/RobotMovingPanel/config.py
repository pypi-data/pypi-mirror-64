import os
from argsParser import arguments
from pulseapi_integration import *

args = arguments.parse_args()
robot = NewRobotPulse(args.host)

PATH_2_CSV = os.path.join(os.path.dirname(__file__), 'data/points/points.scv')
PATH_2_TOOL_JSON = os.path.join(os.path.dirname(__file__), 'data/tools/tools.json')
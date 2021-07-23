# NanoAvionicsCanbusDebugTerminal
Debug Terminal for Nano Avionics Cubesat parts (UHF, EPS) to do Remote CLI Configuration via Cubesat Protocol Transactions

use csprun alias to run the script easier

set $build to your libcsp build directory after compilation

then run

csprun CSPTERM.py --canbus [your socketcan interface]

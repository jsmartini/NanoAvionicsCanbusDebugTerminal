# NanoAvionicsCanbusDebugTerminal
Debug Terminal for Nano Avionics Cubesat parts (UHF, EPS) to do Remote CLI Configuration via Cubesat Protocol Transactions
# University of Alabama UASpace Bama-1 Cube Satellite 

use csprun alias to run the script easier

set $build to your libcsp build directory after compilation

run

source alias.sh

then run

csprun CSPTERM.py --canbus [your socketcan interface]

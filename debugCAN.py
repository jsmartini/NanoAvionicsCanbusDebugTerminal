import libcsp_py3 as libcsp

import argparse
import sys
from ctypes import *

global DEFAULT_DEBUG_PORT
DEFAULT_DEBUG_PORT = 13

global SERVER
global PORT
SERVER = 1

def console_print(out: dict):
    for k in out.keys():
        print(f"\t{k} {out[k]}")

def parse_response(struct):
    grab_str = lambda f: bytearray(getattr(struct, f)).decode()

    return {
        "errorCode": int(getattr(struct, "errorCode")),
        "packetId": int(getattr(struct, "packetId")),
        "isFinal": bool(getattr(struct, "isFinal")),
        "outputData": grab_str("outputData")
    }

class NA_REMOTECLI:

    # Nano Avionics Remote Cli Req/Res msgs

    class NAReq(Structure):
        _pack_=0
        _fields_=[
            ("delayBetweenPacketsInMs", c_uint8),
            ("inputData", c_uint8*128)
        ]
    
    class NAFRes(Structure):
        _pack_=0
        _fields_=[
            ("errorCode", c_uint8),
            ("packetId", c_uint8),
            ("isFinal", c_bool),
            ("outputData", c_uint8*128)
        ]


def opt():
    parser = argparse.ArgumentParser(
        description="DebugTerminal Via Can Devices"
    )
    parser.add_argument("-a", "--address", default=10, help="Address of Device <int>")
    parser.add_argument("-can", "--canbus", help="CANBUS interface i.e. can0")
    parser.add_argument("-R", "--routing_table", default="0/0 CAN", help="Routing Table Configuration")
    return parser.parse_args(sys.argv[1:])

global args
args = opt()


libcsp.init(opt.address, "DebugTerminal", "debugging", "1.4", 10, 300)

try:
    libcsp.can_socketcan_init(args.canbus, f"{args.canbus}")
except BaseException as e:
    print(e)
    print(f"CSP Socketcan Init Failed Spectacularly @{args.canbus}")
    exit(-1)

if args.routing_table:
    libcsp.rtable_load(args.routing_table)
else:
    libcsp.rtable_load(f"0/0 {args.canbus}")

print("Routes:")
libcsp.print_routes()

import cmd

PORT = DEFAULT_DEBUG_PORT

class CSPTERM(cmd.CMD):
    prompt= "[CSP]?>"

    def do_node(self, addr):
        global SERVER, PORT
        SERVER = int(addr)
        print(f"\tSet Targeted CSP Node {SERVER}:{PORT}")

    def do_port(self, port):
        global PORT, DEFAULT_DEBUG_PORT
        if port == "default":
            PORT = DEFAULT_DEBUG_PORT
        else:
            PORT = int(port)

    def do_request(self, msg):
        global args, SERVER, PORT
        
        # its the same thing
        target_request = NA_REMOTECLI.NAFReq
        target_response = NA_REMOTECLI.NAFRes

        if msg < 128:
            msg += (128-len(msg))*"\u0000" # may be an error if sent? null literal?
        msg = target_request(3, msg.encode())
        outbuf = bytearray(target_request)
        inbuf = bytearray(sizeof(target_response))
        libcsp.transaction(0, SERVER, PORT, 1000, outbuf, inbuf)
        res = target_response.from_buffer(inbuf)
        console_print(
            parse_response(res)
        )

if __name__ == '__main__':
    print("Jonathan Martini @2021 UASPACE")
    CSPTERM.cmdloop()




    

    
import argparse, sys

USAGE_ARGS = "Correct usage: CHAP start web_server|stream_server|control_listener"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Select a CHAP server process to start.')
    parser.add_argument('-s', '--start',help="web_server|stream_server|control_listener")
    args = parser.parse_args()
    
    if args.start == "web_server":
        import web_server as service
    elif args.start == "stream_server":
        import stream_server as service
    elif args.start == "control_listener":
        import control_listener as service
    else:
        parser.print_help()
        sys.exit(2)
        
    service.start()
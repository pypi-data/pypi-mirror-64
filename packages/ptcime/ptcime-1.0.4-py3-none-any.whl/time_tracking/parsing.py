import argparse

main_parser = argparse.ArgumentParser("ptcime", "Start and stop times.")
main_parser.add_argument(
    "action", choices=["start", "stop", "day", "week", "current", "toggle"])

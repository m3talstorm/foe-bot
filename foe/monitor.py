
"""
"""

# Native
import random
import time
import curses
from curses import wrapper
import argparse

# # 3rd-Party

# # Proprietary
from monitors.building_monitor import BuildingMonitor



def main(screen):

    parser = argparse.ArgumentParser(description='Building Monitor')

    parser.add_argument('--interval', action='store', default=1.0)

    args = parser.parse_args()

    monitor = BuildingMonitor(screen, interval=args.interval)
    monitor.run()



wrapper(main)

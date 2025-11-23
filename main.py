"""
Tron Legacy Style Terminal Emulator
This script creates a fancy terminal emulator using the 'curses' library.
It mimics the Tron Legacy movie style terminal for a prank effect.
"""

import signal
import sys
import curses
import time
import random
import threading
from shutil import get_terminal_size

# Global variables
stop_threads = False
lock = threading.Lock()
ascii_chars = "@%#*+=-:. "


def handle_exit(signum, frame):
    """Handle graceful exit on SIGINT (Ctrl+C)"""
    global stop_threads
    stop_threads = True
    curses.endwin()
    sys.exit(0)


# Attach signal handler
signal.signal(signal.SIGINT, handle_exit)


def setup_terminal(stdscr):
    """Setup curses environment with colors and settings"""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.clear()


def tron_legacy_animation(stdscr):
    """
    Display a Tron Legacy style terminal animation.
    Shows animated grid with random characters that cycle through the color scheme.
    """
    setup_terminal(stdscr)
    height, width = stdscr.getmaxyx()

    # Initialize the grid
    grid = [[" " for _ in range(width)] for _ in range(height)]

    frame = 0
    while not stop_threads:
        try:
            stdscr.clear()

            # Update the grid with random characters
            for row in range(height):
                for col in range(width):
                    # 5% chance of changing a character
                    if random.random() < 0.05:
                        grid[row][col] = random.choice(ascii_chars)
                        # Cycle through colors
                        color_pair = ((frame + row + col) % 4) + 1
                        stdscr.addstr(row, col, grid[row][col], curses.color_pair(color_pair))
                    else:
                        # Display existing character with cycling color
                        if grid[row][col] != " ":
                            color_pair = ((frame + row + col) % 4) + 1
                            stdscr.addstr(row, col, grid[row][col], curses.color_pair(color_pair))

            # Add some status text at the bottom
            status_text = f"TRON LEGACY TERMINAL | FRAME: {frame} | ESC to exit"
            if height > 0 and width > len(status_text):
                stdscr.addstr(height - 1, 0, status_text, curses.color_pair(1))

            stdscr.refresh()
            time.sleep(0.08)
            frame += 1

            # Check for exit key (ESC)
            try:
                key = stdscr.getch()
                if key == 27:  # ESC key
                    break
            except curses.error:
                pass

        except curses.error:
            # Handle curses errors gracefully
            pass


def boot_sequence(stdscr):
    """Display a boot sequence animation before the main animation"""
    setup_terminal(stdscr)
    height, width = stdscr.getmaxyx()

    boot_messages = [
        "GRID CORE ONLINE",
        "DISC PROTOCOL NEGOTIATED",
        "ISO PRESENCE ACKNOWLEDGED",
        "PROCESSOR RAILS NOMINAL",
        "LEGACY TERMINAL READY",
        "",
        "Press any key to continue or ESC to exit..."
    ]

    for i, message in enumerate(boot_messages):
        stdscr.clear()
        row = height // 2 - len(boot_messages) // 2 + i
        if 0 <= row < height:
            col = max(0, (width - len(message)) // 2)
            stdscr.addstr(row, col, message, curses.color_pair(2))
        stdscr.refresh()
        time.sleep(0.4)

    # Wait for user input
    while True:
        try:
            key = stdscr.getch()
            if key == 27:  # ESC key
                return False
            if key != -1:  # Any key pressed
                return True
        except curses.error:
            time.sleep(0.1)


def main(stdscr):
    """Main entry point for the terminal application"""
    # Show boot sequence
    if not boot_sequence(stdscr):
        return

    # Run the main animation
    tron_legacy_animation(stdscr)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()


import sys
import re
from pathlib import Path
from dataclasses import dataclass

# Sentinel object used as a return signal when user want to flip between the two menus
SWITCH_VIEW = object()


@dataclass
class ExportFolder:
    username: str|None
    date: str|None
    path: Path


def parse_export_folder_name(path: Path) -> ExportFolder:
    """parse the export folder name, and extract the username and export date"""
    
    match = re.match(r"instagram-(.+?)-(\d{4})-(\d{2})-(\d{2})", path.name, re.IGNORECASE)

    if not match:
        return ExportFolder(None, None, path)

    username, y, m, d = match.groups()
    return ExportFolder(username, f"{y}-{m}-{d}", path)


def print_options(title: str, lines: list, hints: list):
    line = "=" * 70
    print(f"\n{line}\n{title}\n{line}")
    print("\n".join(lines))
    print(line)
    print("\n".join(hints))
    print(line)


def ask_choice(keys: set, count: int) -> str|int:
    """Ask until the user enters a valid choice"""

    while True:
        choice = input("Your choice: ").strip().upper()

        if choice in keys:
            return choice
        if choice.isdigit() and 1 <= int(choice) <= count:
            return int(choice)

        valid = sorted(keys - {""})
        suffix = f", or one of: {', '.join(valid)}." if valid else "."
        print(f"Invalid input. " + (f"Enter a number from 1 to {count}" if count > 1 else "Enter 1") + suffix)


def choose_recognised(recognised: list, can_switch: bool):

    count = len(recognised)
    title = "Found 1 Instagram export folder:" if count == 1 else f"Found {count} Instagram export folders:"

    lines = [
        f"  {i}. {f.username:<20}  (exported date: {f.date})" + ("  <- most recent" if i == 1 else "")
        for i, f in enumerate(recognised, start=1)
    ]

    hints = ["  Press ENTER to use the most recent export"]

    keys = {"", "E"}

    if count > 1:
        hints.append("  Type a number to pick a different export")
    if can_switch:
        hints.append("  Type 'O' to see folders that could not be recognised")
        keys.add("O")
    hints.append("  Type 'E' to exit")

    print_options(title, lines, hints)

    choice = ask_choice(keys, count)

    if choice == "E":
        sys.exit("Exiting the program.")

    if choice == "O":
        return SWITCH_VIEW
    
    if choice == "":
        return recognised[0]
    
    return recognised[choice - 1]  



def choose_unrecognised(unrecognised: list, can_switch: bool):

    lines = [f"  {i}. {p.path.name}" for i, p in enumerate(unrecognised, start=1)]

    hints = ["  Type a number to use that folder anyway"]
    keys = {"E"}

    if can_switch:
        hints.append("  Type 'B' to go back to the recognised exports")
        keys.add("B")

    hints.append("  Type 'E' to exit")

    print_options("These folders don't match the expected export name:", lines, hints)

    choice = ask_choice(keys, len(unrecognised))

    if choice == "E":
        sys.exit("Exiting the program.")

    if choice == "B":
        return SWITCH_VIEW
    
    return unrecognised[choice - 1]


def scan_export_folders():
    """Split Instagram folders into recognised and unrecognised ones"""

    recognised, unrecognised = [], []

    for path in Path.cwd().glob("instagram*"):

        if not path.is_dir():
            continue

        export_folder = parse_export_folder_name(path)

        if export_folder.username:
            recognised.append(export_folder)
        else:
            unrecognised.append(export_folder)

    recognised.sort(key = lambda x: x.date, reverse=True)   # newset first
    unrecognised.sort(key = lambda x: x.path.name.lower())  # sort by folder name

    return recognised, unrecognised


def find_instagram_data_folder() -> ExportFolder:

    recognised, unrecognised = scan_export_folders()

    if not recognised and not unrecognised:
        sys.exit("No Instagram export folders found in the current directory.")

    if not recognised:
        print("No recognised exports found. Showing other Instagram folders instead.")

    showing_recognised = bool(recognised)

    while True:

        if showing_recognised:
            result = choose_recognised(recognised, can_switch=bool(unrecognised))

        else:
            result = choose_unrecognised(unrecognised, can_switch=bool(recognised))

        if result is SWITCH_VIEW:
            showing_recognised = not showing_recognised
        else:
            return result

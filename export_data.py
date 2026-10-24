import re
from datetime import datetime, timezone
from pathlib import Path

def ask_valid_username() -> str|None:
    """Prompts the user to enter a valid Instagram username or 'E' to cancel"""
    
    while True:
        print("\nPlease enter your username to continue, or type 'E' to go back.")
        username = input("Username: ").strip()

        if username.upper() == "E":
            return None

        # Validate username structure
        if username and re.fullmatch(r"[A-Za-z0-9_](?:[A-Za-z0-9_.]*[A-Za-z0-9_])?", username):
            return username

        print("Invalid username, try again.")


def ask_valid_date() -> str|None:
    """Prompts the user to enter an export date (YYYY-MM-DD) or 'E' to cancel"""
    
    while True:
        print("\nPlease enter your export date to continue, or type 'E' to go back.")
        date = input("Export Date (YYYY-MM-DD): ").strip()

        if date.upper() == "E":
            return None

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date

        except ValueError:
            print("Invalid date! Please use a valid calendar date")


def export_to_txt(path, users: set[str]):
    """Write set of usernames to a text file"""

    with open(path, "w", encoding="utf-8") as file:
        for user in sorted(users):
            file.write(f"{user}\n")


def export_with_following_durations(path: Path, users: set[str], timestamps: dict[str, int|None]):
    """Writes usernames along with followed duration.
    Use for not_following_back users"""
    
    now = datetime.now(timezone.utc)

    with open(path, "w", encoding="utf-8") as file:
        for user in sorted(users):
            timestamp = timestamps.get(user)

            # If the timestamp is not stored in the dict
            if timestamp is None:
                file.write(f"{user:<30} Unknown\n")
                continue

            # Convert timestamp to UTC date
            followed_date = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            days = (now - followed_date).days
            file.write(f"{user:<30} {days} " + ("day\n" if days == 1 else "days\n"))


def export_data(instagram_data):
    """Main export function"""

    if not instagram_data.username:
        print("Your username and export date cannot be recognised for this export folder.")
        
        username = ask_valid_username()
        if not username:
            return
        instagram_data.username = username

        date = ask_valid_date()
        if not date:
            return
        instagram_data.export_date = date

    parent_folder = Path("Exported_data")
    parent_folder.mkdir(exist_ok=True)
    user_folder = parent_folder/ f"{instagram_data.username}"
    user_folder.mkdir(exist_ok=True)
    new_folder = user_folder / f"{instagram_data.export_date}"

    # Handle directory conflict and confirm overwrite
    if new_folder.exists():
        choice = input(f"An export folder already exists. Do you want to overwrite it (Y/N): ").strip()
        if choice.upper() != 'Y':
            print("Export cancelled.")
            return

    # Create the folder, if it doesn't exist
    new_folder.mkdir(exist_ok=True)

    files_to_create = {
        "followers.txt": instagram_data.followers,
        "followings.txt": instagram_data.followings,
        "not_followed_back.txt": instagram_data.not_followed_back,
        "mutual_follows.txt": instagram_data.mutual_follows,
    }

    for file, users_list in files_to_create.items():
        path = new_folder/ file
        export_to_txt(path, users_list)

    export_with_following_durations(new_folder/"not_following_back.txt", instagram_data.not_following_back, instagram_data.timestamps)

    print("\nData successfully exported.")
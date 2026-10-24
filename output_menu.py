from pathlib import Path

from export_data import export_data, ask_valid_username


def print_header(title: str):
    line = "=" * 70
    print(f"\n{line}\n{title}\n{line}\n")


def print_usernames(title: str, users: set[str]):
    """Print usernames in a formatted way"""

    print_header(f"{title} ({len(users)})")

    # Use two-column output for large lists
    if len(users) >= 100:
        print_many_usernames(sorted(list(users)))
        return
    
    for i, user in enumerate(sorted(users), start=1):
        print(f"{i}. {user}")


def print_many_usernames(users: list[str]):
    """Print usernames in two side-by-side columns"""

    count = (len(users) + 1) // 2

    for i in range(count):
        left_data = f"{i + 1}. {users[i]}"

        right_index = count + i
        right_data = (
            f"{right_index + 1}. {users[right_index]}"
            if right_index < len(users)
            else ""
        )

        print(f"{left_data:<35} {right_data}")    
            

def manage_ignored_users(instagram_data):
    """Sub menu for viewing, adding and removing from ignored list """

    if not instagram_data.username:
        username = ask_valid_username()

        if not username:
            return

        instagram_data.username = username

    path = Path("Exported_data")/ instagram_data.username/ "ignore.txt"

    print_usernames("Ignored Users", instagram_data.ignored_users)

    while True:
        ignored = instagram_data.ignored_users

        print_header("Manage Ignored Users")
        print(f"Currently ignored: {len(ignored)}")
        print("1. View ignored users")
        print("2. Add a user")
        print("3. Remove a user")
        print("E. Return to the main menu")

        choice = input("Your choice: ").strip()

        if choice.upper() == "E":
            return

        if choice == "1":
            print_usernames("Ignored Users", ignored)

        elif choice == "2":

            while True:
                users = sorted(instagram_data.not_following_back)

                if not users:
                    print("There are no users available to ignore.")
                    break

                print_usernames("Not Following Back", set(users))

                selection = input("\nEnter the number of the user to ignore, or E to go back: ").strip()

                if selection.upper() == "E":
                    break

                if not selection.isdigit():
                    print("Please enter a valid number.")
                    continue

                number = int(selection)

                if not 1 <= number <= len(users):
                    print("Invalid number. Please select from the displayed list.")
                    continue

                username = users[number - 1]

                # Ensure that directory exists before opening
                path.parent.mkdir(parents=True, exist_ok=True)

                with path.open("a", encoding="utf-8") as file:
                    file.write(f"{username}\n")

                print(f"Added {username} to the ignore list.")


        elif choice == "3":
            if not ignored:
                print("Ignore list is currently empty.")
                continue

            print_usernames("Ignored Users", ignored)

            username = input("Username to remove: ").strip()

            matching = None
            for u in ignored:
                if u.casefold() == username.casefold():
                    matching = u
                    break

            if matching is None:
                print(f"{username} is not in the ignore list.")
                continue

            remaining = ignored - {matching}    # Remove

            # Rewrite the updated list
            with path.open("w", encoding="utf-8") as file:
                for user in sorted(remaining):
                    file.write(f"{user}\n")

            print(f"Removed {matching} from the ignore list.")

        else:
            print("Invalid option. Please try again.")                
    
     
def run_menu(instagram_data):
    """Main menu"""

    print_header("Instagram Follow Analysis")
    print(f"Username: {instagram_data.username}")
    print(f"Export date: {instagram_data.export_date}")
    print(f"Followers: {len(instagram_data.followers)}")
    print(f"Following: {len(instagram_data.followings)}")

    # Display initial primary overview
    print_usernames("Don't Follow You Back", instagram_data.not_following_back)

    actions = {
        "1": lambda: print_usernames("Don't Follow You Back", instagram_data.not_following_back),
        "2": lambda: print_usernames("You Don't Follow Back", instagram_data.not_followed_back),
        "3": lambda: print_usernames("Mutual Follows", instagram_data.mutual_follows),
        "4": lambda: manage_ignored_users(instagram_data),
        "5": lambda: export_data(instagram_data),
    }

    while True:
        print_header("Menu")
        print("Select an option:")
        print("1. View People Who Don't Follow You Back")
        print("2. View People You Don't Follow Back")
        print("3. View Mutual Follows")
        print("4. Manage Ignored Users")
        print("5. Export Data to txt Files")
        print("E. Exit")

        choice = input("Your choice: ").strip()

        if choice.upper() == "E":
            print("Exiting the program.")
            return

        action = actions.get(choice)
        if action:
            action()
        else:
            print("\nInvalid option. Please try again.")
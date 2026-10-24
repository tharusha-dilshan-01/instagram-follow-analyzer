import sys
import json
from pathlib import Path

class InstagramData:
    def __init__ (self, username: str|None, export_date: str|None, followers: set[str], followings: set[str], timestamps: dict[str, int|None]):
        self.username = username
        self.export_date = export_date  # YYYY-MM-DD
        self.followers = followers
        self.followings = followings
        self.timestamps = timestamps
        self.not_followed_back = self.followers - self.followings
        self.mutual_follows = self.followers & self.followings

    @property
    def ignored_users(self) -> set[str]:

        if not self.username:
            return set()
        
        path = Path("Exported_data")/ self.username/ "ignore.txt"
        if not path.exists():
            return set()
        
        with open(path, "r", encoding="utf-8") as file:
            return {
                line.strip().casefold()
                for line in file
                if line.strip()     # Ignore blank lines
            }            

    @property
    def not_following_back(self) -> set[str]:
        return self.followings - self.followers - self.ignored_users



def load_json_file(file_path: Path):
    """Open and load a json file"""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
        
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        sys.exit(1)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)


def get_followers(data_dir: Path) -> set[str]:
    """Collect follower usernames from every followers_*.json file in data_dir"""

    followers = set()

    # Load all followers files. (Ex: followers_1.json, followers_2.json, ...)
    follower_files = list(data_dir.glob("followers_*.json"))

    if not follower_files:
        print("No followers_*.json files found in this directory.")
        sys.exit(1)

    for file in follower_files:

        followers_data = load_json_file(file)

        if not isinstance(followers_data, list):
            print(f"Invalid json structure in {file}.")
            sys.exit(1)

        for user in followers_data:
            try:
                username = user["string_list_data"][0]["value"].casefold()
                followers.add(username)
            except (KeyError, IndexError, TypeError, AttributeError):
                continue  # Skip entries with unexpected/missing fields

    return set(followers)


def get_followings(data_dir) -> tuple[set[str], dict[str, int|None]]:
    """Read following.json and return usernames(set) and timestamps(dict)"""

    file_path = data_dir / "following.json"

    if not file_path.exists():
        print("No followings.json files found in this directory.")
        sys.exit(1)

    followings_data = load_json_file(file_path)

    # Expected shape: {"relationships_following": [ {...}, {...} ]}
    if not isinstance(followings_data, dict) or \
        "relationships_following" not in followings_data or \
        not isinstance(followings_data["relationships_following"], list):

        print("Invalid json structure in following.json.")
        sys.exit(1)

    followings = set()
    timestamps = {}

    for user in followings_data["relationships_following"]:
        if isinstance(user, dict) and user.get("title"):

            # Extract username
            username = user["title"].casefold()
            followings.add(username)

            # Extract timestamp
            timestamp = None
            string_data = user.get("string_list_data")

            if isinstance(string_data, list) and string_data:
                if isinstance(string_data[0], dict):
                    timestamp = string_data[0].get("timestamp")

            timestamps[username] = timestamp

    return followings, timestamps


def get_instagram_data(data_folder) -> InstagramData:
    """Build an InstagramData object from a chosen export folder."""

    username = data_folder.username
    export_date =  data_folder.date

    # Subfolder where followers and followings files exist
    data_dir = data_folder.path / "connections" / "followers_and_following"

    if not data_dir.is_dir():
        print(f"Directory not found: {data_dir}")
        sys.exit(1)

    followers = get_followers(data_dir)
    followings, timestamps = get_followings(data_dir)

    return InstagramData(username, export_date, followers, followings, timestamps)
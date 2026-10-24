from export_folders import find_instagram_data_folder
from instagram_data import get_instagram_data
from output_menu import run_menu


def main():
    """Main function to execute the script"""

    # Locate and select valid Instagram export directory
    data_folder = find_instagram_data_folder()

    # Read JSON files and load data
    instagram_data = get_instagram_data(data_folder)

    # Trigger interactive menu
    run_menu(instagram_data)

if __name__ == "__main__":
    main()
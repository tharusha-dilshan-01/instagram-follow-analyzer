# Instagram Follow Analyzer

A Python CLI tool that analyzes Instagram followers and following relationships using your downloaded Instagram data export.

## Features

- Identify people who don't follow you back (with follow duration).
- Identify followers you don't follow back.
- Find mutual follows.
- Manage an ignore list.
- Export analysis results to text files.

## Prerequisites & Setup

- Python 3.10 or later.
- Instagram Data Export:
    1. Request your data download from Instagram in **JSON format** (not HTML).
    2. Unzip the downloaded folder into your project root directory.

*Note: This tool uses standard Python library modules (`sys`, `re`, `json`, `pathlib`, `dataclasses`, `datetime`) so no external `pip` dependencies are required.*

## Usage

1. Place your extracted Instagram export folder inside the root directory of this repository (or run the tool directly where the folder exists).
2. Run the program:

   ```bash
   python main.py
   ```

3. Follow the instructions displayed in the terminal.

## Directory Structure & Reports

When exporting data, report files are automatically organized inside an `Exported_data` directory:

```text
Exported_data/
└── <username>/
    ├── ignore.txt
    └── <export_date>/
        ├── followers.txt
        ├── followings.txt
        ├── mutual_follows.txt
        ├── not_followed_back.txt
        └── not_following_back.txt  (Includes days followed)
```

## How Ignore Lists Work

If you follow accounts that you don't expect to follow you back (e.g., news outlets, celebrities), you can add them to an ignore list directly within the CLI menu. 

- The ignore list is saved per username at `Exported_data/<username>/ignore.txt`.
- Ignored users are filtered out from users who don't follow you back.

## Future Improvements

- Compare two Instagram exports to identify changes over time.
- Improve error handling and usability.

## Status

This project is under development.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
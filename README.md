# Satellite Tracker Bot


The Satellite Tracker Bot is a Discord bot that provides information about satellite passes over a specified location. Users can request pass-over data for a given satellite name or NORAD ID and a set of coordinates (latitude and longitude). The bot then retrieves satellite information and calculates the next 24-hour pass times in the local time zone of the provided coordinates.

## Features

- Retrieve satellite information based on satellite name or NORAD ID.
- Calculate and display the next 24-hour passes for the specified location.
- Convert pass times to the local time zone of the provided coordinates.

## Prerequisites

Before using the bot, you will need the following:

- Python 3.x
- Discord bot token (for running the bot on Discord)
- N2YO API key (for accessing satellite information)


Install the required Python packages:

shell

    pip install -r requirements.txt

    Configure the bot:
        Replace YOUR_DISCORD_TOKEN with your Discord bot token in the script (satbot.py).
        Replace YOUR_N2YO_API_KEY with your N2YO API key in the script (satbot.py).

Usage

    Invite the bot to your Discord server.

    Run the bot using the following command:

    shell

python satbot.py

In your Discord server, use the following command to get satellite pass-over data:

bash

    /satellite "satellite name or NORAD ID" "latitude longitude"

    Replace "satellite name or NORAD ID" with the satellite you want to track and "latitude longitude" with the coordinates of the location where you want to track the satellite.

    The bot will respond with pass-over times in the local time zone of the provided coordinates.

Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

    Fork the repository.
    Create a new branch for your feature or bug fix.
    Make your changes and commit them.
    Push your changes to your fork.
    Create a pull request to submit your changes for review.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    This bot was created by kezzkezzkezz.
    Special thanks to the N2YO API for providing satellite tracking data.

If you have any questions or issues, feel free to open an issue.

Happy satellite tracking!

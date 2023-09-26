import os
import requests
import json
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz
import traceback  # Add this import

# Define your Discord bot token and N2YO API key
N2YO_API_KEY = 'PUT YOUR N2YO API KEY HERE'
DISCORD_TOKEN = 'PUT YOUR DISCORD BOT TOKEN HERE'

MY_GUILD = discord.Object(id=PUT YOUR DISCORD SERVER ID HERE)  # replace with your guild id

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command()
async def satellite_get(interaction: discord.Interaction):
    await get_satellite(interaction)

@client.tree.command()
async def satellite_set(interaction: discord.Interaction, lat: float, lon: float):
    await set_satellite(interaction, lat, lon)

@client.tree.command()
async def satellite_pass(interaction: discord.Interaction, satid: int):
    try:
        print(f"NORAD ID: {satid}")
        satid = str(satid).strip()

        if str(interaction.user.id) not in user_coordinates:
            await interaction.response.send_message("User coordinates not found. Please set your coordinates using a command.")
            return

        lat, lon = user_coordinates[str(interaction.user.id)]

        response = requests.get(f'https://api.n2yo.com/rest/v1/satellite/radiopasses/{satid}/{lat}/{lon}/0/1/20/&apiKey={N2YO_API_KEY}')
        response.raise_for_status()
        data = json.loads(response.content)
        print("API Response:", data)

        if 'passes' not in data:
            await interaction.response.send_message("No pass data available for this satellite.")
            return

        if 'info' not in data or 'satname' not in data['info']:
            await interaction.response.send_message(f"Could not find a satellite with SATID: {satid}.")
            return

        satname = data['info']['satname']

        timezone_finder = TimezoneFinder()
        timezone_str = timezone_finder.timezone_at(lng=float(lon), lat=float(lat))

        if timezone_str is None:
            await interaction.response.send_message("Unable to determine the time zone for the provided coordinates.")
            return

        local_tz = pytz.timezone(timezone_str)

        embed = discord.Embed(
            title=f"Upcoming Satellite Passes",
            description=f"Next pass of {satname}",
            color=discord.Color.blue()
        )

        current_time_local = datetime.now(local_tz)

        for i, pass_info in enumerate(data['passes']):
            start_time_utc = datetime.utcfromtimestamp(pass_info['startUTC']).replace(tzinfo=pytz.utc)
            end_time_utc = datetime.utcfromtimestamp(pass_info['endUTC']).replace(tzinfo=pytz.utc)

            start_time_local = start_time_utc.astimezone(local_tz)
            end_time_local = end_time_utc.astimezone(local_tz)

            if start_time_local > current_time_local:
                embed.add_field(
                    name=f"Available Passes",
                    value=f"Start Time ({timezone_str}): {start_time_local.strftime('%I:%M %p %d %b %Y')}\nEnd Time ({timezone_str}): {end_time_local.strftime('%I:%M %p %d %b %Y')}",
                    inline=False
                )

        if not embed.fields:
            embed.add_field(
                name="No Upcoming Passes",
                value="There are no upcoming passes for the specified satellite in the provided location.",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    except discord.errors.NotFound as not_found_error:
        print(f"Interaction not found: {not_found_error}")
        await interaction.response.send_message("An error occurred: Interaction no longer exists.")
    except Exception as e:
        traceback.print_exc()
        await interaction.response.send_message(f"An error occurred: {e}")


# Load user coordinates from the JSON file during bot initialization
def load_user_coordinates():
    try:
        with open('user_coordinates.json', 'r') as file:
            coordinates = json.load(file)
            print("Loaded User Coordinates:", coordinates)
            return coordinates
    except FileNotFoundError:
        print("User Coordinates File Not Found")
        return {}

# Global user coordinates
user_coordinates = load_user_coordinates()

# Save user coordinates to the JSON file
def save_user_coordinates(coordinates):
    with open('user_coordinates.json', 'w') as file:
        json.dump(coordinates, file)

# Function to get satellite information
async def get_satellite(interaction: discord.Interaction):
    try:
        if str(interaction.user.id) in user_coordinates:
            lat, lon = user_coordinates[str(interaction.user.id)]
            await interaction.response.send_message(f"Your coordinates are Latitude: {lat}, Longitude: {lon}")
        else:
            await interaction.response.send_message("User coordinates not found. Please set your coordinates using /userdata set.")

    except Exception as e:
        traceback.print_exc()
        await interaction.response.send_message(f"An error occurred: {e}")

# Function to set user coordinates
async def set_satellite(interaction: discord.Interaction, lat: float, lon: float):
    try:
        global user_coordinates
        user_coordinates[interaction.user.id] = (lat, lon)
        save_user_coordinates(user_coordinates)
        await interaction.response.send_message("Coordinates set successfully.")

    except Exception as e:
        traceback.print_exc()
        await interaction.response.send_message(f"An error occurred: {e}")

# Start the bot
client.run(DISCORD_TOKEN)

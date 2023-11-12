import asyncio
from aiogram import Bot
from aiogram.types import ChatPermissions
import csv
from telethon import TelegramClient

# Replace 'YOUR_BOT_TOKEN' with your bot's token.
bot = Bot(token='YOUR_BOT_TOKEN')

# Your API credentials received when registering the application
api_id = 1111111 # your API_ID
api_hash = 'YOUR API HASH' # your API_HASH 
session_name = 'YOUR NAME' # the session name can be any

# Connecting to Telegram API
client = TelegramClient(session_name, api_id, api_hash)

# Link to the channel from which you want to get the list of users
channel_link = 'https://t.me/your_channel_name'

# The path to the file where the user list will be saved
csv_file_path = 'subscribers.csv'

# Function to get the list of users in the channel and save it to a CSV file
async def save_subscribers():
    async with client:
        # Receive channel object by reference
        channel = await client.get_entity(channel_link)
        # Get a list of users in the channel
        users = await client.get_participants(channel)
        # Write the list of users to a CSV file
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                if user.id != 111111111: # replace with your user ID
                    writer.writerow({
                        'id': user.id
                    })

async def remove_users():
    try:
        channel_id = -1001364400596  # Replace with the actual channel_id

        while True:
            # Open the user_id file
            with open('subscribers.csv', 'r') as file:
                lines = file.readlines()    
                for line in lines[2:]: # Skip the first line with the heading 'id'
                    user_id = int(line.strip())  # Convert the string to an integer #
                    user = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
                    if not user.status == "administrator":
                        await bot.ban_chat_member(chat_id=channel_id, user_id=user_id)
                        print(f"The user with ID {user_id} has been removed from the channel.")
                    else:
                        print(f"The user with ID {user_id} is the chat administrator and cannot be deleted.")
            # When the deletion of all users is complete, we will start collecting users again
            await save_subscribers()
            
    except Exception as e:
        print(f"Failed to delete user: {str(e)}")

if __name__ == '__main__':
    # Start an infinite loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(remove_users())

==========================
How to Launch the Bot 🤖
==========================

**Welcome to the Telegram bot simulator of Школа 21!** 🤖  
This bot is designed for a game where you will battle verters and learn to program.

Bot Features:
=============
- **Character Selection**: Choose your hero from a variety of unique characters! 🧑‍🎤
- **Item Selection**: Obtain items to help you in the game! 🗡️
- **Explore Locations**: Move between different areas of the school and find projects to complete. 🌍
- **Fight Verters**: Battle verters and improve your skills! ⚔️
- **Talk to NPCs**: Interact with NPCs to receive tasks and bonuses! 🗣️
- **Simple Interface**: Use commands and buttons to navigate through the game easily.

Commands You Can Use:
=====================
- **/start**: Begin your adventure!
- **🧑‍🎤 Choose Player**: Select your character.
- **🗡️ Choose First Item**: Choose your starting item.
- **🎮 Start Game**: Start the game!
- **❌ End Game**: End the current game.

Steps to Launch the Bot:
========================
To launch the bot yourself, follow these steps:

1. **Clone the Repository**  
   Clone the bot's project repository to your local machine:

   ```bash
   git clone <repository>
   ```
2. **Move to src folder**
    Move into src:

    ```bash
    cd src
    ```

3. **Insert your API_KEY**
    Insert your API_KEY from your telegram-bot into bot.py <API_KEY>


4. **Use Makefile to install dependencies**

    ```
    make create_venv && make start_bot
    ```
    # or 
    ```
    make run_in_docker
    ```


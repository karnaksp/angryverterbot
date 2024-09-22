"""
Telegram bot on aiogram and asyncio for play in s21_school text game
"""

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from load_data import init_game_elements
from load_map import init_start_location, load_map
import asyncio
import logging
import io
import os
import contextlib
from colorlog import ColoredFormatter


def setup_logger():
    """
    Configures and returns a logger with colored console output.

    The color scheme for the log levels is as follows:
    - DEBUG: Cyan
    - INFO: Green
    - WARNING: Yellow
    - ERROR: Red
    - CRITICAL: Bold Red

    Returns:
        logging.Logger: A configured logger instance with colored console output.

    Example:
        logger = setup_logger()
        logger.info("This is an info message")
        logger.error("This is an error message")
    """
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


logger = setup_logger()

API_TOKEN = os.environ.get("TOKEN")  # api token for your bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
player = None
verters = []
npcs = []
player_choices = {}
player_location = {}
valid_player_names = [
    "🐱 Karnaks Puck",
    "🦉 Odis Wish",
    "🦾 Alucard",
    "🎸 Johnny Silverhand",
]
valid_items = ["🧴 Head & Shoulders", "👕 T-shirt", "☕ Thermomug", "📦 Stickerpack"]
locations = load_map()

logger.info(f"Map loaded with {len(locations)} locations.")

main_menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧑‍🎤 Choose Player"),
            KeyboardButton(text="🗡️ Choose First Item"),
        ],
        [KeyboardButton(text="🎮 Start Game")],
        [KeyboardButton(text="❌ End Game")],
    ],
    resize_keyboard=True,
)

player_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🐱 Karnaks Puck"), KeyboardButton(text="🦉 Odis Wish")],
        [
            KeyboardButton(text="🦾 Alucard"),
            KeyboardButton(text="🎸 Johnny Silverhand"),
        ],
        [KeyboardButton(text="🔙 Back to Main Menu")],
    ],
    resize_keyboard=True,
)

item_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧴 Head & Shoulders"), KeyboardButton(text="👕 T-shirt")],
        [KeyboardButton(text="☕ Thermomug"), KeyboardButton(text="📦 Stickerpack")],
        [KeyboardButton(text="🔙 Back to Main Menu")],
    ],
    resize_keyboard=True,
)


@dp.message(F.text == "/start")
async def send_welcome(message: types.Message):
    """
    Handles the '/start' command when the user initiates the bot.

    Initializes the user's player choices and sends a welcome message with the main menu buttons.

    Args:
        message (types.Message): The message object containing the user's command.
    """
    player_choices[message.from_user.id] = {"player": None, "item": None}
    logger.info(f"New user started the bot: {message.from_user.id}")
    await message.answer("Welcome! Choose an option:", reply_markup=main_menu_buttons)


@dp.message(F.text.in_({"🧑‍🎤 Choose Player", "🗡️ Choose First Item"}))
async def show_submenu(message: types.Message):
    """
    Handles menu choices for selecting a player or first item.

    Based on the user's choice, presents the appropriate submenu to choose either a player or an item.

    Args:
        message (types.Message): The message object containing the user's choice.
    """
    if message.text == "🧑‍🎤 Choose Player":
        logger.debug(f"User {message.from_user.id} is choosing a player.")
        await message.answer("Choose a player type:", reply_markup=player_buttons)
    elif message.text == "🗡️ Choose First Item":
        logger.debug(f"User {message.from_user.id} is choosing an item.")
        await message.answer("Choose an item type:", reply_markup=item_buttons)


def initialize_user_if_needed(user_id):
    """
    Initializes the player's choices for a given user if they haven't been initialized yet.

    Args:
        user_id (int): The ID of the user to initialize.
    """
    global player_choices
    if user_id not in player_choices:
        player_choices[user_id] = {"player": None, "item": None}
        logger.info(f"Initialized player choices for user {user_id}.")


@dp.message(F.text.in_(valid_player_names))
async def choose_player(message: types.Message):
    """
    Handles the user's selection of a player.

    Validates the player's choice and updates the user's player choice, then prompts to select an item.

    Args:
        message (types.Message): The message object containing the player's choice.
    """
    user_id = message.from_user.id
    initialize_user_if_needed(user_id)
    chosen_player = (
        message.text if message.text in valid_player_names else message.text.strip()
    )
    player_choices[user_id]["player"] = chosen_player
    logger.info(f"User {user_id} selected player: {chosen_player}")
    await message.answer(
        f"Player {chosen_player} selected. Now choose an item:",
        reply_markup=item_buttons,
    )


@dp.message(F.text.in_(valid_items))
async def choose_item(message: types.Message):
    """
    Handles the user's selection of an item.

    Validates the item choice and updates the user's item choice, then informs the user they can start the game.

    Args:
        message (types.Message): The message object containing the item choice.
    """
    user_id = message.from_user.id
    initialize_user_if_needed(user_id)
    chosen_item = message.text if message.text in valid_items else message.text.strip()
    player_choices[user_id]["item"] = chosen_item
    logger.info(f"User {user_id} selected item: {message.text}")
    await message.answer(
        f"Item {message.text} selected. You can start the game now!",
        reply_markup=main_menu_buttons,
    )


@dp.message(F.text == "🔙 Back to Main Menu")
async def back_to_main_menu(message: types.Message):
    """
    Handles the user's request to return to the main menu.

    Sends the main menu buttons back to the user.

    Args:
        message (types.Message): The message object containing the user's request.
    """
    logger.debug(f"User {message.from_user.id} returned to the main menu.")
    await message.answer("Choose an option:", reply_markup=main_menu_buttons)


@dp.message(F.text == "❌ End Game")
async def end_game(message: types.Message):
    """
    Ends the current game session for the user.

    Removes the user's location and player choices, and provides the option to start a new game.
    Logs the action if the user was in a game, otherwise notifies the user that no game was in progress.

    Args:
        message (types.Message): The message object containing the user's request to end the game.
    """
    user_id = message.from_user.id
    if user_id in player_location:
        del player_location[user_id]
        del player_choices[user_id]
        await message.answer(
            "Game has been ended. You can start a new game by clicking 'Start Game'.",
            reply_markup=main_menu_buttons,
        )
        logger.info(f"User {user_id} has ended the game.")
    else:
        await message.answer("You are not in a game. Start the game first.")


@dp.message(F.text == "🎮 Start Game")
async def start_game(message: types.Message):
    """
    Starts a new game for the user if both player and item have been selected.

    Initializes the game elements (player, verters, npcs) and sets up the starting location.
    If the player or item is not selected, notifies the user to make the necessary selections.

    Args:
        message (types.Message): The message object containing the user's request to start the game.
    """
    global player, verters, npcs
    user_id = message.from_user.id
    initialize_user_if_needed(user_id)
    choices = player_choices[user_id]
    if choices["player"] and choices["item"]:
        logger.info(
            f"User is starting the game with player {choices['player']} and item {choices['item']}."
        )
        player, verters, npcs = init_game_elements(choices["player"], choices["item"])
        init_start_location()
        await show_location_info(message)
    else:
        logger.warning(
            f"User {user_id} tried to start the game without selecting both player and item."
        )
        await message.answer(
            "Please select both a player and an item before starting the game."
        )


async def congratulate_player(message: types.Message):
    """
    Sends a congratulatory message to the user for completing the game by reaching level 9.

    After congratulating, the game session is ended.

    Args:
        message (types.Message): The message object containing the user's level-up event.
    """
    await message.answer(
        "🎉 Congratulations on reaching level 9! You've completed the game!"
    )
    await end_game(message)


async def show_location_info(message: types.Message):
    """
    Displays the current location information to the player, along with available actions.

    This function sends the player a detailed description of the current location, including:
    1. The location's name and description.
    2. Verters (enemies) present in the location, with options to engage in combat.
    3. NPCs present in the location, with options to start a conversation.
    4. Available directions for moving to adjacent locations.

    Three different inline keyboards are generated for:
    - Navigating to different directions.
    - Fighting available Verters.
    - Interacting with NPCs.

    Args:
        message (types.Message): The message object from the user, used to display the location and available actions.
    Global Variables:
        player (Player): The player object containing the current location.
        verters (List[Verter]): List of Verters present in the game world.
        npcs (List[NPC]): List of NPCs present in the game world.
    """

    global player, verters, npcs
    current_location = locations[str(player.current_location)]
    npcs_in_location = [npc for npc in npcs if npc.location == current_location["name"]]
    verters_in_location = [
        verter for verter in verters if verter.location == current_location["name"]
    ]

    direction_keyboard = InlineKeyboardBuilder()
    for direction in current_location["connections"]:
        direction_keyboard.button(
            text=direction.capitalize(), callback_data=f"move_{direction}"
        )
    verter_keyboard = InlineKeyboardBuilder()
    for verter in verters_in_location:
        verter_keyboard.button(
            text=f"Try {verter.name}", callback_data=f"fight_{verter.name}"
        )
    npc_keyboard = InlineKeyboardBuilder()
    for npc in npcs_in_location:
        npc_keyboard.button(text=npc.name, callback_data=f"talk_{npc.name}")

    verter_keyboard.adjust(3)
    npc_keyboard.adjust(3)
    direction_keyboard.adjust(2)

    await message.answer(
        text=f"Location: {current_location['name']}\n\nDescription: {current_location['description']}\n\nFrom this location you can go to direction:",
        reply_markup=direction_keyboard.as_markup(),
    )
    await message.answer(
        text="In this location you can start project:",
        reply_markup=verter_keyboard.as_markup(),
    )
    await message.answer(
        text="Try speakin with Peer in this location:",
        reply_markup=npc_keyboard.as_markup(),
    )


@dp.callback_query(lambda c: c.data.startswith("fight_"))
async def fight_verter(query: types.CallbackQuery):
    """
    Handles the player's request to fight a Verter (enemy).

    This function processes the callback query triggered when the player selects a Verter to fight.
    It retrieves the Verter based on the name in the callback data and initiates the combat sequence by calling the player's attack method.
    After the fight, it checks if the player reached level 9 and triggers a congratulation message if necessary.

    Args:
        query (types.CallbackQuery): The callback query from the player's interaction with the Verter.

    Global Variables:
        player (Player): The player object who is attacking the Verter.
        verters (List[Verter]): List of all available Verters in the game world.
    """
    global player
    verter_name = query.data.split("_")[1]
    verter = next((verter for verter in verters if verter.name == verter_name), None)

    if verter:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            player.attack(verter)

        response = output.getvalue().strip()
        await query.message.answer(response or "No response from the Verter.")
        await query.answer("You try project: " + verter_name + ".")
        if player.level == 9:
            await congratulate_player(query.message)
        if "therapist" in response:
            await end_game(query.message)
    else:
        await query.answer("This Verter does not exist.")


@dp.callback_query(lambda c: c.data.startswith("talk_"))
async def talk_to_npc(query: types.CallbackQuery):
    """
    Handles the player's request to talk to an NPC.

    This function processes the callback query when the player chooses to talk to an NPC.
    It retrieves the NPC based on the name in the callback data and initiates the dialogue using the player's talk_to method.

    Args:
        query (types.CallbackQuery): The callback query from the player's interaction with the NPC.

    Global Variables:
        player (Player): The player object who is talking to the NPC.
        npcs (List[NPC]): List of all available NPCs in the game world.
    """
    global player
    npc_name = query.data.split("_")[1]
    npc = next((npc for npc in npcs if npc.name == npc_name), None)

    if npc:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            player.talk_to(npc)

        response = output.getvalue().strip()
        await query.message.answer(response or "No response from the NPC.")
        await query.answer("You talked to " + npc_name + ".")
    else:
        await query.answer("This NPC does not exist.")


@dp.callback_query(F.data.startswith("move_"))
async def handle_move_callback(query: types.CallbackQuery):
    """
    Handles the player's movement between locations.

    This function processes the callback query when the player selects a direction to move.
    It updates the player's current location based on the selected direction and displays information about the new location.

    Args:
        query (types.CallbackQuery): The callback query from the player's interaction with the movement buttons.

    Global Variables:
        player (Player): The player object whose location is being updated.
        locations (Dict[str, Dict]): A dictionary representing all locations and their connections in the game world.
    """
    global player
    direction = query.data.split("_")[1]
    current_location = locations[str(player.current_location)]
    if direction in current_location["connections"].keys():
        new_location = current_location["connections"][direction]
        player.current_location = new_location
        await show_location_info(query.message)
        await query.answer()
    else:
        await query.answer(
            f"Invalid direction! Available directions: {', '.join(locations[current_location]['connections'].keys())}."
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

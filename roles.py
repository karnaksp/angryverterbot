"""
Module containing classes for creating game roles.

Game Roles:
1. Protagonist - The main character, a student at a programming school.
2. NPC - Characters that can be interacted with (Peers).
3. Enemy (Projects, Verter) - Enemies that must be fought (projects and their verification system).

The protagonist interacts with NPCs, completes projects, and their knowledge and skills grow depending on the success of the projects.
"""

import random
from collections import defaultdict
from typing import Dict, DefaultDict, List, Any


class Protagonist:
    """
    Class representing the protagonist (main character) of the game.

    Attributes:
        ----------
        id: str
            Unique identifier of the player.
        name: str
            Name of the player.
        hp: int
            Number of "nerve cells" (life points) of the player.
        level_points: int
            Experience points used for leveling up.
        level: int
            Current level of the player.
        inventory: DefaultDict[str, int]
            Inventory of the player.
        quests: Dict[str, Dict[str, Union[int, bool]]]
            Active quests of the player.
    """

    def __init__(self, name: str, id: str, item: str = "Head & Shoulders"):
        """
        Initialize the protagonist with basic parameters.

        Parameters:
        ----------
            name: str
                Name of the player.
            id: str
                Unique identifier of the player.
        """
        self.id = id
        self.name: str = name
        self.hp: int = 100
        self.level_points: int = 10
        self.level: int = 1
        self.inventory: DefaultDict[str, int] = defaultdict(int)
        self.inventory[item] += 1
        self.quests: Dict[Any, Any] = {}
        self.current_location = 1

    def talk_to(self, npc: "NPC") -> None:
        """
        The protagonist interacts with an NPC and receives a random phrase in return.
        If the NPC is a Peer, handle quests and items as well.

        Parameters:
            ----------
            npc: NPC
                The NPC being interacted with.
        """

        npc.talk(self)
        for quest_name in self.quests:
            quest = self.quests[quest_name]
            if quest.get("type") == "interaction" and (quest.get("npc_name") == npc.name or quest.get("npc_type") == npc.type):
                self.check_quests("iteraction", quest_name)

            elif quest.get("type") == "item_transfer" and (quest.get("npc_name") == npc.name or quest.get("npc_type") == npc.type):
                if self.give(npc, quest.get("item")):
                    self.check_quests("item_transfer", quest_name)

    def take_answer(self, yes: bool = False):
        """
        Protagonist responds depending on whether they have the quest done or not.

        Parameters:
            ----------
            yes: bool
                The variable representing whether the quest is done or not.
        """
        if yes:
            print(f"**You**: Oh, thank you very much. I'll go hard.\n")
        else:
            print(f"**You**: Thank you, but I have it already!\n")

    def attack(self, enemy: "Enemy") -> None:
        """
        The protagonist attempts to complete a project by "attacking" an enemy (project).

        Parameters:
            ----------
            enemy: Enemy
                The enemy (project) being interacted with.
        """
        reason_to_fight = self.quests.get(enemy.name)

        if reason_to_fight is None or reason_to_fight.get("done") == False:
            protagonist_rand = random.randint(70, 100) * self.hp / 100
            enemy_rand = enemy.attack()

            if enemy_rand > protagonist_rand:
                print(
                    f"Peers said you completed the project with: {protagonist_rand}, Verter rated your project: {enemy_rand}. You are the best! and you're hp increase by 1 point\n"
                )
                self.heal(1)
            if enemy_rand > 80:
                print(f"You successfully completed the project {enemy.name}!\n")
                self.advance_knowledge(enemy.points)
                self.advance_level()
                self.check_quests("project", enemy.name)
            else:
                print(
                    f"The project '{enemy.name}' was too difficult. , Verter rated your project: {enemy_rand}. You lost 10% of your nerve cells.\n"
                )
                self.take_hit()
        else:
            print("~~You have alredy defeated this Verter.~~")

    def take_hit(self, value: int = -10) -> None:
        """
        The protagonist loses a certain number of nerve cells.

        Parameters:
            ----------
            value: int
                The number of nerve cells lost (default is -10).
        """

        self.hp += value
        if self.hp <= 30:
            print(
                "####You have been expelled. You are given a certificate to visit a therapist.####"
            )

    def heal(self, value: int = 10) -> None:
        """
        The protagonist recovers a certain number of nerve cells.

        Parameters:
            ----------
            value: int
                The number of nerve cells recovered (default is 10).
        """
        self.hp += value

    def advance_knowledge(self, value: int = 1) -> None:
        """
        The protagonist improves their knowledge.

        Parameters:
            ----------
            value: int
                The amount of knowledge gained (default is 1).
        """
        self.level_points += value
        print(f"Your knowledge increased! You now have "
              f"{self.level_points} points.\n")

    def advance_level(self) -> None:
        """
        Method to update the player's level based on their level points.
        Levels progress according to:
        - Level 2: > 100 points
        - Level 3: > 300 points
        - Level 4: > 700 points
        - Level 5: > 1500 points
        - And so on up to level 9.
        """

        match self.level_points:
            case points if points > 7000:
                self.level = 9
            case points if points > 5000:
                self.level = 8
            case points if points > 3800:
                self.level = 7
            case points if points > 2500:
                self.level = 6
            case points if points > 1500:
                self.level = 5
            case points if points > 700:
                self.level = 4
            case points if points > 300:
                self.level = 3
            case points if points > 100:
                self.level = 2
            case _:
                self.level = 1

        print(f"Your level: {self.level}\n")

    def take(self, item: str) -> None:
        """
        The protagonist takes an item and adds it to their inventory.

        Parameters:
            ----------
            item: str
                The name of the item to be added to the inventory.
        """
        self.inventory[item] += 1
        print(f"You received an item: {item}.\n")

    def give(self, npc: "NPC", item: str) -> bool:
        """
        The protagonist gives an item to an NPC.

        Parameters:
            ----------
            npc: NPC
                The NPC receiving the item.
            item: str
                The name of the item being given.
        Returns:
        -------
            bool
                Whether the item was given or not.
        """
        if self.inventory[item] > 0:
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]
            npc.take(item)
            print(f"You gave {item} to NPC {npc.name}.\n")
            return True
        else:
            print(f"You don't have the item {item}.\n")
            return False

    def accept_quest(self, quest: Dict[Any, Any]) -> None:
        """
        The protagonist accepts a quest from an NPC.

        Parameters:
            ----------
            quest: Dict[str, Union[int, bool]]
                The quest being accepted.
        """
        quest_name = quest["name"]
        if quest["name"] in self.quests:
            self.take_answer(False)
        else:
            self.quests[quest_name] = quest
            self.take_answer(True)
            print(f"You accepted the quest: {quest_name}")
            print(f"{quest["description"]}\n")

    def check_quests(self, action_type: str, action_value: str) -> None:
        """
        Checks if the conditions for any quests are fulfilled.

        Parameters:
            ----------
            action_type: str
                The type of action performed (e.g., "project", "interaction", "item_transfer").
            action_value: str
                The value associated with the action (e.g., project name, NPC name, item name).
        """

        quest = self.quests.get(action_value)

        if quest is not None and quest.get("done") == False:
            self.quests[action_value]["done"] = True
            self.hp += quest.get("health", 0)
            self.level_points += quest.get("level_points", 0)
            print(f"Quest '{action_value}' completed! You gained {quest["health"]} HP and {quest["level_points"]} level points.\n")
            self.quests[action_value] = {"done": True}

        elif action_type == "project":
            self.quests[action_value] = {"done": True}

    def whereami(self):
        """
        Prints the description of the current location.
        """
        location = self.game_map.get(self.current_location)
        if location:
            print(f"You are at {location['name']}. {location['description']}\n")
        else:
            print("You are in an unknown place.\n")

    def get_location_by_name(self, name):
        for _, location_info in self.game_map.items():
            if location_info.get('name') == name:
                return location_info
        return None

    def go(self, direction: str):
        """
        Move to another location in the given direction.
        """
        if self.current_location:
            connections = self.current_location.get("connections", {})
            if direction in connections:
                self.current_location = connections[direction]
                print(self.current_location)
                self.whereami()
            else:
                print(f"You can't go {direction} from here.\n")
        else:
            print("Invalid current location.\n")


class NPC():
    """
    Class representing an NPC, a type of basic non-playable character.

    Attributes
    ----------
    phrases : List[str]
        A list of phrases that the NPC can say.
    location : str
        The location where Peer is situated.
    quest : Dict[str, Dict[str, Any] or None
        The current quest assigned to the Peer, selected randomly from the provided list of quests.
    inventory : Dict[str, int]
        A  dictionary of items NPC has and it's amount.
    """
    def __init__(self, name: str, type: str, quests: Dict[str, Dict[Any, Any]], location: Dict[Any, Any], phrases: List[str], inventory: List[Dict[Any, Any]]):
        """
        Initializes an NPC.

        Parameters
        ----------
        location : str
            The location where NPC is situated.
        phrases : List[str]
            A list of possible phrases that the NPC can say.
        quests : List[Dict[str, Dict[str, Any]]]
            A list of possible quests that the NPC can offer to protagonist.
        
        Raises
        ------
        ValueError
            If any required data is missing or empty.
        """
        if not name:
            raise ValueError("Name is required for NPC initialization.")
        self.name: str = name

        if not type:
            raise ValueError("Type is required for NPC initialization.")
        self.type: str = type

        if not phrases or len(phrases) < 5:
            raise ValueError("At least 5 phrases are required for NPC initialization.")
        self.phrases = random.sample(phrases, 5)

        if not location:
            raise ValueError("Valid location is required for NPC initialization.")
        self.location: Dict[Any, Any] = location

        if not inventory:
            raise ValueError("Inventory is required for NPC initialization.")
        self.inventory: List[Dict[str, Any]] = random.sample(inventory, 2)

        if not quests:
            raise ValueError("Quests are required for NPC initialization.")
        self.quest = self.select_random_quest(quests) if quests else None

    def select_random_quest(
        self, quests_json: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Selects a random quest from the given quests JSON and add phrase from quest to all pull phrases.

        Parameters
        ----------
        quests_json : Dict[str, Dict[str, Any]]
            A dictionary of quests where each key is a quest name and the value is a dictionary with quest details.

        Returns
        -------
        Dict[str, Any]
            A dictionary with the selected quest details, including the quest name.
        """
        quest_name = random.choice(list(quests_json.keys()))
        quest_details = quests_json[quest_name]
        quest_details["name"] = quest_name
        self.phrases.append(quest_details["phrase"])
        return quest_details

    def talk(self, protagonist: "Protagonist") -> None:
        """
        Communicate with the protagonist. If the NPC offers a quest or item, handle it.

        Parameters
        ----------
        protagonist : Protagonist
            The protagonist interacting with the NPC.
        """

        selected_phrase = random.choice(self.phrases)
        print(f"**{self.name}**: {selected_phrase}\n")

        if self.quest and selected_phrase == self.quest["phrase"]:
            self.give_quest(protagonist, self.quest)
            return

        for item in self.inventory:
            if selected_phrase == item.get("phrase"):
                self.give(protagonist, item["name"])
                item["amount"] -= 1
                protagonist.heal(item["mental_health"])
                print(f"You healed {item['mental_health']} HP.\n")
                return

    def give_quest(self, protagonist: "Protagonist", quest: Dict[str, Any]) -> None:
        """
        Provides the protagonist with a quest.

        Parameters
        ----------
        protagonist : Protagonist
            The protagonist interracting with the NPC.
        quest : Dict[str, Any]
            The quest that protagonist will be provided with
        """
        protagonist.accept_quest(quest)

    def take(self, item: str) -> None:
        """
        Adds a given item to NPC's inventory.

        Parameters
        ----------
        item : str
            The name of the item
        """
        for item in self.inventory:
            if item["name"] == item:
                item["amount"] += 1

    def give(self, protagonist: "Protagonist", item) -> None:
        """
        Provides the protagonist with the item.

        Parameters
        ----------
        item : str
            The name of the item
        """
        protagonist.take(item)


class Enemy:
    """
    Class representing an enemy chrarcter.

    Attributes
    ----------
    quest : Dict[Any,Any]
        A dictionary that provides information about enemy's health and points protagonist will be awarded with after enemy's defeat.
    hp : int
        An amount of enemy's health
    points : int
        An amount of points protagonist will be awarded with enemy's defeat.
    """
    def __init__(self, quest: Dict[Any, Any], location: str):
        """
        Initializes an Enemy.

        Parameters
        ----------
        location : str
            The location where Peer is situated.
        quest: Dict[Any, Any]
            A dictionary containing all basic info about enemy
        
        Raises
        ------
        ValueError
            If any required data is missing or empty.
        """
        if not isinstance(quest, dict):
            raise ValueError("A valid quest dictionary is required for Enemy initialization.")
        self.quest = quest
        if not isinstance(quest["health"], (int, float)):
            raise ValueError("A valid 'health' value is required in the quest for Enemy initialization.")
        self.hp = quest["health"]

        if not isinstance(quest["level_points"], int):
            raise ValueError("A valid 'level_points' value is required in the quest for Enemy initialization.")
        self.points = quest["level_points"]

        if not isinstance(location, str):
            raise ValueError("A valid location is required for Enemy initialization.")
        self.location = location


class Verter(Enemy):
    """
    Class representing a Verter, a type of enemy character.

    Attributes
    ----------
    quest : Dict[Any,Any]
        A dictionary that provides information about both enemy's health and points protagonist will be awarded with after enemy's defeat.
    hp : int
        An amount of enemy's health
    points : int
        An amount of points protagonist will be awarded with enemy's defeat.
    """

    def __init__(self, quest: Dict[Any, Any], location: str, phrases: List[str]):
        """
        Initializes an Verter.

        Parameters
        ----------
        quest : Dict[Any,Any]
            A dictionary that provides information about enemy's health and points protagonist will be awarded with after enemy's defeat.
        hp : int
            An amount of enemy's health
        points : int
            An amount of points protagonist will be awarded with enemy's defeat.
        phrases : List[str]
            A list of possible phrases that the Verter can say.
        name : str
            A name of quest where Verter is from.
        
        Raises
        ------
        ValueError
            If any required data is missing or empty.
        """
        super().__init__(quest, location)
        if not isinstance(quest, dict):
            raise ValueError("A valid quest dictionary is required for Verter initialization.")
        
        if not isinstance(quest["name"], str):
            raise ValueError("A valid 'name' must be provided in the quest for Verter initialization.")
        self.name = quest["name"]

        if not isinstance(phrases, list) or len(phrases) < 1:
            raise ValueError("A valid list of phrases is required for Verter initialization.")
        self.phrases = phrases

    def attack(self) -> int:
        """
        Reduce Verter's health by provided value.

        Returns
        -------
        int
            Amount of damage protagonist will get
        """

        enemy_rand = random.randint(70, 100)
        print(f"Verter: {random.choice(self.phrases)}\n")

        return enemy_rand

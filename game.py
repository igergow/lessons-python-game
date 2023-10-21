import random
import math
import time
from enum import Enum, auto
from typing import Any
from unique_names_generator import get_random_name
from unique_names_generator.data import ADJECTIVES, STAR_WARS, NAMES
from termcolor import colored
from prettytable import PrettyTable

MAX_ITEMS = 3
MAX_CHANCE = 3
HEALTH_PER_LEVEL = 100
EXP_PER_LEVEL = 100

def padLine(length: int = 100, char: str = "-") -> str:
    return print(colored(char * length, 'grey'))

def splash_screen():
  print('''
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛🟥🟥🟥🟥🟥🟥⬛⬛⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛⬜⬜⬜
⬜⬜⬜⬜⬜⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛⬜⬜
⬜⬜⬜⬜⬜⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛⬜⬜
⬜⬜⬜⬜⬜⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛⬜⬜
⬜⬜⬜⬜⬜⬛🟥🟥🟥🟥🟥⬛🏽🏽🟥🟥🟥🟥🟥🏽⬛⬜⬜
⬜⬜⬜⬜⬜⬛🟥🟥🟥🟥⬛⬛⬛🏽🏽🏽🟥🟥🏽🏽⬛⬜⬜
⬛⬛⬜⬜⬜⬜⬛🟥🟥🟥⬛⬛⬜⬜🏽🏽🟥🟥🏽🏽⬛⬜⬜
⬛🟫⬛⬜⬜⬜⬛🟥🟥🟥⬛⬛⬜⬜⬜🏽🟥🟥🏽⬛⬜⬜⬜
⬜⬛🟫⬛⬜⬜⬜⬛🟥🟥🟥⬛⬛⬛🏽🏽🟥🟥🏽⬛⬜⬜⬜
⬜⬜⬛🟫⬛⬜⬜⬜⬛🟥🟥🟥⬛⬛🏽🟥🟥🟥🟥⬛⬜⬜⬜
⬜⬜⬜⬛🟫⬛⬜⬛⬛⬛🟥🟥🟥🟥🟥🟥🟥🟥⬛⬜⬜⬜⬜
⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛🟥🟥🟥🟥🟥⬛⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟥⬛⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛🟥🟥🟥🟥🟥🟥⬛⬛⬜⬜⬜
⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛🟥🟥🟥🟥🟥🟥⬛⬛⬜⬜⬜
⬜⬜⬜⬜⬛🟥⬛⬛⬛⬛⬛⬛⬛🟥🟥🟥🟥🟥⬛⬛⬜⬜⬜
⬜⬜⬜⬛⬛🟥🟥⬛⬛⬛⬛⬛⬛🟥🟥🟥🟥🟥⬛⬛⬛⬜⬜
⬜⬜⬜⬛⬛⬛🟥🟥⬛⬛⬛⬛⬛🟥🟥🟥🟥🟥⬛⬛⬛⬜⬜
⬜⬜⬜⬛🟥⬛⬛⬛⬜⬜⬛⬛⬛🟥🟥🟥🟥🟥⬛⬛⬛⬜⬜
⬜⬜⬛🟥🟥🟥⬛⬜⬜⬜⬛⬛⬛🟥🟥⬛⬛⬛⬛⬛⬛⬛⬜
⬜⬜⬛🟥🟥🟥⬛⬜⬜⬜⬛⬛⬛⬛⬛⬜🟥⬜⬛⬛🟥⬛⬜
⬜⬜⬛⬛⬛⬛⬛⬜⬜⬛⬛⬛⬛⬛⬛⬜🟥⬜⬛⬛🟥⬛⬜
⬜⬜⬛🟥🟥🟥🟥⬛⬜⬛⬛⬛🟥🟥🟥⬛⬛⬛⬛⬛⬛⬛⬜
⬜⬜⬛🟥🟥🟥🟥⬛⬛⬛⬛🟥🟥🟥🟥🟥🟥🟥⬛⬛🟥🟥⬛
⬜⬜⬛🟥🟥🟥⬛🟥⬛⬛🟥🟥🟥🟥⬛🟥⬛🟥⬛⬛⬛🟥⬛
⬜⬜⬜⬛🟥🟥⬛⬛⬛🟥🟥🟥🟥🟥⬛⬛🟥🟥🟥⬛⬛🟥⬛
⬜⬜⬜⬜⬛⬛⬛⬛🟥🟥🟥🟥🟥🟥⬛🟥🟥🟥🟥⬛⬛⬛⬛
⬜⬜⬜⬜⬜⬜⬛🟥🟥🟥🟥🟥🟥⬛⬛🟥🟥🟥🟥⬛⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬛🟥⬛🟥⬛🟥🟥⬛⬛🟥🟥⬛🟥⬛⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬛🟥⬛⬛🟥🟥⬛⬜⬛🟥🟥⬛⬛⬛⬜⬜⬜
⬜⬜⬜⬜⬜⬛🟥🟥🟥🟥🟥⬛⬜⬜⬛🟥🟥🟥🟥⬛⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜
⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬛⬛⬛⬛⬛🟥⬛⬜⬜
⬜⬜⬜⬜⬛🟥🟥🟥⬛⬛⬜⬜⬜⬜⬜⬛⬛⬛🟥🟥🟥⬛⬜
⬜⬜⬜⬜⬛🟥🟥🟥🟥⬛⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜
⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
''')

def random_with_small_priority(max_value):
    exp = random.randint(1, 3)
    return math.ceil((random.random() ** exp) * max_value)

def color_print(hero_name, opponent_name, damage, is_double_attack=False, is_reversed_colors=False, using_item=False):
    crit_emoji = ' ⚡ CRITICAL STRIKE' if is_double_attack else ''
    hero_name = hero_name if not using_item else f"🗡️ {hero_name}"
    color = 'blue' if is_reversed_colors else 'red'
    inversed_color = 'red' if is_reversed_colors else 'blue'
    print(colored(hero_name, color) + ' attacked ' + colored(opponent_name, inversed_color) + ' with ' + colored(str(damage), 'yellow') + ' 😈' + crit_emoji)

def generate_monster(level=1):
    monster_name = get_random_name(combo=[ADJECTIVES, STAR_WARS])
    monster_level = random_with_small_priority(level)
    monster_health = monster_level * HEALTH_PER_LEVEL
    monster_attack = monster_level * 10 - 5
    monster_type = get_random_name(separator="-", style="lowercase")
    monster = Monster(monster_name, monster_health, monster_attack, monster_type, level=monster_level)
    return monster

def print_health_bar(name, current_health, max_health, max_bar_length=50, is_hero=True):
    proportion = current_health / max_health
    number_of_hashes = int(proportion * max_bar_length)
    bar = '#' * number_of_hashes + '-' * (max_bar_length - number_of_hashes)
    max_name_length = 25
    formatted_name = name.ljust(max_name_length)
    color = 'blue' if is_hero else 'red'
    health_text = colored("💀", 'red') if current_health<=0 else f"{current_health}/{max_health}"
    print(f"{colored(formatted_name, color)}: |{colored(bar, 'red')}| {health_text}")

class Skill:
    LEVEL_UP_DAMAGE_INCREASE: float = 0.3

    def __init__(self, name: str, damage: int, level_required: int, blockable: bool) -> None:
        self.name = name
        self.blockable = blockable
        self.damage = damage
        self.level = 1
        self.level_required = level_required
        self.countdown = random.randint(0, int(level_required / 2))

    def is_available(self) -> bool:
        return self.countdown == 0

    def recharge(self) -> None:
        if self.countdown > 0:
          self.countdown -= 1
        else:
          self.countdown = 0

    def _reset_countdown(self) -> None:
        self.countdown = self.level_required + self.level

    def level_up(self) -> None:
        self.damage = self.damage + int(self.damage * self.LEVEL_UP_DAMAGE_INCREASE)
        self.level += 1
        self._reset_countdown()

    def use(self) -> None:
        self.countdown = self._reset_countdown()

    def get_skill_info(self) -> None:
        print(f"The skill {colored(self.name, 'blue')} has {colored('leveled up', 'green')}! Damage {colored(self.damage, 'red')}, Level {colored(self.level, 'magenta')}")


SKILL_POOL = [
    Skill("Berserk", 15, 2, False),
    Skill("Thunderstrike", 25, 5, False),
    Skill("Blade Dance", 35, 8, False),
    Skill("Arcane Nova", 45, 10, False),
    Skill("Void Rift", 65, 15, False),
]

class Creator:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def introduce_myself(self):
        x = PrettyTable()
        x.field_names = ["Property", "Value"]
        x.add_row(["Name", self.name])
        x.add_row(["Health", self.health])
        x.add_row(["Attack", self.attack])
        x.align["Property"] = "l"
        x.align["Value"] = "l"
        print(x)

    def is_alive(self):
        return self.health > 0

    def print_health(self, name_color):
        if self.health > 0:
            print(f"{colored(self.name, name_color)} has {colored(str(self.health), 'green')} health")
        else:
            print(colored(f"{self.name} is dead", 'red'))

    def perform_attack(self, opponent):
        raise NotImplementedError("This method should be overridden by subclass")

    def perform_damage_check(self, damage, is_double_attack, attacker_name, opponent_name):
        if damage == 0:
            if is_double_attack:
                print(colored(f"{attacker_name} is unlucky 😔", 'blue'))
            print(colored(f"{opponent_name} blocked our attack 🛡️", 'yellow'))
            return False
        return True

class Hero(Creator):
    def __init__(self, name, health, attack):
        super().__init__(name, health, attack)
        self.default_health = health
        self.level = 1
        self.skills = []
        self.items = []
        self.weapon_in_use = None
        self.xp = 0
        self.critical_strike_chance = 0.05

    def find_item(self):
        chance = random.randint(0, MAX_CHANCE)
        
        if chance not in [1, 2]:
            return
        
        item = ITEMS_POOL[chance - 1]
        item.found()

        if item.type == ItemType.ATTACK:
            if not self.weapon_in_use:
                self.use_weapon(item)
                print(f"{colored(self.name, 'blue')} is equipped with {colored(item.name, 'yellow')}")
                return
            
            if item.value > self.weapon_in_use.value:
                if self.get_strongest_weapon() and self.get_strongest_weapon().value > item.value:
                    print(f"{colored(self.name, 'blue')} found {colored(item.name, 'yellow')} but it's weaker than {colored(self.get_strongest_weapon().name, 'yellow')}")
                    return
                else:
                    if self.get_strongest_weapon():
                        self.items.remove(self.get_strongest_weapon())
                    self.pick_item(self.weapon_in_use)  
                    self.use_weapon(item)
                    print(f"{colored(self.name, 'blue')} is equipped with {colored(item.name, 'yellow')}")
            else:
                print(f"{colored(self.name, 'blue')} found {colored(item.name, 'yellow')} but it's weaker than {colored(self.weapon_in_use.name, 'yellow')}")
        else: 
            self.pick_item(item)
            print(f"{colored(self.name, 'blue')} is equipped with {colored(item.name, 'yellow')}")


    def use_weapon(self, item):
        if self.weapon_in_use is None:
            self.weapon_in_use = item
            return


    def pick_item(self, item):
        if len(self.items) > MAX_ITEMS:
            return

        self.items.append(item)

    def get_strongest_weapon(self):
        if len(self.items) == 0:
            return None
        attack_items_only = list(filter(lambda item: item.type == ItemType.ATTACK, self.items))
        return max(attack_items_only, key=lambda item: item.value if item.type == ItemType.ATTACK else 0)

    def get_strongest_skill(self):
        return max(self.skills, key=lambda skill: skill.damage)

    def gain_xp(self, xp):
        self.xp += xp
        if self.xp >= EXP_PER_LEVEL * self.level:
            self.level_up()
            self.xp = 0

    def get_attack(self) -> tuple:
        is_double_attack = False
        is_special_skill = False
        is_blockable = False

        for skill in self.skills:
            skill.recharge()

        attack = self.attack
        bonus_attack = 0
        top = int(1 / self.critical_strike_chance)
        chance = random.randint(1, top)

        if len(self.skills) > 0 and len(list(filter(lambda skill: skill.is_available(), self.skills))) > 0:
            use_skill = input(f"{colored(self.name, 'blue')} can use a special skill. Do you want to use it? (y/n): ")
            if use_skill.lower() == 'y':
                print("Available skills:")
                for idx, skill in enumerate(self.skills):
                    if not skill.is_available():
                        continue
                    print(f"{idx + 1}. {skill.name}")

                skill_choice = int(input(colored("Choose a skill to use: ", 'yellow'))) - 1
                skill = self.skills[skill_choice]
                is_blockable = skill.blockable
                is_special_skill = True
                skill._reset_countdown()
                print(f"{colored(self.name, 'blue')} has activated a special skill [{colored(skill.name, 'red')} +{skill.damage}] ({colored(f'Next to use {skill.countdown} turns', 'yellow')})")
                bonus_attack += skill.damage
                attack += skill.damage
            else:
                for skill in self.skills:
                    skill.recharge()
        elif chance == 1 and not is_special_skill:
            attack *= 1.2
            attack = int(attack)
            is_double_attack = True
            print(colored(f"{self.name}", 'blue') + " has gained " + colored("double attack", 'red') + " " + colored(f"{attack}", 'yellow') + " 💪")

        start = 0
        if is_special_skill and not is_blockable:
            start = bonus_attack

        if self.weapon_in_use is None:
            print(f"{colored(self.name, 'blue')} is using bare hands")
        else:
            if self.weapon_in_use.durability > 0:
                attack += self.weapon_in_use.value
                start += self.weapon_in_use.value
                self.weapon_in_use.durability -= 1
                print(f"{colored(self.name, 'blue')} is using {colored(self.weapon_in_use.name, 'yellow')}")
            else:
                self.weapon_in_use.drop(self, True)
                print(f"{colored(self.name, 'blue')} is using bare hands") 

        damage = random.randint(int(start), attack)

        return damage, attack, is_double_attack

    def use_item(self):
        for item in self.items:
            if item.type == ItemType.DEFENCE and self.health < int(self.default_health / 2):
                item.use(self)
                return

    def perform_attack(self, opponent):
        damage, max_attack, is_double_attack = self.get_attack()
        if not self.perform_damage_check(damage, is_double_attack, self.name, opponent.name):
            return
        else:
            opponent.health -= damage
            color_print(self.name, opponent.name, damage, is_double_attack, using_item=self.weapon_in_use is not None)

    def level_up(self):
        self.level += 1
        self.attack += 5
        self.default_health += 10

        for skill in self.skills:
            skill._reset_countdown()

        self.health = self.default_health
        print(f"{self.name} {colored('leveled up', 'green')} to {colored(self.level, 'magenta')}!")
        self.critical_strike_chance += 0.02
        self.introduce_myself()
        self.add_skill()
        self.upgade_skill()

    def upgade_skill(self):
      if len(list(filter(lambda skill: skill.level_required < self.level, self.skills))) == 0:
          print(colored("No skills to level up.", 'red'))
          return

      print(colored("Choose a skill to level up:", 'yellow'))
      for i, skill in enumerate(self.skills):
          print(f"{i+1}. {colored(skill.name, 'blue')} {colored(str(skill.damage), 'red')} -> {colored(str(int(skill.damage * 1.3)), 'green')}")
      
      choice = int(input(colored("Enter the number of the skill you want to level up: ", 'yellow'))) - 1
      
      if 0 <= choice < len(self.skills):
          self.skills[choice].level_up()
          self.skills[choice].get_skill_info()
          print(f"You've leveled up {colored(self.skills[choice].name, 'blue')}! 👊")
      else:
          print(colored("Invalid choice, no skills were leveled up.", 'red'))

    def inventory(self):
        text = f"{colored(self.name, 'blue')}'s inventory: "
        text += f"{colored('No items found', 'red')}" if len(self.items) == 0 else ",".join([f"{colored(item.name, 'yellow')} ({f'{item.durability}' if item.type == ItemType.ATTACK else f'{item.count}'})" for item in self.items]) 
        print(text)

    def add_skill(self):
        for skill in SKILL_POOL:
            if skill.level_required == self.level:
                self.skills.append(skill)
                print(f"{colored(self.name, 'red')} learned a new skill: {colored(skill.name, 'blue')} +{colored(str(skill.damage), 'green')} damage")

    def print_health(self):
        super().print_health('blue')


class Monster(Creator):
    def __init__(self, name, health, attack, monster_type, level=1):
        super().__init__(name, health, attack)
        self.type = monster_type
        self.level = level
        self.default_health = health

    def perform_attack(self, opponent):
        damage = random.randint(0, self.attack)

        if not self.perform_damage_check(damage, False, self.name, opponent.name):
            return
        else:
            opponent.health -= damage
            color_print(self.name, opponent.name, damage, is_reversed_colors=True)

    def print_health(self):
        super().print_health('red')


def battle(hero, monster):
    should_start = 'n'
    while should_start != 'y':
        should_start = input(colored("Do you want to start the battle? [y/n]: ", 'yellow'))

    print(colored(f"Battle started 🎉", 'green'))
    if hero.is_alive():
        hero.find_item()

    hero.inventory()

    turn = 0
    while hero.health > 0 and monster.health > 0:
        turn += 1

        while True:
            try:
                time.sleep(.2)
                break
            except KeyboardInterrupt:
                # Pause until enter is pressed or q is pressed to quit
                userInput = input(colored("Press enter to continue or q to quit: ", 'yellow'))
                if userInput == 'q':
                    exit()
                break
        padLine()
        print(f"{colored('Turn', 'grey')} {colored(str(turn), 'cyan')}")
        padLine()
        hero.use_item()
        hero.perform_attack(monster)
        if monster.health >= 0:
            monster.perform_attack(hero)

        padLine()
        print(colored(f"Final results after this round", 'grey'))
        padLine()
        print_health_bar(hero.name, hero.health, hero.default_health)
        print_health_bar(monster.name, monster.health, monster.default_health, is_hero=False)
        padLine()
        print(f"\n\n")

    print(colored(f"Battle finished 🎉", 'green'))
    if hero.health > 0:
        hero.gain_xp(monster.level * EXP_PER_LEVEL)
        print(colored(f"{hero.name} is victorious 🥳", 'blue'))
        input(colored("Press enter to complete the battle...", 'yellow'))
    elif monster.health > 0:
        print(colored(f"{monster.name} [{monster.type}] is victorious 😈", 'red'))


class ItemType(Enum):
    ATTACK = 1
    DEFENCE = 2

class Item:
    ITEM_PREFIXES = {
        "Common": 0.75,
        "Epic": 1.25,
        "Rare": 1.5,
        "Legendary": 2.0
    }

    DEFENCE_PREFIXES = {
        "Small": 0.75,
        "Medium": 1.0,
        "Large": 1.25,
        "Huge": 1.5
    }

    def __init__(self, name: str, value: int, type: ItemType, count: int = 1) -> None:
        prefix = False
        if type == ItemType.ATTACK:
            prefix_keys = list(self.ITEM_PREFIXES.keys())
            prefix = prefix_keys[random_with_small_priority(len(prefix_keys)) - 1]
            multiplier = random.uniform(self.ITEM_PREFIXES[prefix], self.ITEM_PREFIXES[prefix_keys[-1]])
            value *= multiplier
        else:
            prefix_keys = list(self.DEFENCE_PREFIXES.keys())
            prefix = prefix_keys[random_with_small_priority(len(prefix_keys)) - 1]
            multiplier = random.uniform(self.DEFENCE_PREFIXES[prefix], self.DEFENCE_PREFIXES[prefix_keys[-1]])
            value *= multiplier

        self.in_use = False
        self.name = f"{prefix} {name}"
        self.value = int(value)
        self.type = type
        self.count = random.randint(1, count)
        self.durability = random.randint(1, 20)
        
    def is_type(self, type: ItemType) -> bool:
        return self.type == type

    def __str__(self) -> str:
        return f"{self.name} ({self.type}) +{self.value} ({self.count})"

    def use(self, hero: Hero) -> None:
        if self.type == ItemType.ATTACK:
            hero.weapon_in_use = self
            self.remove(hero, True)
        elif self.type == ItemType.DEFENCE:
            hero.health += int(self.value)
            self.count -= 1
            if self.count == 0:
                self.remove(hero)
                return
        print(f"{colored(hero.name, 'blue')} is using {colored(self.name, 'yellow')}")

    def is_in_use(self) -> bool:
        return self.in_use

    def remove(self, hero: Hero, move_to_hand=False) -> None:
        hero.items.remove(self)
        if not move_to_hand:
            print(f"{colored(hero.name, 'blue')} removed {colored(self.name, 'yellow')} from inventory!")

    def drop(self, hero: Hero, is_damaged=False) -> None:
        hero.weapon_in_use = None
        damaged_text = f" because it was ({colored('damaged', 'red')})" if is_damaged else ""
        print(f"{colored(hero.name, 'blue')} dropped {colored(self.name, 'yellow')} ${damaged_text}")

    def found(self) -> None:
        type_color = 'green' if self.type == ItemType.DEFENCE else 'magenta'
        # if self.type == ItemType.DEFENCE: get count of defence items else nothing
        additional_info = f"Qty ({self.count})" if self.type == ItemType.DEFENCE else f"Durability ({self.durability})"
        print(f"New item has been found {colored(self.name, 'yellow')} [{colored(additional_info, type_color)}] Value: {colored(self.value, 'red')}")

ITEMS_POOL = [
    Item("Healing Potion", 10, ItemType.DEFENCE, 5),
    Item("Sword", 3, ItemType.ATTACK),
]

splash_screen()
input(colored("Press enter to start the game...", 'yellow'))
hero = Hero("Rambo", 100, 10)
i = 0
while hero.is_alive() and i < 20:
    i += 1
    monster = generate_monster(hero.level)
    print("\033[H\033[J")
    print(colored(f"Monster {monster.name} found!", 'red'))
    monster.introduce_myself()
    battle(hero, monster)

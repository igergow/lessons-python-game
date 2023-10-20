import random
import math
from unique_names_generator import get_random_name
from unique_names_generator.data import ADJECTIVES, STAR_WARS, NAMES
from termcolor import colored
from prettytable import PrettyTable

def random_with_small_priority(max_value):
    exp = random.randint(1, 3)
    return math.ceil((random.random() ** exp) * max_value)

def color_print(hero_name, opponent_name, damage, is_double_attack=False, is_reversed_colors=False):
    crit_emoji = ' ⚡ CRITICAL STRIKE' if is_double_attack else ''
    if is_reversed_colors:
      print(colored(hero_name, 'red') + ' attacked ' + colored(opponent_name, 'blue') + ' with ' + colored(str(damage), 'yellow') + ' 😈' + crit_emoji)
    else:
      print(colored(hero_name, 'blue') + ' attacked ' + colored(opponent_name, 'red') + ' with ' + colored(str(damage), 'yellow') + ' 😈' + crit_emoji)

def print_item_found(hero_name, item_name, item_type):
    type_color = 'green' if item_type == 'defence' else 'magenta'
    print(colored(hero_name, 'blue') + " has found item " + colored(item_name, 'yellow') + " [" + colored(item_type, type_color) + "]")

class Skill:
    def __init__(self, name, damage, level_required, blockable):
        self.name = name
        self.blockable = blockable
        self.damage = damage
        self.level = 1
        self.level_required = level_required
        self.countdown = self.level_required + self.level

    def is_available(self):
        return self.countdown == 0

    def reset_countdown(self):
        self.countdown = self.level_required + self.level

    def level_up(self):
        self.damage = self.damage + int(self.damage * 0.3)
        self.level += 1
        self.reset_countdown()
        print(f"The skill {colored(self.name, 'blue')} has {colored('leveled up', 'green')}! Damage {colored(self.damage, 'red')}, Level {colored(self.level, 'magenta')}")


SKILL_POOL = [
    Skill("Berserk", 15, 2, False),
    Skill("Thunderstrike", 25, 5, False),
    Skill("Blade Dance", 35, 8, False),
    Skill("Arcane Nova", 45, 10, False),
    Skill("Void Rift", 65, 15, False),
]


class Item:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type


ITEMS_POOL = [
    Item("Healing Potion", 5, "defence"),
    Item("Sword", 3, "attack"),
]


class Hero:
    def __init__(self, name, health, attack):
        self.name = name
        self.default_health = health
        self.health = health
        self.attack = attack
        self.level = 1
        self.skills = []
        self.items = []
        self.xp = 0
        self.critical_strike_chance = 0.05

    def find_item(self):
        if len(self.items) > 5:
            return

        chance = random.randint(0, 9)
        if chance == 1:
            item = ITEMS_POOL[0]
            print_item_found(self.name, item.name, item.type)
            self.items.append(ITEMS_POOL[0])
        elif chance == 2:
            item = ITEMS_POOL[0]
            print_item_found(self.name, item.name, item.type)
            self.items.append(ITEMS_POOL[1])

    def is_alive(self):
        return self.health > 0

    def get_strongest_skill(self):
        top_skill = self.skills[0]
        for skill in self.skills:
            if skill.damage > top_skill.damage:
                top_skill = skill

        return top_skill

    def gain_xp(self, xp):
        self.xp += xp
        if self.xp >= 100 * self.level:
            self.level_up()
            self.xp = 0

    def get_attack(self):
        is_double_attack = False
        is_special_skill = False
        is_blockable = False

        for skill in self.skills:
            if skill.countdown > 0:
                skill.countdown -= 1

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
                skill.reset_countdown()
                print(f"{colored(self.name, 'blue')} has activated a special skill [{colored(skill.name, 'red')} +{skill.damage}] ({colored(f'Next to use {skill.countdown} turns', 'yellow')})")
                bonus_attack += skill.damage
                attack += skill.damage
        elif chance == 1 and not is_special_skill:
            attack *= 2
            is_double_attack = True
            print(colored(f"{self.name}", 'blue') + " has gained " + colored("double attack", 'red') + " " + colored(f"{attack}", 'yellow') + " 💪")

        start = 0
        if is_special_skill and not is_blockable:
            start = bonus_attack

        damage = random.randint(int(start), attack)

        return damage, attack, is_double_attack

    def use_item(self):
        remove_item = False
        for item in self.items:
            if item.type == "attack":
                print(f"{colored(self.name, 'blue')} has used item {colored(item.name, 'yellow')} [{item.type}] {colored(f'+{item.value}', 'green')} attack")
                self.attack += item.value
                remove_item = item
                break
        if remove_item:
            self.items.remove(remove_item)

        remove_item = False
        if self.health < int(self.default_health / 2):
            for item in self.items:
                if item.type == "defence":
                    print(f"{colored(self.name, 'blue')} has used item {colored(item.name, 'yellow')} [{item.type}] {colored(f'+{item.value}', 'green')} health")
                    self.health += item.value
                    remove_item = item
                    break
            if remove_item:
                self.items.remove(remove_item)

    def perform_attack(self, opponent):
        damage, max_attack, is_double_attack = self.get_attack()
        if damage == 0:
            if is_double_attack:
                print(colored(f"{self.name} is unlucky 😔", 'blue'))
            print(colored(f"{opponent.name} blocked our attack 🛡️", 'yellow'))
        else:
            opponent.health -= damage
            color_print(self.name, opponent.name, damage, is_double_attack)

    def introduce_myself(self):
        x = PrettyTable()

        x.field_names = ["Property", "Value"]

        x.add_row(["Name", self.name])
        x.add_row(["Health", self.health])
        x.add_row(["Attack", self.attack])
        x.add_row(["Level", self.level])
        x.align["Property"] = "l"
        x.align["Value"] = "l"
        print(x)

    def print_health(self):
        if self.health > 0:
            print(f"{colored(self.name, 'blue')} has {colored(str(self.health), 'green')} health")
        else:
            print(colored(f"{self.name} is dead", 'red'))

    def level_up(self):
        self.level += 1
        self.attack += 5
        self.default_health += 10

        for skill in self.skills:
            skill.reset_countdown()

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
          print(f"You've leveled up {colored(self.skills[choice].name, 'blue')}! 👊")
      else:
          print(colored("Invalid choice, no skills were leveled up.", 'red'))

    def add_skill(self):
        for skill in SKILL_POOL:
            if skill.level_required == self.level:
                self.skills.append(skill)
                print(f"{colored(self.name, 'red')} learned a new skill: {colored(skill.name, 'blue')} +{colored(str(skill.damage), 'green')} damage")


class Monster:
    def __init__(self, name, monster_type, health, attack, level=1):
        self.name = name
        self.type = monster_type
        self.health = health
        self.attack = attack
        self.level = level

    def perform_attack(self, opponent):
        damage = random.randint(0, self.attack)
        if damage == 0:
            print(colored(f"{opponent.name} blocked attack 🛡️", 'yellow'))
        else:
            opponent.health -= damage
            color_print(self.name, opponent.name, damage, is_reversed_colors=True)


    def introduce_myself(self):
        x = PrettyTable()

        x.field_names = ["Property", "Value"]

        x.add_row(["Name", self.name])
        x.add_row(["Type", self.type])
        x.add_row(["Health", self.health])
        x.add_row(["Attack", self.attack])
        x.align["Property"] = "l"
        x.align["Value"] = "l"
        print(x)
        
    def print_health(self):
      if self.health > 0:
          print(f"{colored(self.name, 'red')} has {colored(str(self.health), 'green')} health")
      else:
          print(colored(f"{self.name} [{self.type}] is dead", 'red'))


def battle(hero, monster):
    should_start = 'n'
    while should_start != 'y':
        should_start = input(colored("Do you want to start the battle? [y/n]: ", 'yellow'))

    print("\033[H\033[J")
    print(colored(f"Battle started 🎉", 'green'))
    if hero.is_alive():
        hero.find_item()

    turn = 0
    while hero.health > 0 and monster.health > 0:
        turn += 1
        print(f"{colored('Turn', 'grey')} {colored(str(turn), 'cyan')}")
        hero.use_item()
        hero.perform_attack(monster)
        monster.print_health()
        if monster.health >= 0:
            monster.perform_attack(hero)
            hero.print_health()

    print(colored(f"Battle finished 🎉", 'green'))
    if hero.health > 0:
        hero.gain_xp(monster.level * 100)
        print(colored(f"{hero.name} is victorious 🥳", 'blue'))
        input(colored("Press enter to complete the battle...", 'yellow'))
        print("\033[H\033[J")
    elif monster.health > 0:
        print(colored(f"{monster.name} [{monster.type}] is victorious 😈", 'red'))


hero = Hero("Rambo", 100, 10)
i = 0
while hero.is_alive() and i < 20:
    i += 1
    monster_name = get_random_name(combo=[ADJECTIVES, STAR_WARS])
    monster_level = random_with_small_priority(hero.level)
    monster_health = monster_level * 100
    monster_attack = monster_level * 10 - 5
    monster_type = get_random_name(separator="-", style="lowercase")
    monster = Monster(monster_name, monster_type, monster_health, monster_attack, level=monster_level)
    print("\033[H\033[J")
    print(colored(f"Monster {monster_name} found!", 'red'))
    monster.introduce_myself()
    battle(hero, monster)

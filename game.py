import random
from unique_names_generator import get_random_name
from unique_names_generator.data import ADJECTIVES, STAR_WARS, ANIMALS


class Skill:
    def __init__(self, name, damage, level_required, blockable):
        self.name = name
        self.blockable = blockable
        self.damage = damage
        self.level = 1
        self.level_required = level_required

    def level_up(self):
        self.damage = self.damage + int(self.damage * 0.3)
        self.level += 1
        print(f"The skill {self.name} has leveled up! Damage {self.damage}, Level {self.level}")


SKILL_POOL = [
    Skill("Berserk", 10, 2, True),
    Skill("Thunderstrike", 12, 3, False),
    Skill("Blade Dance", 15, 4, False),
    Skill("Arcane Nova", 20, 5, False),
    Skill("Void Rift", 25, 6, False),
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
        self.skill_cooldown = 5
        self.critical_strike_chance = 0.05

    def find_item(self):
        if len(self.items) > 5:
            return

        chance = random.randint(0, 9)
        if chance == 1:
            item = ITEMS_POOL[0]
            print(f"{self.name} has found item {item.name}[{item.type}]")
            self.items.append(ITEMS_POOL[0])
        elif chance == 2:
            item = ITEMS_POOL[0]
            print(f"{self.name} has found item {item.name}[{item.type}]")
            self.items.append(ITEMS_POOL[1])

    def is_alive(self):
        return self.health > 0

    def get_strongest_skill(self):
        top_skill = self.skills[0]
        for skill in self.skills:
            if skill.damage > top_skill.damage:
                top_skill = skill

        return top_skill

    def get_attack(self):
        is_double_attack = False
        is_special_skill = False
        is_blockable = False
        self.skill_cooldown -= 1

        attack = self.attack
        top = int(1 / self.critical_strike_chance)
        chance = random.randint(1, top)
        if chance == 1:
            attack *= 2
            is_double_attack = True
            print(f"{self.name} has gained double attack {attack}")
        elif len(self.skills) > 0 and self.skill_cooldown == 0:
            skill = self.get_strongest_skill()
            is_blockable = skill.blockable
            is_special_skill = True
            print(f"{self.name} has used a special skill [{skill.name} +{skill.damage}]")
            attack += skill.damage
            self.skill_cooldown = 5

        start = 0
        if is_special_skill and not is_blockable:
            start = attack / 2

        damage = random.randint(int(start), attack)

        return damage, attack, is_double_attack

    def use_item(self):
        remove_item = False
        for item in self.items:
            if item.type == "attack":
                print(f"{self.name} has used item {item.name}[{item.type}] +{item.value} attack")
                self.attack += item.value
                remove_item = item
                break
        if remove_item:
            self.items.remove(remove_item)

        remove_item = False
        if self.health < int(self.default_health / 2):
            for item in self.items:
                if item.type == "defence":
                    print(f"{self.name} has used item {item.name}[{item.type}] +{item.value} health")
                    self.health += item.value
                    remove_item = item
                    break
            if remove_item:
                self.items.remove(remove_item)

    def perform_attack(self, opponent):
        damage, max_attack, is_double_attack = self.get_attack()
        if damage == 0:
            if is_double_attack:
                print(f"{self.name} is unlucky")
            print(f"{opponent.name} blocked our attack")
        else:
            opponent.health -= damage
            print(f"{self.name} attacked {opponent.name} with {damage} of {max_attack}")

    def introduce_myself(self):
        print("name=", self.name)
        print("health=", self.health)
        print("attack=", self.attack)
        print("level=", self.level)

    def print_health(self):
        if self.health > 0:
            print(f"{self.name} has {self.health} health")
        else:
            print(f"{self.name} is dead")

    def level_up(self):
        self.level += 1
        self.attack += 5
        self.default_health += 10
        self.health = self.default_health
        print(f"{self.name} leveled up to {self.level}!")
        self.critical_strike_chance += 0.02
        self.introduce_myself()
        self.add_skill()
        for skill in self.skills:
            skill.level_up()

    def add_skill(self):
        for skill in SKILL_POOL:
            if skill.level_required == self.level:
                self.skills.append(skill)
                print(f"{self.name} learned a new skill: {skill.name} +{skill.damage} damage")


class Monster:
    def __init__(self, name, monster_type, health, attack):
        self.name = name
        self.type = monster_type
        self.health = health
        self.attack = attack

    def perform_attack(self, opponent):
        damage = random.randint(0, self.attack)
        if damage == 0:
            print(f"{opponent.name} blocked our attack")
        else:
            opponent.health -= damage
            print(f"{self.name} attacked {opponent.name} with {damage}")

    def introduce_myself(self):
        print("name=", self.name)
        print("type=", self.type)
        print("health=", self.health)
        print("attack=", self.attack)

    def print_health(self):
        if self.health > 0:
            print(f"{self.name}[{self.type}] has {self.health} health")
        else:
            print(f"{self.name}[{self.type}] is dead")


def battle(hero, monster):
    if hero.is_alive():
        hero.find_item()

    turn = 0
    while hero.health > 0 and monster.health > 0:
        turn += 1
        print(f"Turn {turn}")
        hero.use_item()
        hero.perform_attack(monster)
        monster.print_health()
        if monster.health >= 0:
            monster.perform_attack(hero)
            hero.print_health()

    print("Battle finished")
    if hero.health > 0:
        print(f"{hero.name} is victorious")
        hero.level_up()
    elif monster.health > 0:
        print(f"{monster.name}[{monster.type}] is victorious")


hero = Hero("Rambo", 100, 10)
i = 0
while hero.is_alive() and i < 10:
    i += 1
    monster_name = get_random_name(combo=[ADJECTIVES, STAR_WARS])
    monster_health = hero.health - 5
    monster_attack = hero.attack
    monster_type = ANIMALS[random.randint(0, len(ANIMALS))]
    monster = Monster(monster_name, monster_type, monster_health, monster_attack)
    monster.introduce_myself()
    battle(hero, monster)
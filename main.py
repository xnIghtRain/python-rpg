from classes.game import bcolors, Person
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic/Aoe Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
ice = Spell("Ice", 25, 600, "black")
blizzard = Spell("Blizzard", 30, 900, "aoe")
meteor = Spell("Meteor", 50, 1500, "aoe")
earthquake = Spell("Earthquake", 40, 1200, "aoe")

# Create White Magic
cure = Spell("Cure", 25, 700, "white")
cura = Spell("Cura", 42, 1500, "white")
curaga = Spell("Curaga", 60, 6000, "white")

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 Hp", 500)
elixer = Item("Elixier", "elixer",
              "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mega Elixier", "elixer",
                "Fully restores party's HP/MP ", 9999)
grenade = Item("Grenate", "attack", "Deals 500 damage", 500)

# Create Player/Enemy Spells+Items
player_spells = [fire, thunder, ice, blizzard,
                 meteor, earthquake, cure, cura, curaga]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 8},
                {"item": superpotion, "quantity": 6},
                {"item": elixer, "quantity": 10},
                {"item": hielixer, "quantity": 10},
                {"item": grenade, "quantity": 10},
                ]
enemy_spells = [fire, thunder, ice, cure]

# Create Players/Enemy
print("Please input the Name of the Heroes (5 char max)\n")

p1_name = input("   Name of your first Member:")[:5]
p2_name = input("   Name of your second Member:")[:5]
p3_name = input("   Name of your third Member:")[:5]


player1 = Person(p1_name, 3200, 200, 300, 100, player_spells, player_items)
player2 = Person(p2_name, 3200, 200, 300, 100, player_spells, player_items)
player3 = Person(p3_name, 3200, 200, 300, 100, player_spells, player_items)

enemy1 = Person("Imp   ", 1200, 139, 420, 20, enemy_spells, [])
enemy2 = Person("Magus ", 12000, 139, 420, 20, enemy_spells, [])
enemy3 = Person("Imp   ", 1200, 139, 420, 20, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]


# Start Game

running = True
i = 0




while running:
    print(bcolors.RED + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
    print("=========================")
    print("\n")
    print("NAME                 HP                                      MP")
    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        print("\n" + bcolors.HEADER + "---------------------------" + "Your turn,",
              player.name + "---------------------------" + bcolors.ENDC, "\n")
        player.get_stats()
        player.choose_action()
        choice = int(input("    Choose action:")) - 1

        if choice == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(
                " ", "") + " for", dmg, " points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died!")
                del enemies[enemy]

        elif choice == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.RED + "\nNot enough MP\n" + bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.BLUE + "\n" + spell.name + " heals for",
                      str(magic_dmg), "HP." + bcolors.ENDC)

            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.BLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

            elif spell.type == "aoe":
                for i in enemies:
                    i.take_damage(magic_dmg)
                print(bcolors.BLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to all Enemies " + bcolors.ENDC)

        elif choice == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.GREEN + "\n" + item.name +
                      " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixier":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    print(bcolors.GREEN + "\n" + item.name +
                          " fully restores HP/MP of everyone in your Party" + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.GREEN + "\n" + item.name +
                          " fully restores HP/MP of", player.name + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.RED + "\n" + item.name + " deals", str(item.prop),
                      "points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # choose attack
            target = random.randrange(0, 2)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " +
                  players[target].name.replace(" ", "") + " for", enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.YELLOW + spell.name + " heals " +
                      enemy.name + " for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 2)
                players[target].take_damage(magic_dmg)
                print(bcolors.BLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals",
                      str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[player]

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Player won
    if defeated_enemies == 3:
        print(bcolors.GREEN + "You win!" + bcolors.ENDC)
        running = False

    # Check if Enemy won
    elif defeated_players == 3:
        print(bcolors.RED + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

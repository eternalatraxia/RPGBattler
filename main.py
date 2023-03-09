from Classes.game import Person, bcolors
from Classes.magic import Spell
from Classes.inventory import Item
import random

#Black Magic
fire = Spell("Fire", 10, 100, "black")
ice = Spell("Ice", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
meteor = Spell("Meteor", 10, 100, "black")
quake = Spell("Quake", 10, 100, "black")
#White magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")
curaga = Spell("Curaga", 50, 6000, "white")
#Create items
potion = Item("Potion", "potion", "heals for 50 HP", 50,15)
hipotion = Item("Hi-potion", "potion", "heals for 100 HP", 100, 10)
superpotion = Item("Superpotion", "potion", "heals for 500 HP", 500, 5)
elixir = Item("Elixir", "elixir", "fully restores mp and hp for 1 party member", 9999, 5)
hielixir = Item("MegaElixir", "elixir", "fully resorts mp and hp for all party members", 9999, 1)

grenade = Item("Grenade", "attack", "deals 500 dmg", 500, 5)

player_magic = [fire, thunder, ice, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [potion, hipotion, superpotion, elixir, hielixir, grenade]

player1 = Person("Deathpolca", 3200, 65, 60, 34,player_magic, player_items)
player2 = Person("Sarasa", 3000, 65, 60, 34,player_magic, player_items)
player3 = Person("Najezta", 3300, 65, 60, 34,player_magic, player_items)
players = [player1, player2, player3]

enemy1 = Person("Niglet", 120, 130, 200, 25, enemy_spells, [])
enemy2 = Person("Negus", 1200, 65, 500, 25, enemy_spells, [])
enemy3 = Person("Niglet", 120, 130, 200, 25, enemy_spells, [])
enemies = [enemy1, enemy2, enemy3]
running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS" + bcolors.ENDC)

while running:
    print("=================")
    print("\n\n")
    print("NAME                 HP                                     MP")

    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

        print("\n")



    for player in players:
        player.choose_actions()
        choice = input("Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

            print(player.name + " attacked " + enemies[enemy].name.replace(" ", "") + " for" + str(dmg), "points of damage.")
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic: ")) - 1
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            cost = player.reduce_mp(spell.cost)


            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg) + "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg) + " points of dmg to" + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

            player.reduce_mp(spell.cost)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1
            if item_choice == -1:
                continue

            item = player.items[item_choice]
            if item.quantity == 0:
                print(bcolors.FAIL + "You have no more " + item.name +"s!" + bcolors.ENDC)
                continue

            item.quantity -= 1




            if item.type == ("potion"):
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop), "HP", bcolors.ENDC)
            elif item.type == ("elixir"):
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)

            elif item.name == ("MegaElixir"):
                for i in players:
                    i.hp = i.maxhp
                    i.mp = i.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP of all party members" + bcolors.ENDC)

            elif item.type == ("attack"):
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to" + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]



        # Check if battle is over
        defeated_enemies = 0
        defeated_players = 0

        for enemy in enemies:
            if enemy.get_hp() == 0:
                defeated_enemies += 1

            if defeated_enemies == len(enemies):
                print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                running = False
        # Check if player won
        for player in players:
            if player.get_hp() == 0:
                defeated_players += 1

            if defeated_enemies == len(players):
                print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
                running = False

    for enemy in enemies:
        enemy_choice = random.randrange(0,3)

        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemies[target].generate_damage()
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + enemies[enemy_choice].name.replace(" ","") + " attacks", players[target].name.replace(" ",""), "for " + str(enemy_dmg) + " points of damage" + bcolors.ENDC)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name +  "for" + str(magic_dmg) + "HP" + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg) + " points of dmg to" + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + " has died.")
                    del players[player]

            print("Enemy chose", spell, "magic damage is ", magic_dmg)









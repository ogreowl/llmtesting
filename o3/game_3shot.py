import random, os, time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def color_text(text, color):
    return f"{color}{text}{RESET}"

class Combatant:
    def __init__(self, name, hp, attack, defense, heal_count=0):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_cooldown = 0
        self.heal_count = heal_count
        self.defending = False
        self.dodging = False
        self.charged = False
        self.charge_turns_left = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return dmg

    def update_status(self):
        self.defending = False
        self.dodging = False
        if self.charged:
            self.charge_turns_left -= 1
            if self.charge_turns_left <= 0:
                self.charged = False
        if self.special_cooldown > 0:
            self.special_cooldown -= 1

def display_status(player, enemy):
    print(f"{color_text(player.name, CYAN)}: {player.hp}/{player.max_hp} HP", end=" | ")
    print(f"{color_text(enemy.name, RED)}: {enemy.hp}/{enemy.max_hp} HP")

def basic_attack(attacker, defender):
    mult = random.uniform(0.9, 1.1)
    bonus = 1.5 if attacker.charged else 1.0
    if attacker.charged:
        attacker.charged = False
        attacker.charge_turns_left = 0
    dmg = int(attacker.attack * mult * bonus) - defender.defense
    dmg = max(dmg, 0)
    if random.random() < 0.1:
        dmg *= 2
        print(color_text("Critical hit!", YELLOW))
    if defender.dodging:
        if random.random() < 0.5:
            print(f"{defender.name} dodged the attack!")
            return 0
        else:
            print(f"{defender.name} failed to dodge!")
    if defender.defending:
        dmg //= 2
    return defender.take_damage(dmg)

def special_attack(attacker, defender):
    mult = random.uniform(1.5, 2.0)
    dmg = int(attacker.attack * mult) - int(defender.defense * 0.75)
    dmg = max(dmg, 0)
    if random.random() < 0.1:
        dmg *= 2
        print(color_text("Critical hit!", YELLOW))
    if defender.dodging:
        if random.random() < 0.4:
            print(f"{defender.name} dodged the special attack!")
            return 0
        else:
            print(f"{defender.name} failed to dodge the special!")
    if defender.defending:
        dmg //= 2
    return defender.take_damage(dmg)

def heal_target(target):
    amount = random.randint(15, 25)
    target.hp = min(target.hp + amount, target.max_hp)
    return amount

def charge_target(attacker):
    attacker.charged = True
    attacker.charge_turns_left = 1

def player_turn(player, enemy):
    while True:
        display_status(player, enemy)
        print("\nChoose an action:")
        print("1. Attack")
        print("2. Defend")
        print("3. Dodge")
        if player.special_cooldown == 0:
            print("4. Special Attack")
        if player.heal_count > 0:
            print("5. Heal")
        print("6. Charge (boost next attack)")
        choice = input("Action: ").strip()
        if choice == "1":
            dmg = basic_attack(player, enemy)
            print(f"You attack and deal {dmg} damage.")
            break
        elif choice == "2":
            player.defending = True
            print("You take a defensive stance.")
            break
        elif choice == "3":
            player.dodging = True
            print("You prepare to dodge the next attack.")
            break
        elif choice == "4" and player.special_cooldown == 0:
            dmg = special_attack(player, enemy)
            print("You gather your strength and unleash a powerful blow!")
            print(f"You deal {dmg} damage with your special attack!")
            player.special_cooldown = 3
            break
        elif choice == "5" and player.heal_count > 0:
            amount = heal_target(player)
            player.heal_count -= 1
            print(f"You heal for {amount} HP.")
            break
        elif choice == "6":
            if player.charged:
                print("You're already charged!")
            else:
                charge_target(player)
                print("You focus your energy to charge your next attack!")
            break
        else:
            print("Invalid action. Try again.")
    time.sleep(1)

def enemy_decision(enemy, player):
    if enemy.hp < enemy.max_hp * 0.3 and enemy.heal_count > 0:
        return "heal"
    if enemy.special_cooldown == 0 and random.random() < 0.3:
        return "special"
    if enemy.charged:
        return "attack"
    roll = random.random()
    if roll < 0.5:
        return "attack"
    elif roll < 0.7:
        return "defend"
    elif roll < 0.85:
        return "dodge"
    else:
        return "charge"

def enemy_turn(enemy, player):
    action = enemy_decision(enemy, player)
    if action == "attack":
        dmg = basic_attack(enemy, player)
        print(f"{enemy.name} lunges forward and deals {dmg} damage!")
    elif action == "defend":
        enemy.defending = True
        print(f"{enemy.name} braces for your attack.")
    elif action == "dodge":
        enemy.dodging = True
        print(f"{enemy.name} prepares to dodge your next move.")
    elif action == "special":
        dmg = special_attack(enemy, player)
        print(f"{enemy.name} unleashes a devastating special attack dealing {dmg} damage!")
        enemy.special_cooldown = 3
    elif action == "heal":
        amount = heal_target(enemy)
        enemy.heal_count -= 1
        print(f"{enemy.name} rejuvenates, healing for {amount} HP.")
    elif action == "charge":
        if not enemy.charged:
            charge_target(enemy)
            print(f"{enemy.name} is charging up for a powerful strike!")
        else:
            dmg = basic_attack(enemy, player)
            print(f"{enemy.name} attacks and deals {dmg} damage!")
    time.sleep(1)

def game_loop():
    player = Combatant("Hero", 120, 25, 8, heal_count=2)
    enemy = Combatant("Goblin Warlord", 100, 20, 6, heal_count=1)
    turn = 1
    while player.is_alive() and enemy.is_alive():
        clear_screen()
        print(color_text(f"--- Turn {turn} ---", YELLOW))
        player_turn(player, enemy)
        if not enemy.is_alive():
            break
        enemy_turn(enemy, player)
        player.update_status()
        enemy.update_status()
        turn += 1
    clear_screen()
    if player.is_alive():
        print(color_text("Victory! You have triumphed over your foe.", GREEN))
    else:
        print(color_text("Defeat... You have fallen in battle.", RED))

def main():
    while True:
        clear_screen()
        print(color_text("Welcome to the Strategic Turn-Based Combat Game!", CYAN))
        game_loop()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != 'y':
            break

if __name__ == '__main__':
    main()

class Player:
    name:str
    health:int=100
    attack:int=10

    def talk(self):
        print(f"Hello, I am {self.name}")

    def attack_enemy(self,enemy):
        enemy.health-=self.attack
        print(f"{self.name} attacked {enemy.name} ")
        print(f"{enemy.name} health is now {enemy.health}")
        if enemy.health<=0:
            print(f"{enemy.name} is dead")
            print(f"{self.name} wins")
            exit()


class Enemy:
    name:str
    health:int=100
    attack:int=5
 
    def attack_player(self,player):
        player.health-=self.attack
        print(f"{self.name} attacked {player.name} ")
        print(f"{player.name} health is now {player.health}")
        if player.health<=0:
            print(f"{player.name} is dead")
            print(f"{self.name} wins")
            exit()

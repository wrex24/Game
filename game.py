import random as r
import time
import numpy as np


def main():
    round = 1
    arraySize = 3
    p1 = Player("player 1", [0, 1], 10, 5)
    p2 = Player("player 2", [2, 1], 10, 5)

    while True:
        print("round %s" %round)
        arena = updateMap(p1.cord, p2.cord, arraySize)
        for row in range(len(arena)):
            print(arena[row])
        if nextToEachother(p1.cord, p2.cord):
            p1.attack(p2)
            p2.attack(p1)
        if p1.health <= 0 or p2.health <= 0:
            if p1.health < p2.health:
                print("player 2 wins")
            else:
                print("player 1 wins")
            break
        p1.move(p2)
        p2.move(p1)
        print("\n")
        round += 1
        time.sleep(3)



class Player:
    def __init__(self, name, cord, health, defense):
        self.name = name
        self.cord = cord
        self.health = health
        self.defense = defense

    def attack(self, target):
        damage = r.randint(5, 10) - target.defense
        target.health -= damage
        print(
            "%s did %s damage to %s \n%s has %s health" % (self.name, damage, target.name, target.name, target.health))

    def findDifference(self, target):
        difference = [0, 0]
        for i in range(len(self.cord)):
            difference[i] = self.cord[i] - target.cord[i]
        return difference

    def move(self, other):
        difference = self.findDifference(other)
        while True:
            newCord = [0,0]
            newCord[0] = self.cord[0]
            newCord[1] = self.cord[1]
            if self.health <= 4:
                direction = r.randint(1, 4)
            else:
                if difference[0] == -2:
                    direction = 2
                elif difference[0] == 2:
                    direction = 1
                elif difference[1] == -2:
                    direction = 4
                elif difference[1] == 2:
                    direction = 3
                elif nextToEachother(self.cord, other.cord):
                    direction = 0
                else:
                    direction = r.randint(1, 4)

            if direction == 0:
                break
            if direction == 1:
                newCord[0] -= 1
                if newCord[0] >= 0 and newCord != other.cord:
                    self.cord[0] -= 1
                    break
            if direction == 2:
                newCord[0] += 1
                if newCord[0] <= 2 and newCord != other.cord:
                    self.cord[0] += 1
                    break
            if direction == 3:
                newCord[1] -= 1
                if newCord[1] >= 0 and newCord != other.cord:
                    self.cord[1] -= 1
                    break
            if direction == 4:
                newCord[1] += 1
                if newCord[1] <= 2 and newCord != other.cord:
                    self.cord[1] += 1
                    break


def updateMap(p1Cord, p2Cord, arraySize):
    newArena = np.zeros((arraySize, arraySize), dtype= int)
    newArena[p1Cord[0]][p1Cord[1]] = 1
    newArena[p2Cord[0]][p2Cord[1]] = 2
    return newArena


def nextToEachother(p1Cord, p2Cord):
    difference = [0, 0]
    for i in range(len(p1Cord)):
        difference[i] = p1Cord[i] - p2Cord[i]
    if difference == [0, 1] or difference == [0, -1] or difference == [1, 0] or difference == [-1, 0]:
        return True
    return False


if __name__ == '__main__':
    main()

import random as r
import time
import numpy as np
from caseyGraphics import *


def main():
    win = GraphWin('game', 300, 300)
    round = 1
    arraySize = 3
    windowSize = 300
    p1 = Player("player 1", [0, 1], [windowSize/2, 50], 15, 5, "red")
    p2 = Player("player 2", [2, 1], [windowSize/2, 250],  15, 5, "blue")
    map = Map(3)

    map.draw(p1, p2, win)
    while True:

        map.update(p1.cord, p2.cord)
        print(map.map)
        print("round %s" %round)
        arena = updateMap(p1.cord, p2.cord, arraySize)
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
        map.redraw(p1, p2, win)
        round += 1
        time.sleep(.5)



class Map:
    def __init__(self, arraySize):
        self.map = []
        self.arraySize = arraySize

    def update(self, p1Cord, p2Cord):
        newArena = np.zeros((self.arraySize, self.arraySize), dtype=int)
        newArena[p1Cord[0]][p1Cord[1]] = 1
        newArena[p2Cord[0]][p2Cord[1]] = 2
        self.map = newArena

    def draw(self, p1, p2, win):
        p1.sprite.draw(win)
        p2.sprite.draw(win)

    def redraw(self, p1, p2, win):
        for i in range(20):
            p1.sprite.move(p1.distance[0]/20, p1.distance[1]/20)
            p2.sprite.move(p2.distance[0]/20, p2.distance[1]/20)
            time.sleep(.03)






class Player:
    def __init__(self, name, cord, position, health, defense, color):
        self.name = name
        self.cord = cord #array
        self.position = position #map
        self.health = health
        self.defense = defense
        self.color = color
        self.distance = [0, 0]
        self.sprite = Circle(Point(self.position[0], self.position[1]), 25)
        self.sprite.setFill(self.color)

    def attack(self, target):
        damage = r.randint(5, 10) - target.defense
        target.health -= damage
        print("%s did %s damage to %s \n%s has %s health" % (self.name, damage, target.name, target.name, target.health))

    def findCordDifference(self, target):
        difference = [0, 0]
        for i in range(len(self.cord)):
            difference[i] = self.cord[i] - target.cord[i]
        return difference

    def findPositionDifference(self, oldPosition):
        difference = [0, 0]
        for i in range(len(self.position)):
            difference[i] = self.position[i] - oldPosition[i]
        self.distance = difference

    def move(self, other):
        oldPosition = [0, 0]
        oldPosition[0] = self.position[0]
        oldPosition[1] = self.position[1]
        difference = self.findCordDifference(other)
        while True:
            newCord = [0,0]
            newCord[0] = self.cord[0]
            newCord[1] = self.cord[1]
            if self.health <= 10:
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
                self.findPositionDifference(oldPosition)
                break

            if direction == 1: #up
                newCord[0] -= 1
                if newCord[0] >= 0 and newCord != other.cord:
                    self.cord[0] -= 1
                    self.position[1] -= 100
                    self.findPositionDifference(oldPosition)
                    break
            if direction == 2: #down
                newCord[0] += 1
                if newCord[0] <= 2 and newCord != other.cord:
                    self.cord[0] += 1
                    self.position[1] += 100
                    self.findPositionDifference(oldPosition)
                    break
            if direction == 3: #left
                newCord[1] -= 1
                if newCord[1] >= 0 and newCord != other.cord:
                    self.cord[1] -= 1
                    self.position[0] -= 100
                    self.findPositionDifference(oldPosition)
                    break
            if direction == 4: #right
                newCord[1] += 1
                if newCord[1] <= 2 and newCord != other.cord:
                    self.cord[1] += 1
                    self.position[0] += 100
                    self.findPositionDifference(oldPosition)
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

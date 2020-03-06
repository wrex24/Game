import random as r
import time
import numpy as np
from caseyGraphics import *


def main():

    roundIndex = 1
    arraySize = 3
    windowSize = 900
    mapSize = 500
    borderSize = (windowSize - mapSize)/2
    p1 = Player("bartholomew", [windowSize/2, borderSize + 50], 30, 5, 4, "bartholomew")
    p2 = Player("chicken man", [windowSize/2, windowSize-borderSize-50],  30, 5, 4, "chickenMan")
    map = Map("beyblade.png", mapSize, windowSize, borderSize, roundIndex)
    win = GraphWin('game', windowSize, windowSize)

    win.getMouse()

    map.draw(p1, p2, win)
    while True:
        if nextToEachother(p1.cord, p2.cord):
            p1.attack(p2, map)
            p2.attack(p1, map)
            #map.update(p1, p2, win)
        if p1.health <= 0 or p2.health <= 0:
            if p1.health < p2.health:
                print("player 2 wins")
                map.end(p2, win)
            else:
                print("player 1 wins")
                map.end(p1, win)
            win.getMouse()
            break
        if p1.health >= p2.health:
            p1.move(p2, map)
            p2.move(p1, map)
        else:
            p2.move(p1, map)
            p1.move(p2, map)

        print("\n")
        map.redraw(p1, p2, win, roundIndex)
        roundIndex += 1

        time.sleep(.5)



class Map:
    def __init__(self, background, mapSize, windowSize, borderSize, roundIndex):
        self.background = Image(Point(windowSize/2, windowSize/2), background)
        self.mapSize = mapSize
        self.windowSize = windowSize
        self.borderSize = borderSize
        self.isHealthDrawn = False
        self.roundCounter = Text(Point(25, 25), "%s" % roundIndex)

    def draw(self, p1, p2, win):
        self.background.draw(win)
        self.roundCounter.draw(win)
        p1.sprite.draw(win)
        p1.healthCounter.draw(win)
        p2.sprite.draw(win)
        p2.healthCounter.draw(win)
        self.isHealthDrawn = True

    def redraw(self, p1, p2, win, roundIndex):

        self.roundCounter.setText("%s" % roundIndex)
        if self.isHealthDrawn == False:
            p1.healthCounter.draw(win)
            p2.healthCounter.draw(win)

        p1.sprite.draw(win)
        p2.sprite.draw(win)

        for i in range(20):
            p1.sprite.move(p1.distance[0]/20, p1.distance[1]/20)
            p1.healthCounter.move(p1.distance[0]/20, p1.distance[1]/20)
            p2.sprite.move(p2.distance[0]/20, p2.distance[1]/20)
            p2.healthCounter.move(p2.distance[0]/20, p2.distance[1]/20)
            self.isHealthDrawn = True
            time.sleep(.03)

    def undraw(self, p1, p2, mode):
        if mode == "sprite":
            p1.sprite.undraw()
            p2.sprite.undraw()
        if mode == "health":
            p1.healthCounter.undraw()
            p2.healthCounter.undraw()
            self.isHealthDrawn = False



    def end(self, winner, win):
        winMessage = Text(Point(self.windowSize/2, self.windowSize/2), "%s has won" % winner.name)
        winMessage.setFace("arial")
        winMessage.setSize(30)
        winMessage.draw(win)



class Player:
    def __init__(self, name, cord, health, defense, endurance, fileName):
        self.name = name
        self.cord = cord #array
        self.maxHealth = health
        self.health = health
        self.defense = defense
        self.distance = [0, 0]
        self.endurance = endurance
        self.fatigue = endurance
        self.fileName = fileName
        self.barSize = ((80/self.health) * self.health)-40
        self.sprite = Image(Point(self.cord[0], self.cord[1]), "%sDown.png" %self.fileName)
        self.healthCounter = Rectangle(Point(self.cord[0]-40, self.cord[1]+50), Point(self.cord[0]+self.barSize, self.cord[1]+45) )
        self.healthCounter.setFill("green")

    def attack(self, target, map):
        map.undraw(self, target, "health")

        damage = r.randint(5, 10) - target.defense
        target.health -= damage
        target.barSize = ((80/target.maxHealth) * target.health) - 40
        target.healthCounter = Rectangle(Point(target.cord[0]-40, target.cord[1]+50), Point(target.cord[0]+target.barSize, target.cord[1]+45) )
        target.healthCounter.setFill("green")

        print("%s did %s damage to %s \n%s has %s health" % (self.name, damage, target.name, target.name, target.health))

    def findPlayerDifference(self, target):
        difference = [0, 0]
        for i in range(len(self.cord)):
            difference[i] = self.cord[i] - target.cord[i]
        return difference

    def findCordDifference(self, oldCord):
        difference = [0, 0]
        for i in range(len(self.cord)):
            difference[i] = self.cord[i] - oldCord[i]
        self.distance = difference

    def move(self, other, map):
        oldCord = [0, 0]
        oldCord[0] = self.cord[0]
        oldCord[1] = self.cord[1] #updates old position
        difference = self.findPlayerDifference(other) #finds difference between two players
        fatigue = self.endurance
        while True:
            newCord = [0,0]
            newCord[0] = self.cord[0]
            newCord[1] = self.cord[1]
            if self.health <= 20 and self.health < other.health:
                self.fatigue -= 1
                if self.fatigue == 0:
                    print("%s fatigued" %(self.name))
                    self.fatigue = fatigue
                    direction = 0
                else:
                    direction = r.randint(1, 4)

            else:
                if difference[1] <= -200: #too far down
                    direction = 2
                elif difference[1] >= 200: #too far up
                    direction = 1
                elif difference[0] <= -200: #too far right
                    direction = 4
                elif difference[0] >= 200: #too far left
                    direction = 3
                elif difference == [-100, -100]: #too far right down
                    direction = r.choice((2,4))
                elif difference == [100, -100]:  # too far left down
                    direction = r.choice((2,3))
                elif difference == [-100, 100]:  # too far right up
                    direction = r.choice((1,4))
                elif difference == [100, 100]:  # too far left up
                    direction = r.choice((1,3))
                elif nextToEachother(self.cord, other.cord):
                    direction = 0
                else:
                    direction = r.randint(1, 4)

            if direction == 0:
                map.undraw(self, other, "sprite")
                self.findCordDifference(oldCord)
                break

            if direction == 1: #up
                newCord[1] -= 100
                if newCord[1] >= map.borderSize and newCord != other.cord:
                    map.undraw(self,other, "sprite")
                    self.sprite = Image(Point(self.cord[0], self.cord[1]), "%sUp.png" % self.fileName)
                    self.cord[1] -= 100
                    self.findCordDifference(oldCord)

                    break
            if direction == 2: #down
                newCord[1] += 100
                if newCord[1] <= map.windowSize - map.borderSize and newCord != other.cord:
                    map.undraw(self,other, "sprite")
                    self.sprite = Image(Point(self.cord[0], self.cord[1]), "%sDown.png" % self.fileName)
                    self.cord[1] += 100
                    self.findCordDifference(oldCord)

                    break
            if direction == 3: #left
                newCord[0] -= 100
                if newCord[0] >= map.borderSize and newCord != other.cord:
                    map.undraw(self,other, "sprite")
                    self.sprite = Image(Point(self.cord[0], self.cord[1]), "%sLeft.png" % self.fileName)
                    self.cord[0] -= 100
                    self.findCordDifference(oldCord)

                    break
            if direction == 4: #right
                newCord[0] += 100
                if newCord[0] <= map.windowSize - map.borderSize and newCord != other.cord:
                    map.undraw(self,other, "sprite")
                    self.sprite = Image(Point(self.cord[0], self.cord[1]), "%sRight.png" % self.fileName)
                    self.cord[0] += 100
                    self.findCordDifference(oldCord)

                    break
            self.fatigue += 1



def nextToEachother(p1Cord, p2Cord):
    difference = [0, 0]
    for i in range(len(p1Cord)):
        difference[i] = p1Cord[i] - p2Cord[i]
    if difference == [0, 100] or difference == [0, -100] or difference == [100, 0] or difference == [-100, 0]:
        return True
    return False


if __name__ == '__main__':
    main()

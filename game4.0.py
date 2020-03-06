import random as r
import time
import numpy as np
from caseyGraphics import *
import math


def main():

    roundIndex = 1
    arraySize = 3
    windowSize = 900
    mapSize = 500
    borderSize = (windowSize - mapSize)/2
    p1 = Player("chicken man", [windowSize/2, borderSize + 50], 30, 5, 4, "chickenMan")
    p2 = Player("bird", [windowSize/2, windowSize-borderSize-50],  30, 5, 4, "bird")
    map = Map("krusty.png", mapSize, windowSize, borderSize, roundIndex)
    win = GraphWin('game', windowSize, windowSize)
    map.draw(p1, p2, win)
    win.getMouse()

    while True:
        if map.tooClose(p1, p2):
            p1.attack(p2, map, win)
            p2.attack(p1, map, win)
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
            p1.move(p2, map, win)
            p2.move(p1, map, win)
        else:
            p2.move(p1, map, win)
            p1.move(p2, map, win)

        map.redraw(p1, p2, win, roundIndex)
        roundIndex += 1
        time.sleep(.3)

class Map:
    def __init__(self, background, mapSize, windowSize, borderSize, roundIndex):
        self.background = Image(Point(windowSize/2, windowSize/2), background)
        self.mapSize = mapSize
        self.windowSize = windowSize
        self.borderSize = borderSize
        self.upperBorder = int(borderSize)
        self.lowerBorder = int(self.windowSize - self.borderSize)
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
        p1.frame = math.ceil(abs(math.sqrt((p1.distance[0])**2 + (p1.distance[1])**2))/10)
        p2.frame = math.ceil(abs(math.sqrt((p2.distance[0])**2 + (p2.distance[1])**2))/10)
        self.roundCounter.setText("%s" % roundIndex)
        if self.isHealthDrawn == False:
            p1.healthCounter.draw(win)
            p2.healthCounter.draw(win)

        p1.sprite.draw(win)
        p2.sprite.draw(win)

        if p2.onTheRun:
            first = p2
            second = p1
        else:
            first = p1
            second = p2

        while True:
            for i in range(first.frame):
                if self.tooClose(p1, p2):
                    break
                first.sprite.move(first.distance[0]/first.frame, first.distance[1]/first.frame)
                first.healthCounter.move(first.distance[0]/first.frame, first.distance[1]/first.frame)
                first.cord[0] += first.distance[0]/first.frame
                first.cord[1] += first.distance[1]/first.frame
                self.isHealthDrawn = True
                if first.distance != [0, 0]:
                    time.sleep(.035)
            for i in range(second.frame):
                if self.tooClose(p1, p2) and second.knockedBack == False:
                    break
                second.sprite.move(second.distance[0]/second.frame, second.distance[1]/second.frame)
                second.healthCounter.move(second.distance[0]/second.frame, second.distance[1]/second.frame)
                second.cord[0] += second.distance[0]/second.frame
                second.cord[1] += second.distance[1]/second.frame
                self.isHealthDrawn = True
                if second.distance != [0, 0]:
                    time.sleep(.035)
            second.knockedBack = False
            break

    def undraw(self, p1, p2, mode):
        if mode == "sprite":
            p1.sprite.undraw()
            p2.sprite.undraw()
        if mode == "health":
            p1.healthCounter.undraw()
            p2.healthCounter.undraw()
            self.isHealthDrawn = False

    def end(self, winner, win):
        winner.healthCounter.draw(win)
        winMessage = Text(Point(self.windowSize/2, self.windowSize/2), "%s has won" % winner.name)
        winMessage.setFace("arial")
        winMessage.setSize(30)
        winMessage.draw(win)

    def tooClose(self, p1, p2):
        difference = 0
        difference = abs((((p1.cord[0] - p2.cord[0])**2) + ((p1.cord[1] - p2.cord[1])**2))**.5)
        if difference <= 100:
            return True
        return False


class Player:
    def __init__(self, name, cord, health, defense, endurance, fileName):
        self.name = name
        self.cord = cord #array
        self.newCord = [0, 0]
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
        self.onTheRun = False
        self.knockedBack = False
        self.frame = 0

    def attack(self, target, map, win):
        map.undraw(self, target, "health")

        damage = r.randint(5, 10) - target.defense
        target.health -= damage
        target.barSize = ((80/target.maxHealth) * target.health) - 40
        target.healthCounter = Rectangle(Point(target.cord[0]-40, target.cord[1]+50), Point(target.cord[0]+target.barSize, target.cord[1]+45) )
        target.healthCounter.setFill("green")
        if damage >= 0 and self.onTheRun:
            target.knockedBack = True
            print("%s is knocked back" % target.name)

        print("\n%s did %s damage to %s \n%s has %s health" % (self.name, damage, target.name, target.name, target.health))

    def findPlayerDifference(self, target):
        difference = [0, 0]
        for i in range(len(self.cord)):
            difference[i] = self.cord[i] - target.cord[i]
        return difference

    def findCordDifference(self, newCord, oldCord):
        difference = [0, 0]
        for i in range(len(newCord)):
            difference[i] = newCord[i] - oldCord[i]
        self.distance = difference


    def move(self, other, map, win):
        seedDirection = [0, 0]
        lowerBorder = map.lowerBorder
        upperBorder = map.upperBorder
        oldCord = [0, 0]
        oldCord[0] = self.cord[0]
        oldCord[1] = self.cord[1] #updates old position
        difference = self.findPlayerDifference(other) #finds difference between two players
        fatigue = self.endurance
        for i in range(1):
            direction = [0, 0]
            maxCord = [0, 0] #max distance possible
            startCord = [0,0] #where the character starts
            newCord = [0, 0] # max disrance within bounds
            maxCord[0] = self.cord[0]
            maxCord[1] = self.cord[1]
            startCord[0] = self.cord[0]
            startCord[1] = self.cord[1]
            newCord[0] = self.cord[0]
            newCord[1] = self.cord[1]

            if self.health <= 20 and self.health < other.health:
                self.onTheRun = True
                self.fatigue -= 1
                if map.tooClose(self, other):
                    if other.cord[0] - self.cord[0] >= 0:
                        seedDirection[0] = r.randint(-200, -100)
                    if other.cord[0] - self.cord[0] <= 0 :
                        seedDirection[0] = r.randint(100, 200)
                else:
                    seedDirection[0] = r.randint(-200, 200)
            else:
                self.onTheRun = False
                if other.cord[0] - self.cord[0] > 0:
                    seedDirection[0] = r.randint(0, 200)
                if other.cord[0] - self.cord[0] < 0:
                    seedDirection[0] = r.randint(-200, 0)

            if maxCord[0] + seedDirection[0] > lowerBorder:
                seedDirection[0] = map.lowerBorder - startCord[0]

            if maxCord[0] + seedDirection[0] < upperBorder:
                seedDirection[0] = map.upperBorder - startCord[0]

            direction[1] = abs(((40000 - seedDirection[0] ** 2) ** .5)) * r.choice((-1, 1))

            if self.onTheRun:
                if other.cord[1] - self.cord[1] >= 0 and direction[1] > 0:
                    direction[1] *= -1
                if other.cord[1] - self.cord[1] <= 0 and direction[1] < 0:
                    direction[1] *= -1
            else:
                if other.cord[1] - self.cord[1] <= 0 and direction[1] > 0:
                    direction[1] *= -1
                if other.cord[1] - self.cord[1] >= 0 and direction[1] < 0:
                    direction[1] *= -1

            if maxCord[1] + direction[1] > lowerBorder:
                direction[1] = map.lowerBorder - startCord[1]

            if maxCord[1] + direction[1] < upperBorder:
                direction[1] = map.upperBorder - startCord[1]

            direction[0] = abs(((40000 - direction[1] ** 2) ** .5))
            if seedDirection[0] < 0:
                direction[0] *= -1

            if maxCord[0] + direction[0] > lowerBorder:
                direction[0] = map.lowerBorder - startCord[0]

            if maxCord[0] + direction[0] < upperBorder:
                direction[0] = map.upperBorder - startCord[0]

            if self.fatigue == 0:
                print("%s fatigued" % (self.name))
                self.fatigue = fatigue
                direction = [0, 0]

            if other.onTheRun == False and self.onTheRun == False and map.tooClose(self, other):
                direction = [0, 0]

            if self.knockedBack:
                print("%s knocked back" %(self.name))
                if self.cord[0] - other.cord[0] > 0:
                    direction[0] = 50
                else:
                    direction[0] = -50
                if self.cord[1] - other.cord[1] > 0:
                    direction[1] = 50
                else:
                    direction[1] = -50

            if maxCord[0] + direction[0] > lowerBorder:
                direction[0] = map.lowerBorder - startCord[0]

            if maxCord[0] + direction[0] < upperBorder:
                direction[0] = map.upperBorder - startCord[0]

            if maxCord[1] + direction[1] > lowerBorder:
                direction[1] = map.lowerBorder - startCord[1]

            if maxCord[1] + direction[1] < upperBorder:
                direction[1] = map.upperBorder - startCord[1]


            newCord[0] = maxCord[0] + direction[0]
            newCord[1] = maxCord[1] + direction[1]

            self.newCord[0] = newCord[0]
            self.newCord[1] = newCord[1]
            self.findCordDifference(newCord, oldCord)
            map.undraw(self, other, "sprite")



if __name__ == '__main__':
    main()

from snake import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Thread, Lock
import time
from random import randint


class CMap:

    def __init__(self, parent):
        super().__init__()

        self.thread = Thread(target=self.playgame)

        self.lock = Lock()

        self.bRun = True

        self.bMove = True

        self.bGame = False

        self.foodcnt = 0

        self.lines = 15

        self.snake = CSnake(self.lines)

        self.food = CNode(-1, -1)

        self.parent = parent

        self.outrect = parent.rect()

        gap = 20
        self.inrect = self.outrect.adjusted(gap, gap, -gap, -gap)

        self.wsize = self.inrect.width() / self.lines
        self.hsize = self.inrect.height() / self.lines

        self.left = self.inrect.left()
        self.top = self.inrect.top()
        self.right = self.inrect.right()
        self.bottom = self.inrect.bottom()

        self.rect = [[QRectF for _ in range(self.lines)] for _ in range(self.lines)]

        topleft = QPoint(self.left, self.top)
        size = QSize(self.wsize, self.hsize)

        for i in range(self.lines):
            for j in range(self.lines):
                self.rect[i][j] = QRect(self.left + (j * self.wsize)
                                        , self.top + (i * self.hsize)
                                        , self.wsize
                                        , self.hsize)
                self.rect[i][j].adjust(2, 2, -2, -2)

    def reStart(self):

        del (self.thread)
        self.thread = Thread(target=self.playgame)

        self.bRun = True
        self.bGame = False
        self.bMove = True
        self.foodcnt = 0

        del (self.snake)
        self.snake = CSnake(self.lines)

        del (self.food)
        self.food = CNode(-1, -1)

    def draw(self, qp):

        for i in range(self.lines + 1):
            qp.drawLine(self.left, self.top + (i * self.hsize), self.right, self.top + (i * self.hsize))
            qp.drawLine(self.left + (i * self.wsize), self.top, self.left + (i * self.wsize), self.bottom)

        i = 0
        self.lock.acquire()
        for node in self.snake.node:
            if i == 0:
                qp.setBrush(QColor(33, 53, 194))
            else:
                qp.setBrush(QColor(83, 103, 255, 128))
            if self.bRun:
                qp.drawRect(self.rect[node.y][node.x])
            i += 1
        self.lock.release()

        self.lock.acquire()

        if self.food.x != -1 and self.food.y != -1:
            qp.setBrush(QColor(255, 0, 0))
            qp.drawEllipse(self.rect[self.food.y][self.food.x])
        self.lock.release()

        qp.drawText(self.outrect, Qt.AlignTop | Qt.AlignLeft, '점수:' + str(self.foodcnt))

        if not self.bGame:
            qp.setFont(QFont('맑은 고딕', 20))
            qp.drawText(self.outrect, Qt.AlignCenter, '키보드 방향키를 누르면 시작')

    def keydown(self, key):

        if (key == Qt.Key_Right or key == Qt.Key_Up or key == Qt.Key_Down) and self.bGame == False:
            self.bGame = True
            self.snake.changeDir(key)
            self.thread.start()

        if (key == Qt.Key_Left or key == Qt.Key_Right or key == Qt.Key_Up or key == Qt.Key_Down) and self.bGame == True:
            if self.bMove:
                self.snake.changeDir(key)
                self.bMove = False

    def makeFood(self):
        if self.food.x != -1 and self.food.y != -1:
            return

        cnt = 0
        while True:
            x = randint(0, self.lines - 1)
            y = randint(0, self.lines - 1)
            node = CNode(x, y)

            bDiff = False

            for snode in self.snake.node:
                if node == snode:
                    bDiff = True
                    break

            if not bDiff:
                self.food = node
                break

            if cnt >= self.lines * self.lines:
                break

            cnt += 1

    def isEat(self, node):

        if self.food == node:
            return True
        else:
            return False

    def isOut(self, head):
        if head.x < 0 or head.x >= self.lines:
            return True
        elif head.y < 0 or head.y >= self.lines:
            return True
        else:
            return False

    def playgame(self):

        while self.bRun:
            self.lock.acquire()

            if not self.snake.move() or self.isOut(self.snake.node[0]):
                self.parent.update()
                self.bRun = False
                self.bGame = False
                self.lock.release()
                break

            self.makeFood()

            bEat = self.isEat(self.snake.node[0])

            if bEat:
                self.snake.addNode()
                self.foodcnt += 1
                self.food.x = -1
                self.food.y = -1

            self.lock.release()

            self.bMove = True

            self.parent.update()
            if self.foodcnt <= 10:
                time.sleep(0.3)
            elif self.foodcnt <= 30:
                time.sleep(0.25)
            else:
                time.sleep(0.2)

        if not self.bGame:
            self.parent.endSignal.emit()
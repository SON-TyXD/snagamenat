from PyQt5.QtCore import Qt


class CNode:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


class CSnake:
    def __init__(self, lines):

        self.node = []

        self.dir = Qt.Key_Right

        self.bAdd = False

        self.init(lines)

    def init(self, lines):
        cx = lines // 2
        cy = lines // 2
        for i in range(3):
            self.node.append(CNode(cx, cy))
            cx -= 1

    def changeDir(self, key):

        if self.isChangeDir(key) == False:
            return None

        self.dir = key

    def isChangeDir(self, key):
        if self.dir == Qt.Key_Left and key == Qt.Key_Right:
            return False
        elif self.dir == Qt.Key_Right and key == Qt.Key_Left:
            return False
        elif self.dir == Qt.Key_Up and key == Qt.Key_Down:
            return False
        elif self.dir == Qt.Key_Down and key == Qt.Key_Up:
            return False
        else:
            return True

    def isCrach(self):

        if self.nodeCount() < 5:
            return False

        head = CNode(self.node[0].x, self.node[0].y)

        bodylist = self.node[4:]

        for body in bodylist:
            if head == body:
                return True

        return False

    def move(self):

        if self.isCrach():
            return False

        head = CNode(self.node[0].x, self.node[0].y)

        if self.dir == Qt.Key_Left:
            head.x -= 1
        elif self.dir == Qt.Key_Right:
            head.x += 1
        elif self.dir == Qt.Key_Up:
            head.y -= 1
        elif self.dir == Qt.Key_Down:
            head.y += 1

        self.node.insert(0, head)

        if self.bAdd:
            self.bAdd = False
        else:
            self.node.pop()

        return True

    def addNode(self):
        self.bAdd = True

    # 뱀 길이 얻기
    def nodeCount(self):
        return len(self.node)
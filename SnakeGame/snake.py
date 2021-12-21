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

        # 뱀 마디 리스트
        self.node = []

        # 뱀 방향
        self.dir = Qt.Key_Right

        # 뱀 마디 추가
        self.bAdd = False

        self.init(lines)

    def init(self, lines):
        cx = lines // 2
        cy = lines // 2
        # 기본 뱀 3마디 생성
        for i in range(3):
            self.node.append(CNode(cx, cy))
            cx -= 1

    def changeDir(self, key):

        if self.isChangeDir(key) == False:
            return None

        self.dir = key

    def isChangeDir(self, key):
        # 현재 방향과 이동할 방향이 반대인지?
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

        # 뱀 머리
        head = CNode(self.node[0].x, self.node[0].y)

        # 몸통은 4번째 마디부터 충돌가능하므로
        bodylist = self.node[4:]

        for body in bodylist:
            if head == body:
                return True

        return False

    def move(self):

        # 머리, 몸통 충돌 검사
        if self.isCrach():
            return False

        # 뱀 머리
        head = CNode(self.node[0].x, self.node[0].y)

        if self.dir == Qt.Key_Left:
            head.x -= 1
        elif self.dir == Qt.Key_Right:
            head.x += 1
        elif self.dir == Qt.Key_Up:
            head.y -= 1
        elif self.dir == Qt.Key_Down:
            head.y += 1

        # 이동방향으로 뱀머리 추가
        self.node.insert(0, head)

        # 이동시 밥 먹었으면 꼬리 유지, 아니면 제거
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
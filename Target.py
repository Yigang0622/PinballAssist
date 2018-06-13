class Target:

    x = 0
    y = 0
    level = 0
    number = -1

    def info(self):
        print('位于第',self.level, '层， 坐标:', self.x, ',', self.y, "数字识别结果:", self.number)

    def get_coordinate(self):
        return self.x, self.y



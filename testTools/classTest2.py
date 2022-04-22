class F:
    def __init__(self, name):
        self.name = name
        print('name:'+self.name)
    def setName(self):
        return 'F2:'+self.name
    def getName(self):
        return 'F:' + self.name
class S(F):
    def getName(self):
        return 'S:' + self.name
if __name__ == '__main__':
    s = S('sun')
    print(s.setName())

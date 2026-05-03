class Test(object):
    def __init__(self, name):
        self.name = name
    def __or__(self, other):
        return MySequence(self, other)
    def __str__(self):
        return self.name

class MySequence(object):
    # *args表示接受任意数量的位置参数，args是一个元组，包含所有传入的位置参数。
    def __init__(self, *args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)
    def __or__(self, other):
        self.sequence.append(other)
        return self
    def run(self):
        for i in self.sequence:
            print(i)


if __name__ == '__main__':
    a = Test('a')
    b = Test('b')
    c = Test('c')
    # 通过重载|运算符，实现[a, b, c]的效果。
    # a | b 之后（a｜b）变为一个MySequence对象，继续与c进行|运算时，MySequence对象的__or__方法被调用，将c添加到sequence列表中。
    d = a | b | c # a.__or__(b)，d也就是a ｜ b | c，是一个MySequence对象。
    
    # 调用Mysequence类中的run方法，依次打印a、b、c的name属性。
    d.run()
    print(type(d))
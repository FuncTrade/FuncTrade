class AbstractTask:
    def __rshift__(self, other):
        print(f"{self} >> {other}")
        return (self, other)   # 记录调用关系

    def __lshift__(self, other):
        print(f"{self} << {other}")
        return (other, self)
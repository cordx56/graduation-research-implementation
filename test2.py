class A:
    def f(self) -> int:
        return 0

class B:
    def f(self) -> int:
        return 0
    def g(self) -> int:
        return 1

a: A = B()
print(a.f())

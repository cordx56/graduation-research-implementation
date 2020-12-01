def test(n: int) -> str:
    if n < 0:
        return "negative"
    elif 0 < n:
        return "positive"
    else:
        return "zero"

def muladd(a: int, b: int) -> int:
    def add(a: int, b: int) -> int:
        return a + b
    def mul(a: int, b: int) -> int:
        return a * b
    return mul(add(a, b), b)

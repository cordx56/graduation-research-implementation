
def test():
    a = {}
    return a

def return_str():
    a = A()
    if a == "test":
        b = a
    return a.return_string()

class A:
    a = "test"
    def return_string(self):
        return self.a

if __name__ == "__main__":
    print(return_str())

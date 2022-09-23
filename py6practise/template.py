from typing import Union

def add(a:Union[float,int],b:Union[float,int] )-> float:
    return round(a + b, 2)

if __name__ == "__main__":
    print((add(1,2)))
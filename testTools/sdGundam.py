
def autoGet(number,numberEnd):
    while number <= numberEnd:
        print("sdgundamext -f \"anrs\\{}.ani\" GPackData.zpk SDGO_TEMP".format(number))
        number += 1




if __name__ == "__main__":
    number = 39456
    numberEnd =  39464
    autoGet(number,numberEnd)
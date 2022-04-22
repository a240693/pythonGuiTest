if __name__ == "__main__":
    demo = "PJJC防守成功"
    if "PJJC".__eq__(demo):
        print(1)
    elif "PJJC%".__eq__(demo) | ("成功" in demo):
        print(2)
    elif "PJJC" in demo :
        print(3)
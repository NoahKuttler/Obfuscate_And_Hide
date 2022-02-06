import random
import time

x = 6
def check():
    if x < 10:
        time.sleep(random.randint(1,7))
        print("yes")

if __name__ == '__main__':
    check()
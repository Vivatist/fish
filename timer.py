import time
import random

start = time.time()

a = random.randint(20, 50) / 60

for i in range(100000):
    x = int(a)

end = time.time()


print("The time of execution of above program is :", (end - start) * 10**3, "ms")

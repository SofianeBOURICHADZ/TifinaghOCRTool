import random
random.seed(0)

chars = [chr(x) for x in range(0x2D30,0x2D66)] + [chr(0x2D6F)] + list("0123456789,.-!?")

with open("corpus.txt", "w",encoding="utf-8") as f:
    for _ in range(0, 50000):
        line = " ".join("".join(random.choices(chars, k=random.randint(1, 13))) for _ in range(random.randint(2, 9)))
        f.write(line +"\n")
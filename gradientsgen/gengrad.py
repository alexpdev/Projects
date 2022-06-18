import random

htd = {
    "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "9": 9, "8": 8,
    "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2, "1": 1, "0": 0
}
dth = {
    0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6",
    7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D",
    14: "E", 15: "F"
}

START = ["00", "FF", "44"]

def minus(seq, index):
    current = seq[index]
    if htd[current[1]]:
        value = current[0] + dth[htd[current[1]] - 1]
        seq[index] = value
        return
    if htd[current[0]]:
        value = dth[htd[current[0]]-1] + "F"
        seq[index] = value
        return
    seq[index] = "FF"

def plus(seq, index):
    current = seq[index]
    if htd[current[1]] != "F":
        value = current[0] + dth[htd[current[1]] + 1]
        seq[index] = value
        return
    if htd[current[0]] != "F":
        value = dth[htd[current[0]]+1] + "0"
        seq[index] = value
        return
    seq[index] = "00"

def main(start):
    last = 0
    while True:
        last = random.choice([i for i in range(3) if i != last])
        number = random.randint(16,127)
        direction = random.randint(0,1)
        for _ in range(number):
            if direction:
                plus(start, last)
            else:
                minus(start, last)
            yield(start)

animals = ["dog", "cat", "bat", "cock", "cow", "pig",
           "fox", "ant", "bird", "lion", "wolf", "deer", "bear",
           "frog", "hen", "mole", "duck", "goat"]
def count_animals(txt):
    counts = []
    def f(t, c):
        for a in animals:
            s = t
            for x in a: s = s.replace(x, "", 1)
            if len(s) + len(a) == len(t): f(s, c + 1)
        counts.append(c)
    f(txt, 0)
    return max(counts)

if __name__ == '__main__':
    print(count_animals("cockdogwdufrbir"))
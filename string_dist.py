def string_dist(s1, s2):
    return sum (1 for char in set(s1) if char not in set(s2))

print(string_dist("crandell", "crandall"))
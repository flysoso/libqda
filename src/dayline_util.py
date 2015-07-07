
import math

def calculate_factor(dayline):
    n = 0
    k = 0
    e = 0
    for dtime,dcash in dayline:
        n += 1
        k += dcash*dcash
        e += dcash
    e = e / n
    d = k - n*e*e
    shake_factor = math.sqrt(d) / e
    return shake_factor

def calculate_minus(dayline):
    return dayline[0][1] - dayline[-1][1]

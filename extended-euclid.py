def gcd_extended(a, b):
    if a == 0:
        x1 = 0
        y1 = 1
        return b, x1, y1

    gcd, x1, y1 = gcd_extended(b % a, a)

    x = y1 - (b/a) * x1
    y = x1

    return gcd, x, y


def main():
    a = 35
    b = 15
    gcd, m, n = gcd_extended(a, b)
    print "a = " + str(a) + ", b = " + str(b)
    print "gcd = " + str(gcd) + ", m = " + str(m) + ", n = " + str(n)


if __name__ == "__main__":
    main()
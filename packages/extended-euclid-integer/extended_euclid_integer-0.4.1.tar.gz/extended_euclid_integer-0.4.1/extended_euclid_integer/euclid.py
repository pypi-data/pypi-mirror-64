class EuclidInteger:
    a = None
    b = None
    gcd = None
    mod_inv = None

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.gcd = egcd(a,b)[0]
        self.mod_inv = modinv(a,b)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, x, y = egcd(b_mod_a, a)
        return (g, y - b_div_a * x, x)

def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g != 1:
        raise Exception('gcd(b, n) != 1')
    return x % n


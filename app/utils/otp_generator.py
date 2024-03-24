import random


def generate_otp():
    otp = random.sample(range(100000, 9000000), 5)
    return str(otp[0])[0:6]

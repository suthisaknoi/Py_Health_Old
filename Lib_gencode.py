import random
import string

def generate_random_string(length=80):
    characters = string.ascii_letters + string.digits + "!^@#$&*"
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def ENmix_hcodeTOstring(hcode):
    length = 80
    d1= hcode[0:1]
    d2 = hcode[1:2]
    d3 = hcode[2:3]
    d4 = hcode[3:4]
    d5 = hcode[4:5]
    characters = string.ascii_letters + string.digits + "!^@#$&*"
    random_string1 = ''.join(random.choice(characters) for _ in range(13))
    random_string2 = ''.join(random.choice(characters) for _ in range(9))
    random_string3 = ''.join(random.choice(characters) for _ in range(21))
    random_string4 = ''.join(random.choice(characters) for _ in range(7))
    random_string5 = ''.join(random.choice(characters) for _ in range(11))
    random_string6 = ''.join(random.choice(characters) for _ in range(4))
    ## 5-1-4-3-2
    return random_string1+d5+random_string2+d1+random_string3+d4+random_string4+d3+random_string5+d2+random_string6

def DEmix_hcodeTOstring(code_allow):
    d1 = code_allow[23:24]
    d2 = code_allow[65:66]
    d3 = code_allow[53:54]
    d4 = code_allow[45:46]
    d5 = code_allow[13:14]
    return d1+d2+d3+d4+d5



# ENstring_code = ENmix_hcodeTOstring('07789')
# print(ENstring_code)
#
# DEstring_code = DEmix_hcodeTOstring(ENstring_code)
# print(DEstring_code)

# Generate a random string of length 10
# random_string = generate_random_string()
# print(random_string)
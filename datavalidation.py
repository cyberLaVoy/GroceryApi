from fractions import Fraction

def isValidQuantityString(quantity):
    try:
        parts = quantity.strip().split() 
        if len(parts) > 2:
            return False
        elif len(parts) == 2:
            int(parts[0])
            if parts[1].count('/') != 1:
                return False
        for part in parts:
            Fraction(part)
        return True
    except Exception as e:
        print(e)
        return False
def parseQuantityString(quantity):
    total = Fraction(0)
    parts = quantity.strip().split() 
    for part in parts:
        total += Fraction(part)
    quantity = str(total)
    denominator = total.denominator
    wholeNumber = total.numerator // denominator
    if wholeNumber != 0:
        numerator = total.numerator - denominator*wholeNumber
        if numerator == 0:
            quantity = str(wholeNumber)
        else:
            fraction = Fraction(numerator, denominator)
            quantity = str(wholeNumber) + ' ' + str(fraction)
    return quantity
def addQuantityStrings(quantity1, quantity2):
    total = Fraction(0)
    parts1 = quantity1.strip().split()
    for part in parts1:
        total += Fraction(part)
    parts2 = quantity2.strip().split()
    for part in parts2:
        total += Fraction(part)
    return parseQuantityString(str(total))

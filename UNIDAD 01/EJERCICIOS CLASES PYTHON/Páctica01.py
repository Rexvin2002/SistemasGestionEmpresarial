class Fraction:
    def __init__(self, numerator, denominator):
        self.signo = -1 if numerator * denominator < 0 else 1
        numerator = abs(numerator)
        denominator = abs(denominator)
        self.simplify(numerator, denominator)

    def simplify(self, numerator, denominator):
        gcd = self.gcd(numerator, denominator)
        self.numerator = numerator // gcd
        self.denominator = denominator // gcd

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def __add__(self, other):
        numerator = self.numerator * other.denominator + other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __str__(self):
        return f"{self.signo * self.numerator}/{self.denominator}"

while True:
    # Prompt user to input fractions
    numerator1 = int(input("\nEnter numerator of first fraction: "))
    denominator1 = int(input("Enter denominator of first fraction: "))

    numerator2 = int(input("\nEnter numerator of second fraction: "))
    denominator2 = int(input("Enter denominator of second fraction: "))

    f1 = Fraction(numerator1, denominator1)
    f2 = Fraction(numerator2, denominator2)

    print("\n--RESULTS--")
    print(f"First fraction: {f1}")
    print(f"Second fraction: {f2}")

    f3 = f1 + f2  # Sum f1 and f2
    print(f"Sum: {f3}")

    print(f"Are f1 and f2 equal? {f1 == f2}")

    answer = input("\nDo you want to exit? (y/n): ")

    if answer.lower() == 'y':
        print("\nProgram completed")
        break
    elif answer.lower() == 'n':
        print("\nLet's continue!")
    else:
        print("\nInvalid input. Please enter 'y' or 'n'.")
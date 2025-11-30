from pandas import read_excel
from datetime import datetime
import re
import sys
import glob

class Charge:
    def __init__(self, chargeDate, price):
        self.chargeDate = chargeDate
        self.price = price


if len(sys.argv) != 3:
    print("Invalid arguments supplied.")
else:

    fromDate = datetime.strptime(sys.argv[1], "%m/%d/%Y")
    toDate = datetime.strptime(sys.argv[2], "%m/%d/%Y")

    print()
    print("Calculating charges from {0}/{1}/{2} to {3}/{4}/{5}".format(fromDate.month, fromDate.day, fromDate.year, toDate.month, toDate.day, toDate.year))
    print("---")

    fileNames = glob.glob("*.xlsx")
    print()
    print("Read {0} files".format(len(fileNames)))
    print("---")
    for file in fileNames:
        print(file)

    print()
    chargeList = []

    for file in fileNames:

        df = read_excel(file, "BMW Charging")

        pricePattern = "[0-9]+.[0-9]+"
        for index, row in df.iterrows():
            if "USD" in str(row.iloc[8]):
                chargeDate = datetime.strptime(row.iloc[0], "%m/%d/%Y %H:%M %p")
                amount = 0
                amounts = re.findall(pricePattern, row.iloc[8])
                if len(amounts) > 0:
                    amount = float(amounts[0])
                    chargeList.append(Charge(chargeDate, amount))

    # Sort based on Dates
    chargeList.sort(key = lambda x: x.chargeDate)

    print("Charge Date \t Price(USD)")
    print("----------------------------")
    total = 0.0
    for charge in chargeList:
        if fromDate <= charge.chargeDate <= toDate:
            print("{0}/{1}/{2} \t ${3}".format(charge.chargeDate.month, charge.chargeDate.day, charge.chargeDate.year, charge.price))
            total += charge.price

    print("----------------------------")
    print("Total: \t\t ${:.2f}".format(total))

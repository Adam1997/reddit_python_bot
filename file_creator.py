import os

def writeFile():
    print("Enter file name here (without .txt extension): ")
    filename = input() + ".txt"
    file = open("%s" % (filename),"w+")
    print("Enter how many companies you want to enter: ")
    #need controls here
    num_companies = enterInteger()
    for i in range(0, num_companies):
        print("Enter company name: ")
        file.write(input() + ":" + "\n")
        print("How many search terms do you want to use for this company?")
        num = enterInteger()
        for i in range(0, num):
            print("Enter #%s search term: " % (i + 1))
            file.write("-" + input() + "\n")
    return filename

def enterInteger():
    #function to get integer input
    num = 0
    isInt = False
    while(isInt == False):
        try:
            num = int(input())
            isInt = True
        except ValueError:
            print("You did not enter a valid integer...please try again")
    return num

def getDataFromFile(variable):
    file = open("Data.txt", "r")
    for line in file:
        line1 = line.split(" ")[0]
        line2 = line.split(" ")[1]
        if (line1 == variable):
            return(line2.strip('\n'))
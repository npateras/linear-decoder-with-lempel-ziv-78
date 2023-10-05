import os

def WriteIntoFile(encodedStr):
    file = 'EncodedMessage.txt'
    if not os.path.exists(file):
        open('file', 'w').close()
    f = open(file, 'r+')
    f.truncate(0)
    f = open(file,'w')
    f.write(str(encodedStr).replace("b'", '').replace("'", ''))
    f.close()

def getMessage():
    file = open("Message.txt", "r")
    for line in file:
        return(line.strip('\n'))
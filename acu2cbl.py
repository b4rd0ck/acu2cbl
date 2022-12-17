import binascii
import getopt
import sys
import re

# constants
IDENTIFICATION_DIVISION = 'IDENTIFICATION DIVISION'
START_POSITION_BEGINNING_CODE_MARK = 7
END_POSITION_BEGINNING_CODE_MARK = 9

def printUsage():
    print("\n\nUsage: acu2cbl -o <object cobol> or acu2cbl --object=<object cobol>\n")


def processArguments(argv):
    nameFileObject = 'C:\\Projects\\acu2cbl\\samples\\sample001.acu'
    return nameFileObject
"""
    try:
        options, arguments = getopt.getopt(argv, "o:", ["object="])
    except getopt.GetoptError as error:
        print(error)
        printUsage()
        sys.exit(1)

    for o, a in options:
        if o in ("-o", "--object"):
            nameFileObject = a
        else:
            printUsage()
            sys.exit(2)

    if nameFileObject == "":
        printUsage()
        sys.exit(3)

    return nameFileObject
"""

def findBeginningMarkCodeObject(fileObject):
    objectCodeMark = []

    numberOfByte = 0
    byteObject = fileObject.read(1)
    while byteObject:
        numberOfByte += 1

        if START_POSITION_BEGINNING_CODE_MARK <= numberOfByte and numberOfByte <= END_POSITION_BEGINNING_CODE_MARK:
            objectCodeMark.append(byteObject)
            if objectCodeMark.__len__() == 3:
                return objectCodeMark

        byteObject = fileObject.read(1)

def positionAtBeginningOfCode(fileObject, objectCodeMark):
    

def main():
    objectCodeMark = []
    nameFileObject = processArguments(sys.argv[1:])

    try:
        fileObject = open(nameFileObject, 'rb')
    except IOError:
        print("\nError trying to open file: ", nameFileObject, "\n")
        sys.exit(4)

    objectCodeMark = findBeginningMarkCodeObject(fileObject)


    try:
        fileObject.close()
    except IOError:
        print("\nError trying to close file: ", nameFileObject, "\n")
        sys.exit(5)


if __name__ == "__main__":
    main()
    sys.exit(0)
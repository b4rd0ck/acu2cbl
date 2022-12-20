import binascii
import getopt
import sys
import re

# constants
IDENTIFICATION_DIVISION = 'IDENTIFICATION DIVISION'
START_POSITION_BEGINNING_CODE_MARK = 7
END_POSITION_BEGINNING_CODE_MARK = 9
NUMBER_BYTES_CODE_MARK = 3

def printUsage():
    print("\n\nUsage: acu2cbl -o <object cobol> or acu2cbl --object=<object cobol>\n")

def processArguments(argv):
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

def findBeginningMarkCodeObject(fileObject):
    objectCodeMark = []

    numberOfByte = 0
    byteObject = fileObject.read(1)
    while byteObject:
        numberOfByte += 1

        if START_POSITION_BEGINNING_CODE_MARK <= numberOfByte and numberOfByte <= END_POSITION_BEGINNING_CODE_MARK:
            objectCodeMark.append(byteObject)
            if len(objectCodeMark) == 3:
                return objectCodeMark

        byteObject = fileObject.read(1)

def positionAtBeginningOfCode(fileObject, objectCodeMark):
    bytesCodeBeginning = []

    byteObject = fileObject.read(1)
    while byteObject:
        if len(bytesCodeBeginning) < NUMBER_BYTES_CODE_MARK:
            bytesCodeBeginning.append(byteObject)
        else:
            bytesCodeBeginning[0] = bytesCodeBeginning[1]
            bytesCodeBeginning[1] = bytesCodeBeginning[2]
            bytesCodeBeginning[2] = byteObject
        if bytesCodeBeginning[0] == objectCodeMark[0] and \
           bytesCodeBeginning[1] == objectCodeMark[1] and \
           bytesCodeBeginning[2] == objectCodeMark[2]:
            return True
        byteObject = fileObject.read(1)
    return False

def jumpFillerObjectCode(fileObject):
    countFillerBytes = 1
    while countFillerBytes <= 3:
        fileObject.read(1)
        countFillerBytes += 1

def printLineOfCode(lineOfCode):
    numberOfSpaces = int.from_bytes(lineOfCode[0], 'little')
    for i in range(numberOfSpaces):
        print(' ', end='')
    for character in lineOfCode[1:]:
        print(character.decode(), end='')
    print()

def parseObjectCode(fileObject):
    lineOfCode = []
    startOfLine = True
    bytesNumberOfLine = []
    bytesFiller = []
    lengthOfCode = 0
    numberOfByte = 0

    byteObject = fileObject.read(1)
    while byteObject:
        numberOfByte += 1
        if startOfLine:
            lengthOfCode = int.from_bytes(byteObject, byteorder='little')
            numberOfByte = 0
            startOfLine = False
            byteObject = fileObject.read(1)
            continue
        if len(bytesNumberOfLine) < 3:
            bytesNumberOfLine.append(byteObject)
            byteObject = fileObject.read(1)
            continue
        if len(bytesFiller) < 3:
            bytesFiller.append(byteObject)
            byteObject = fileObject.read(1)
            continue
        if numberOfByte == lengthOfCode:
            printLineOfCode(lineOfCode)
            startOfLine = True
            bytesNumberOfLine = []
            bytesFiller = []
            lineOfCode = []
            byteObject = fileObject.read(1)
            continue

        lineOfCode.append(byteObject)

        byteObject = fileObject.read(1)

def main():
    objectCodeMark = []
    nameFileObject = processArguments(sys.argv[1:])

    try:
        fileObject = open(nameFileObject, 'rb')
    except IOError:
        print("\nError trying to open file: ", nameFileObject, "\n")
        sys.exit(4)

    objectCodeMark = findBeginningMarkCodeObject(fileObject)
    if positionAtBeginningOfCode(fileObject, objectCodeMark):
        jumpFillerObjectCode(fileObject)
        parseObjectCode(fileObject)

    try:
        fileObject.close()
    except IOError:
        print("\nError trying to close file: ", nameFileObject, "\n")
        sys.exit(5)


if __name__ == "__main__":
    main()
    sys.exit(0)
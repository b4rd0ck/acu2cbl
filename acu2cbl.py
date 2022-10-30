import binascii
import getopt
import sys
import re

# constants
IDENTIFICATION_DIVISION = 'IDENTIFICATIONDIVISION'
LINE_BEGIN = '7f'
POS_MARK1_BEGIN_SOURCE = 6
POS_MARK2_BEGIN_SOURCE = 7
POS_MARK3_BEGIN_SOURCE = 8

# global variables
mark1BeginOfCode = 0
mark2BeginOfCode = 0
mark3BeginOfCode = 0

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

def isAlphabetic(ordByte):
    if (ord('A') <= ordByte and ordByte <= ord('Z')) or \
       (ord('a') <= ordByte and ordByte <= ord('z')):
        return True
    else:
        return False

def isLineBegin(byte):
    if byte.hex() == LINE_BEGIN:
        return True
    else:
        return False

def defineBeginingOfCode(fileObject):
    global mark1BeginOfCode
    global mark2BeginOfCode
    global mark3BeginOfCode

    byteIndex = 0
    while (byte := fileObject.read(1)):
        if byteIndex == POS_MARK1_BEGIN_SOURCE:
            mark1BeginOfCode = "{0:02x}".format(ord(byte))
        else:
            if byteIndex == POS_MARK2_BEGIN_SOURCE:
                mark2BeginOfCode = "{0:02x}".format(ord(byte))
            else:
                if byteIndex == POS_MARK3_BEGIN_SOURCE:
                    mark3BeginOfCode = "{0:02x}".format(ord(byte))
                    return
        byteIndex = byteIndex + 1

def positionBeginingOfCode(fileObject):
    byte1 = ''
    byte2 = ''
    byte3 = ''
    while (byte := fileObject.read(1)):
        byteHex = "{0:02x}".format(ord(byte))
        if byte1 == '':
            byte1 = byteHex
        else:
            if byte2 == '':
                byte2 = byteHex
            else:
                if byte3 == '':
                    byte3 = byteHex
                else:
                    byte1 = byte2
                    byte2 = byte3
                    byte3 = byteHex
        if byte1 == mark1BeginOfCode and byte2 == mark2BeginOfCode and byte3 == mark3BeginOfCode:
            return

def printCodeLine(codeLine):
    index = 3
    line = ' ' * codeLine[2]
    while (index <= len(codeLine) - 6):
        line = line + chr(codeLine[index])
        index = index + 1
    print(line)

def parseSourceFromObject(fileObject):
    defineBeginingOfCode(fileObject)
    positionBeginingOfCode(fileObject)

    codeLine = []
    while (byte := fileObject.read(1)):
        if isLineBegin(byte):
            if len(codeLine) > 0:
                printCodeLine(codeLine)
                codeLine = []
        else:
            codeLine.append(ord(byte))

def main():
    nameFileObject = processArguments(sys.argv[1:])

    try:
        fileObject = open(nameFileObject, 'rb')
    except IOError:
        print("\nError trying to open file: ", nameFileObject, "\n")
        sys.exit(4)

    parseSourceFromObject(fileObject)

    try:
        fileObject.close()
    except IOError:
        print("\nError trying to close file: ", nameFileObject, "\n")
        sys.exit(5)


if __name__ == "__main__":
    main()
    sys.exit(0)
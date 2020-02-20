import binascii
import getopt
import sys

# constants
POS_MARK1_BEGIN_SOURCE = 6
POS_MARK2_BEGIN_SOURCE = 7

nameFileObject = ""
fileObject = ""
byteFileObject = ""
nthByte = -1
sourceLine = ""
markBeginSource = ""
hexValueAnt = ""
hexValueAct = ""
flagSource = 0


def printUsage():
    print("\n\nUsage: acu2cbl -o <object cobol> or acu2cbl --object=<object cobol>\n")


def processArguments(argv):
    global nameFileObject

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


def processByte(hexValue):
    global nthByte
    global sourceLine
    global markBeginSource
    global hexValueAnt
    global hexValueAct
    global flagSource

    nthByte += 1

    # identify the beginning of the source
    if nthByte == POS_MARK1_BEGIN_SOURCE or nthByte == POS_MARK2_BEGIN_SOURCE:
        markBeginSource += hexValue
        return

    hexValueAnt = hexValueAct
    hexValueAct = hexValue
    if hexValueAnt == "8d" and hexValueAct == "6e":
        print("aca")
        print(markBeginSource[0:2])
        print(markBeginSource[2:])
    # if the previous and the actual characters match with "markBeginSource" set the
    # flag "flagSource" to 1
    if hexValueAnt == markBeginSource[0:2] and hexValueAct == markBeginSource[2:]:
        flagSource = 1
        return

    # inside the part of the source
    if flagSource == 1:
        intValue = int(hexValue, 16)
        print(chr(intValue))


def main():
    global nameFileObject
    global fileObject
    global byteFileObject
    global nthByte
    global sourceLine
    global hexValueAnt
    global hexValueAct
    global flagSource

    value = ""

    processArguments(sys.argv[1:])

    try:
        fileObject = open(nameFileObject, 'rb')
    except IOError:
        print("\nError trying to open file: ", nameFileObject, "\n")
        sys.exit(4)

    nthByte = -1
    sourceLine = ""
    hexValueAnt = ""
    hexValueAct = ""
    flagSource = 0
    byteFileObject = fileObject.read(1)
    while len(byteFileObject) > 0:
        hexValue = "{0:02x}".format(ord(byteFileObject))
        processByte(hexValue)
        #print(value, "--->", hex(ord(byteFileObject)))
        byteFileObject = fileObject.read(1)

    try:
        fileObject.close()
    except IOError:
        print("\nError trying to close file: ", nameFileObject, "\n")
        sys.exit(5)


if __name__ == "__main__":
    main()
    sys.exit(0)
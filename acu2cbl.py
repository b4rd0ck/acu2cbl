import binascii
import getopt
import sys

# constants
POS_MARK1_BEGIN_SOURCE = 6
POS_MARK2_BEGIN_SOURCE = 7
POS_MARK3_BEGIN_SOURCE = 8
CNT_BYTES_FIRST_INIT_LINE = 3
CNT_BYTES_FIRST_CNT_SPACES = 10

nameFileObject = ""
fileObject = ""
byteFileObject = ""
nthByte = -1
nthByteSource = -1
nthByteTextSource = -1
sourceLine = ""
markBeginSource = ""
hexValueAnt0 = ""
hexValueAnt1 = ""
hexValueAct = ""
flagSource = 0
flagFirstLineSource = 0
markBeginLine = ""
cnt_initial_spaces = 0
lineSource = ""
lengthSource = 0
flagTextSource = 0


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
    global nthByteSource
    global sourceLine
    global markBeginSource
    global hexValueAnt0
    global hexValueAnt1
    global hexValueAct
    global flagSource
    global flagFirstLineSource
    global cnt_initial_spaces
    global markBeginLine
    global lineSource
    global lengthSource
    global flagTextSource
    global nthByteTextSource

    nthByte += 1

    # identify the beginning of the source
    if nthByte == POS_MARK1_BEGIN_SOURCE or nthByte == POS_MARK2_BEGIN_SOURCE or nthByte == POS_MARK3_BEGIN_SOURCE:
        markBeginSource += hexValue
        return

    hexValueAnt0 = hexValueAnt1
    hexValueAnt1 = hexValueAct
    hexValueAct = hexValue
    # if the two previous and the actual characters match with "markBeginSource" set the
    # flag "flagSource" to 1
    if hexValueAnt0 == markBeginSource[0:2] and hexValueAnt1 == markBeginSource[2:4] and hexValueAct == markBeginSource[4:]:
        flagSource = 1
        # initialize position of byte in the source
        nthByteSource = -1
        # indicate that next line is the first of the source
        flagFirstLineSource = 1
        #
        nthByteTextSource = -1
        return

    # check if it inside the the source
    if flagSource == 1:
        nthByteSource += 1
        nthByteTextSource += 1
        # check if actual line is the first of the source
        if flagFirstLineSource == 1:
            #nthByteSource += 1
            # check if position is previous indicator's init first line
            if nthByteSource < CNT_BYTES_FIRST_INIT_LINE:
                return
            # check if position is equal indicator's init first line
            if nthByteSource == CNT_BYTES_FIRST_INIT_LINE:
                markBeginLine = hexValue
                lengthSource = int(hexValue, 16)
                nthByteTextSource = 0
                return
            # check if position is equal indicator's count spaces
            if nthByteSource == CNT_BYTES_FIRST_CNT_SPACES:
                cnt_initial_spaces = int(hexValue, 16)
                flagTextSource = 1
                return

        if nthByteTextSource == lengthSource:
            print(lineSource)
            lineSource = ""
            flagFirstLineSource = 0

        if flagTextSource == 1:
            intValue = int(hexValue, 16)
            lineSource += chr(intValue)


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
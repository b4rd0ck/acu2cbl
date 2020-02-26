# acu2cbl

Script written in python (3.x) that extract the source code of a Acucobol object compiled with debug option.
The idea behind this script is to compare, before production deployment, the object candidate with the object to replace. This way,
the developer can assure that the difference of the objects refer only to the code lines implemented for the requirement solicited.
Is mandatory that the source code has been compiled with the debug option, to recover the names of the paragraphs, variables,
sections and so on.

Belown is shown the usage of the script:

  "python3 acu2cbl -o <object cobol> or --object=<object cobol>"

Actually, the source code resulting is printed to screen, enabling it to a file for later comparison.

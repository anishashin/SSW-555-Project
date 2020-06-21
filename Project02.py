'''
Created on 5/25/20
@author:   Anisha Shin
Pledge:    I pledge my honor that I have abided by the Stevens Honor System.

CS555 - Project 02
'''

INPUT_FILE = 'proj02test.ged'

VALID_TAGS = {'0':('INDI','FAM','HEAD','TRLR','NOTE'),
              '1':('NAME','SEX','BIRT','DEAT','FAMC','FAMS','MARR','HUSB','WIFE','CHIL','DIV'),
              '2':('DATE')}

def readFile(fileName):
    '''Reads in a GEDCOM file and prints input and output lines'''
    try:
        file = open(fileName, 'r')
        for line in file:
            print('-->', line, end='')
            line = line.strip().split()
            level = line[0]
            tag = line[1]
            arguments = ' '.join(line[2:])
            if (tag == 'INDI' or tag == 'FAM') and arguments != 'INDI' and arguments != 'FAM':
                print('<--', level + '|' + tag + '|' + 'N' + '|' + arguments)
            else:
                if arguments == 'INDI' or arguments == 'FAM':
                    temp = arguments
                    arguments = tag
                    tag = temp
                print('<--', level + '|' + tag + '|' + isValid(level,tag) + '|' + arguments)
        file.close()
    except IOError:
        print('Error')

def isValid(level,tag):
    '''Returns the value 'Y' if the tag is one of the supported tags or 'N' otherwise'''
    if level not in VALID_TAGS:
        return 'N'
    elif tag in VALID_TAGS[level]:
        return 'Y'
    else:
        return 'N'

def main():
    readFile(INPUT_FILE)

if __name__ == '__main__': main()

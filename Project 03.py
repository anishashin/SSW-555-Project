from datetime import date
#from prettytable import PrettyTable

INPUT_FILE = 'test_file.ged'
INDI_IDS = {}
FAM_IDS = {}

VALID_TAGS = {'0':('INDI','FAM','HEAD','TRLR','NOTE'),
              '1':('NAME','SEX','BIRT','DEAT','FAMC','FAMS','MARR','HUSB','WIFE','CHIL','DIV'),
              '2':('DATE')}

MONTHS = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}

current_indi_id = ''
current_fam_id = ''

def readFile(fileName):
    '''Reads in a GEDCOM file and prints input and output lines'''
    current_tag = ''
    current_date = ''
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
                    tag, arguments = arguments, tag
                print('<--', level + '|' + tag + '|' + isValid(level,tag) + '|' + arguments)
                if isValid(level,tag) == 'Y':
                    if tag == 'INDI':
                        addIndividual(tag, arguments)
                        current_tag = tag
                    elif tag == 'FAM':
                        addFamily(tag, arguments)
                        current_tag = tag
                    elif tag == 'BIRT' or tag == 'DEAT' or tag == 'MARR' or tag == 'DIV':
                        current_date = tag          
                    elif current_tag == 'INDI':
                        if level == '2':
                            tag = current_date
                        addIndividual(tag, arguments)
                    elif current_tag == 'FAM':
                        if level == '2':
                            tag = current_date
                        addFamily(tag, arguments)
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

def addIndividual(tag, arguments):
    '''Adds a new individual to the dictionary INDI_IDS or adds information about the individual
    if he/she already exists in the dictionary'''
    global current_indi_id
    if tag == 'INDI':
        INDI_IDS[arguments] = ['NA','NA','NA','NA','True','NA','NA','NA']
        current_indi_id = arguments
    elif tag == 'NAME':
        INDI_IDS[current_indi_id][0] = arguments
    elif tag == 'SEX':
        INDI_IDS[current_indi_id][1] = arguments
    elif tag == 'BIRT':
        INDI_IDS[current_indi_id][2] = arguments
        INDI_IDS[current_indi_id][3] = str(calculateAge(arguments))
    elif tag == 'DEAT':
        INDI_IDS[current_indi_id][4] = 'False'
        INDI_IDS[current_indi_id][5] = arguments
    elif tag == 'FAMC':
        if INDI_IDS[current_indi_id][6] == 'NA':
            INDI_IDS[current_indi_id][6] = [arguments]
        else:
            INDI_IDS[current_indi_id][6] += [arguments]
    elif tag == 'FAMS':
        if INDI_IDS[current_indi_id][7] == 'NA':
            INDI_IDS[current_indi_id][7] = [arguments]
        else:
            INDI_IDS[current_indi_id][7] += [arguments]

def addFamily(tag, arguments):
    '''Adds a new family to the dictionary FAM_IDS or adds information about the family
    if it already exists in the dictionary'''
    global current_fam_id
    if tag == 'FAM':
        FAM_IDS[arguments] = ['NA','NA','NA','NA','NA','NA','NA']
        current_fam_id = arguments
    elif tag == 'MARR':
        FAM_IDS[current_fam_id][0] = arguments
    elif tag == 'DIV':
        FAM_IDS[current_fam_id][1] = arguments
    elif tag == 'HUSB':
        FAM_IDS[current_fam_id][2] = arguments
        try:
            FAM_IDS[current_fam_id][3] = INDI_IDS[arguments][0]
        except:
            pass
    elif tag == 'WIFE':
        FAM_IDS[current_fam_id][4] = arguments
        try:
            FAM_IDS[current_fam_id][5] = INDI_IDS[arguments][0]
        except:
            pass
    elif tag == 'CHIL':
        if FAM_IDS[current_fam_id][6] == 'NA':
            FAM_IDS[current_fam_id][6] = [arguments]
        else:
            FAM_IDS[current_fam_id][6] += [arguments]

def calculateAge(birthday):
    '''Returns the age of an individual with birth date 'birthday'''
    birthday = birthday.strip().split()
    day = birthday[0]
    month = birthday[1]
    year = birthday[2]
    birthday = date(int(year), MONTHS[month], int(day))
    today = date.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

def main():
    readFile(INPUT_FILE)
    for indi in sorted(INDI_IDS):
        print(indi + ': ' + str(INDI_IDS[indi]))
    for fam in sorted(FAM_IDS):
        print(fam + ': ' + str(FAM_IDS[fam]))
    #MAKE SURE YOU SORT ALPHABETICALLY
    #indi_table = PrettyTable(['ID','Name','Gender','Birthday','Age','Alive','Death','Child','Spouse'])
    #fam_table = PrettyTable(['ID','Married','Divorced','Husband ID','Husband Name','Wife ID','Wife Name','Children'])
    #print(indi_table)
    #print(fam_table)

if __name__ == '__main__': main()

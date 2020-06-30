from datetime import date
from prettytable import PrettyTable
import operator

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
    Lines = []
    try:
        file = open(fileName, 'r')
        for line in file:
            temp = '-->'+ line
            #print('-->', line, end='')
            line = line.strip().split()
            level = line[0]
            tag = line[1]
            arguments = ' '.join(line[2:])
            if (tag == 'INDI' or tag == 'FAM') and arguments != 'INDI' and arguments != 'FAM':
                temp += '<--'+ level + '|' + tag + '|' + 'N' + '|' + arguments
                x = level + " " + tag + " " + arguments
                #print('<--', level + '|' + tag + '|' + 'N' + '|' + arguments)
                raise Exception('Invalid line: {}'.format(x))
                #print('Invalid line: ' + x)
            else:
                if arguments == 'INDI' or arguments == 'FAM':
                    tag, arguments = arguments, tag
                temp += '<--'+ level + '|' + tag + '|' + isValid(level,tag) + '|' + arguments
                #print('<--', level + '|' + tag + '|' + isValid(level,tag) + '|' + arguments)
                if isValid(level, tag) == 'N':
                    x = level + " " + tag + " " + arguments
                    raise Exception('Invalid line: {}'.format(x))
                    #print('Invalid line: ' + x)
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
            Lines += temp
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
    birthday = convertToDate(birthday)
    today = date.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

def individualsTable():
    '''Printing Individuals Table'''
    indi_table = PrettyTable()
    indi_table.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive','Death', 'Child', 'Spouse']
    for id in sorted(INDI_IDS.keys()):
        indi_table.add_row([id, INDI_IDS[id][0], INDI_IDS[id][1], INDI_IDS[id][2], INDI_IDS[id][3], INDI_IDS[id][4], INDI_IDS[id][5], INDI_IDS[id][6], INDI_IDS[id][7]])
    print('People')
    print(indi_table)

def familiesTable():
    '''Printing Families Table'''
    fam_table = PrettyTable()
    fam_table.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
    for id in sorted(FAM_IDS.keys()):
        fam_table.add_row([id, FAM_IDS[id][0], FAM_IDS[id][1], FAM_IDS[id][2], FAM_IDS[id][3], FAM_IDS[id][4], FAM_IDS[id][5], FAM_IDS[id][6]])
    print('Families')
    print(fam_table)

def convertToDate(date_string):
    '''Converts a string with format DAY MONTH YEAR to a date object'''
    date_components = date_string.strip().split()
    day = date_components[0]
    month = date_components[1]
    year = date_components[2]
    return date(int(year), MONTHS[month], int(day))

def datesWithinLimit(date1, date2, limit, units):
    '''Returns True if date1 and date2 are within the given limit, where date1 and date2 are date objects (date1 <= date2), 
    limit is a number, and units is one of the following strings: {'days', 'months', 'years'}'''
    conversion_factor = {'days': 1, 'months': 30.4, 'years': 365.25}
    return (date2-date1).days / conversion_factor[units] <= limit

def us01DatesBeforeCurrentDate(input_date, id_name, indi_or_fam, date_type):
    '''Returns an error message if a date (birth, marriage, divorce, death) is after the current date'''
    input_date = convertToDate(input_date)
    if input_date > date.today():
        return 'ERROR: ' + indi_or_fam + ': US01: ' + id_name + ': ' + date_type + ' ' + str(input_date) + ' occurs in the future'
    return

def us02BirthBeforeMarriage(marriage, id_name):
    '''Returns an error message if an individual's birth occurs after his/her marriage'''
    error_messages = []
    marriage = convertToDate(marriage)

    husband_id = FAM_IDS[id_name][2]
    husband_birt = INDI_IDS[husband_id][2]
    husband_birt = convertToDate(husband_birt)

    wife_id = FAM_IDS[id_name][4]
    wife_birt = INDI_IDS[wife_id][2]
    wife_birt = convertToDate(wife_birt)

    if husband_birt > marriage:
        error_messages += ['ERROR: FAMILY: US02: ' + id_name + ": Husband's birth date " + str(husband_birt) + ' after marriage date ' + str(marriage)]
    if wife_birt > marriage:
        error_messages += ['ERROR: FAMILY: US02: ' + id_name + ": Wife's birth date " + str(wife_birt) + ' after marriage date ' + str(marriage)]
    return error_messages

def us03BirthBeforeDeath(id_name):
    '''Returns an error message if an individual's birth occurs after his death'''
    birthday = INDI_IDS[id_name][2]
    birth_date = convertToDate(birthday)
    death = INDI_IDS[id_name][5]

    if death != 'NA':
        death_date = convertToDate(death)
        if birth_date > death_date:
            return 'ERROR: INDIVIDUAL: US03: ' + id_name + ': Died ' + str(death_date) + ' before born ' + str(birth_date)
        return

def us04MarriageBeforeDivorce(id_name):
    '''Returns an error message if the marriage of individuals occurs after divorce'''
    marriage = FAM_IDS[id_name][0]
    marriage_date = convertToDate(marriage)
    divorce = FAM_IDS[id_name][1]

    if divorce != 'NA':
        divorce_date = convertToDate(divorce)
        if divorce_date < marriage_date:
            return 'ERROR: FAMILY: US04: ' + id_name + ': Divorced ' + str(divorce_date) + ' before married ' + str(marriage_date)
        return

def us07LessThan150YearsOld(id_name):
    '''Returns an error message if an individual died when he/she was at least 150 years old 
    or if an individual who is currently living is at least 150 years old'''
    error_messages = []
    birthday = convertToDate(INDI_IDS[id_name][2])
    if not datesWithinLimit(birthday, date.today(), 150, 'years'):
        error_messages += ['ERROR: INDIVIDUAL: US07: ' + id_name + ': More than 150 years old - Birth date ' + str(birthday)]
    if INDI_IDS[id_name][5] != 'NA':
        death = convertToDate(INDI_IDS[id_name][5])
        if not datesWithinLimit(birthday, death, 150, 'years'):
            error_messages += ['ERROR: INDIVIDUAL: US07: ' + id_name + ': More than 150 years old at death - Birth ' + str(birthday) + ': Death ' + str(death)]
    return error_messages

def us08BirthBeforeMarriageOfParents(id_name):
    '''Returns an anomaly message if an individual was born before his/her parents' marriage
    or if an individual was born more than 9 months after his/her parents' divorce'''
    error_messages = []
    marriage = convertToDate(FAM_IDS[id_name][0])
    for child_id in FAM_IDS[id_name][6]:
        birthday = convertToDate(INDI_IDS[child_id][2])
        if birthday < marriage:
            error_messages += ['ANOMALY: FAMILY: US08: ' + id_name + ': Child ' + child_id + ' born ' + str(birthday) + ' before marriage on ' + str(marriage)]
    if FAM_IDS[id_name][1] != 'NA':
        divorce = convertToDate(FAM_IDS[id_name][1])
        for child_id in FAM_IDS[id_name][6]:
            birthday = convertToDate(INDI_IDS[child_id][2])
            if not datesWithinLimit(divorce, birthday, 9, 'months'):
                error_messages += ['ANOMALY: FAMILY: US08: ' + id_name + ': Child ' + child_id + ' born ' + str(birthday) + ' after divorce on ' + str(divorce)]
    return error_messages

def main():
    readFile(INPUT_FILE)
    individualsTable()
    familiesTable()

    for id_name in INDI_IDS:
        if INDI_IDS[id_name][2] != 'NA':
            birt = INDI_IDS[id_name][2]
            if us01DatesBeforeCurrentDate(birt, id_name, 'INDIVIDUAL', 'Birthday') != None:
                print(us01DatesBeforeCurrentDate(birt, id_name, 'INDIVIDUAL', 'Birthday'))
            if us03BirthBeforeDeath(id_name) != None:
                print(us03BirthBeforeDeath(id_name))
            if us07LessThan150YearsOld(id_name) != []:
                for error_message in us07LessThan150YearsOld(id_name):
                    print(error_message)

        if INDI_IDS[id_name][5] != 'NA':
            deat = INDI_IDS[id_name][5]
            if us01DatesBeforeCurrentDate(deat, id_name, 'INDIVIDUAL', 'Death') != None:
                print(us01DatesBeforeCurrentDate(deat, id_name, 'INDIVIDUAL', 'Death'))

    for id_name in FAM_IDS:
        if FAM_IDS[id_name][0] != 'NA':
            marr = FAM_IDS[id_name][0]
            if us01DatesBeforeCurrentDate(marr, id_name, 'FAMILY', 'Marriage date') != None:
                print(us01DatesBeforeCurrentDate(marr, id_name, 'FAMILY', 'Marriage date'))
            if us04MarriageBeforeDivorce(id_name) != None:
                print(us04MarriageBeforeDivorce(id_name))
            if us08BirthBeforeMarriageOfParents(id_name) != []:
                for error_message in us08BirthBeforeMarriageOfParents(id_name):
                    print(error_message)
            
            if FAM_IDS[id_name][2] != 'NA' and FAM_IDS[id_name][4] != 'NA':
                if us02BirthBeforeMarriage(marr, id_name) != []:
                    for error_message in us02BirthBeforeMarriage(marr, id_name):
                        print(error_message)

        if FAM_IDS[id_name][1] != 'NA':
            div = FAM_IDS[id_name][1]
            if us01DatesBeforeCurrentDate(div, id_name, 'FAMILY', 'Divorce date') != None:
                print(us01DatesBeforeCurrentDate(div, id_name, 'FAMILY', 'Divorce date'))

if __name__ == '__main__': main()
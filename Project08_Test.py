import unittest
import Project08
from datetime import date
from Project08 import us01DatesBeforeCurrentDate
from Project08 import us02BirthBeforeMarriage
from Project08 import us03BirthBeforeDeath
from Project08 import us04MarriageBeforeDivorce
from Project08 import us07LessThan150YearsOld
from Project08 import us08BirthBeforeMarriageOfParents
from Project08 import us09BirthBeforeDeathOfParents
from Project08 import us10MarriageAfter14
from Project08 import us15FewerThan15Siblings
from Project08 import us16MaleLastNames
from Project08 import us21CorrectGenderForRoles
from Project08 import us22UniqueIDs

class Test(unittest.TestCase):

    def test01(self):
        self.assertEqual(us01DatesBeforeCurrentDate('2 AUG 2021', 'US01_I01', 'INDIVIDUAL', 'Birthday'), 'ERROR: ' + 'INDIVIDUAL' + ': US01: ' + 'US01_I01' + ': ' + 'Birthday' + ' ' + '2021-08-02' + ' occurs in the future')
        self.assertEqual(us01DatesBeforeCurrentDate('22 AUG 2020', 'US01_I08', 'INDIVIDUAL', 'Death'), 'ERROR: ' + 'INDIVIDUAL' + ': US01: ' + 'US01_I08' + ': ' + 'Death' + ' ' + '2020-08-22' + ' occurs in the future')
        self.assertEqual(us01DatesBeforeCurrentDate('27 AUG 2020', 'US01021015_F01', 'FAMILY', 'Divorce date'), 'ERROR: ' + 'FAMILY' + ': US01: ' + 'US01021015_F01' + ': ' + 'Divorce date' + ' ' + '2020-08-27' + ' occurs in the future')
        self.assertEqual(us01DatesBeforeCurrentDate('13 SEP 2022', 'US01021021_F03', 'FAMILY', 'Marriage date'), 'ERROR: ' + 'FAMILY' + ': US01: ' + 'US01021021_F03' + ': ' + 'Marriage date' + ' ' + '2022-09-13' + ' occurs in the future')

    def test02(self):
        self.assertEqual(us02BirthBeforeMarriage('23 MAY 2020', 'US01021015_F01'), ['ERROR: FAMILY: US02: ' + 'US01021015_F01' + ": Husband's birth date " + '2094-03-01' + ' after marriage date ' + '2020-05-23', 'ERROR: FAMILY: US02: ' + 'US01021015_F01' + ": Wife's birth date " + '2021-08-02' + ' after marriage date ' + '2020-05-23'])

    def test03(self):
        self.assertEqual(us03BirthBeforeDeath('US0103_I11'), 'ERROR: INDIVIDUAL: US03: ' + 'US0103_I11' + ': Died ' + '1995-04-26' + ' before born ' + '2035-01-01')

    def test04(self):
        self.assertEqual(us04MarriageBeforeDivorce('US0204081016_F02'), 'ERROR: FAMILY: US04: ' + 'US0204081016_F02' + ': Divorced ' + '1995-11-29' + ' before married ' + '1997-11-29')

    def test07(self):
        self.assertEqual(us07LessThan150YearsOld('US07_I05'), ['ERROR: INDIVIDUAL: US07: US07_I05: More than 150 years old - Birth date 1867-09-23'])
        self.assertEqual(us07LessThan150YearsOld('US07_I10'), ['ERROR: INDIVIDUAL: US07: US07_I10: More than 150 years old - Birth date 1843-01-15', 'ERROR: INDIVIDUAL: US07: US07_I10: More than 150 years old at death - Birth 1843-01-15: Death 2019-06-30'])

    def test08(self):
        self.assertEqual(us08BirthBeforeMarriageOfParents('US0102081021_F03'), ['ANOMALY: FAMILY: US08: US0102081021_F03: Child I09 born 2018-09-14 before marriage on 2022-09-13'])

    def test09(self):
        self.assertEqual(us09BirthBeforeDeathOfParents('US020910_F04'), ['ERROR: FAMILY: US09: US020910_F04: Child I04 born 2020-01-15 more than 9 months after death of father 1995-04-26', 'ERROR: FAMILY: US09: US020910_F04: Child I04 born 2020-01-15 after death of mother 2019-06-30', 'ERROR: FAMILY: US09: US020910_F04: Child I12 born 1996-02-26 more than 9 months after death of father 1995-04-26'])

    def test10(self):
        self.assertEqual(us10MarriageAfter14('US0204081016_F02'), ['ERROR: FAMILY: US10: US0204081016_F02: Wife I04 not married 1997-11-29 at least 14 years after birth 2020-01-15'])
        self.assertEqual(us10MarriageAfter14('US0102081021_F03'), ['ERROR: FAMILY: US10: US0102081021_F03: Husband US0121_I02 not married 2022-09-13 at least 14 years after birth 2094-03-01'])

    def test15(self):
        self.assertEqual(us15FewerThan15Siblings('US01021015_F01'), 'ERROR: FAMILY: US15: US01021015_F01: There are 15 siblings or more in family')
        self.assertEqual(us15FewerThan15Siblings('US0204081016_F02'), None)
        self.assertEqual(us15FewerThan15Siblings('US0102081021_F03'), None)
        self.assertEqual(us15FewerThan15Siblings('US020910_F04'), None)

    def test16(self):
        self.assertEqual(us16MaleLastNames('US01021015_F01'), [])
        self.assertEqual(us16MaleLastNames('US0204081016_F02'), ['ERROR: FAMILY: US16: US0204081016_F02: Child I06 has a different last name than father'])
        self.assertEqual(us16MaleLastNames('US0102081021_F03'), [])
        self.assertEqual(us16MaleLastNames('US020910_F04'), [])

    def test21(self):
        self.assertEqual(us21CorrectGenderForRoles('US0102081021_F03'), ['ERROR: FAMILY: US21: US0102081021_F03: husband US0121_I02 is not male','ERROR: FAMILY: US21: US0102081021_F03: wife US0121_I08 is not female'])

    def test22(self):
        self.assertEqual(us22UniqueIDs('US22_I13-Not Unique 0'), ['ERROR: INDIVIDUAL: US22: US22_I13-Not Unique 0: is not unique: The Not Unique indicates this'])
        self.assertEqual(us22UniqueIDs('US22_I13-Not Unique 1'), ['ERROR: INDIVIDUAL: US22: US22_I13-Not Unique 1: is not unique: The Not Unique indicates this'])
        self.assertEqual(us22UniqueIDs('US021022_F05-Not Unique 0'), ['ERROR: FAMILY: US22: US021022_F05-Not Unique 0: is not unique: The Not Unique indicates this'])

if __name__ == "__main__":
    Project08.main()
    unittest.main()
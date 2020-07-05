import unittest
import Project06
from datetime import date
from Project06 import us01DatesBeforeCurrentDate
from Project06 import us02BirthBeforeMarriage
from Project06 import us03BirthBeforeDeath
from Project06 import us04MarriageBeforeDivorce
from Project06 import us07LessThan150YearsOld
from Project06 import us08BirthBeforeMarriageOfParents
from Project06 import us09BirthBeforeDeathOfParents
from Project06 import us10MarriageAfter14

class Test(unittest.TestCase):

    def test01(self):
        self.assertEqual(us01DatesBeforeCurrentDate('2 AUG 2021', 'US01_I01', 'INDIVIDUAL', 'Birthday'), 'ERROR: ' + 'INDIVIDUAL' + ': US01: ' + 'US01_I01' + ': ' + 'Birthday' + ' ' + '2021-08-02' + ' occurs in the future')
        self.assertEqual(us01DatesBeforeCurrentDate('22 AUG 2020', 'US01_I08', 'INDIVIDUAL', 'Death'), 'ERROR: ' + 'INDIVIDUAL' + ': US01: ' + 'US01_I08' + ': ' + 'Death' + ' ' + '2020-08-22' + ' occurs in the future')
        self.assertEqual(us01DatesBeforeCurrentDate('27 AUG 2020', 'US010210_F01', 'FAMILY', 'Divorce date'), 'ERROR: ' + 'FAMILY' + ': US01: ' + 'US010210_F01' + ': ' + 'Divorce date' + ' ' + '2020-08-27' + ' occurs in the future')
        self.assertEqual(us01DatesBeforeCurrentDate('13 SEP 2022', 'US010210_F03', 'FAMILY', 'Marriage date'), 'ERROR: ' + 'FAMILY' + ': US01: ' + 'US010210_F03' + ': ' + 'Marriage date' + ' ' + '2022-09-13' + ' occurs in the future')

    def test02(self):
        self.assertEqual(us02BirthBeforeMarriage('23 MAY 2020', 'US010210_F01'), ['ERROR: FAMILY: US02: ' + 'US010210_F01' + ": Husband's birth date " + '2094-03-01' + ' after marriage date ' + '2020-05-23', 'ERROR: FAMILY: US02: ' + 'US010210_F01' + ": Wife's birth date " + '2021-08-02' + ' after marriage date ' + '2020-05-23'])

    def test03(self):
        self.assertEqual(us03BirthBeforeDeath('US0103_I11'), 'ERROR: INDIVIDUAL: US03: ' + 'US0103_I11' + ': Died ' + '1995-04-26' + ' before born ' + '2035-01-01')

    def test04(self):
        self.assertEqual(us04MarriageBeforeDivorce('US02040810_F02'), 'ERROR: FAMILY: US04: ' + 'US02040810_F02' + ': Divorced ' + '1995-11-29' + ' before married ' + '1997-11-29')

    def test07(self):
        self.assertEqual(us07LessThan150YearsOld('US07_I05'), ['ERROR: INDIVIDUAL: US07: US07_I05: More than 150 years old - Birth date 1867-09-23'])
        self.assertEqual(us07LessThan150YearsOld('US07_I10'), ['ERROR: INDIVIDUAL: US07: US07_I10: More than 150 years old - Birth date 1843-01-15', 'ERROR: INDIVIDUAL: US07: US07_I10: More than 150 years old at death - Birth 1843-01-15: Death 2019-06-30'])

    def test08(self):
        self.assertEqual(us08BirthBeforeMarriageOfParents('US01020810_F03'), ['ANOMALY: FAMILY: US08: US01020810_F03: Child I09 born 2018-09-14 before marriage on 2022-09-13'])

    def test09(self):
        self.assertEqual(us09BirthBeforeDeathOfParents('US020910_F04'), ['ERROR: FAMILY: US09: US020910_F04: Child I04 born 2020-01-15 more than 9 months after death of father 1995-04-26', 'ERROR: FAMILY: US09: US020910_F04: Child I04 born 2020-01-15 after death of mother 2019-06-30', 'ERROR: FAMILY: US09: US020910_F04: Child I12 born 1996-02-26 more than 9 months after death of father 1995-04-26'])

    def test10(self):
        self.assertEqual(us10MarriageAfter14('US02040810_F02'), ['ERROR: FAMILY: US10: US02040810_F02: Wife I04 not married 1997-11-29 at least 14 years after birth 2020-01-15'])
        self.assertEqual(us10MarriageAfter14('US01020810_F03'), ['ERROR: FAMILY: US10: US01020810_F03: Husband US01_I02 not married 2022-09-13 at least 14 years after birth 2094-03-01'])

if __name__ == "__main__":
    Project06.main()
    unittest.main()
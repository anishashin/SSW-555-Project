import unittest
import Project04
from datetime import date
from Project04 import us01DatesBeforeCurrentDate
from Project04 import us02BirthBeforeMarriage
from Project04 import us03BirthBeforeDeath
from Project04 import us04MarriageBeforeDivorce

class Test(unittest.TestCase):

    def test01(self):
        self.assertEqual(us01DatesBeforeCurrentDate('2 AUG 2021', 'US01_I01', 'INDIVIDUAL', 'Birthday'), 'ERROR: ' + 'INDIVIDUAL' + ': US01: ' + 'US01_I01' + ': ' + 'Birthday' + ' ' + '2021-08-02' + ' occurs in the future')
        self.assertEqual(us01DatesBeforeCurrentDate('22 AUG 2020', 'US01_I08', 'INDIVIDUAL', 'Death'), 'ERROR: ' + 'INDIVIDUAL' + ': US01: ' + 'US01_I08' + ': ' + 'Death' + ' ' + '2020-08-22' + ' occurs in the future')
        self.assertEqual(us01DatesBeforeCurrentDate('27 AUG 2020', 'US01US02_F01', 'FAMILY', 'Divorce date'), 'ERROR: ' + 'FAMILY' + ': US01: ' + 'US01US02_F01' + ': ' + 'Divorce date' + ' ' + '2020-08-27' + ' occurs in the future')
        self.assertEqual(us01DatesBeforeCurrentDate('13 SEP 2022', 'US01US02_F03', 'FAMILY', 'Marriage date'), 'ERROR: ' + 'FAMILY' + ': US01: ' + 'US01US02_F03' + ': ' + 'Marriage date' + ' ' + '2022-09-13' + ' occurs in the future')

    def test02(self):
        self.assertEqual(us02BirthBeforeMarriage('23 MAY 2020', 'US01US02_F01'), ['ERROR: FAMILY: US02: ' + 'US01US02_F01' + ": Husband's birth date " + '2094-03-01' + ' after marriage date ' + '2020-05-23', 'ERROR: FAMILY: US02: ' + 'US01US02_F01' + ": Wife's birth date " + '2021-08-02' + ' after marriage date ' + '2020-05-23'])

    def test03(self):
        self.assertEqual(us03BirthBeforeDeath('US01US03_I11'), 'ERROR: INDIVIDUAL: US03: ' + 'US01US03_I11' + ': Died ' + '1995-04-26' + ' before born ' + '2035-01-01')

    def test04(self):
        self.assertEqual(us04MarriageBeforeDivorce('US04_F02'), 'ERROR: FAMILY: US04: ' + 'US04_F02' + ': Divorced ' + '1995-11-29' + ' before married ' + '1997-11-29')

if __name__ == "__main__":
    Project04.main()
    unittest.main()
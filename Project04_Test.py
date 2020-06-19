import unittest
from datetime import date
from Project04 import us01DatesBeforeCurrentDate
from Project04 import us02BirthBeforeMarriage
from Project04 import us03BirthBeforeDeath
from Project04 import us04MarriageBeforeDivorce

class Test(unittest.TestCase):

    def test01(self):
        self.assertEqual(us01DatesBeforeCurrentDate(input_date, id_name, indi_or_fam, date_type), 'ERROR: ' + indi_or_fam + ': US01: ' + id_name + ': ' + date_type + ' ' + str(input_date) + ' occurs in the future')

    def test02(self):
        self.assertEqual(us02BirthBeforeMarriage(marriage, id_name), ['ERROR: FAMILY: US02: ' + id_name + ": Husband's birth date " + str(husband_birt) + ' after marriage date ' + str(marriage)])
        self.assertEqual(us02BirthBeforeMarriage(marriage, id_name), ['ERROR: FAMILY: US02: ' + id_name + ": Wife's birth date " + str(wife_birt) + ' after marriage date ' + str(marriage)])

    def test03(self):
        self.assertEqual(us03BirthBeforeDeath(id_name), 'ERROR: INDIVIDUAL: US03: ' + id_name + ': Died ' + str(death_date) + ' before born ' + str(birth_date))

    def test04(self):
        self.assertEqual(us04MarriageBeforeDivorce(id_name), 'ERROR: FAMILY: US04: ' + id_name + ': Divorced ' + str(divorce_date) + ' before married ' + str(marriage_date))

    def test05(self):
        self.assertEqual()

    def test06(self):
        self.assertEqual()


if __name__ == "__main__":
    unittest.main()
import unittest
import datetime
from contacts_helper import *

class TestSequenceFunctions(unittest.TestCase):

	def setUp(self):
		pass
		
	def testDateFormat(self):
		curDate, year, month, day = findDateFormat("March 1 2011")
		self.assertEqual(curDate.year, 2011)
		self.assertEqual(curDate.month, 3)
		self.assertEqual(curDate.day, 1)
		self.assertTrue(year)
		self.assertTrue(month)
		self.assertTrue(day)
		 
	def testDateFormat2(self):
		curDate, year, month, day = findDateFormat("3/1/11")
		self.assertEqual(curDate.year, 2011)
		self.assertEqual(curDate.month, 3)
		self.assertEqual(curDate.day, 1)
		self.assertTrue(year)
		self.assertTrue(month)
		self.assertTrue(day)
		 
	def testDateFormat3(self):
		curDate, year, month, day = findDateFormat("3/1")
		self.assertEqual(curDate.month, 3)
		self.assertEqual(curDate.day, 1)
		self.assertFalse(year)
		self.assertTrue(month)
		self.assertTrue(day)
		 
		 
	def testDateFormat4(self):
		curDate, year, month, day = findDateFormat("March")
		self.assertEqual(curDate.month, 3)
		self.assertFalse(year)
		self.assertTrue(month)
		self.assertFalse(day)
	
	def testDateFormatFailure(self):
		curDate, year, month, day = findDateFormat("2001")
		self.assertIsNone(curDate)
		self.assertIsNone(year)
		self.assertIsNone(month)
		self.assertIsNone(day)
		
	def testformatSearchTermsDate(self):
		searchTerms = self.createMockSearchDict()
		searchTerms['birthday'] = "2011-3-1"
		curDate = formatSearchTerms(searchTerms)
		
		self.assertEqual(curDate['b_date'].year, 2011)
		self.assertEqual(curDate['b_date'].month, 3)
		self.assertEqual(curDate['b_date'].day, 1)
		self.assertTrue(curDate['b_year'])
		self.assertTrue(curDate['b_day'])
		self.assertTrue(curDate['b_month'])
	
	def testformatSearchTermsLabels(self):
		searchTerms = self.createMockSearchDict()
		searchTerms['labels'] = "foo, foo,    foo,foo"
		terms = formatSearchTerms(searchTerms)
		
		for word in terms['labels']:
			self.assertEqual(word, "foo")
			
	def testformatSearchTermsPhone(self):
		searchTerms = self.createMockSearchDict()
		searchTerms["phone"] = "(912) 617-6803"
		word = formatSearchTerms(searchTerms)
		
		self.assertEqual(word['phone'], "9126176803")
		
	def testformatSearchTermsEmail(self):
		searchTerms = self.createMockSearchDict()
		searchTerms["email"] = "AaAa@gmail.com"
		word = formatSearchTerms(searchTerms)
		
		self.assertEqual(word['email'], "aaaa@gmail.com")
		
	def test_convertGoogleDateWithYear(self):
		date, yearPresent = convertGoogleDate("2011-3-1")
		self.assertEqual(date.year, 2011)
		self.assertEqual(date.month, 3)
		self.assertEqual(date.day, 1)
		self.assertTrue(yearPresent)
		
	def test_convertGoogleDateWithoutYear(self):
		date, yearPresent = convertGoogleDate("--3-1")
		self.assertEqual(date.month, 3)
		self.assertEqual(date.day, 1)
		self.assertFalse(yearPresent)
		
	def test_matchTextOrNotApplicableSingleWords(self):
		value = Entry(text="abc");
		self.assertTrue(matchTextOrNotApplicable("abc", value))
	
	def test_matchTextOrNotApplicableNoTerm(self):
		value = Entry(text="a");
		self.assertTrue(matchTextOrNotApplicable("", value))
		
	def test_matchTextOrNotApplicableNoText(self):
		value = Entry(text="");
		self.assertFalse(matchTextOrNotApplicable("a", value))
	
	def test_matchTextOrNotApplicableNoMatch(self):
		value = Entry(text="abc");
		self.assertFalse(matchTextOrNotApplicable("bc", value))

	def test_matchTextOrNotApplicableTwoWordEntry(self):
		value = Entry(text="abc bc");
		self.assertTrue(matchTextOrNotApplicable("ab", value))
		
	def test_matchTextOrNotApplicablePartialMatch(self):
		value = Entry(text="abc def");
		self.assertFalse(matchTextOrNotApplicable("bc abc", value))
	
	def test_matchTextOrNotApplicableTwoWords(self):
		value = Entry(text="abc def ghi");
		self.assertTrue(matchTextOrNotApplicable("de abc gh", value))
		
	def test_matchTextOrNotApplicableDoubleWordEntry(self):
		value = Entry(text="abc abc abc");
		self.assertFalse(matchTextOrNotApplicable("de abc gh", value))
		
	def test_matchTextOrNotApplicableDoubleWordTerm(self):
		value = Entry(text="de ABC gh");
		self.assertTrue(matchTextOrNotApplicable("abc abc abc", value))

#def matchOrNotApplicable(term, value):

	def test_matchOrNotApplicableValidMatch(self):
		self.assertTrue(matchOrNotApplicable("abc", "ABC"))
	
	def test_matchOrNotApplicableNoMatch(self):
		self.assertFalse(matchOrNotApplicable("abc", "def"))
	
	def test_matchOrNotApplicableSubstringMatch(self):
		self.assertFalse(matchOrNotApplicable("def", "abcdef"))

#def matchOrgTitleOrNotApplicable(term,value): value.org_title.text

	def test_matchOrgTitleOrNotApplicableMatch(self):
		text = Entry(text="abc");
		org = Entry(org_title=text)
		self.assertTrue(matchOrgTitleOrNotApplicable("abc", org))
		
	
	def test_matchOrgTitleOrNotApplicableSubstringMatch(self):
		text = Entry(text="aaaaaabc");
		org = Entry(org_title=text)
		self.assertTrue(matchOrgTitleOrNotApplicable("abc", org))
	
	
	def test_matchOrgTitleOrNotApplicableNoMatch(self):
		text = Entry(text="abc");
		org = Entry(org_title=text)
		self.assertFalse(matchOrgTitleOrNotApplicable("def", org))
		
	def test_matchOrgTitleOrNotApplicableNoTerm(self):
		text = Entry(text="abc");
		org = Entry(org_title=text)
		self.assertTrue(matchOrgTitleOrNotApplicable("", org))
		
#def matchOrgNameOrNotApplicable(term,value): value.org_name.text

	def test_matchOrgNameOrNotApplicable_Match(self):
		text = Entry(text="abc");
		org = Entry(org_name=text)
		self.assertTrue(matchOrgNameOrNotApplicable("abc", org))
		
	def test_matchOrgNameOrNotApplicable_NoMatch(self):
		text = Entry(text="abc");
		org = Entry(org_name=text)
		self.assertFalse(matchOrgNameOrNotApplicable("def", org))
		
	def test_matchOrgNameOrNotApplicable_NoTerm(self):
		text = Entry(text="abc");
		org = Entry(org_name=text)
		self.assertTrue(matchOrgNameOrNotApplicable("", org))
		
#def matchEmailOrNotApplicable(term,value): email.primary, email.address

	def test_matchEmailOrNotApplicable_Match(self):
		entries = { Entry(address="abc", primary=True) }
		self.assertTrue(matchEmailOrNotApplicable("abc", entries))
		
	def test_matchEmailOrNotApplicable_MatchNonPrimary(self):
		entries = { Entry(address="abc", primary=False) }
		self.assertFalse(matchEmailOrNotApplicable("abc", entries))
		
	def test_matchEmailOrNotApplicable_MatchArray(self):
		entries = { Entry(address="abc", primary=False),  Entry(address="abc", primary=True) }
		self.assertTrue(matchEmailOrNotApplicable("abc", entries))
		
	def test_matchEmailOrNotApplicable_NoTerm(self):
		entries = { Entry(address="abc", primary=False),  Entry(address="abc", primary=True) }
		self.assertTrue(matchEmailOrNotApplicable("", entries))
		
	def test_matchEmailOrNotApplicable_NoMatch(self):
		entries = { Entry(address="abc", primary=True),  Entry(address="def", primary=True) }
		self.assertFalse(matchEmailOrNotApplicable("fi", entries))
		
#def matchPhoneOrNotApplicable(term,value): number.primary number.text

	def test_matchPhoneOrNotApplicable_Match(self):
		entries = { Entry(text="912", primary=True) }
		self.assertTrue(matchPhoneOrNotApplicable("912", entries))
		
	def test_matchPhoneOrNotApplicable_MatchNonPrimary(self):
		entries = { Entry(text="912", primary=False) }
		self.assertFalse(matchPhoneOrNotApplicable("912", entries))
		
	def test_matchPhoneOrNotApplicable_MatchArray(self):
		entries = { Entry(text="912", primary=True), Entry(text="912", primary=False) }
		self.assertTrue(matchPhoneOrNotApplicable("912", entries))
		
	def test_matchPhoneOrNotApplicable_MatchFormatted(self):
		entries = { Entry(text="(912)617-6803", primary=True), Entry(text="912", primary=False) }
		self.assertTrue(matchPhoneOrNotApplicable("9126176803", entries))
		
	def test_matchPhoneOrNotApplicable_NoMatch(self):
		entries = { Entry(text="(912)617-6803", primary=True), Entry(text="912", primary=False) }
		self.assertFalse(matchPhoneOrNotApplicable("9126176804", entries))
		
#def matchLabelsOrNotApplicable(terms,value): for group in value: group.text

	def test_matchLabelsOrNotApplicable_Match(self):
		entries = { Entry(text="abc"), Entry(text="def") }
		self.assertTrue(matchLabelsOrNotApplicable( {"abc"}, entries))
		
	def test_matchLabelsOrNotApplicable_MatchTwo(self):
		entries = { Entry(text="abc"), Entry(text="def"), Entry(text="hig") }
		self.assertTrue(matchLabelsOrNotApplicable( {"def", "abc"}, entries))
		
	def test_matchLabelsOrNotApplicable_MatchPartial(self):
		entries = { Entry(text="abc"), Entry(text="def"), Entry(text="hig") }
		self.assertFalse(matchLabelsOrNotApplicable( {"def", "qwerty"}, entries))
		
	def test_matchLabelsOrNotApplicable_MatchDouble(self):
		entries = { Entry(text="abc")}
		self.assertTrue(matchLabelsOrNotApplicable( {"abc", "abc"}, entries))
		
	def test_matchLabelsOrNotApplicable_NoTerm(self):
		entries = { Entry(text="abc")}
		self.assertTrue(matchLabelsOrNotApplicable("", entries))
		
#def excludeLabelsOrNotApplicable(terms,value):for group in value: group.text

	def test_excludeLabelsOrNotApplicable_Match(self):
		entries = { Entry(text="abc"), Entry(text="def") }
		self.assertFalse(excludeLabelsOrNotApplicable( {"abc"}, entries))
		
	def test_excludeLabelsOrNotApplicable_MatchTwo(self):
		entries = { Entry(text="abc"), Entry(text="def"), Entry(text="hig") }
		self.assertFalse(excludeLabelsOrNotApplicable( {"def", "abc"}, entries))
		
	def test_excludeLabelsOrNotApplicable_MatchPartial(self):
		entries = { Entry(text="abc"), Entry(text="def"), Entry(text="hig") }
		self.assertFalse(excludeLabelsOrNotApplicable( {"def", "qwerty"}, entries))
		
	def test_excludeLabelsOrNotApplicable_MatchNone(self):
		entries = { Entry(text="abc"), Entry(text="jkl")}
		self.assertTrue(excludeLabelsOrNotApplicable( {"def", "qwert"}, entries))
		
	def test_excludeLabelsOrNotApplicable_NoTerm(self):
		entries = { Entry(text="abc"), Entry(text="jkl")}
		self.assertTrue(excludeLabelsOrNotApplicable("", entries))
		
#def matchBirthdayOrNotApplicable(b_date, b_year, b_month, b_day, value): value.when

	def test_matchBirthdayOrNotApplicable_FullMatch(self):
		value = Entry(when="2011-1-30");
		b_date = datetime.date(year=2011, month=1, day=30)
		self.assertTrue(matchBirthdayOrNotApplicable(b_date, True, True, True, value))
		
	def test_matchBirthdayOrNotApplicable_MissingEntryYear(self):
		value = Entry(when="--1-30");
		b_date = datetime.date(year=2011, month=1, day=30)
		self.assertTrue(matchBirthdayOrNotApplicable(b_date, True, True, True, value))
		
	def test_matchBirthdayOrNotApplicable_MissingYearBoth(self):
		value = Entry(when="--1-30");
		b_date = datetime.date(year=2001, month=1, day=30)
		self.assertTrue(matchBirthdayOrNotApplicable(b_date, False, True, True, value))
		
	def test_matchBirthdayOrNotApplicable_MissingTermDay(self):
		value = Entry(when="2011-1-30");
		b_date = datetime.date(year=2001, month=1, day=23)
		self.assertTrue(matchBirthdayOrNotApplicable(b_date, False, True, False, value))
	
	def test_matchBirthdayOrNotApplicable_NoMatch(self):
		value = Entry(when="2011-1-30");
		b_date = datetime.date(year=2001, month=1, day=23)
		self.assertFalse(matchBirthdayOrNotApplicable(b_date, True, True, True, value))
		
	def test_matchBirthdayOrNotApplicable_NoDate(self):
		value = Entry(when="2011-1-30");
		b_date = datetime.date(year=2001, month=1, day=23)
		self.assertTrue(matchBirthdayOrNotApplicable("", True, True, True, value))

#def matchNameRangeOrNotApplicable(rangename,beginswith,endswith,givenname,familyname):

	def test_matchNameRangeOrNotApplicable_MatchFirst(self):
		self.assertTrue(matchNameRangeOrNotApplicable("first","A","Z", "alpha" ,"beta"))
	
	def test_matchNameRangeOrNotApplicable_MatchLast(self):
		self.assertTrue(matchNameRangeOrNotApplicable("first","A","Z", "alpha" ,"zeta"))
	
	def test_matchNameRangeOrNotApplicable_NoMatchFirst(self):
		self.assertFalse(matchNameRangeOrNotApplicable("first","B","Z", "alpha" ,"beta"))
		
	def test_matchNameRangeOrNotApplicable_SmallRange(self):
		self.assertTrue(matchNameRangeOrNotApplicable("first","B","B", "beta" ,"zeta"))

	def test_matchNameRangeOrNotApplicable_NoTerm(self):
		self.assertTrue(matchNameRangeOrNotApplicable("first","","", "beta" ,"zeta"))
	

#helper code

	def createMockSearchDict(self):
		searchTerms = {}
		searchTerms["search"] = ""
		searchTerms["firstname"] = ""
		searchTerms["lastname"] = ""
		searchTerms["job"] = ""
		searchTerms["company"] = ""
		searchTerms["birthday"] = ""
		searchTerms["email"] = ""
		searchTerms["labels"] = ""
		searchTerms["exclude"] = ""
		searchTerms["rangename"] = ""
		searchTerms["beginswith"] = ""
		searchTerms["endswith"] = ""
		searchTerms["phone"] = ""
		return searchTerms
		
class Entry:
    def __init__(self, text = "", org_name = "", org_title = "", primary = "", address = "", when = ""):
        self.text, self.org_name, self.org_title = text, org_name, org_title
        self.primary, self.address, self.when = primary, address, when

if __name__ == '__main__':
	unittest.main()
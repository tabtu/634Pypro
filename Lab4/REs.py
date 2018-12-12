import re

re0 = r'60-6\d{2,2}'
str0='60-63467'
m0 = re.match(re0, str0)
str1='03-60-667'
#m1 = re.match(re0, str1)
m1 = re.search(re0, str1)
fm1 = re.findall(re0, str1)
str2='60-556'
#m2 = re.match(re0, str2)
m2 = re.search(re0, str2)
fm2 = re.findall(re0, str2)
str3='60-6999'
m3 = re.match(re0, str3)

re1 = r'\w+[@]\w+([._]?\w+)*[.][a-zA-Z]{2,3}'
st0= 'ab@cd.ef'
n0 = re.match(re1, st0)
st1= 'ab@cd.ef_gh.ij'
n1 = re.match(re1, st1)
st2= 'ab.cd.ef_gh.i'
#n2 = re.match(re1, st2)
n2 = re.search(re1, st2)
fn2 = re.findall(re1, st2)
st3= '12@34.56.gh_ij'
n3 = re.match(re1, st3)

print(m0)
#print(m0.group())
#print(m0.span())

print(m1.group())
print(m1.span())
print(fm1)

#print(m2.group())
#print(m2.span())
#print(fm2)

print(m3.group())
print(m3.span())

print(n0.group())
print(n0.span())

print(n1.group())
print(n1.span())

#print(n2.group())
#print(n2.span())
#print(fn2)

print(n3.group())
print(n3.span())


# 0-digit phone numbers of the form: (abc)def-ghij. Here a, b, c, …j represent digits [0-9].
# The very first digit cannot be 0 and the string should contain exactly 10 digits and no whitespaces.
# So, your RE should match (519)253-3000 It should not match (019)253-3000 or 519-253-3000 or (519)253-30001 or (519)253-30ab.
str00 = '(519)253-3000', '(019)253-3000','519-253-3000', '(519)253-30001', '(519)253-30ab'
#str00 = input("Please input the string that you want to match: ")
for tmp00 in str00:
    re00 = r'[(][1-9]\d{2}[)]\d{3}[-]\d{4}$'
    mn0 = re.match(re00, tmp00)
    print(mn0)
#r'\w+[@]\w+([._]?\w+)*[.][a-zA-Z]{2,3}'

# Use named groups to extract the area code so that m.group('areacode')=519,
# where m is the match obj returned when re.match() is called with your RE and str=(519)253-3000.
str01 = '(519)253-3000'
re01 = r'^\((?P<areacode>[1-9][0-9]{2,2})\)[0-9]{3,3}[-][0-9]{4,4}$'
mn1 = re.match(re01, str01)
print(mn1.group('areacode'))

# Allow the string to contain an optional extension.
# So in addition to phone numbers of the form given above, your RE should match strings with a valid phone number followed by the letter ‘x’ followed by an extension of 3-5 digits.
# There should be no white spaces between the phone number and the extension.
# So your RE should match (519)253-3000x123 or (519)253-3000x1234 or (519)253-3000x12345; but it should not match (519)253-3000 x 123 or (519)253-3000x123456 or (519)253-3000x12 or (519)253-3000x.
# Extract the extension as well as the area code using named groups.
str02 = '(519)253-3000x123', '(519)253-3000x1234', '(519)253-3000x12345', '(519)253-3000 x 123', '(519)253-3000x123456', '(519)253-3000x12', '(519)253-3000x', '(519)253-3000x1235'
for tmp02 in str02:
    re02 = r'^\((?P<areacode>[1-9][0-9]{2,2})\)[0-9]{3,3}[-][0-9]{4,4}(?P<extcode>[x][0-9]{3,5})?$'
    mn2 = re.match(re02, tmp02)
    print(mn2)
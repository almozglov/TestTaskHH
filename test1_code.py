import re, string

def get_alph_sum(word):
	res = 0
	for i in word:
		letter_pos = string.ascii_uppercase.find(i) + 1
		res += letter_pos
	return res


raw_string = ''
file = open("test1.txt")

for i in file:
	raw_string += i

names_no_quotes= re.sub('"', '', raw_string)
names_no_commas = re.sub(',', ' ', names_no_quotes)
names_split = names_no_commas.split()

sorted_names = sorted(names_split)

result = 0
for i in sorted_names:
	name_pos = sorted_names.index(i)+1
	name_sum = get_alph_sum(i)
	result += name_pos * name_sum

print(result)
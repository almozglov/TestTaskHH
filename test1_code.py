import re, string

# Данный код осуществляет чтение списка имён из файла, его лексическую 
# сортировку, а также считает позицию каждой буквы имени в алфавите
# 
#


def get_alph_sum(word):
	# Функция считает "алфавитную сумму" - сумму порядковых номеров каждой 
	# буквы в слове
	res = 0
	# string.ascii_uppercase - часть модуля string, в которой находятся
	# все заглавные латинские буквы.
	string_uppercase = string.ascii_uppercase
	for i in word:
		letter_pos = string_uppercase.find(i) + 1
		res += letter_pos
	return res


raw_string = ''
file = open("test1.txt")

# По умолчанию python читает файл посимвольно. Цикл ниже считывает файл и 
# записывает всё его содержимое в переменную raw_string

for i in file:
	raw_string += i

names_no_quotes= re.sub('"', '', raw_string)
names_no_commas = re.sub(',', ' ', names_no_quotes)
names_split = names_no_commas.split()


sorted_names = sorted(names_split)
print(sorted_names)
result = 0

# Цикл ниже делает всю работу. Сначала получает позицию имени в списке, 
# затем считает её алфавитную сумму, и затем умножает одно на другое.
# Результат прибавляет к переменной result
for i in sorted_names:
	name_pos = sorted_names.index(i)+1
	name_sum = get_alph_sum(i)
	tmp = name_pos * name_sum
	result += tmp

print(result)
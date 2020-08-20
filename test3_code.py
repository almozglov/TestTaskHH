# В данном задании я решил не пользоваться SQL, и все превращения следать силами python и pandas
# В некоторых местах код выглядит действительно страшно, согласен. Местами он работает медленно,
# да Однако, это цена его понимания. 
# Для работы необходимо наличие библиотек pandas и numpy. 
# almozglov@yandex.com


import pandas as pd 
import numpy as np

# Пути к исходным файлам.
users_path = './tech_quality/users.txt'
lessons_path = './tech_quality/lessons.txt'
participants_path = './tech_quality/participants.txt'
quality_path = './tech_quality/quality.txt'


def read_txt_to_df(path_to_file):
	#Данная функция немного расширяет функционал pandas. Исходная 
	# библиотека не способна корректно читать файлы формата txt. 
	data = pd.read_csv(path_to_file, sep='|')
	# Удаление первой строки 
	data = data.drop([0])
	a = data.shape[0]
	# Удаление последней строки
	data = data.drop([a])
	# Обновление индексов датафрейма
	data.reset_index(drop=True, inplace=True)
	return data

# Чтение всех файлов и создание соответствующих датафреймов
users_df = read_txt_to_df(users_path)
lessons_df = read_txt_to_df(lessons_path)
part_df = read_txt_to_df(participants_path)
quality_df = read_txt_to_df(quality_path)
quality_df.dropna(inplace=True)

#В данной строке осуществляется выборка всех строк из файла users, где 
# в колонке роли указано 'tutor'. Все id учителей записываются в список.
tutor_list = users_df.loc[users_df[users_df.columns[1]]==' tutor']['                  id                  '].to_list()

# Выборка всех уроков по физике в отдельный датафрейм. Обновление индексов и 
# игнорирование незаполненных строк (строк, где не выставлены оценки)
phys_lessons = lessons_df.loc[lessons_df[' subject '] == ' phys    ']['                  id                  '].to_list()
#phys_lessons.reset_index(drop=True, inplace=True)

quality_df.dropna(inplace=True)

#Перевод event_id и tech_quality из строкового формата в int
quality_df[' tech_quality '] = pd.to_numeric(quality_df[' tech_quality '], errors='coerce')
part_df[' event_id '] = pd.to_numeric(part_df[' event_id '], errors='coerce')

# Удаление из списка оценок всех уроков, кроме уроков по физике
for i in range(quality_df.shape[0]):
	lesson_id = quality_df['              lesson_id               '][i]
	if lesson_id not in phys_lessons:
		quality_df.drop([i], inplace=True)

# Данная строка сортирует датафрейм с оценками по id урока, а затем считает
#среднюю оценку для каждого занятия.
#avg_score_array_raw = quality_df.groupby(['              lesson_id               ']).mean()
quality_df.reset_index(drop=True, inplace=True)
avg_score_array_raw = quality_df.sort_values(by=['              lesson_id               '])
avg_score_array_raw.reset_index(drop=True, inplace=True)
avg_score_array_raw = avg_score_array_raw.groupby(['              lesson_id               ']).mean()

tutors_array = []
dates_array = []
# Данный цикл делает финальную работу.
#
for i in range(avg_score_array_raw.shape[0]):
	# Получение индекса i-го элемента (а данном случае в индексе записан id урока) 
	lesson_index = avg_score_array_raw.index.tolist()[i]
	# Сохранение даты урока в массив
	dates_array.append(lessons_df.loc[lessons_df['                  id                  '] == lesson_index]['       scheduled_time       '].to_list()[0][:11])
	#Получение event_id урока, затем поиск по этому id всех пользователей, которые 
	#присутствовали на занятии
	event_id = lessons_df[lessons_df['                  id                  '] == lesson_index][' event_id '].iloc[0]
	users_ids = part_df[part_df[' event_id '] == event_id] 
	#Если количество пользователей на уроке больше 0
	if users_ids.shape[0] > 0:
		# Цикл ниже пробегает по всем присутствующим, и проверяет, есть ли среди них учителя.
		# Если учителей несколько, цикл остановится на первом.
		for t in range(users_ids.shape[0]):
			user_id = users_ids.iloc[t]['               user_id                '] + ' '
			if user_id in tutor_list:
				tutors_array.append(user_id)
				break


avg_score_array_fin = avg_score_array_raw[' tech_quality '].to_list()

data = {'day': dates_array, 'tutor_id': tutors_array, 'avg_score':avg_score_array_fin}
# Ниже создаётся новый датафрейм с тремя колонками: дата урока, id учителя и средняя оценка за урок
res_df = pd.DataFrame(data)
#
res_df.sort_values(by=['day'], ascending=True, inplace=True)
res_df.reset_index(drop=True, inplace = True)
res_df = res_df.loc[res_df.groupby('day')['avg_score'].idxmin()]
res_df.set_index('day', inplace = True)
print(res_df)

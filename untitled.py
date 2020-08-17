import pandas as pd 
import numpy as np

users_path = './tech_quality/users.txt'
lessons_path = './tech_quality/lessons.txt'
participants_path = './tech_quality/participants.txt'
quality_path = './tech_quality/quality.txt'


def read_txt_to_df(path_to_file):
	data = pd.read_csv(path_to_file, sep='|')
	data = data.drop([0])
	a = data.shape[0]
	data = data.drop([a])
	data.reset_index(drop=True, inplace=True)
	return data

users_df = read_txt_to_df(users_path)
lessons_df = read_txt_to_df(lessons_path)
part_df = read_txt_to_df(participants_path)
quality_df = read_txt_to_df(quality_path)
quality_df.dropna(inplace=True)

tutor_list = users_df.loc[users_df[users_df.columns[1]]==' tutor']['                  id                  '].to_list()

phys_lessons = lessons_df.loc[lessons_df[' subject '] == ' phys    ']
phys_lessons.reset_index(drop=True, inplace=True)
quality_df.dropna(inplace=True)

quality_df[' tech_quality '] = pd.to_numeric(quality_df[' tech_quality '], errors='coerce')
part_df[' event_id '] = pd.to_numeric(part_df[' event_id '], errors='coerce')
avg_score_array_raw = quality_df.groupby(['              lesson_id               ']).mean()

tutors_array = []
dates_array = []

for i in range(avg_score_array_raw.shape[0]):
	lesson_index = avg_score_array_raw.index.tolist()[i]
	dates_array.append(lessons_df.loc[lessons_df['                  id                  '] == lesson_index]['       scheduled_time       '].to_list()[0])
	event_id = lessons_df[lessons_df['                  id                  '] == lesson_index][' event_id '].iloc[0]
	users_ids = part_df[part_df[' event_id '] == event_id] 
	if users_ids.shape[0] > 0:
		for t in range(users_ids.shape[0]):
			user_id = users_ids.iloc[t]['               user_id                '] + ' '
			if user_id in tutor_list:
				tutors_array.append(user_id)
				break

avg_score_array_fin = avg_score_array_raw[' tech_quality '].to_list()

data = {'day': dates_array, 'tutor_id': tutors_array, 'avg_score':avg_score_array_fin}
res_df = pd.DataFrame(data)
res_df.set_index('day', inplace = True)
res_df.sort_values(by=['avg_score'], ascending=True, inplace=True)
print(res_df)
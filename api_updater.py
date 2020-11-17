import os
from mongo_config import questions_collection, client

def get_relative_path(*args):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

questions_collection.delete_many({})  # clears all questions in MongoDB

question_objects = []
lines = [line[:-1] for line in open(get_relative_path('trivia.txt'), 'r').readlines()] + ['']
for idx in range(0, len(lines), 6):
    question = lines[idx]
    correct_answer = lines[idx + 1]
    wrong_answers = lines[idx + 2 : idx + 5]
    choices = [correct_answer] + wrong_answers  # not shuffled yet
    question_object = {'question': question, 'correct_answer': correct_answer, 'choices': choices}
    question_objects.append(question_object)

questions_collection.insert_many(question_objects)  # puts all questions from txt file into MongoDB
client.close()

print('Questions updated!')

import json
import random
from http_client import *

url = ("raw.githubusercontent.com","/deepmind/AQuA/master/test.json")

#questions = [json.loads(i) for i in open("test.json").read().splitlines()]
questions = [json.loads(i) for i in https_get(url[0],url[1]).splitlines()]

# random.seed(42)

def get_random_question():
	question_num = random.randint(0,len(questions)-1)
	correct_answer = ord(questions[question_num]["correct"]) - ord("A")
	choices = [0,1,2,3,4]
	choices.remove(correct_answer)
	choices = random.choices(choices,k=2)
	choices.append(correct_answer)
	random.shuffle(choices)
	correct_answer = choices.index(correct_answer)
	answers = [questions[question_num]["options"][i][2:] for i in choices]
	question = questions[question_num]["question"]
	rationale = questions[question_num]["rationale"]
	rationale = rationale[:rationale.rfind('\n')]
	return question, answers, correct_answer, rationale

cache = []
cache_bad = []
def get_question(turn, num):
	assert isinstance(turn,int) and isinstance(num,int), "inputs should be int"
	assert num==0 or num==1 or num==2, "num should be either 0, 1 or 2"
	assert turn>=0, "turn should be >=0"
	ind = turn*3+num
	while ind>=len(cache):
		cache.append(get_random_question())
	while turn>=len(cache_bad):
		cache_bad.append(random.randint(0,2))
	is_bad = cache_bad[turn] == num
	return is_bad, cache[ind]


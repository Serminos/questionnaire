import requests
import pytest
from requests.auth import HTTPBasicAuth

from config import API_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from datetime import date, timedelta
from test_dataset_admin import *

basicAuth = HTTPBasicAuth(ADMIN_PASSWORD, ADMIN_PASSWORD)

survey_packet = {"survey":			
				{
					"title": "Python Developers Survey - 2020",
					"description": "We set out to identify the latest trends and gather insight into what the world of Python development looks like in 2020.",
					"start_date": "2021-07-01",
					"end_date": "2021-09-01"
				}			
		}

class TestQuestions:
	surveyId = None
	questionId = None
	

	def test_create_survey(self):
		survey_packet['survey']['start_date'] = date.today().strftime('%Y-%m-%d')
		survey_packet['survey']['end_date'] = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
		resp = requests.post(API_URL + '/survey/', auth=basicAuth, json=survey_packet)
		assert resp.status_code == 200
		TestQuestions.surveyId = resp.json()['id']

	def test_add_question_with_wrong_id_survey(self):
		resp = requests.post(API_URL + '/survey/%d/questions/'%123456, auth=basicAuth, json=questions_one)
		assert resp.status_code == 404

	def test_add_question_to_survey(self):
		resp = requests.post(API_URL + '/survey/%d/questions/'%TestQuestions.surveyId, auth=basicAuth, json=questions_one)
		assert resp.status_code == 200
		TestQuestions.questionId = resp.json()[0]['id']

	def test_add_questions_all_type_to_survey(self):
		resp = requests.post(API_URL + '/survey/%d/questions/'%TestQuestions.surveyId, auth=basicAuth, json=questions_all_type_questions)
		assert resp.status_code == 200

	def test_add_question_invalid_type(self):
		resp = requests.post(API_URL + '/survey/%d/questions/'%TestQuestions.surveyId, auth=basicAuth, json=questions_type_invalid)
		assert resp.status_code == 400

	def test_add_question_one_answeroptions(self):
		resp = requests.post(API_URL + '/survey/%d/questions/'%TestQuestions.surveyId, auth=basicAuth, json=questions_one_answeroptions)
		assert resp.status_code == 200

	def test_add_question_no_answeroptions(self):
		resp = requests.post(API_URL + '/survey/%d/questions/'%TestQuestions.surveyId, auth=basicAuth, json=questions_no_answeroptions)
		assert resp.status_code == 400
	
	def test_delete_question(self):
		resp = requests.delete(API_URL + '/survey/%d/questions/%d' % (TestQuestions.surveyId, TestQuestions.questionId), auth=basicAuth)
		assert resp.status_code == 204

	def test_delete_question_with_wrong_id_survey(self):
		resp = requests.delete(API_URL + '/survey/%d/questions/%d' % (123456, TestQuestions.questionId), auth=basicAuth)
		assert resp.status_code == 404

	def test_delete_question_with_wrong_id_question(self):
		resp = requests.delete(API_URL + '/survey/%d/questions/%d' % (TestQuestions.surveyId, 123456), auth=basicAuth)
		assert resp.status_code == 404

	def test_patch_question(self):
		resp = requests.post(API_URL + '/survey/%d/questions/'%TestQuestions.surveyId, auth=basicAuth, json=questions_all_type_questions)		
		assert resp.status_code == 200
		old_questions = resp.json()

		# questions_patch_type
		resp = requests.patch(API_URL + '/survey/%d/questions/%d' % (TestQuestions.surveyId, old_questions[0]['id']), auth=basicAuth, json=questions_patch_type)
		assert resp.status_code == 200
		new_question = resp.json()
		assert old_questions[0]['id'] == new_question['id']
		assert old_questions[0]['question_type'] != new_question['question_type']
		assert old_questions[0]['question_text'] == new_question['question_text']
		assert not 'answeroptions' in new_question.items()
		# questions_patch_option
		resp = requests.patch(API_URL + '/survey/%d/questions/%d' % (TestQuestions.surveyId, old_questions[1]['id']), auth=basicAuth, json=questions_patch_option)
		assert resp.status_code == 200
		new_question = resp.json()
		assert old_questions[1]['id'] == new_question['id']
		assert old_questions[1]['question_type'] != new_question['question_type']
		assert old_questions[1]['question_text'] == new_question['question_text']
		assert not 'answeroptions' in new_question.items()
		l1 = old_questions[2]['answeroptions']
		l3 = new_question['answeroptions']
		res = [x for x in l1 + l3 if x not in l1 or x not in l3]
		assert res
		# questions_patch_type_answer
		resp = requests.patch(API_URL + '/survey/%d/questions/%d' % (TestQuestions.surveyId, old_questions[2]['id']), auth=basicAuth, json=questions_patch_type_text_answer)
		assert resp.status_code == 200
		new_question = resp.json()
		assert old_questions[2]['id'] == new_question['id']
		assert old_questions[2]['question_type'] != new_question['question_type']
		assert old_questions[2]['question_text'] != new_question['question_text']
		assert not 'answeroptions' in new_question.items()
		l1 = old_questions[2]['answeroptions']
		l3 = new_question['answeroptions']
		res = [x for x in l1 + l3 if x not in l1 or x not in l3]
		assert res

	def test_delete_survey(self):
		resp = requests.delete(API_URL + '/survey/%d' % TestQuestions.surveyId, auth=basicAuth)
		assert resp.status_code == 204

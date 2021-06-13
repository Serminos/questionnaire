import requests
import requests
import pytest
from requests.auth import HTTPBasicAuth
from datetime import date, timedelta
import json

from config import API_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from test_dataset_user import questions_all_type_questions

basicAuth = HTTPBasicAuth(ADMIN_PASSWORD, ADMIN_PASSWORD)
'''

'''
USER_ID = 33
OTHER_USER_ID = 55
survey_packet = {"survey":			
				{
					"title": "Python Developers Survey - 2021",
					"description": "We set out to identify the latest trends and gather insight into what the world of Python development looks like in 2021.",
					"start_date": "2021-09-01",
					"end_date": "2021-10-01"
				}			
		}

class TestUser:
	surveyId = None
	question_in_survey = None
	
	def test_create_survey(self):
		survey_packet['survey']['start_date'] = date.today().strftime('%Y-%m-%d')
		survey_packet['survey']['end_date'] = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
		resp = requests.post(API_URL + '/survey/', auth=basicAuth, json=survey_packet)
		assert resp.status_code == 200
		TestUser.surveyId = resp.json()['id']

	def test_add_questions_all_type_to_survey(self):
		resp = requests.post(API_URL + '/survey/%d/questions/'%TestUser.surveyId, auth=basicAuth, json=questions_all_type_questions)
		assert resp.status_code == 200
		TestUser.question_in_survey = resp.json()

	def test_available_survey(self):
		resp = requests.get(API_URL)
		assert resp.status_code == 200

	def test_add_submisson(self):
		user_result = {		
					"results": []
					}
		for question in TestUser.question_in_survey:
			if question['question_type'] == 'T':
				answer = 'text answer'
			elif question['question_type'] == 'O':
				answer = [str(question['answeroptions'][0]['id'])]
			elif question['question_type'] == 'M':
				answer = [str(question['answeroptions'][0]['id']), str(question['answeroptions'][1]['id'])]
			user_result['results'].append({str(question['id']):answer})
		resp = requests.post(API_URL+'/results/%s/survey/%s'%(USER_ID,TestUser.surveyId), json=user_result)
		assert resp.status_code == 200
		resp = requests.get(API_URL+'/results/%s/survey/%s'%(USER_ID,TestUser.surveyId), json=user_result)
		assert len(TestUser.question_in_survey) == len(resp.json()[0]['results'])
		for result in resp.json()[0]['results']:
			if result['question_type'] == 'T':
				assert 'text answer' == result['answer_text']
			elif result['question_type'] == 'O':
				assert ['Data analysis'] == result['answer_text']
			elif result['question_type'] == 'M':
				assert ["JavaScript","Bash/Shell"] == result['answer_text']




	def test_add_submisson_repeatedly(self):
		user_result = {		
					"results": []
					}
		for question in TestUser.question_in_survey:
			if question['question_type'] == 'T':
				answer = 'text answer'
			elif question['question_type'] == 'O':
				answer = [str(question['answeroptions'][0]['id'])]
			elif question['question_type'] == 'M':
				answer = [str(question['answeroptions'][0]['id']), str(question['answeroptions'][1]['id'])]
			user_result['results'].append({str(question['id']):answer})
		resp = requests.post(API_URL+'/results/%s/survey/%s'%(USER_ID,TestUser.surveyId), json=user_result)
		assert resp.status_code == 400
		assert 'You have already taken the survey' in resp.text

	def test_add_submisson_with_wrong_data(self):
		user_result = {		
					"results": []
					}
		# wrong text type
		for question in TestUser.question_in_survey:
			if question['question_type'] == 'T':
				answer = ['text answer','text answer']
			elif question['question_type'] == 'O':
				answer = [str(question['answeroptions'][0]['id'])]
			elif question['question_type'] == 'M':
				answer = [str(question['answeroptions'][0]['id']), str(question['answeroptions'][1]['id'])]
			user_result['results'].append({str(question['id']):answer})
		resp = requests.post(API_URL+'/results/%s/survey/%s'%(OTHER_USER_ID,TestUser.surveyId), json=user_result)
		assert resp.status_code == 400
		assert 'has wrong data' in resp.text
		# wrong one choice data
		user_result = {		
					"results": []
					}
		for question in TestUser.question_in_survey:
			if question['question_type'] == 'T':
				answer = 'text answer'
			elif question['question_type'] == 'O':
				answer = [str(question['answeroptions'][0]['id']), str(question['answeroptions'][1]['id'])]
			elif question['question_type'] == 'M':
				answer = [str(question['answeroptions'][0]['id']), str(question['answeroptions'][1]['id'])]
			user_result['results'].append({str(question['id']):answer})
		resp = requests.post(API_URL+'/results/%s/survey/%s'%(OTHER_USER_ID,TestUser.surveyId), json=user_result)
		assert resp.status_code == 400
		assert 'has wrong data' in resp.text
		# wrong one choice data
		user_result = {		
					"results": []
					}
		for question in TestUser.question_in_survey:
			if question['question_type'] == 'T':
				answer = 'text answer'
			elif question['question_type'] == 'O':
				answer = []
			elif question['question_type'] == 'M':
				answer = [str(question['answeroptions'][0]['id']), str(question['answeroptions'][1]['id'])]
			user_result['results'].append({str(question['id']):answer})
		resp = requests.post(API_URL+'/results/%s/survey/%s'%(OTHER_USER_ID,TestUser.surveyId), json=user_result)
		assert resp.status_code == 400
		assert 'meet the specified requirements' in resp.text
		# wrong multy data
		user_result = {		
					"results": []
					}
		for question in TestUser.question_in_survey:
			if question['question_type'] == 'T':
				answer = 'text answer'
			elif question['question_type'] == 'O':
				answer = [str(question['answeroptions'][0]['id'])]
			elif question['question_type'] == 'M':
				answer = [str(question['answeroptions'][0]['id'])]
			user_result['results'].append({str(question['id']):answer})
		resp = requests.post(API_URL+'/results/%s/survey/%s'%(OTHER_USER_ID,TestUser.surveyId),json=user_result)
		assert resp.status_code == 400
		assert 'Requirements many choise' in resp.text

	def test_add_submisson_to_not_startet_survey(self):
		survey_packet['survey']['start_date'] = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
		survey_packet['survey']['end_date'] = (date.today() + timedelta(days=15)).strftime('%Y-%m-%d')
		resp = requests.post(API_URL + '/survey/', auth=basicAuth, json=survey_packet)
		assert resp.status_code == 200		
		TestUser.surveyId = resp.json()['id']

		user_result = {		
					"results": []
					}
		for question in TestUser.question_in_survey:
			if question['question_type'] == 'T':
				answer = 'text answer'
			elif question['question_type'] == 'O':
				answer = [str(question['answeroptions'][0]['id'])]
			elif question['question_type'] == 'M':
				answer = [str(question['answeroptions'][0]['id']), str(question['answeroptions'][1]['id'])]
			user_result['results'].append({str(question['id']):answer})
		resp = requests.post(API_URL+'/results/%s/survey/%s'%(USER_ID,TestUser.surveyId), json=user_result)
		assert resp.status_code == 400
		assert 'Survey not startet' in resp.text
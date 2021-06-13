import requests
from requests.auth import HTTPBasicAuth
from config import API_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from test_dataset_admin import *
from datetime import date, timedelta

basicAuth = HTTPBasicAuth(ADMIN_PASSWORD, ADMIN_PASSWORD)

survey_packet = {"survey":			
				{
					"title": "Python Developers Survey - 2021",
					"description": "We set out to identify the latest trends and gather insight into what the world of Python development looks like in 2020.",
					"start_date": "2021-09-01",
					"end_date": "2021-10-01"
				}			
		}

class TestSurvey:
	surveyId = None

	def test_no_auth(self):
		resp = requests.get(API_URL + '/survey/')
		assert resp.status_code == 401

	def test_auth(self):
		resp = requests.get(API_URL + '/survey/', auth=basicAuth)
		assert resp.status_code == 200
		assert type(resp.json()) is list

	def test_create_survey(self):
		survey_packet['survey']['start_date'] = date.today().strftime('%Y-%m-%d')
		survey_packet['survey']['end_date'] = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
		resp = requests.post(API_URL + '/survey/', auth=basicAuth, json=survey_packet)
		assert resp.status_code == 200
		TestSurvey.surveyId = resp.json()['id']
	
	def test_create_survey_with_invalid_start_date(self):
		survey_packet['survey']['start_date'] = (date.today() - timedelta(days=10)).strftime('%Y-%m-%d')
		survey_packet['survey']['end_date'] = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')	
		resp = requests.post(API_URL + '/survey/', auth=basicAuth, json=survey_packet)
		assert resp.status_code == 400

	def test_create_survey_with_invalid_end_date(self):
		survey_packet['survey']['start_date'] = date.today().strftime('%Y-%m-%d')
		survey_packet['survey']['end_date'] = (date.today() - timedelta(days=10)).strftime('%Y-%m-%d')
		resp = requests.post(API_URL + '/survey/', auth=basicAuth, json=survey_packet)
		assert resp.status_code == 400

	def test_create_survey_with_invalid_start_and_end_date(self):
		survey_packet['survey']['start_date'] = (date.today() - timedelta(days=10)).strftime('%Y-%m-%d')
		survey_packet['survey']['end_date'] = (date.today() - timedelta(days=10)).strftime('%Y-%m-%d')
		resp = requests.post(API_URL + '/survey/', auth=basicAuth, json=survey_packet)
		assert resp.status_code == 400

	def get_first_survey(self):
		resp = requests.get(API_URL + '/survey/', auth=basicAuth)
		assert resp.status_code == 200
		assert type(resp.json()[0]['id']) == str

	def test_get_survey_by_id(self):
		resp = requests.get(API_URL + '/survey/%d' % TestSurvey.surveyId, auth=basicAuth)
		assert resp.status_code == 200
		assert resp.json()['id'] == TestSurvey.surveyId

	def test_get_survey_by_invalid_id(self):
		resp = requests.get(API_URL + '/survey/%d' % 123456, auth=basicAuth)
		assert resp.status_code == 400

	def test_patch_survey(self):
		survey_packet['survey']['start_date'] = date.today().strftime('%Y-%m-%d')
		survey_packet['survey']['end_date'] = date.today().strftime('%Y-%m-%d')
		survey_packet['survey']['title'] = "Python Developers Survey - 2022"
		survey_packet['survey']['description'] = "We set out to identify the latest trends and gather insight into what the world of Python development looks like in 2022."
		resp = requests.get(API_URL + '/survey/%d' % TestSurvey.surveyId, auth=basicAuth)
		assert resp.status_code == 200
		oldSurvey = resp.json()
		resp = requests.patch(API_URL + '/survey/%d' % TestSurvey.surveyId, auth=basicAuth, json=survey_packet)
		assert resp.status_code == 200
		newSurvey = resp.json()
		assert oldSurvey['id'] == newSurvey['id']
		assert oldSurvey['title'] != newSurvey['title']
		assert oldSurvey['description'] != newSurvey['description']
		assert oldSurvey['start_date'] == newSurvey['start_date']
		assert oldSurvey['end_date'] != newSurvey['end_date']

	def test_delete_survey_by_invalid_id(self):
		resp = requests.delete(API_URL + '/survey/%d' % 123456, auth=basicAuth, json=survey_packet)		
		assert resp.status_code == 404

	def test_delete_survey(self):
		resp = requests.delete(API_URL + '/survey/%d' % TestSurvey.surveyId, auth=basicAuth)
		assert resp.status_code == 204


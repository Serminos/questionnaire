from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from datetime import date
from ..models import Survey, Question, Answer, Submission, Results
from ..serializers import SurveySerializer, SubmissionSerializer, ResultsSerializer, QuestionSerializer, AnswerSerializer
import json
# Create your views here.

class UserViewSurvey(APIView):
	def get(self, request,s_id=None):		
		if s_id:
			today = date.today()
			surveys = Survey.objects.filter(start_date__lte=today, end_date__gt=today, id=s_id).first()
			surveys_serilaizer = SurveySerializer(surveys)
			questions_serilaizer = QuestionSerializer(surveys.question, many=True)
			result = {}
			result['survey'] = surveys_serilaizer.data
			result['questioninsurveys'] = questions_serilaizer.data
			for i,record in enumerate(questions_serilaizer.data):
				answers = Answer.objects.filter(question=record['id'])		
				result['questioninsurveys'][i]['answeroptions'] = AnswerSerializer(answers, many=True).data
			return Response(result)
		else:
			today = date.today()
			surveys = Survey.objects.filter(start_date__lte=today,end_date__gt=today) 
			serializer = SurveySerializer(surveys, many=True)
			return Response(serializer.data)
		


class UserResults(APIView):
	def get(self, request, u_id, s_id=None):
		try:
			if s_id:
				submission = Submission.objects.filter(user_id=u_id,survey=s_id)
			else:
				submission = Submission.objects.filter(user_id=u_id)
			resp_data = []
			for i,submis in enumerate(submission):
				answers = []
				data = {}
				data['results'] = []
				for answer in submis.result.all():
					answer_text = answer.answer_text
					answer_text = json.loads(answer_text)
					if answer.question_type == 'T':
						answer_text = answer_text[0]
					data['results'].append({'question_type':answer.question_type,'question_text':answer.question_text,'answer_text':answer_text})
				resp_data.append({'id_survey':submis.survey.id,'user_id':submis.user_id,'results':data['results']})
			return Response(resp_data)
		except Exception as ex:
			raise ParseError(ex)

	def post(self, request, u_id, s_id):
		try:
			surveys = Survey.objects.get(pk=s_id)
			today = date.today()
			if surveys.start_date > today:				
				raise Exception('Survey not startet')
			if surveys.end_date < today:
				raise Exception('Survey ended')
			if Submission.objects.filter(user_id=u_id,survey=s_id).first():
				raise Exception('You have already taken the survey')		
			if not 'results' in request.data:
				raise Exception("Attribute 'results' is missing")
			if type(request.data['results']) != list:
				raise Exception("Attribute 'results' is wrong format")
			results = request.data['results']
			list_results = []
			if len(surveys.question.all()) != len(results):
				raise Exception("Not all questions are listed, attribute 'results' has wrong data.")
			for question in surveys.question.all():
				# для всех вопросов из опроса сопоставим c указанным с результатом, получим теск ответов по индексу ответов
				answer_text = ''
				for result in results:
					answers = []
					if str(question.id) in result:
						if str(question.question_type) in ['O','M']:							
							if type(result[str(question.id)]) != list:
								raise Exception("For question with ID '%s' , attribute 'question_type' has wrong data."%question.id)
							for i in question.answer.all():								
								if str(i.id) in result[str(question.id)]:
									answers.append(str(i.text))
						elif question.question_type == 'T':
							if type(result[str(question.id)]) != str:
								raise Exception("For question with ID '%s' , attribute 'question_type' has wrong data."%question.id)
							answers.append(result[str(question.id)])
						else:
							raise Exception("For question with ID '%s' , attribute 'question_type' has wrong data."%question.id)
						
						if len(answers)==0:
							raise Exception("For question with ID '%s' and the specified answers, do not meet the specified requirements."%question.id)						
						if str(question.question_type) == 'O' and len(answers)!=1:
							raise Exception("For question with ID '%s', attribute 'question_type' has wrong data. Requirements many choise"%question.id)
						if str(question.question_type) == 'M' and len(answers)<2:
							raise Exception("For question with ID '%s', attribute 'question_type' has wrong data. Requirements many choise"%question.id)

						list_results.append({'question_type':question.question_type,'question_text':question.question_text,'answer_text':json.dumps(answers)})
			submission = SubmissionSerializer(data = {'user_id':u_id, 'survey':surveys.id})
			if submission.is_valid(raise_exception=True):
				submission.save()
			for ids, val in enumerate(list_results):
				list_results[ids]['submission'] = submission.data['id']

			results = ResultsSerializer(data=list_results, many=True)			
			if results.is_valid(raise_exception=True):
				results.save()
				return Response(results.data)
			return Response(results.errors)

		except Exception as ex:
			raise ParseError(ex)

class UserSurveyResults(APIView):
	"""Методы опросов"""
	def get(self, request, s_id=None):
		try:
			submission = Submission.objects.filter(survey=s_id)
			resp_data = []
			for i,submis in enumerate(submission):
				answers = []
				data = {}
				data['results'] = []
				for answer in submis.result.all():
					answer_text = answer.answer_text
					answer_text = json.loads(answer_text)
					if answer.question_type == 'T':
						answer_text = answer_text[0]
					data['results'].append({'question_type':answer.question_type,'question_text':answer.question_text,'answer_text':answer_text})
				resp_data.append({'id_survey':submis.survey.id,'user_id':submis.user_id,'results':data['results']})
			return Response(resp_data)
		except Exception as ex:
			raise ParseError(ex)

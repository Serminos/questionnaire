from django.shortcuts import render
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAdminUser 
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from datetime import date, datetime
from ..models import Survey, Question, Answer, Submission, Results
from ..serializers import SurveySerializer, QuestionSerializer, AnswerSerializer
# Create your views here.

class AdminSurvey(APIView):

	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAdminUser]

	def get(self, request, s_id=None):
		try:
			if s_id:
				surveys = get_object_or_404(Survey, id=s_id)
				serializer = SurveySerializer(surveys)
			else:
				surveys = Survey.objects.all()
				serializer = SurveySerializer(surveys, many=True)
			return Response(serializer.data)
		except Exception as ex:
			raise ParseError(ex)
		
	def post(self, request):
		try:
			today = date.today()
			req_data = request.data.get('survey')
			start_date = req_data.get('start_date')
			end_date = req_data.get('end_date')			
			try:
				start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
				end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
			except Exception as e:
				raise Exception("Incorrect date format, should be YYYY-MM-DD")
			#end_date = datetime.strptime(end_date, '%Y-%m-%d')
			if start_date>end_date:				
				raise Exception('Attribute date invalid - start_date > end_date')
			if end_date<today:				
				raise Exception('Attribute date invalid - end_date < today')
			if start_date<today:
				raise Exception('Attribute date invalid - start_date < today')
			serializer = SurveySerializer(data=req_data)
			if serializer.is_valid(raise_exception=True):
				survey_saved = serializer.save()
				return Response(serializer.data)
			return Response(serializer.errors)
		except Exception as ex:
			raise ParseError(ex)
	
	def patch(self, request, s_id):		
		survey_saved = get_object_or_404(Survey, id=s_id)
		req_data = request.data.get('survey')
		req_data['id'] = s_id
		req_data.pop('start_date')
		serializer = SurveySerializer(instance=survey_saved, data=req_data, partial=True)
		if serializer.is_valid(raise_exception=True):
			survey_saved = serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)

	def delete(self, request, s_id):
		survey_to_delete = get_object_or_404(Survey, id=s_id)
		survey_to_delete.delete()
		return Response({"message": "Survey with id '{}' has been deleted.".format(s_id)}, status=204)

class AdminQuestionInSurvey(APIView):

	authentication_classes = [BasicAuthentication]
	permission_classes = [IsAdminUser]

	def get(self, request, s_id=None, q_id=None):
		if q_id:
			questions = get_object_or_404(Question, id=q_id)
			serializer = QuestionSerializer(questions)
			result = serializer.data
			answers = Answer.objects.filter(question=q_id)		
			result['answeroptions'] = AnswerSerializer(answers, many=True).data			
		elif s_id:
			#questions = question.objects.filter(survey=s_id)
			questions = get_list_or_404(Question, survey=s_id)
			serializer = QuestionSerializer(questions, many=True)
			result = serializer.data
			for i,record in enumerate(result):
				answers = Answer.objects.filter(question=record['id'])		
				result[i]['answeroptions'] = AnswerSerializer(answers, many=True).data
		return Response(result)

	def post(self, request, s_id=None):
		survey_saved = get_object_or_404(Survey, id=s_id)
		try:
			prepared_questions = []
			question_in_surveys = request.data.get('questioninsurveys')
			for questions in question_in_surveys:
				questions['id'] = None
				questions['survey'] = s_id
				answer_options = questions.get('answeroptions')
				if not questions.get('question_text'):
					raise Exception("Attribute 'question_text' missing")
				if questions.get('question_type') not in ['O','M','T']:
					raise Exception("question '%s' - Attribute 'question_type' invalid"%questions['question_text'])
				if questions['question_type'] in ['O','M']:
					if (type(answer_options)!=list):
						raise Exception("question '%s' - Attribute answer_options invalid - not list"%questions['question_text'])
					if (len(answer_options)<2):
						raise Exception("question '%s' - Attribute answer_options invalid - Need more choice"%questions['question_text'])									
					for i in range(0,len(answer_options)):
						if type(answer_options[i])!=dict or not answer_options[i].get('text'):
							raise Exception("question '%s' - Attribute answer_options invalid"%questions['question_text'])
				questions['answeroptions'] = answer_options
				question_serializer = QuestionSerializer(data=questions)
				if not question_serializer.is_valid():
					raise Exception("question '%s' - Attribute question invalid - Need more choice"%questions['question_text'])

				prepared_questions.append(questions)

			question_serializer = QuestionSerializer(data=prepared_questions, many=True)
			question_serializer.is_valid(raise_exception=True)
			question_saved = question_serializer.save()			
			for ids,questions in enumerate(prepared_questions):
				if questions['question_type'] in ['O','M']:
					answer_options = questions.get('answeroptions')
					index = 0
					for i in range(0,len(answer_options)):
						answer_options[i]['index'] = index
						answer_options[i]['question'] = question_serializer.data[ids]['id']
						index += 1	
					answer_serializer = AnswerSerializer(data=answer_options, many=True)
					if answer_serializer.is_valid(raise_exception=True):
						answer_saved = answer_serializer.save()
			result = question_serializer.data
			for i,record in enumerate(result):
				answers = Answer.objects.filter(question=record['id'])		
				result[i]['answeroptions'] = AnswerSerializer(answers, many=True).data
			return Response(result)
		except Exception as ex:
			raise ParseError(ex)

	def patch(self, request, s_id=None, q_id=None):
		prev_question = get_object_or_404(Question, id=q_id)
		try:
			next_question = request.data.get('questioninsurveys')
			next_question['id'] = q_id
			next_question['survey'] = s_id
			#questions_instance = question.objects.filter(survey=s_id,id=q_id).first()
			answer_options = next_question.get('answeroptions')
			if not next_question.get('question_text'):
				raise Exception("Attribute 'question_text' missing")
			if next_question.get('question_type') not in ['O','M','T']:
				raise Exception("question '%s' - Attribute 'question_type' invalid"%next_question['question_text'])
			if next_question['question_type'] in ['O','M']:
				if (type(answer_options)!=list):
					raise Exception("question '%s' - Attribute answer_options invalid - not list"%next_question['question_text'])
				if (len(answer_options)<2):
					raise Exception("question '%s' - Attribute answer_options invalid - Need more choice"%next_question['question_text'])									
				for i in range(0,len(answer_options)):
					if type(answer_options[i])!=dict or not answer_options[i].get('text'):
						raise Exception("question '%s' - Attribute answer_options invalid"%next_question['question_text'])	
			question_serializer = QuestionSerializer(instance=prev_question, data=next_question, partial=True)
			if question_serializer.is_valid(raise_exception=True):
				question_saved = question_serializer.save()				
			if question_serializer.data['question_type'] in ['O','M']:
				Answer.objects.filter(question=q_id).delete()
				index = 0
				for i in range(0,len(answer_options)):
					answer_options[i]['index'] = index
					answer_options[i]['question'] = question_serializer.data['id']
					index += 1	
				answer_serializer = AnswerSerializer(data=answer_options, many=True)
				if answer_serializer.is_valid(raise_exception=True):
					answer_saved = answer_serializer.save()
			result = question_serializer.data
			answers = Answer.objects.filter(question=result['id'])		
			result['answeroptions'] = AnswerSerializer(answers, many=True).data
			return Response(result)	
		except Exception as ex:
			raise ParseError(ex)

	def delete(self, request, s_id, q_id):
		questions_instance = get_object_or_404(Question, id=q_id)
		try:
			questions_instance.delete()
			return Response({"message": "Question with id '{}'has been deleted.".format(q_id)}, status=204)
		except Exception as ex:
			raise ParseError(ex)
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import Survey, Question, Answer, Submission, Results, QUESTION_CHOICES


class SurveySerializer(serializers.ModelSerializer):
	class Meta:
		model = Survey
		fields = ('id', 'title', 'description','start_date','end_date')

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = ('id', 'survey', 'question_type','question_text')
		#read_only_fields = ('created','updated')

	def update(self, instance, validated_data):
		instance.survey = validated_data.get('survey', instance.survey)
		instance.question_type = validated_data.get('question_type', instance.question_type)
		instance.question_text = validated_data.get('question_text', instance.question_text)
		instance.save()
		return instance

class AnswerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Answer
		fields = ('id', 'question', 'index','text')

class SubmissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Submission
		fields = ('id', 'user_id', 'survey','completion_time')

class ResultsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Results
		fields = ('id', 'submission', 'question_type','question_text', 'answer_text')


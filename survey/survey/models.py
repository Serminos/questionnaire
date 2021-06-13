from django.db import models

# Create your models here.
QUESTION_CHOICES = (
		('O', 'Один вариант ответа'),
		('M', 'Много вариантов ответа'),
		('T', 'Текстовый ответ'),
		)

class Survey(models.Model):
	'''
	Таблица опросов
	'''
	title = models.CharField("Заголовок", max_length=120)
	description = models.TextField("Описание опроса")
	
	end_date = models.DateField("Дата завершения опроса")
	start_date = models.DateField("Дата старта опроса")
	#def __str__(self):
	#	return self.title


class Question(models.Model):
	'''
	Банк вопросов.Таблица вопросы в опросе
	'''	
	survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='question')
	question_type = models.CharField("Тип вопроса", max_length=1, choices=QUESTION_CHOICES)
	question_text = models.TextField("Текст вопроса")
	#def __str__(self):
	#	return self.question_text

class Answer(models.Model):
	'''
	Банк ответов. Варианты ответов на вопросы
	'''
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
	index = models.PositiveIntegerField("ID варианта ответа")
	text = models.CharField("Текст варианат ответа", max_length=120)
	#def __str__(self):
	#	return self.text


class Submission(models.Model):
	'''
	Попытки сдачи опросов
	'''
	user_id = models.IntegerField("ID пользователя", db_index=True)
	survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
	completion_time = models.DateTimeField("Дата завершения", auto_now_add=True)


class Results(models.Model):
	'''
	Ответы на вопросы пользователей для запущенных/пройденных опросов
	'''
	submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='result')
	question_type = models.CharField("Тип вопроса", max_length=1, choices=QUESTION_CHOICES)
	question_text = models.TextField("Текст вопроса")
	answer_text = models.TextField("Ответ пользователя")
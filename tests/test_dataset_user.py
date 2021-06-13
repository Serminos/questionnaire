survey_packet = {"survey":			
				{
					"title": "Python Developers Survey - 2020",
					"description": "We set out to identify the latest trends and gather insight into what the world of Python development looks like in 2020.",
					"start_date": "2021-07-01",
					"end_date": "2021-10-01"
				}			
		}


questions_all_type_questions={"questioninsurveys":
			[		
				{
				"question_type":"O",
				"question_text":"What do you use Python for the most?",
				"answeroptions":
					[
						{"text": "Data analysis"},
						{"text": "Machine Learning"},
						{"text": "Game Development"},
						{"text": "Web Development"},
						{"text": "Computer Vision and Image Processing"}
					]
				},
				{
				"question_type":"M",
				"question_text":"What language do you still use?",
				"answeroptions":
					[
						{"text": "JavaScript"},
						{"text": "Bash/Shell"},
						{"text": "HTML/CSS"},
						{"text": "SQL"},
						{"text": "C/C++"},
						{"text": "Java"}
					]
				},
				{
				"question_type":"T",
				"question_text":"How do you see the future of python?"
				}
			]		
}

submission_user = {
				"id_survey": "182",
				"results":	
				[					
				{"1": "We set out to identify the latest trends and gather insight into what the world of Python development looks like in 2020."},
				{"2": ["1"]},
				{"3": ["2","4"]}
				]
}
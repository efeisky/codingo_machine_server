from django.shortcuts import render
from django.http import JsonResponse
from .models import User,LessonResult,Lesson
import json

from Functions.giveFactor import distrubeFactor
from Functions.orderingQuestion import orderData

#DB fonksiyonları
def get_user_id(username):
    try:
        user = User.objects.filter(username=username).values('id','userEducation').first()
    except User.DoesNotExist:
        user = None
    return user

def get_user_lesson(userID,selectedLesson):
    try:
        lesson = LessonResult.objects.extra(
            tables=['table_lesson'],
            where=['table_lessonresult.lessonID = table_lesson.id',
                   'table_lessonresult.username = %s',
                   'table_lesson.lessonName = %s'
                   ],
            params=[userID,selectedLesson],
            select={
                'lesson_id': 'table_lesson.id',
                'lesson_order' : 'table_lesson.lessonOrder',
                'lesson_class': 'table_lesson.lessonClass',
                'lesson_result': 'table_lessonresult.lessonResult',
            }
        )
    except LessonResult.DoesNotExist:
        lesson = None
    return lesson

def complete_user_data(lessonData):
    complexData = []
    for data in lessonData:
        lesson_id = data['lesson_id']
        questions = LessonResult.objects.extra(
                select={
            'id': 'table_lessonresult.lessonID',
            'content': 'table_question.questionContent',
            'questionLevel': 'table_question.level',
            'A': 'table_question.optionA',
            'B': 'table_question.optionB',
            'C': 'table_question.optionC',
            'D': 'table_question.optionD',
            'questionAnswer': 'table_question.answer',
            'type': 'table_question.questionType'
            },
            tables=['table_question'],
            where=[
                'table_question.lessonID = table_lessonresult.lessonID',
                'table_question.lessonID = %s'
            ],
            params=[lesson_id]
        ).values(
            'id',
            'content',
            'questionLevel',
            'A',
            'B',
            'C',
            'D',
            'questionAnswer',
            'type'
        )
        for eachQuestion in questions:
            complexData.append(eachQuestion)

    return complexData;

def get_random_question(lesson,userClass):
    questionsList = []
    questions = Lesson.objects.extra(
        select={
            'content': 'table_question.questionContent',
            'questionLevel': 'table_question.level',
            'A': 'table_question.optionA',
            'B': 'table_question.optionB',
            'C': 'table_question.optionC',
            'D': 'table_question.optionD',
            'questionAnswer': 'table_question.answer',
            'type': 'table_question.questionType',
            'class' : 'table_lesson.lessonClass'
            },
        tables=['table_question'],
        where=[
                'table_question.lessonID = table_lesson.id',
                'table_lesson.lessonName = %s'
            ],
        params=[
                lesson
            ]
    ).values(
        'id',
        'content',
        'questionLevel',
        'A',
        'B',
        'C',
        'D',
        'questionAnswer',
        'type',
        'class'
    )

    for eachQuestion in questions:
        if eachQuestion['class'] <= userClass and len(questionsList) < 20:
            questionsList.append(eachQuestion)
    return questionsList
#View
def index(request):
    if request.method == 'POST':
        data_body = json.loads(request.body)
        data_username = data_body['username']
        data_lesson = data_body['lesson']

        userID = get_user_id(data_username);
        if userID == None:
            return JsonResponse({
                'status' : 0,
                'error' : 'This user is not registered in the system'
            })
        
        definedID = int(userID['id'])
        definedEducation = int(userID['userEducation'])
        userLesson = get_user_lesson(userID=definedID,selectedLesson=data_lesson)
        
        data = []
        for lesson in userLesson:
            data.append({
                'lessonID' : lesson.lesson_id,
                'lessonOrder' : lesson.lesson_order,
                'lessonResult' : lesson.lesson_result,
                'lessonClass' : lesson.lesson_class
            })
            
        if len(data) == 0:
            randomData = get_random_question(data_lesson,definedEducation)
            return JsonResponse({
                'status' : 0,
                'data' : randomData
            })
        
        distrubedData = distrubeFactor(data=data)
        
        orderedData = orderData(distrubedData)

        completedData = complete_user_data(orderedData)

        return JsonResponse({
            'status' : 1,
            'data' : completedData
        })
    
    return JsonResponse({
        'status' : 0,
        'error': 'Invalid request'
    })


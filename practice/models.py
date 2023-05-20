from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    realName = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    school = models.CharField(max_length=255)
    pictureSrc = models.CharField(max_length=255)
    userScore = models.IntegerField()
    userEducation = models.IntegerField()
    userPython = models.CharField(max_length=255)
    userProvince = models.CharField(max_length=255)
    userMathLesson = models.IntegerField()
    userPyLesson = models.IntegerField()

    class Meta:
        db_table = 'table_user'

class LessonResult(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10)
    lessonID = models.CharField(max_length=2)
    lessonResult = models.TextField()
    lessonDate = models.DateField()
    
    class Meta:
        db_table = 'table_lessonresult'

class Lesson(models.Model):
    id = models.IntegerField(primary_key=True)
    lessonName = models.CharField(max_length=255)
    lessonSubject = models.CharField(max_length=255)
    lessonClass = models.CharField(max_length=255)
    lessonOrder = models.CharField(max_length=255)
    lessonQuestionCount = models.CharField(max_length=255)

    
    class Meta:
        db_table = 'table_lesson'

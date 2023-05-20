import json
import math
def distrubeFactor(data):
    max_question_count = 0
    for plainData in data:
        data_count_values = json.loads(plainData['lessonResult'])
        true_answer_count = data_count_values['trueAnswerCount']
        false_answer_count = data_count_values['falseAnswerCount']
        if true_answer_count + false_answer_count > max_question_count:
            max_question_count = true_answer_count + false_answer_count
    
    xFactor = math.log(math.pi * max_question_count)
    distrubedData = []
    for plainData in data:
        data_count_values = json.loads(plainData['lessonResult'])
        plainData["givedFactor"] = (data_count_values['trueAnswerCount'] / max_question_count) / xFactor
        distrubedData.append({
            'lesson_id' : plainData["lessonID"],
            'lesson_givenFactor' : plainData['givedFactor']
        })
        
    return distrubedData;
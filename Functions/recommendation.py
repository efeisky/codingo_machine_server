from typing import List, Dict

def recommend_range(values: List[Dict[int, str]]):
    firstQuestionStatus = values[0]['qS']
    secondQuestionStatus = values[1]['qS']
    thirdQuestionStatus = values[2]['qS']

    firstQuestionID = values[0]['qID']
    secondQuestionID = values[1]['qID']
    thirdQuestionID = values[2]['qID']
    startPoint = 0
    if firstQuestionStatus == 0:
        startPoint -= 2
    elif secondQuestionStatus == 0:
        startPoint -= 1

    if secondQuestionStatus == 1:
        startPoint += .5
    
    if thirdQuestionStatus == 1:
        startPoint += 1
    
    if startPoint < 0:
        xPoint = ((firstQuestionID + secondQuestionID + thirdQuestionID) / 3) / abs(startPoint)
        
        if xPoint < 7.5:
            return {
                'status' : 1,
                'rangeValue' : int(xPoint) - 2
            }
        elif 7.5 < xPoint < 20:
            return {
                'status' : 1,
                'rangeValue' : int(xPoint) - 5
            }
        else:
            return {
                'status' : 1,
                'rangeValue' : int(xPoint)
            }
    else:
        return {
                'status' : 0
            }

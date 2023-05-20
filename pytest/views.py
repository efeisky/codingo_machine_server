from django.http import JsonResponse

import json
from Functions.recommendation import recommend_range

def index(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        result = data.get('result')


        responses = recommend_range([
            {
                'qS': result[0]['QuestionStatus'],
                'qID': result[0]['QuestionID']
            },
            {
                'qS': result[1]['QuestionStatus'],
                'qID': result[1]['QuestionID']
            },
            {
                'qS': result[2]['QuestionStatus'],
                'qID': result[2]['QuestionID']
            }
        ])

        response_data = {
            'status': 'failed' if 'status' in responses and responses['status'] == 1 else 'passed',
            'recommended_result': responses['rangeValue'] if 'rangeValue' in responses else ''
        }

        return JsonResponse(response_data)


    return JsonResponse({
        'status' : 0,
        'error': 'Invalid request'
    })

def orderData(data):
    sorted_list = sorted(data, key=lambda x: x['lesson_givenFactor'])
    return sorted_list;
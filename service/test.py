import json
my_dict = [{'class_idx': 350, 'confidence': 0.19552487, 'idx': 0, 'label': '350 volcano - \xe7\x81\xab\xe5\xb1\xb1'}, {'class_idx': 84, 'confidence': 0.19237792, 'idx': 1, 'label': '84 castle - \xe5\x9f\x8e\xe5\xa0\xa1'}, {'class_idx': 306, 'confidence': 0.12936093, 'idx': 2, 'label': '306 sky - \xe5\xa4\xa9\xe7\xa9\xba'}, {'class_idx': 334, 'confidence': 0.080491573, 'idx': 3, 'label': '334 tower - \xe5\xa1\x94\xe6\xa5\xbc'}, {'class_idx': 214, 'confidence': 0.064310804, 'idx': 4, 'label': '214 lighthouse - \xe7\x81\xaf\xe5\xa1\x94'}]

json_str = json.dumps(my_dict)
print(json_str)
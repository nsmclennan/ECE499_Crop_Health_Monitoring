from pprint import pprint

list_of_photos = [   {   'affected_regions': ['leaf', 'shoot'],
        'alternative_explanations': ['dust', 'other fungus'],
        'confidence': 0.92,
        'evidence': [   'White-gray powdery coating visible on multiple leaves',
                        'Patchy, velvety surface growth consistent with mildew',
                        'Several leaves show curling and distortion'],
        'id': 'add3cda4',
        'json_path': '/home/nmclennan/test/photo-analyzer/photo-analyzer/results/add3cda4_result.json',
        'lat': 0,
        'lng': 0,
        'location': {'lat': 0, 'lng': 0},
        'notes': (   'Analysis message: System prompt:\n'
                     'You are an agricultural image inspection assistant.\n'
                     'Analyze tree images for visible signs of powdery '
                     'mildew.\n'
                     'Base your answer only on what is visible in the image.\n'
                     'If evidence is weak or ambiguous, say "uncertain".\n'
                     'Return valid JSON only.\n'
                     '\n'
                     'User prompt:\n'
                     'Task: Check this tree image for powdery mildew.\n'
                     '\n'
                     'Look for visible cues such as:\n'
                     '- White or gray powdery coating on leaves, shoots, or '
                     'fruit\n'
                     '- Patchy surface growth consistent with mildew\n'
                     '- Leaf curling, distortion, or affected clusters if '
                     'visible\n'
                     '\n'
                     'Return this JSON schema:\n'
                     '{\n'
                     '  "powdery_mildew_detected": true|false|null,\n'
                     '  "confidence": 0.0-1.0,\n'
                     '  "severity": "none|low|medium|high|uncertain",\n'
                     '  "evidence": ["short visual observations"],\n'
                     '  "affected_regions": ["leaf", "shoot", "fruit", '
                     '"unknown"],\n'
                     '  "alternative_explanations": ["dust", "lighting glare", '
                     '"other fungus", "none"],\n'
                     '  "recommended_action": "one short sentence"\n'
                     '}\n',
                     'Confidence: 0.92\n'),
        'original_name': 'IMG_5205.PNG',
        'photo_id': 'add3cda4',
        'photo_url': '/uploads/add3cda4_IMG_5205.PNG',
        'powdery_mildew_detected': True,
        'recommended_action': 'Remove heavily affected growth and monitor the '
                              'tree for spread.',
        'severity': 'medium'},{   'affected_regions': ['leaf', 'shoot'],
        'alternative_explanations': ['dust', 'other fungus'],
        'confidence': 0.92,
        'evidence': [   'White-gray powdery coating visible on multiple leaves',
                        'Patchy, velvety surface growth consistent with mildew',
                        'Several leaves show curling and distortion'],
        'id': 'add3cda4',
        'json_path': '/home/nmclennan/test/photo-analyzer/photo-analyzer/results/add3cda4_result.json',
        'lat': 0,
        'lng': 0,
        'location': {'lat': 0, 'lng': 0},
        'notes': (   'Analysis message: System prompt:\n'
                     'You are an agricultural image inspection assistant.\n'
                     'Analyze tree images for visible signs of powdery '
                     'mildew.\n'
                     'Base your answer only on what is visible in the image.\n'
                     'If evidence is weak or ambiguous, say "uncertain".\n'
                     'Return valid JSON only.\n'
                     '\n'
                     'User prompt:\n'
                     'Task: Check this tree image for powdery mildew.\n'
                     '\n'
                     'Look for visible cues such as:\n'
                     '- White or gray powdery coating on leaves, shoots, or '
                     'fruit\n'
                     '- Patchy surface growth consistent with mildew\n'
                     '- Leaf curling, distortion, or affected clusters if '
                     'visible\n'
                     '\n'
                     'Return this JSON schema:\n'
                     '{\n'
                     '  "powdery_mildew_detected": true|false|null,\n'
                     '  "confidence": 0.0-1.0,\n'
                     '  "severity": "none|low|medium|high|uncertain",\n'
                     '  "evidence": ["short visual observations"],\n'
                     '  "affected_regions": ["leaf", "shoot", "fruit", '
                     '"unknown"],\n'
                     '  "alternative_explanations": ["dust", "lighting glare", '
                     '"other fungus", "none"],\n'
                     '  "recommended_action": "one short sentence"\n'
                     '}\n',
                     'Confidence: 0.92\n'),
        'original_name': 'IMG_5205.PNG',
        'photo_id': 'add3cda4',
        'photo_url': '/uploads/add3cda4_IMG_5205.PNG',
        'powdery_mildew_detected': True,
        'recommended_action': 'Remove heavily affected growth and monitor the '
                              'tree for spread.',
        'severity': 'uncertain'},
        {   'affected_regions': ['leaf', 'shoot'],
        'alternative_explanations': ['dust', 'other fungus'],
        'confidence': 0.92,
        'evidence': [   'White-gray powdery coating visible on multiple leaves',
                        'Patchy, velvety surface growth consistent with mildew',
                        'Several leaves show curling and distortion'],
        'id': 'add3cda4',
        'json_path': '/home/nmclennan/test/photo-analyzer/photo-analyzer/results/add3cda4_result.json',
        'lat': 0,
        'lng': 0,
        'location': {'lat': 0, 'lng': 0},
        'notes': (   'Analysis message: System prompt:\n'
                     'You are an agricultural image inspection assistant.\n'
                     'Analyze tree images for visible signs of powdery '
                     'mildew.\n'
                     'Base your answer only on what is visible in the image.\n'
                     'If evidence is weak or ambiguous, say "uncertain".\n'
                     'Return valid JSON only.\n'
                     '\n'
                     'User prompt:\n'
                     'Task: Check this tree image for powdery mildew.\n'
                     '\n'
                     'Look for visible cues such as:\n'
                     '- White or gray powdery coating on leaves, shoots, or '
                     'fruit\n'
                     '- Patchy surface growth consistent with mildew\n'
                     '- Leaf curling, distortion, or affected clusters if '
                     'visible\n'
                     '\n'
                     'Return this JSON schema:\n'
                     '{\n'
                     '  "powdery_mildew_detected": true|false|null,\n'
                     '  "confidence": 0.0-1.0,\n'
                     '  "severity": "none|low|medium|high|uncertain",\n'
                     '  "evidence": ["short visual observations"],\n'
                     '  "affected_regions": ["leaf", "shoot", "fruit", '
                     '"unknown"],\n'
                     '  "alternative_explanations": ["dust", "lighting glare", '
                     '"other fungus", "none"],\n'
                     '  "recommended_action": "one short sentence"\n'
                     '}\n',
                     'Confidence: 0.92\n'),
        'original_name': 'IMG_5205.PNG',
        'photo_id': 'add3cda4',
        'photo_url': '/uploads/add3cda4_IMG_5205.PNG',
        'powdery_mildew_detected': True,
        'recommended_action': 'Remove heavily affected growth and monitor the '
                              'tree for spread.',
        'severity': 'uncertain'}]

VALID_SEVERITY_LEVELS = ['low', 'medium', 'high', 'critical', 'uncertain']

def count_param(statistics_dict: dict, photo_dict: dict, param: str) -> None:
    if param not in statistics_dict:
        statistics_dict[param] = {}
    param_value = photo_dict.get(param)

    if param_value:
        if param_value not in statistics_dict[param]:
            statistics_dict[param][param_value] = {}
            statistics_dict[param][param_value]['count'] = 0
        statistics_dict[param][param_value]['count'] += 1

def pull_statistics(list_of_photos: list[dict]) -> dict:
    """ Obtain statistics based on image."""
    statistics_dict = {}

    
    for photo_data in list_of_photos:
            count_param(statistics_dict, photo_data, "severity")

    
    for severity_level in VALID_SEVERITY_LEVELS:
        if severity_level not in statistics_dict['severity']:
            statistics_dict['severity'][severity_level] = {}
            statistics_dict['severity'][severity_level]['count'] = 0
        total_items = len(list_of_photos)
        statistics_dict['severity'][severity_level]['percent'] = round((statistics_dict['severity'][severity_level]['count']/ total_items) * 100, 1)

    return statistics_dict

statistics_dict = pull_statistics(list_of_photos)

pprint(statistics_dict, indent=4)
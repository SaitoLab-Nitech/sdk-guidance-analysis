import time
start = time.time()

import csv
import json
from glob import glob
from pprint import pprint

from map_data_types_to_taint_sources_for_ner_eval import map_taint_source_to_data_types
from answers_for_ner_eval import answers_for_ner_eval

from sentiment_analyzer import SentimentAnalyzer

from helper import get_sdk_name

sentiment_analyzer = SentimentAnalyzer('siebert/sentiment-roberta-large-english')

# Scenario 1
# guidance_result_path_base = 'extracted_data_for_scenario_1/'
# output_dir = 'results_scenario_1/'
# Scenario 2
guidance_result_path_base = 'extracted_data_for_scenario_2/'
output_dir = 'results_scenario_2/'

count_data_pattern_usage = {}

def count_data_pattern(data_type, guidance_id):
    if (data_type not in count_data_pattern_usage.keys()): count_data_pattern_usage[data_type] = set()
    count_data_pattern_usage[data_type].add(guidance_id)

def get_practices(data_types, guidance_results, guidance_id):
    practices = []
    for item in guidance_results:
        data_enumerated_in_guidance = item['DAT']

        for data_type in data_types:
            if (data_enumerated_in_guidance.lower().find(data_type.lower()) > -1):
                practices.append({ 'PRA': item['PRA'], 'CON': item['CON'] })
                count_data_pattern(data_type, guidance_id)
                break
    return practices

def detect_inconsistencies_based_on_practice_info(practice, data_types, guidance_id):
    if (practice['CON'] != ''):
        sa_result, used_text = sentiment_analyzer.analyze(practice['CON'])
        if (sa_result[0]['label'] == 'POSITIVE'):
            for data_type in data_types:
                if (practice['CON'].lower().find(data_type.lower()) > -1):
                    count_data_pattern(data_type, guidance_id)
                    return sa_result, used_text, 'Consistent'
            return sa_result, used_text, 'Inconsistent'
    if (practice['PRA'] != ''):
        sa_result, used_text = sentiment_analyzer.analyze(practice['PRA'])
        if (sa_result[0]['label'] == 'POSITIVE'):
            return sa_result, used_text, 'Consistent'
        else:
            return sa_result, used_text, 'Inconsistent'
    else:
        return None, None, 'Consistent'

def detect_for_sdk(guidance_id):
    output_data = f'{guidance_id = }\n'
    # guidance_id = map_sdks_to_guidance_ids[sdk]

    guidance_result_path = f'{guidance_result_path_base}{guidance_id}.csv'
    guidance_results = []
    with open(guidance_result_path, 'r') as f:
        for row in csv.reader(f):
            if (row[1] == 'DAT'):
                assert row[2] == 'PRA' and row[3] == 'DES' and row[4] == 'CON'
                continue
            guidance_results.append({ 'DAT': row[1], 'PRA': row[2], 'DES': row[3], 'CON': row[4]})
    # print(f'{guidance_results[0] = }')

    taint_sources = set()
    taint_sources.add('ID')
    print(f'Actually-leaking data: {taint_sources}')
    output_data += f'{taint_sources = }\n'

    for i, taint_source in enumerate(taint_sources):
        data_types = map_taint_source_to_data_types(taint_source)
        print(f'{i = }, {taint_source = }, {data_types = }')
        output_data += f'{i = }, {taint_source = }, {data_types = }\n'

        detection_result = 'Inconsistent'

        practices = get_practices(data_types, guidance_results, guidance_id)
        print(f'{practices = }')
        output_data += f'    {practices = }\n'
        if (len(practices) == 0):
            print('Inconsistent')
            output_data += '    Inconsistent\n'

        for practice in practices:
            sa_result, used_text, final_result = detect_inconsistencies_based_on_practice_info(practice, data_types, guidance_id)
            print(f'{sa_result = }')
            print(f'{used_text = }')
            print(f'{final_result = }')
            output_data += f'    {sa_result = }\n'
            output_data += f'    {used_text = }\n'
            output_data += f'    {final_result = }\n'
            if (final_result == 'Consistent'):
                detection_result = 'Consistent'

        ans = answers_for_ner_eval[guidance_id][taint_source]
        print(f'{detection_result = }, {ans = }, {detection_result == ans}')
        output_data += f'[NER_EVAL] {detection_result = }, {ans = }, {detection_result == ans}'

    with open(f'{output_dir}{guidance_id}.txt', 'w') as f:
        f.write(output_data)

counter = 0
for guidance_id in answers_for_ner_eval.keys():
    detect_for_sdk(guidance_id)
    counter += 1
print(f'{counter = }')
print(f'{time.time() - start = }')

print('\n The number of data pattern usage')
for key, val in count_data_pattern_usage.items():
    print(f'{key}: {len(val)}')

print('\nDone!')

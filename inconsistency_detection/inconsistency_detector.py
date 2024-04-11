import time
start = time.time()

import csv
import json
from glob import glob
from pprint import pprint

from map_data_types_to_taint_sources import map_taint_source_to_data_types

from sentiment_analyzer import SentimentAnalyzer

sentiment_analyzer = SentimentAnalyzer('siebert/sentiment-roberta-large-english')

from helper import get_sdk_name
from map_sdks_to_guidance_ids import map_sdk_bases_to_guidance_ids
map_sdks_to_guidance_ids = {}
sdk_result_dirs = ['../sample_app_analysis/results_pixel3_real/',
                   '../sample_app_analysis/results_pixel6_emul/',
                   '../sample_app_analysis/results_pixel6_real/',]
for apk in glob(sdk_result_dirs[0]+'*'):
    apk = apk.split('/')[-1]
    map_sdks_to_guidance_ids[apk] = map_sdk_bases_to_guidance_ids[get_sdk_name(apk)]
guidance_result_path_base = '../guidance_data_extraction/extracted_data_for_inconsistency_detection/'
sdk_result_path_bases = [sdk_result_dirs[0]+'{}/output_oct_07.log',
                         sdk_result_dirs[1]+'{}/output_oct_09.log',
                         sdk_result_dirs[2]+'{}/output_oct_09.log',]
output_dir = 'results/'

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

def detect_for_sdk(sdk):
    output_data = f'{sdk = }\n'
    guidance_id = map_sdks_to_guidance_ids[sdk]

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
    for sdk_result_path_base in sdk_result_path_bases:
        sdk_result_path = sdk_result_path_base.format(sdk)
        result = {}
        with open(sdk_result_path, 'r') as f:
            data = f.read().split('\n')
            result['num_leaks'] = data[0].split(' ')[-1]
            assert data[1] == 'Sources'
            for i, line in enumerate(data):
                if (line == 'Sinks'):
                    result['sinks'] = json.loads(data[i+1])
        # pprint(result)
        # pprint(f'{result["sinks"][0] = }')

        for sink in result['sinks']:
            taint_sources |= set(sink['sources'])
    print(f'Actually-leaking data: {taint_sources}')
    output_data += f'{taint_sources = }\n'

    for i, taint_source in enumerate(taint_sources):
        data_types = map_taint_source_to_data_types(taint_source)
        print(f'{i = }, {taint_source = }, {data_types = }')
        output_data += f'{i = }, {taint_source = }, {data_types = }\n'

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

    with open(output_dir+sdk+'.txt', 'w') as f:
        f.write(output_data)

counter = 0
for sdk in map_sdks_to_guidance_ids.keys():
    detect_for_sdk(sdk)
    counter += 1
print(f'{counter = }')
print(f'{time.time() - start = }')

print('\n The number of data pattern usage')
for key, val in count_data_pattern_usage.items():
    print(f'{key}: {len(val)}')

print('\nDone!')

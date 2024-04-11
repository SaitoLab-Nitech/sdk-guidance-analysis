
mapping = {
    'Device or other IDs': {
        'taint_sources': ['ID'],
        'data_types': [
            'Device or other IDs', # For 4, 6, 34, 40, 47, 48, 49, 50, 51, 52, 54
            'Device or other identifiers', # For 2, 9, 12, 14, 16, 19, 20, 24,
                                           #     25, 31, 41, 42, 53, 55
            'Device and other IDs', # For 5, 45
            'Device and other identifiers', # For 18
            'Device and Account identifiers', # For 7, 8, 11
            'Device identifiers', # For 10, 35, 36, 46, 58
            'Device ID', # For 21, 37, 43, 56, 57
            'Device IDs or other ID', # For 44
            'Custom device key', # For 59
            'other identifiers related to signed - in accounts',  # on the device.',  # For 8
            'Firebase Android App ID', # For 23
            'Crashlytics installation UUID', # For 23
            'Firebase installation ID', # For 23
            'App-instance ID', # For 32
            'Advertising ID', # For 32, 33
            'Android advertising ( ad ) ID', # For 11
            'AAID', # For 5
            'ad id', # For 43
            'User-ID', # For 32
            'Android ID', # For 33
            'installation id', # For 52
            'Custom device key - values', # For 59
            'device - level ID', # For 47
        ],
    },
}

def map_taint_source_to_data_types(taint_source):
    data_types = set()

    for key, val in mapping.items():
        if (taint_source in val['taint_sources']):
            data_types |= set(val['data_types'])

    return data_types

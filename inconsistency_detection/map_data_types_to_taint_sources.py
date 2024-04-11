
mapping = {
    'Device or other IDs': {
        'taint_sources': ['AAID', 'AndroidID', 'UUID', 'IMEI', 'MACAddress'],
        'data_types': [
            'Device or other IDs',
            'Device or other identifiers',
            'Device and other IDs',
            'Device and other identifiers',
            'Device and Account identifiers',
            'Device identifiers',
            'Device ID',
            'Custom device key', # For bugfender (ID=59)
        ],
    },
    'AAID': {
        'taint_sources': ['AAID'],
        'data_types': [
            'Android advertising ( ad ) ID',  # For Taboola (ID=11)
            'Google Advertising ID',  # For Singular (ID=34)
            'AAID',  # For Fyber Fairbid (ID=45)
            'Ad ID', # For Pollfish (ID=42)
        ],
    },
    'AndroidID': {
        'taint_sources': ['AndroidID'],
        'data_types': [
            'Android ID',  # For Flurry (ID=58)
        ],
    },
    'UUID': {
        'taint_sources': ['UUID'],
        'data_types': [
            'Installation ID',  # For Flurry (ID=58), Batch (ID=52), Firebase (ID=23)
            'App - instance ID',  # For Google Analytics (ID=32)
            'other identifiers related to signed - in accounts'  # on the device.',  # For googleads ima (ID=8)
        ],
    },
    'Location': {
        'taint_sources': ['Location'],
        'data_types': [
            'Location',
        ],
    },
    'IPAddress': {
        'taint_sources': ['IPAddress'],
        'data_types': [
            # 'IP Address',
            'Approximate Location',  # For Branch (ID=25)
        ],
    },
}

def map_taint_source_to_data_types(taint_source):
    data_types = set()

    for key, val in mapping.items():
        if (taint_source in val['taint_sources']):
            data_types |= set(val['data_types'])

    return data_types

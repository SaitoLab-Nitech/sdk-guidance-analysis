
# Return SDK name of the given APK name
def get_sdk_name(sdk_dir):
    if (sdk_dir.startswith('googleads')):
        if (sdk_dir.find('interactivemedia') > -1):
            return 'googleads-ima-android'
        else:
            return 'googleads-mobile-android-examples'
    elif (sdk_dir.startswith('fyber-engineering')):
        if (sdk_dir.find('marketplace') > -1):
            return 'fyber-marketplace'
        else:
            return 'fyber-fairbid'
    else:
        return sdk_dir.split('_')[0]

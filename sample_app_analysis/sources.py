# -*- coding: utf-8 -*-

taint_sources = {
    # Hardware Identifier + Phone Number
    'Landroid/telephony/TelephonyManager;': {
        'getDeviceId()Ljava/lang/String;': 'IMEI',
        'getDeviceId(I)Ljava/lang/String;': 'IMEI',
        'getImei()Ljava/lang/String;': 'IMEI',
        'getSimSerialNumber()Ljava/lang/String;': 'ICCID',
        'getSubscriberId()Ljava/lang/String;': 'IMSI',
        'getLine1Number()Ljava/lang/String;': 'PhoneNumber',
    },
    'Landroid/os/Build;': {
        'getSerial()Ljava/lang/String;': 'SERIAL',
    },
    # Network Information
    'Landroid/net/wifi/WifiInfo;': {
        'getMacAddress()Ljava/lang/String;': 'MACAddress',
        'getIpAddress()I': 'IPAddress',
    },
    # Android ID (i.e., SSAID)
    'Landroid/provider/Settings$Secure;': {
        'getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;': 'AndroidID',
    },
    'Landroid/provider/Settings$System;': {
        'getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;': 'AndroidID',
    },
    # Google Advertising ID (AAID)
    'Lcom/google/android/gms/ads/identifier/AdvertisingIdClient$Info;': {
        'getId()Ljava/lang/String;': 'AAID',
    },
    # Instance ID
    'Lcom/google/android/gms/iid/InstanceID;': {
        'getId()Ljava/lang/String;': 'InstanceID',
    },
    # GUID, Universally unique identifier (UUID)
    'Ljava/util/UUID;': {
        'toString()Ljava/lang/String;': 'UUID',
    },
    # Firebase Installation ID
    'Lcom/google/firebase/iid/FirebaseInstanceId;': {
        'getId()Ljava/lang/String;': 'FIID',
    },
    'Lcom/google/firebase/installations/FirebaseInstallations;': {
        'getId()Lcom/google/android/gms/tasks/Task;': 'FIID',
    },
    # Widevine ID
    'Landroid/media/MediaDrm;': {
        'getPropertyByteArray(Ljava/lang/String;)[B': 'WidevineID',
    },

    # Location
    'Landroid/location/Location;': {
        'getLatitude()D': 'Location',
        'getLongitude()D': 'Location',
    },
    # IP Address
    'Ljava/net/InetAddress;': {
        'getHostAddress()Ljava/lang/String;': 'IPAddress',
    },
}

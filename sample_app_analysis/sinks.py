# -*- coding: utf-8 -*-

taint_sinks = {
    #
    # Sink methods
    #

    # URL
    'Ljava/net/URL;': {
        '<init>(': 'sink',
    },
    # URLEncoder
    'Ljava/net/URLEncoder;': {
        'encode(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;': 'sink',
    },
    # Apache
    'Lorg/apache/http/client/methods/HttpGet;': {
        '<init>(': 'sink',
    },
    'Lorg/apache/http/client/methods/HttpPost;': {
        '<init>(': 'sink',
    },
    'Lorg/apache/http/client/entity/UrlEncodedFormEntity;': {
        '<init>(': 'sink',
    },
    'Lorg/apache/http/entity/ByteArrayEntity;': {
        '<init>([B)V': 'sink',
    },
    # 'Lorg/apache/http/message/BasicNameValuePair;': {
    #     '<init>(': 'sink',
    # },
    'Lorg/apache/http/client/utils/URLEncodedUtils;': {
        'format(Ljava/util/List;Ljava/lang/String;)Ljava/lang/String;': 'sink',
    },
    'Lorg/apache/http/entity/StringEntity;': {
        '<init>(': 'sink',
    },
    # String Request
    'Lcom/android/volley/toolbox/StringRequest;': {
        '<init>(': 'sink',
    },
    # OkHttp3
    'Lokhttp3/Request/Builder;': {
        '<init>(': 'sink',
    },
    'Lokhttp3/RequestBody;': {
        '': 'sink',
    },
    # GZIPOutputStream
    'Ljava/util/zip/GZIPOutputStream;': {
        'write(': 'sink',
    },


    #
    # Pre-sink methods
    #
    'Ljava/net/HttpURLConnection;': {
        'getOutputStream()Ljava/io/OutputStream;': 'pre-sink',
    },

    #
    # Combination methods
    #

    # OutputStream
    'Ljava/io/OutputStream;': {
        'write(': 'combination',
    },
    # ByteArrayOutputStream
    'Ljava/io/ByteArrayOutputStream;': {
        'write(': 'combination',
    },
    #  'Ljava/io/ByteArrayOutputStream;': {
    #     'writeTo(Ljava/io/OutputStream;)V',
    # },
    # ByteArrayInputStream
    'Ljava/io/ByteArrayInputStream;': {
        '<init>(': 'combination',
    },
    # FileOutputStream
    'Ljava/io/FileOutputStream;': {
        'write(': 'combination',
    },
    # FilterOutputStream
    'Ljava/io/FilterOutputStream;': {
        'write(': 'combination',
    },
    # ObjectOutputStream
    'Ljava/io/ObjectOutputStream;': {
        'write': 'combination',
    },
    # PipedOutputStream
    'Ljava/io/PipedOutputStream;': {
        'write(': 'combination',
    },
    # AssetFileDescriptor.AutoCloseOutputStream
    'Landroid/content/res/AssetFileDescriptor/AutoCloseOutputStream;': {
        'write(': 'combination',
    },
    # Base64OutputStream
    'Landroid/util/Base64OutputStream;': {
        'write(': 'combination',
    },
    # BufferedOutputStream
    'Ljava/io/BufferedOutputStream;': {
        'write(': 'combination',
    },
    # CheckedOutputStream
    'Ljava/util/zip/CheckedOutputStream;': {
        'write(': 'combination',
    },
    # CipherOutputStream
    'Ljavax/crypto/CipherOutputStream;': {
        'write(': 'combination',
    },
    # DataOutputStream
    'Ljava/io/DataOutputStream;': {
        'write': 'combination',
    },
    # DeflaterOutputStream
    'Ljava/util/zip/DeflaterOutputStream;': {
        'write(': 'combination',
    },
    # DigestOutputStream
    'Ljava/security/DigestOutputStream;': {
        'write(': 'combination',
    },
    # InflaterOutputStream
    'Ljava/util/zip/InflaterOutputStream;': {
        'write(': 'combination',
    },
    # JarOutputStream (No method)
    # ParcelFileDescriptor.AutoCloseOutputStream (No method)
    # PrintStream
    'Ljava/io/PrintStream;': {
        'print': 'combination',
        'write(': 'combination',
    },
    # ZipOutputStream
    'Ljava/util/zip/ZipOutputStream;': {
        'write(': 'combination',
    },

    # Writer
    'Ljava/io/Writer;': {
        'write(': 'combination',
    },
    # BufferedWriter
    'Ljava/io/BufferedWriter;': {
        'write(': 'combination',
    },
    # CharArrayWriter
    'Ljava/io/CharArrayWriter;': {
        'write(': 'combination',
    },
    #  'Ljava/io/CharArrayWriter;': {
    #     'writeTo(Ljava/io/Writer;)V',
    # },
    # FilterWriter
    'Ljava/io/FilterWriter;': {
        'write(': 'combination',
    },
    # OutputStreamWriter
    'Ljava/io/OutputStreamWriter;': {
        'write(': 'combination',
    },
    # PipedWriter
    'Ljava/io/PipedWriter;': {
        'write(': 'combination',
    },
    # PrintWriter
    'Ljava/io/PrintWriter;': {
        'print': 'combination',
        'write(': 'combination',
    },
    # StringWriter
    'Ljava/io/StringWriter;': {
        'write(': 'combination',
    },
    # FileWriter
    'Ljava/io/FileWriter;': {
        'write(': 'combination',
    },

    # DataOutput
    'Ljava/io/DataOutput;': {
        'write': 'combination',
    },
    # ObjectOutput
    'Ljava/io/ObjectOutput;': {
        'write': 'combination',
    },
}

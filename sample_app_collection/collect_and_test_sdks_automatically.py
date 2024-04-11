import os
import sys
import glob
import time
import shutil
import logging
import subprocess


# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Command line arguments
SAMPLES_DIR = sys.argv[1]
URL_LIST_PATH = sys.argv[2]
DEVICE = sys.argv[3]
COMMAND = sys.argv[4]
if (COMMAND not in ['clone', 'build']): raise Exception(f'Unknown command {COMMAND = }')

# Env Var
my_env = os.environ.copy()
my_env['ANDROID_HOME'] = '/home/user/Android/Sdk'
my_jvm_paths = [
    '/usr/local/android-studio-2022-2-1/jbr/',
    '/usr/lib/jvm/jdk-16.0.2/',
    '/usr/lib/jvm/java-14-openjdk-amd64/',
    '/usr/lib/jvm/java-11-openjdk-amd64/',
    '/usr/lib/jvm/java-8-openjdk-amd64/',
]

def clean_workspace(repo_work_dir_path, repo_dir_path):
    if (os.path.isdir(repo_dir_path)):
        logger.info(f'[*] Removing {repo_dir_path = }')
        shutil.rmtree(repo_dir_path)
    elif (not os.path.isdir(repo_work_dir_path)):
        logger.info(f'[*] Creating {repo_work_dir_path = }')
        os.makedirs(repo_work_dir_path)

def clone_repository(url, repo_work_dir_path):
    # Clone
    logger.info(f'  [*] Cloning the repository')
    cmd = ['timeout', '60', 'git', 'clone', url]  # Appboy takes about 31 seconds
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_work_dir_path)
    # logger.info(f'  [+] {result.stdout.strip() = }')  # No output generated
    logger.info(f'  [+] {result.stderr.strip() = }')

def build_project(parent_dir_path):
    for cmd in [ ['./gradlew', 'installDebug'], ['./gradlew', 'installWithpermissionsDebug'] ]:
        for my_jvm_path in my_jvm_paths:
            logger.info(f'    [*] Building with {my_jvm_path = }')
            my_env['JAVA_HOME'] = my_jvm_path
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=parent_dir_path, env=my_env)
            logger.info(f'      [+] {result.stdout.strip() = }')
            logger.info(f'      [+] {result.stderr.strip() = }')
            if (result.stdout.strip().find('BUILD SUCCESSFUL') > -1):
                return True
    return False

def process_gradlew(num, gradlew, repo_work_dir_path, device):
    # Add x permission to gradlew
    logger.info(f'    [*] Adding +x to gradlew')
    cmd = ['chmod', '+x', gradlew]
    subprocess.run(cmd, capture_output=True, text=True)
    
    parent_dir_path = '/'.join(gradlew.split('/')[:-1])
    logger.info(f'    [+] {parent_dir_path = }')

    pkgs_installed_already = get_installed_pkgs(device)

    logger.info(f'    [*] Building the project')
    success = build_project(parent_dir_path)

    if (not success): return

    time.sleep(1)
    get_screenshot(device, repo_work_dir_path, num)

    pkgs_installed_now = get_installed_pkgs(device)
    new_pkgs = list(set(pkgs_installed_now) - set(pkgs_installed_already))
    for new_pkg in new_pkgs:
        new_pkg = new_pkg.split(':')[-1]
        logger.info(f'    [+] {new_pkg = }')
        logger.info(f'      [*] Obtaining the app')
        obtain_app(num, new_pkg, repo_work_dir_path, device)
        logger.info(f'      [*] Uninstalling the app')
        uninstall_app(new_pkg, device)


def get_screenshot(device, destination_dir, num):
    screenshot = f'screenshot_{num}.png'
    logger.info(f'    [*] Taking {screenshot = }')
    cmd = ['adb', '-s', device, 'shell', 'screencap', '-p', f'/sdcard/{screenshot}']
    subprocess.run(cmd, capture_output=True, text=True)
    cmd = ['adb', '-s', device, 'pull', f'/sdcard/{screenshot}', destination_dir]
    subprocess.run(cmd, capture_output=True, text=True)

def get_installed_pkgs(device):
    cmd = ['adb', '-s', device, 'shell', 'pm', 'list', 'packages']
    result = subprocess.run(cmd , capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def obtain_app(num, pkg, dst, device):
    cmd = ['adb', '-s', device, 'shell', 'pm', 'path', pkg]
    result = subprocess.run(cmd, capture_output=True, text=True)

    target_paths = result.stdout.strip().split('\n')

    for target_path in target_paths:
        assert target_path.startswith('package:/')
        target_path = target_path.split('package:')[-1]
        dst_app_path = f'{dst}/{num}_{pkg}_{target_path.split("/")[-1]}'

        cmd = ['adb', '-s', device, 'pull', target_path, dst_app_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(f'        [+] {result.stdout.strip() = }')

def uninstall_app(pkg, device):
    cmd = ['adb', '-s', device, 'uninstall', pkg]
    subprocess.run(cmd, capture_output=True, text=True)

def setup_logger(work_dir):
    log_path = work_dir+'/output.txt'

    # Remove log file that may exist
    try:
        os.remove(log_path)
    except OSError:
        pass

    # Add new handlers
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

def clean_logger():
    # Remove all previous handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

def move_apk(i, apk, repo_work_dir_path):
    cmd = ['mv', apk, f'{repo_work_dir_path}/{i}_{apk.split("/")[-1]}']
    result = subprocess.run(cmd, capture_output=True, text=True)

def process_one_repository(url, samples_dir, device):
    sdk_dir_path = samples_dir+'/'+url.split('/')[-2]
    repo_work_dir_path = sdk_dir_path+'/'+url.split('/')[-1]
    repo_dir_path = repo_work_dir_path+'/'+url.split('/')[-1]

    if (COMMAND == 'clone'):
        # Prepare for cloning
        clean_workspace(repo_work_dir_path, repo_dir_path)
        # Logger
        setup_logger(repo_work_dir_path)
        logger.info(f'[*] Processing {url = }')
        # Clone
        clone_repository(url, repo_work_dir_path)
        # Find apk that already exists
        logger.info(f'  [*] Finding apk existing already')
        apks =  glob.glob(repo_dir_path+'/**/*.apk', recursive=True)
        logger.info(f'  [+] {len(apks) = }')
        for i, apk in enumerate(apks):
            logger.info(f'    [+] Found {i = }, {apk = } [APK ALREADY EXISTS]')
            move_apk(i, apk, repo_work_dir_path)
    else:
        setup_logger(repo_work_dir_path)
        logger.info(f'[*] Processing {url = }')

    # Find and process gradlew scripts
    logger.info(f'  [*] Finding and processing gradlew scripts')
    logger.info(f'    [*] {repo_dir_path = }')
    gradlews =  glob.glob(repo_dir_path+'/**/gradlew', recursive=True)
    logger.info(f'  [+] {len(gradlews) = }')
    for i, gradlew in enumerate(gradlews):
        logger.info(f'  [+] Found {i = }, {gradlew = }')
        process_gradlew(i, gradlew, repo_work_dir_path, device)

    logger.info(f'  [*] Finished')

    clean_logger()

if __name__ == '__main__':
    print('[*] Starting')
    print(f'  [+] {SAMPLES_DIR = }')
    print(f'  [+] {URL_LIST_PATH = }')
    print(f'  [+] {DEVICE = }')
    start = time.time()

    urls = open(URL_LIST_PATH, 'r').read().rstrip('\n').split('\n')
    print(f'  [+] {len(urls) = }')

    for url in urls:
        process_one_repository(url, SAMPLES_DIR, DEVICE)

    print(f'[*] Finished in {time.time() - start} seconds')

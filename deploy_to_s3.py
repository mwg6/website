import boto3
from os import listdir
from os.path import isfile, join

session = boto3.Session()
credentials = session.get_credentials()
# Credentials are refreshable, so accessing your access key / secret key
# separately can lead to a race condition. Use this to get an actual matched
# set.
current_credentials = credentials.get_frozen_credentials()

AWS_ACCESS_KEY_ID = current_credentials.access_key
AWS_SECRET_ACCESS_KEY = current_credentials.secret_key

bucket_name = 'maximgoodman.com'
s3 = boto3.resource('s3')

dirs = ['components', 'css', 'img', 'js']

def get_assets(dirs: list):
    assets = {}
    for d in dirs:
        onlyfiles = [join(d,f) for f in listdir(d) if isfile(join(d, f))]
        if len(onlyfiles)>0:
            assets[d] = onlyfiles
    return assets

def get_html_files():
    html_files = []
    html_files += [each for each in listdir('.') if each.endswith('.html')]
    return html_files

def upload_directory(files: list, s3, bucket, html: bool):
    for f in files:
        #preserve directory and file name 
        print(f"Uploading {f}...")
        if html:
            s3.meta.client.upload_file(f, bucket, f, ExtraArgs={'ContentType':'text/html'})
        else:
            s3.meta.client.upload_file(f, bucket, f)
        print(f"Uploaded {f}!")

html = get_html_files()
assets = get_assets(dirs)
print('Updating html')
upload_directory(html, s3, bucket_name, True)
print('Updated html')
print('Updating assets')
for k in assets:
    upload_directory(assets[k], s3, bucket_name, False)
print('Updated assets')

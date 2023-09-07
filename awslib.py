import boto3
import streamlit as st   # only for secrets!
FELIX_BUCKET = 'cetram-felix'
AWS_KEY = st.secrets['AWS_KEY'] 
AWS_ID = st.secrets['AWS_ID']
##############
def s3_client():
    return boto3.client('s3', 
                        aws_access_key_id=AWS_ID,
                        aws_secret_access_key=AWS_KEY)
def t3_upload(files):
    pass

def s3_contents():
    s3 = s3_client()    
    results = s3.list_objects_v2(Bucket=FELIX_BUCKET)  #, Prefix=folder_prefix)
    file_names = []
    for content in results.get('Contents', []):
        file_names.append(content['Key'])

    # now filter and group by date
    # AUDIO/2023-08-23T08-54-16_soap.txt
    contents = [fn for fn in file_names if fn.startswith('AUDIO/')]
    datetimes = sorted(list(set([fn[:16] for fn in contents])))
    datetimes = [dt for dt in datetimes[-20:] if not dt.endswith('.mp3')]
    dt_contents = {dt: [x for x in contents if x.startswith(dt)] 
                   for dt in datetimes}
    for dt in dt_contents.keys():
        dtv = dt_contents[dt]
        nu_tv = []
        for x in dtv:
            if x.endswith('.txt'):  # read and replace
                obj = s3.get_object(Bucket=FELIX_BUCKET, Key=x)
                xx = obj['Body'].read().decode('utf-8')
                if 'María' in xx or 'Maria' in xx or 'Lucero' in xx:
                    xx = 'CENSURADO'
            else:
                xx = x
            nu_tv.append(xx)
        dt_contents[dt] = nu_tv
    #print('CONTENTS:', dt_contents)
    
    return dt_contents
    
def s3_upload(files):
    s3 = s3_client() 
    for file in files:     
        print('S3 save:', file)
        try:
            s3.upload_fileobj(open(file,'rb'), 
                          FELIX_BUCKET, file)
        except Exception as e:
            raise Exception(f'FILE: {file}\n ERROR: {e} ')

from flask import Flask, flash, render_template, request, jsonify, url_for
import boto3
import logging
import requests
from botocore.exceptions import ClientError

app = Flask(__name__)

from werkzeug.utils import secure_filename

s3 = boto3.client('s3')

BUCKET_NAME='bekim-cribl1'
ALLOWED_EXTENSIONS = {'tgz'}
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024    # 1 Mb limit

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

#result = create_presigned_post("bekim-cribl1", "diag.tgz")

# Generate a presigned S3 POST URL
# object_name = 'diag.tgz'

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


@app.route('/')  
def home():
    return render_template("file_upload_to_s3.html")

@app.route('/healthz')
def handle_health():
    data = {"message": "Healthy!"}
    resp = jsonify(data)
    resp.headers['Status'] = 200
    resp.status_code = 200
    return resp

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        diag_file = request.files['file']
        if diag_file:
            filename = secure_filename(diag_file.filename)
            if allowed_file(filename):
                diag_file.save(filename)
                result = create_presigned_post("bekim-cribl1", filename)
                print(filename)
                with open(filename, 'rb') as f:
                    files = {'file': (filename, f)}
                    http_response = requests.post(result['url'], data=result['fields'], files=files)
                # If successful, returns HTTP status code 204
                logging.info(f'File upload HTTP status code: {http_response.status_code}')
                msg = str(create_presigned_url("bekim-cribl1", filename))
            else:
                logging.warning("Non tgz file attempt" + filename)
                msg = filename + " does not end with .tgz. Try again!"
                
    return render_template("file_upload_to_s3.html",msg =msg)


if __name__ == "__main__":
    
    app.run(host='0.0.0.0',debug=True)



# diagservice
Flask App to upload files to AWS S3 using Pre-signed URL

Steps to run locally:

Make sure you're running python 3.7 <

1. git clone https://github.com/bekimdisha/diagservice.git

2. cd ~/diagservice

3. python -m venv myprojects_virtualenv

4. virtualenv myprojects_virtualenv

5. pip3 install -r requirements.txt

6. python tests.py (tests should pass)

7. python -m flask run

8. Open a browser and run: http://127.0.0.1:5000/

9. Select a file (.tgz under 1 mb)

10. Profit


Approach Diagram



CI CD Architecture Diagram

![CICD_architecture](https://user-images.githubusercontent.com/1514469/139479049-43e77e1f-9b7c-4027-8d74-0b6feb10bf78.png)

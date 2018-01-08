# img-service
A flask web app for storing images.

The project was done during September-November 2017, together with Karen Yahan Yang (https://github.com/karenyahanyang)

Read the docs to find out more.

##Required library
- boto3
- Flask
- MySQL Connector
- Wand 
- Pillow
##To run:
1. Set up a S3 bucket. You will need an access key-pair, the url to your bucket and the Boto3 python library. Check app/config.py 
for environment variable setups.
2. Get a MySQL server running. We used AWS RDS while testing this out. Again, check app/config.py
3. To run with flask's built-in test server, simply run `python run.py`
4. Optionally, use gunicorn for better performance.

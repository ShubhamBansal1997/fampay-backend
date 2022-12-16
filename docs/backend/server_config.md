# Server Architecture and configurations

## Concepts

Our overall stack looks like this:

```
the web client <-> the web server (nginx) <-> the socket <-> uWSGI <-> Django
```

A web server faces the outside world. It can serve files (HTML, images, CSS, etc) directly from the file system. However, it can’t talk directly to Django applications; it needs something that will run the application, feed it requests from web clients (such as browsers) and return responses.

uWSGI is a [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) implementation, it creates a Unix socket, and serves responses to the web server via the uwsgi protocol.

## Third Party Services

Following third-party services are required in order to setup/deploy this project successfully.

### Amazon S3

Amazon Simple Storage Service ([Amazon S3]) is used to store the uploaded media files and static content. It is a scalable and cost-efficient storage solution. 

After [signing up][s3-signup] for Amazon S3, [setup][s3-iam-setup] an IAM user with access to a S3 bucket, you'll need `BUCKET_NAME`, and `AWS_ACCESS_ID` & `AWS_ACCESS_SECRET` of IAM user to setup the project.

[Amazon S3]: http://aws.amazon.com/s3/
[s3-signup]: http://docs.aws.amazon.com/AmazonS3/latest/gsg/SigningUpforS3.html
[s3-iam-setup]: https://rbgeek.wordpress.com/2014/07/18/amazon-iam-user-creation-for-single-s3-bucket-access/

Note: 

- IAM user must have permission to list, update, create objects in S3.

## Deploying Project

The deployment are managed via travis, but for the first time you'll need to set the configuration values on each of the server. Read this only, if you need to deploy for the first time.

import os

os.environ["DEPLOYMENT_STAGE"] = os.getenv("DEPLOYMENT_STAGE", "test")
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"

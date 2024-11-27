import os
import boto3
from dotenv import load_dotenv

load_dotenv()

class Config:

    #RAG
    DATA_PATH = "zhengyun21/PMC-Patients"
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    GENERATIVE_MODEL_NAME = "gpt-4o"
    COLLECTION_NAME = "Patient_insight"
    N_RESULTS = 3
    GENERATIVE_MODEL_TEMPERATURE = 0.7
    GENERATIVE_MODEL_MAX_TOKENS = 650
    GENERATIVE_MODEL_INPUT_COST = 2.5 / 1000000
    GENERATIVE_MODEL_OUTPUT_COST = 10 / 1000000
    
    # API Keys (from environment variables)
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # S3 Configuration
    S3_BUCKET = "patientinsightbucket"
    S3_PATH = "files/md5/44/14d973e28b5eedd86d5b5213281870"
    
    # AWS Credentials
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-2")  

    @classmethod
    def validate_env_vars(cls):
        required_vars = [
            "PINECONE_API_KEY",
            "PINECONE_ENVIRONMENT",
            "PINECONE_INDEX_NAME",
            "OPENAI_API_KEY",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please check your .env file."
            )
        return True

    @classmethod
    def verify_s3_access(cls):
        """Verify access to S3 bucket and data"""
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=cls.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=cls.AWS_SECRET_ACCESS_KEY,
                region_name=cls.AWS_REGION
            )
            
            # List objects in the specified path to verify access
            response = s3_client.list_objects_v2(
                Bucket=cls.S3_BUCKET,
                Prefix=cls.S3_PATH
            )
            
            if 'Contents' in response:
                print("S3 access verified successfully")
            else:
                raise FileNotFoundError(f"No files found in S3 path: {cls.S3_PATH}")
            
        except Exception as e:
            raise ConnectionError(f"Failed to access S3: {str(e)}")
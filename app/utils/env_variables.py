import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.environ['MONGODB_URI']
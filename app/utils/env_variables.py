import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Debugging: print sys.argv
print("sys.argv:", sys.argv)

# Check if 'dev' is in the arguments
if 'dev' in sys.argv:
    APP_ENV = 'development'
    print("RUNNING IN DEV")
else:
    APP_ENV = 'production'
    print("RUNNING IN PROD")

if APP_ENV == 'production':
    CONNECTION_STRING = os.environ['MONGODB_URI']
    STRUCTURAL_MODELS_PATH = os.environ['STRUCTURAL_MODELS_PATH']
    GRAPH_DATA_PATH = os.environ['GRAPH_DATA_PATH']
    BLAST_DB_PATH = os.environ['BLAST_DB_PATH']
else:
    CONNECTION_STRING = os.environ['DEV_MONGODB_URI']
    STRUCTURAL_MODELS_PATH = os.environ['DEV_STRUCTURAL_MODELS_PATH']
    GRAPH_DATA_PATH = os.environ['DEV_GRAPH_DATA_PATH']
    BLAST_DB_PATH = os.environ['DEV_BLAST_DB_PATH']

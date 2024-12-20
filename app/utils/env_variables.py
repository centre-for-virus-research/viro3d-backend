import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Debugging: print sys.argv
print("sys.argv:", sys.argv)

# Check if 'run' is in the arguments
if 'run' in sys.argv:
    APP_ENV = 'production'
    print("RUNNING IN PROD")

else:
    APP_ENV = 'development'
    print("RUNNING IN DEV")

if APP_ENV == 'production':
    CONNECTION_STRING = os.environ['MONGODB_URI']
    STRUCTURAL_MODELS_PATH = os.environ['STRUCTURAL_MODELS_PATH']
    GRAPH_DATA_PATH = os.environ['GRAPH_DATA_PATH']
    PDFS_PATH = os.environ['PDFS_PATH']
    BLAST_DB_PATH = os.environ['BLAST_DB_PATH']
else:
    CONNECTION_STRING = os.environ['DEV_MONGODB_URI']
    STRUCTURAL_MODELS_PATH = os.environ['DEV_STRUCTURAL_MODELS_PATH']
    GRAPH_DATA_PATH = os.environ['DEV_GRAPH_DATA_PATH']
    PDFS_PATH = os.environ['DEV_PDFS_PATH']
    BLAST_DB_PATH = os.environ['DEV_BLAST_DB_PATH']

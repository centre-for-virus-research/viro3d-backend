import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.environ['MONGODB_URI']
STRUCTURAL_MODELS_PATH = os.environ['STRUCTURAL_MODELS_PATH']
GRAPH_DATA_PATH = os.environ['GRAPH_DATA_PATH']
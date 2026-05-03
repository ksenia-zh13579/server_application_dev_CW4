import os
from dotenv import dotenv_values, load_dotenv

load_dotenv()
config = dotenv_values(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))
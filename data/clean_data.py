import shutil
import os

SCRIPT_DIR = os.path.dirname(__file__)


ORIGINAL_FILE_NAME = 'DATA_EMPTY.db'
ORIGINAL_FILE_PATH = os.path.join(SCRIPT_DIR, ORIGINAL_FILE_NAME)

NEW_FILE_NAME = 'data.db'
NEW_FILE_PATH = os.path.join(SCRIPT_DIR, NEW_FILE_NAME)


# Use the shutil module to copy the file and rename it
shutil.copy(ORIGINAL_FILE_NAME, NEW_FILE_NAME)

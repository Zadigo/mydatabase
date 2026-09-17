import pathlib

import dotenv

BASE_DIR = pathlib.Path(__file__).parent.absolute()

dotenv.load_dotenv(BASE_DIR / '.env')

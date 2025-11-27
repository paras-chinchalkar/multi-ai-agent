import os
import sys
import subprocess
import threading
import time
from dotenv import load_dotenv

# Ensure project root is importable so package-style imports (from app.*)
# continue to work when the script is executed from different working
# directories (for example: `python app/main.py` vs `python -m app.main`).
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger=get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("starting backend service..")
        subprocess.run(["uvicorn" , "app.backend.api:app" , "--host" , "127.0.0.1" , "--port" , "9999"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Problem with backend service")
        raise CustomException("Failed to start backend", error_detail=e)
    except Exception as e:
        logger.error(f"Unexpected error in backend service: {str(e)}")
        raise CustomException("Failed to start backend", error_detail=e)
    
def run_frontend():
    try:
        logger.info("Starting Frontend service")
        subprocess.run(["streamlit" , "run" , "app/frontend/ui.py"],check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Problem with frontend service")
        raise CustomException("Failed to start frontend", error_detail=e)
    except Exception as e:
        logger.error(f"Unexpected error in frontend service: {str(e)}")
        raise CustomException("Failed to start frontend", error_detail=e)
    
if __name__=="__main__":
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        run_frontend()
    
    except CustomException as e:
        logger.exception(f"CustomException occured : {str(e)}")
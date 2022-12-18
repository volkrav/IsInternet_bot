pipenv install fastapi
pipenv install "uvicorn[standard]"
pipenv install autopep8 --dev
pipenv install requests


uvicorn isnet:app --reload

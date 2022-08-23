FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
ENTRYPOINT [ "sh", "entrypoint.sh"]

FROM python:3.12.7-slim-bookworm

WORKDIR /scripts

COPY . /scripts/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.runOnSave", "true", "--server.fileWatcherType", "poll"]
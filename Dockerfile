FROM python:latest

WORKDIR /app

COPY requirements.txt ./
COPY home.py ./
COPY utils.py ./

RUN mkdir -p /app/pages
ADD ./pages /app/pages

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501
EXPOSE 11434

ENTRYPOINT ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]

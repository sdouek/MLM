FROM python:3.6

WORKDIR /MLM
ADD . /MLM/
RUN pip install -r requirements.txt

EXPOSE 8084
CMD ["python3", "src/app.py", "--host=0.0.0.0"]
#ENTRYPOINT ["python", "-m", "src.app", "-p", "8084"]

#FROM mysql:8.0
#COPY src/database/createDB.sql /docker-entrypoint-initdb.d/run_createDB.sql

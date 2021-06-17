# python:3.7-stretch의 이미지로부터 가져 온다.
FROM python:3.8.7-alpine3.12

# 실행할 환경 만들기
RUN mkdir /app
RUN pip install pymysql

#run,cmd가 실행될 장소(app)
WORKDIR /app

# 현재 위치에 있는 파일(program.py)을 뒤쪽 위치(app)를 주소로 하여 컨테이너에다가 복사하겠다.
COPY ./program.py /app

# container가 실행(run)할 때 명령이 실행
CMD ["python", "program.py"]

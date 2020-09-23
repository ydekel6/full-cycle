# Phase I - Builder source
FROM python:latest as builder
# PYTHONUNBUFFERED Force logging to stdout / stderr not to be buffered into ram  
ENV PYTHONNUNBUFFERED=1
WORKDIR /usr/src/app
COPY /app ./
WORKDIR /wheels
COPY app/requirements.txt ./
RUN pip wheel -r ./requirements.txt

# Phase II - Linting the code
FROM eeacms/pylint:latest as linting
WORKDIR /code
COPY --from=builder /usr/src/app/pylint.cfg /etc/pylint.cfg
COPY --from=builder /usr/src/app/*.py ./
RUN ["/docker-entrypoint.sh", "pylint"]

# Phase IV - Unit testing
#FROM python:latest as unit-tests
#WORKDIR /usr/src/app
#Copy all packages instead of rerunning pip install
#COPY --from=builder /wheels /wheels
#RUN     pip install -r /wheels/requirements.txt \
#                      -f /wheels \
#       && rm -rf /wheels \
#       && rm -rf /root/.cache/pip/* 

#COPY --from=builder /usr/src/app/ ./
#RUN ["make", "test"]

# Phase V - running the script itself
FROM python:3.8-slim as serve
WORKDIR /usr/src/app
# Copy all packages instead of rerunning pip install
COPY --from=builder /wheels /wheels
RUN     pip install -r /wheels/requirements.txt \
                      -f /wheels \
       && rm -rf /wheels \
       && rm -rf /root/.cache/pip/* 

COPY --from=builder /usr/src/app/*.py ./
CMD ["python", "aws-call.py"]

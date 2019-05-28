FROM python:3.7.2-alpine3.9 as build-backend

RUN apk add build-base

WORKDIR /app

COPY botan /app/botan
COPY test /app/test
COPY config.yaml /app/config.yaml
COPY setup.py /app/setup.py
RUN python -m venv ./venv
RUN source ./venv/bin/activate && pip install -e .
RUN source ./venv/bin/activate && pytest ./test

FROM python:3.7.2-alpine3.9
WORKDIR /app
COPY --from=build-backend /app /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD ["bot", "serve"]
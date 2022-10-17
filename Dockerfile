FROM python:3.10-slim
# COPY --chmod=555 ./bin/* /usr/local/bin/
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /app

COPY brefv/ brefv/

RUN mkdir brefv_spec && \
    datamodel-codegen --input brefv/envelope.json --input-file-type jsonschema --output brefv_spec/envelope.py && \
    datamodel-codegen --input brefv/messages --input-file-type jsonschema  --reuse-model --output brefv_spec/messages

COPY main.py main.py

CMD ["python3", "main.py"]
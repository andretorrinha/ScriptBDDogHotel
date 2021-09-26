FROM python:3
COPY . /Dog_SCRIPT
WORKDIR /Dog_SCRIPT
RUN pip install -r requirements.txt
CMD python ./CleanBD.py


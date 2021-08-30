FROM python:3
COPY . /Dog_SCRIPT
WORKDIR /Dog_SCRIPT
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./CleanBD.py


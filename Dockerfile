FROM python:3.9-slim

ENV SOLAR_STORMS_DATABASE=/test.db

RUN apt-get update && apt-get install -y git
RUN cd / && git clone https://github.com/raymenzel/solar-storms.git
RUN cd /solar-storms && pip install .
RUN cd /solar-storms && python3 -m flask --app solar_storms init-db

EXPOSE 5000

CMD ["python3", "-m", "flask", "--app", "solar_storms", "run", "--host", "0.0.0.0"]

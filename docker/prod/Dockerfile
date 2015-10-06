FROM python:2.7

RUN mkdir /code
WORKDIR /code

RUN \
  git clone https://github.com/LHCbDev/lhcbpr-api.git  . &&  \
  echo "clone completed"

CMD ["./scripts/runserver"]

EXPOSE 80

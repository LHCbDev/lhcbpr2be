FROM python:2.7

RUN mkdir /code
WORKDIR /code
ADD . /code

# Get code
# RUN \
#   branch="prepare-for-docker" && \
#   mkdir /lhcbpr-api  && \
#   cd /lhcbpr-api && \
#   git clone https://github.com/LHCbDev/lhcbpr-api.git  &&  \
#   echo "clone completed"  &&  \
#   cd lhcbpr-api && \
#   git pull origin prepare-for-docker  &&  \
#   echo "checkout completed"

WORKDIR /code

CMD ["./scripts/runserver"]

EXPOSE 8080

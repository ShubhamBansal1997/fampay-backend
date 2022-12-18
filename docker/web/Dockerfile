FROM python:3.9-slim

LABEL maintainer="Shubham Bansal <shubhambansal17@hotmail.com>"

# set work directory
WORKDIR /usr/src/app

# Environment varialbes to control python and pip behaviour.
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # libmagic
  libmagic1 \
  # supervisor
  supervisor \
  # extra packages
  libcurl4 openssl liblzma5 gettext curl gnupg2 wget\
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY ./requirements_dev.txt .

RUN pip install --no-cache-dir -r requirements_dev.txt

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN adduser --system --group app
# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/.staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# copy  entrypoint.sh
COPY ./docker/web/entrypoint.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]

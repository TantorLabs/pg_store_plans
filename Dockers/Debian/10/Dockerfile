FROM debian:10

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install git wget curl lsb-release gnupg2  -y 

RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' && \
    # Import the repository signing key:
    wget --no-check-certificate --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update

RUN apt-get install postgresql-10 postgresql-server-dev-10 libpq-dev -y
RUN apt-get install make gcc devscripts debhelper apt-utils -y
RUN git clone https://github.com/mixmind/pg_store_plans.git && cd pg_store_plans && git checkout add_deb_pkg 

ADD deb /pg_store_plans/deb

RUN cd /pg_store_plans && PATH=/usr/lib/postgresql/10/bin:$PATH make USE_PGXS=1 && \
    PATH=/usr/lib/postgresql/10/bin:$PATH make USE_PGXS=1 PG_MAKE_VERSION=10 build-debs

RUN apt-get install postgresql-11 postgresql-server-dev-11 -y
RUN cd /pg_store_plans  && PATH=/usr/lib/postgresql/11/bin:$PATH make USE_PGXS=1 clean && \
    PATH=/usr/lib/postgresql/11/bin:$PATH make USE_PGXS=1 && \
    PATH=/usr/lib/postgresql/11/bin:$PATH make USE_PGXS=1 PG_MAKE_VERSION=11 build-debs

RUN apt-get install postgresql-12 postgresql-server-dev-12  -y
RUN cd /pg_store_plans  && PATH=/usr/lib/postgresql/12/bin:$PATH make USE_PGXS=1 clean && \
    PATH=/usr/lib/postgresql/12/bin:$PATH make USE_PGXS=1 && \
    PATH=/usr/lib/postgresql/12/bin:$PATH make USE_PGXS=1 PG_MAKE_VERSION=12 build-debs

RUN apt-get install postgresql-13 postgresql-server-dev-13 -y
RUN cd /pg_store_plans  && PATH=/usr/lib/postgresql/13/bin:$PATH make USE_PGXS=1 clean && \
    PATH=/usr/lib/postgresql/13/bin:$PATH make USE_PGXS=1 && \
    PATH=/usr/lib/postgresql/13/bin:$PATH make USE_PGXS=1 PG_MAKE_VERSION=13 build-debs

RUN apt-get install postgresql-14 postgresql-server-dev-14 -y
RUN cd /pg_store_plans  && PATH=/usr/lib/postgresql/14/bin:$PATH make USE_PGXS=1 clean && \
    PATH=/usr/lib/postgresql/14/bin:$PATH make USE_PGXS=1 && \
    PATH=/usr/lib/postgresql/14/bin:$PATH make USE_PGXS=1 PG_MAKE_VERSION=14 build-debs

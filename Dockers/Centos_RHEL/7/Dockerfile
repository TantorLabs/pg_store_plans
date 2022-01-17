FROM centos:7

RUN yum update -y && yum install make gcc sudo curl wget git centos-release-scl epel-release rpm-build -y

RUN sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm && \
    # Install PostgreSQL:
    yum install -y postgresql10-server postgresql10-contrib postgresql10-devel

RUN git clone https://github.com/mixmind/pg_store_plans.git && cd pg_store_plans && git checkout add_deb_pkg 

ADD rpm /pg_store_plans/rpm

RUN cd /pg_store_plans && PATH=/usr/pgsql-10/bin:$PATH make USE_PGXS=1 && \
    PATH=/usr/pgsql-10/bin:$PATH make USE_PGXS=1 PG_MAKE_VERSION=10 build-rpms

RUN yum install -y postgresql11-server postgresql11-contrib postgresql11-devel -y
RUN cd /pg_store_plans && PATH=/usr/pgsql-11/bin:$PATH make USE_PGXS=1 clean && \
    PATH=/usr/pgsql-11/bin:$PATH make USE_PGXS=1 && \
    PATH=/usr/pgsql-11/bin:$PATH make USE_PGXS=1 PG_MAKE_VERSION=11 build-rpms

RUN yum install -y postgresql12-server postgresql12-contrib postgresql12-devel -y
RUN cd /pg_store_plans && PATH=/usr/pgsql-12/bin:$PATH make USE_PGXS=1 clean && \
    PATH=/usr/pgsql-12/bin:$PATH make USE_PGXS=1 && \
    PATH=/usr/pgsql-12/bin:$PATH make USE_PGXS=1 PG_MAKE_VERSION=12 build-rpms

RUN yum install -y postgresql13-server postgresql13-contrib postgresql13-devel -y
RUN cd /pg_store_plans && PATH=/usr/pgsql-13/bin:$PATH make USE_PGXS=1 clean && \
    PATH=/usr/pgsql-13/bin:$PATH make USE_PGXS=1 && \
    PATH=/usr/pgsql-13/bin:$PATH make USE_PGXS=1 PG_MAKE_VERSION=13 build-rpms

RUN yum install -y postgresql14-server postgresql14-contrib postgresql14-devel -y
RUN cd /pg_store_plans && PATH=/usr/pgsql-14/bin:$PATH make USE_PGXS=1 clean && \
    PATH=/usr/pgsql-14/bin:$PATH make USE_PGXS=1 && \
    PATH=/usr/pgsql-14/bin:$PATH make USE_PGXS=1 PG_MAKE_VERSION=14 build-rpms

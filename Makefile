# pg_stat_plan/Makefile

MODULES = pg_store_plans
STOREPLANSVER = 1.6

MODULE_big = pg_store_plans
OBJS = pg_store_plans.o pgsp_json.o pgsp_json_text.o pgsp_explain.o

EXTENSION = pg_store_plans

PG_VERSION := $(shell pg_config --version | sed "s/^PostgreSQL //" | sed "s/\.[0-9]*$$//")

DATA = pg_store_plans--1.6.sql

REGRESS = convert store
REGRESS_OPTS = --temp-config=regress.conf
ifdef USE_PGXS
PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)
include $(PGXS)
else
subdir = contrib/pg_store_plans
top_builddir = ../..
include $(top_builddir)/src/Makefile.global
include $(top_srcdir)/contrib/contrib-global.mk
endif

STARBALL14 = pg_store_plans14-$(STOREPLANSVER).tar.gz
STARBALLS = $(STARBALL14)

TARSOURCES = Makefile *.c  *.h \
	pg_store_plans--*.sql \
	pg_store_plans.control \
	docs/* expected/*.out sql/*.sql \

ifneq ($(shell uname), SunOS)
LDFLAGS+=-Wl,--build-id
endif

BASE_DIR=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
USEDPATH:= usr/lib/postgresql
SHAREPATH:= usr/share/postgresql
## These entries need running server
DBNAME = postgres
PG_BUILD_VERSION=$(if $(PG_MAKE_VERSION),$(PG_MAKE_VERSION),14)

rpms: rpm14

$(STARBALLS): $(TARSOURCES)
	if [ -h $(subst .tar.gz,,$@) ]; then rm $(subst .tar.gz,,$@); fi
	if [ -e $(subst .tar.gz,,$@) ]; then \
	  echo "$(subst .tar.gz,,$@) is not a symlink. Stop."; \
	  exit 1; \
	fi
	ln -s . $(subst .tar.gz,,$@)
	tar -chzf $@ $(addprefix $(subst .tar.gz,,$@)/, $^)
	rm $(subst .tar.gz,,$@)

rpm14: $(STARBALL14)
	MAKE_ROOT=`pwd` rpmbuild -bb SPECS/pg_store_plans14.spec

build-rpms:
	@echo Creating RPMSs ; \
	RPMS="${PG_BUILD_VERSION}" ; \
	for dir_path in $${RPMS}; do \
		echo "Creating rpm for postgresql $${dir_path}" ; \
		rm -rf rpm/$${dir_path}/RPMS && \
		export QA_SKIP_RPATHS=1 && rpmbuild -bb -D "_topdir $(BASE_DIR)/rpm/$${dir_path}" $(BASE_DIR)/rpm/$${dir_path}/SPECS/pg_store_plans$${dir_path}.spec && \
		echo "Created rpm for postgresql $${dir_path}" ; \
		cd $(BASE_DIR) ; \
	done

build-debs: 
	@echo Creating DEBs ; \
	DEB="${PG_BUILD_VERSION}" ; \
	for dir_path in $${DEB}; do \
		echo "Creating deb for postgresql $${dir_path}" ; \
		rm -rf deb/$${dir_path}/pg_store_plans/*.deb && \
		mkdir -p $(BASE_DIR)/deb/$${dir_path}/pg_store_plans/${USEDPATH}/$${dir_path}/lib/bitcode/pg_store_plans  && \
		mkdir -p $(BASE_DIR)/deb/$${dir_path}/pg_store_plans/$(SHAREPATH)/$${dir_path}/extension/ && \
		/usr/bin/install -c -m 755 pg_store_plans.so $(BASE_DIR)/deb/$${dir_path}/pg_store_plans/${USEDPATH}/$${dir_path}/lib/pg_store_plans.so && \
		/usr/bin/install -c -m 644 pg_store_plans.control $(BASE_DIR)/deb/$${dir_path}/pg_store_plans/$(SHAREPATH)/$${dir_path}/extension && \
		/usr/bin/install -c -m 644 pg_store_plans--1.6.sql  $(BASE_DIR)/deb/$${dir_path}/pg_store_plans/$(SHAREPATH)/$${dir_path}/extension && \
		if [ $${dir_path} != 10 ]; then \
			/usr/bin/install -c -m 644 pg_store_plans.bc $(BASE_DIR)/deb/$${dir_path}/pg_store_plans/usr/lib/postgresql/$${dir_path}/lib/bitcode/pg_store_plans && \
			/usr/bin/install -c -m 644 pgsp_json.bc $(BASE_DIR)/deb/$${dir_path}/pg_store_plans/usr/lib/postgresql/$${dir_path}/lib/bitcode/pg_store_plans/./ && \
			/usr/bin/install -c -m 644 pgsp_json_text.bc $(BASE_DIR)/deb/$${dir_path}/pg_store_plans/usr/lib/postgresql/$${dir_path}/lib/bitcode/pg_store_plans/./ && \
			/usr/bin/install -c -m 644 pgsp_explain.bc $(BASE_DIR)/deb/$${dir_path}/pg_store_plans/usr/lib/postgresql/$${dir_path}/lib/bitcode/pg_store_plans/./ ; \
		fi ; \
		cd $(BASE_DIR)/deb/$${dir_path}/pg_store_plans && \
		rm -rf debian/changelog && \
		dch --create --distribution stable --package "pg-store-plans-$${dir_path}" --newversion 1.6 "Release" && \
		dpkg-buildpackage -us -uc && \
		echo "Created deb for postgresql $${dir_path}" ; \
		cd $(BASE_DIR) ; \
	done

testfiles: convert.out convert.sql

convert.out: convert.sql
	psql $(DBNAME) -a -q -X -f convert.sql > $@

convert.sql: makeplanfile.sql json2sql.pl
	psql $(DBNAME) -X -f makeplanfile.sql |& ./json2sql.pl > $@

clean-testfiles:
	rm -f convert.out convert.sql

deploy-testfiles: testfiles
	mv convert.sql sql/
	mv convert.out expected/

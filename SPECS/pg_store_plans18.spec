# SPEC file for pg_store_plans
# Copyright(c) 2025, NTT, Inc.

%global pgdir   /usr/pgsql-18
%global pg_bindir  %{pgdir}/bin
%global pg_libdir  %{pgdir}/lib
%global pg_datadir %{pgdir}/share
%global pg_bcdir %{pg_libdir}/bitcode
%global pg_mybcdir %{pg_bcdir}/pg_store_plans
%global __brp_check_rpaths %{nil}

%if "%(echo ${MAKE_ROOT})" != ""
  %define _rpmdir %(echo ${MAKE_ROOT})/RPMS
  %define _sourcedir %(echo ${MAKE_ROOT})
%endif

## Set general information for pg_store_plans.
Summary:    Record executed plans on PostgreSQL 18
Name:       pg_store_plans18
Version:    1.10.1
Release:    2%{?dist}
License:    BSD
Group:      Applications/Databases
Source0:    %{name}-%{version}.tar.gz
#URL:        http://example.com/pg_store_plans/
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

## We use postgresql-devel package
BuildRequires:  postgresql18-devel
Requires:  postgresql18-libs

## Description for "pg_store_plans"
%description

pg_store_plans provides capability to record statistics for every plan
executed on PostgreSQL.

Note that this package is available for only PostgreSQL 18.

%package llvmjit
Requires: postgresql18-server, postgresql18-llvmjit
Requires: pg_store_plans18 = 1.10.1
Summary:  Just-in-time compilation support for pg_store_plans18

%description llvmjit
Just-in-time compilation support for pg_store_plans18

## pre work for build pg_store_plans
%prep
PATH=/usr/pgsql-18/bin:$PATH
if [ "${MAKE_ROOT}" != "" ]; then
  pushd ${MAKE_ROOT}
  make clean %{name}-%{version}.tar.gz
  popd
fi
if [ ! -d %{_rpmdir} ]; then mkdir -p %{_rpmdir}; fi
%setup -q

## Set variables for build environment
%build
PATH=/usr/pgsql-18/bin:$PATH
pg_config
make USE_PGXS=1 PG_CONFIG=%{pg_bindir}/pg_config %{?_smp_mflags}

## Set variables for install
%install
rm -rf %{buildroot}
PATH=/usr/pgsql-18/bin:$PATH
make USE_PGXS=1 PG_CONFIG=%{pg_bindir}/pg_config DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(0755,root,root)
%{pg_libdir}/pg_store_plans.so
%defattr(0644,root,root)
%{pg_datadir}/extension/pg_store_plans--1.10.sql
%{pg_datadir}/extension/pg_store_plans.control

%files llvmjit
%defattr(0644,root,root)
%{pg_bcdir}/pg_store_plans.index.bc
%{pg_mybcdir}/*.bc

# History of pg_store_plans.
%changelog
* Fri Dec 19 2025 Kyotaro Horiguchi
- Version 1.10. Support PostgreSQL 18.
* Mon Jan 20 2025 Kyotaro Horiguchi
- Version 1.9. Support PostgreSQL 17.
* Fri Feb 02 2024 Kyotaro Horiguchi
- Version 1.8. Support PostgreSQL 16.
* Wed Dec 14 2022 Kyotaro Horiguchi
- Version 1.7. Support PostgreSQL 15.
* Thu Feb 03 2022 Kyotaro Horiguchi
- Version 1.6.1.
* Mon Jan 17 2022 Tatsuro Yamada, Julien Rouhaud, Kyotaro Horiguchi
- Version 1.6. Supports PostgreSQL 14
* Wed Jan 27 2021 Kyotaro Horiguchi
- Version 1.5. Supports PostgreSQL 13
* Thu Jan 30 2020 Kyotaro Horiguchi
- Version 1.4. Supports PostgreSQL 12
* Tue Jan 22 2019 Kyotaro Horiguchi
- Supports PostgreSQL 11
* Tue Oct 10 2017 Kyotaro Horiguchi
- Supports PostgreSQL 10
* Fri Aug 26 2016 Kyotaro Horiguchi
- Some fix in plan representation functions.
* Wed Apr 13 2016 Kyotaro Horiguchi
- Support PostgreSQL 9.5
* Fri Jun 12 2015 Kyotaro Horiguchi
- Initial version.



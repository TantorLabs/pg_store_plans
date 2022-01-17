# SPEC file for pg_store_plans
# Copyright(c) 2021, NIPPON TELEGRAPH AND TELEPHONE CORPORATION

%define _pgdir   /usr/pgsql-12
%define _bindir  %{_pgdir}/bin
%define _libdir  %{_pgdir}/lib
%define _datadir %{_pgdir}/share
%define _bcdir %{_libdir}/bitcode
%define _mybcdir %{_bcdir}/pg_store_plans

%if "%(echo ${MAKE_ROOT})" != ""
  %define _rpmdir %(echo ${MAKE_ROOT})/RPMS
%endif

## Set general information for pg_store_plans.
Summary:    Record executed plans on PostgreSQL 12
Name:       pg_store_plans12
Version:    1.6
Release:    1%{?dist}
License:    BSD
Group:      Applications/Databases
#URL:        http://example.com/pg_store_plans/
Vendor:     NIPPON TELEGRAPH AND TELEPHONE CORPORATION

## We use postgresql-devel package
Requires:  postgresql12-libs, postgresql12-server, postgresql12-llvmjit, centos-release-scl, epel-release

## Description for "pg_store_plans"
%description

pg_store_plans provides capability to record statistics for every plan
executed on PostgreSQL.

Note that this package is available for only PostgreSQL 12.

## Set variables for install
%install
PATH=/usr/pgsql-12/bin:$PATH
mkdir -p %{buildroot}/usr/pgsql-12/lib/bitcode/pg_store_plans
mkdir -p %{buildroot}/usr/pgsql-12/share/extension/
cp -r %{_topdir}/../../*.bc %{buildroot}/usr/pgsql-12/lib/bitcode/pg_store_plans
cp -r %{_topdir}/../../pg_store_plans.so %{buildroot}/usr/pgsql-12/lib/
cp -r %{_topdir}/../../pg_store_plans.control %{buildroot}/usr/pgsql-12/share/extension/
cp -r %{_topdir}/../../pg_store_plans*.sql %{buildroot}/usr/pgsql-12/share/extension/

%post
cd '/usr/pgsql-12/lib/bitcode' && /usr/lib64/llvm5.0/bin/llvm-lto -thinlto -thinlto-action=thinlink -o pg_store_plans.index.bc pg_store_plans/pg_store_plans.bc pg_store_plans/pgsp_json.bc pg_store_plans/pgsp_json_text.bc pg_store_plans/pgsp_explain.bc

%clean
rm -rf %{buildroot}

%files
%defattr(0755,root,root)
%{_mybcdir}/*.bc
%{_libdir}/pg_store_plans.so
%defattr(0644,root,root)
%{_datadir}/extension/pg_store_plans--1.6.sql
%{_datadir}/extension/pg_store_plans.control


# History of pg_store_plans.
%changelog
* Wed Nov 18 2021 Tatsuro Yamada, Julien Rouhaud, Kyotaro Horiguchi
- Version 1.6. Supports PostgreSQL 14
* Wed Jan 27 2021 Kyotaro Horiguchi
- Version 1.5. Supports PostgreSQL 13
* Thu Jan 30 2020 Kyotaro Horiguchi
- Version 1.4. Supports PostgreSQL 12
* Tue Jan 22 2019 Kyotaro Horiguchi
- Supports PostgreSQL 12
* Tue Oct 10 2017 Kyotaro Horiguchi
- Supports PostgreSQL 10
* Fri Aug 26 2016 Kyotaro Horiguchi
- Some fix in plan representation functions.
* Wed Apr 13 2016 Kyotaro Horiguchi
- Support PostgreSQL 9.5
* Fri Jun 12 2015 Kyotaro Horiguchi
- Initial version.



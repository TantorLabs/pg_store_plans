It is a [fork](http://github.com/ossc-db/pg_store_plans) with changes:

* Does not save queryID in its own format, gives up to +10% increase.
* Change path of "pg_store_plans.stat" from global/ into pg_stat_tmp/
* Fix UB from 'memcpy' of overlapping buffer into 'memmove'
* Add time unit support to pg_store_plans.min_duration

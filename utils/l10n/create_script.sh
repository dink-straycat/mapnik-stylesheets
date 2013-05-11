#!/bin/bash -x
psql="psql -hlocalhost -Uosm gis"
org_prefix="planet_osm"
new_prefix="planet_osm_ja"

script="create_view.sql"
tmpfile="/tmp/create_script.$$"


# start script.

rm -f ${script}
tablelist="${new_prefix}_point ${new_prefix}_line ${new_prefix}_polygon ${new_prefix}_roads"

# drop view
for table in $tablelist ; do
cat <<EOF >> ${script}
DROP VIEW ${table};
DELETE FROM geometry_columns where f_table_schema='public' and f_table_name='${table}' and f_geometry_column='way';
EOF
done

# create view script from existing tables.
cat <<EOF | ${psql} > ${tmpfile}
\\a
\\f ,
SELECT '' AS "CREATE VIEW ${new_prefix}_point AS SELECT",*,'' AS "FROM ${org_prefix}_point" from ${org_prefix}_point LIMIT 0;
SELECT '' AS "CREATE VIEW ${new_prefix}_line AS SELECT",*,'' AS "FROM ${org_prefix}_line" from ${org_prefix}_line LIMIT 0;
SELECT '' AS "CREATE VIEW ${new_prefix}_polygon AS SELECT",*,'' AS "FROM ${org_prefix}_polygon" from ${org_prefix}_polygon LIMIT 0;
SELECT '' AS "CREATE VIEW ${new_prefix}_roads AS SELECT",*,'' AS "FROM ${org_prefix}_roads" from ${org_prefix}_roads LIMIT 0;
\\q
EOF

# modify output
sed -ne 's/ SELECT,/ SELECT /;s/,FROM / FROM /;s/$/\;/;s/natural,/"natural",/;s/name:..,//g;s/\([a-z]*:[a-z]*\),/"\1",/g;/^CREATE/p;' ${tmpfile} |\
sed -e 's/name,/case when "name:ja" is null then regexp_replace(name, E'"'"' \\\\(.*\\\\)'"',''"') else "name:ja" end as name,/' >> ${script}

## if you want English version, use this
#sed -ne 's/ SELECT,/ SELECT /;s/,FROM / FROM /;s/$/\;/;s/natural,/"natural",/;s/name:..,//g;s/\([a-z]*:[a-z]*\),/"\1",/g;/^CREATE/p;' ${tmpfile} |\
#sed -e 's/name,/"name:en" as name,/' >> ${script}

rm ${tmpfile}

# geometry_columns
for table in $tablelist ; do
cat <<EOF >> ${script}
INSERT INTO geometry_columns (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, coord_dimension, srid, "type") SELECT '', 'public', '${table}', 'way', ST_CoordDim(way), ST_SRID(way), GeometryType(way) FROM ${table} LIMIT 1;
EOF
done

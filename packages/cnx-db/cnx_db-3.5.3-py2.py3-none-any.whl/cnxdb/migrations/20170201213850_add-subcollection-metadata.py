# -*- coding: utf-8 -*-
import os

from contextlib import contextmanager

from dbmigrator import super_user


@contextmanager
def open_here(filepath, *args, **kwargs):
    """open a file relative to this files location"""

    here = os.path.abspath(os.path.dirname(__file__))
    fp = open(os.path.join(here, filepath), *args, **kwargs)
    yield fp
    fp.close()


def up(cursor):
    """Add subcol metadata support to shredding and data upgrades"""

    with super_user() as super_cursor:
        super_cursor.execute("""
CREATE FUNCTION uuid5(namespace uuid, name text) RETURNS uuid
    LANGUAGE plpythonu
    AS $_$ import uuid; return uuid.uuid5(uuid.UUID(namespace), name) $_$;""")

        super_cursor.execute("""
CREATE OR REPLACE FUNCTION public.is_baked(col_uuid uuid, col_ver text)
 RETURNS boolean
 LANGUAGE sql
AS $function$
SELECT bool_or(is_collated)
    FROM modules JOIN trees
        ON module_ident = documentid
    WHERE uuid = col_uuid AND
          module_version(major_version, minor_version) = col_ver
$function$;""")

        with open_here('../archive-sql/schema/subcol_uuids_func.sql',
                       'rb') as f:
            super_cursor.execute(f.read())

        with open_here('../archive-sql/schema/shred_collxml.sql', 'rb') as f:
            super_cursor.execute(f.read())


def down(cursor):
    with super_user() as super_cursor:
        super_cursor.execute('drop function uuid5(uuid, text)')
        super_cursor.execute('drop function is_baked(uuid, text)')
        super_cursor.execute('drop function subcol_uuids(text, text)')

        with open_here('shred_collxml_20170201213850_pre.sql', 'rb') as f:
            super_cursor.execute(f.read())

-- ###
-- Copyright (c) 2013, Rice University
-- This software is subject to the provisions of the GNU Affero General
-- Public License version 3 (AGPLv3).
-- See LICENCE.txt for details.
-- ###

-- arguments: document_uuid:string; document_version:string
WITH RECURSIVE t(node, title, parent, path, value) AS (
  SELECT nodeid, title, parent_id, ARRAY[nodeid], documentid
  FROM trees tr, modules m
  WHERE m.uuid = %(document_uuid)s::uuid
  AND module_version(m.major_version, m.minor_version) = %(document_version)s
  AND tr.documentid = m.module_ident
  AND tr.parent_id IS NOT NULL
UNION ALL
  SELECT c1.nodeid, c1.title, c1.parent_id,
         t.path || ARRAY[c1.nodeid], c1.documentid
  FROM trees c1
  JOIN t ON (c1.nodeid = t.parent)
  WHERE not nodeid = any (t.path)
),

books(uuid, major_version, minor_version, title, revised, authors, authorUsernames) AS (
  SELECT m.uuid, m.major_version, m.minor_version, COALESCE(t.title, m.name), m.revised,
         (SELECT ARRAY(
           SELECT row_to_json(user_row) FROM
             (SELECT u.username,
             u.first_name as firstname, u.last_name as surname,
             u.full_name as fullname, u.title, u.suffix)

           as user_row)),
          m.authors
  FROM t
  JOIN modules m ON t.value = m.module_ident
  JOIN users as u on u.username = ANY(m.authors)
  WHERE t.parent IS NULL
  ORDER BY uuid, major_version desc, minor_version desc
),

page(authors) as (
  SELECT authors FROM modules m
  WHERE m.uuid = %(document_uuid)s::uuid
  AND module_version(m.major_version, m.minor_version) = %(document_version)s
),

top_books(title, ident_hash, short_ident_hash, authors, revised, authorUsernames) AS (
SELECT first(title),
       ident_hash(uuid, first(major_version), first(minor_version)),
       short_ident_hash(uuid, first(major_version), first(minor_version)),
       first(authors),
       first(revised),
       first(authorUsernames)
  FROM books GROUP BY uuid
)

SELECT tb.title, tb.ident_hash, tb.short_ident_hash as shortId, tb.authors, tb.revised
  FROM top_books tb, page p
  ORDER BY tb.authorUsernames = p.authors DESC, tb.revised DESC

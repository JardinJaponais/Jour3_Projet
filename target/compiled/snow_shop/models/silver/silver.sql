

with src as (
  select
    raw_line
  from "postgres"."PROD"."v_bronze_logs"
  where raw_line is not null
),

parsed as (
  select
    md5(raw_line) as event_hash,

    -- regexp_match renvoie text[] : (m)[1]=ip, (m)[2]=ident, etc.
    (m)[1] as ip,
    nullif((m)[2], '-') as ident,
    nullif((m)[3], '-') as username,

    -- ts_raw ex: "14/Jan/2026:00:20:02 " (note: espace avant ])
    -- on trim + split sur espace (si jamais timezone un jour)
    to_timestamp(split_part(trim((m)[4]), ' ', 1), 'DD/Mon/YYYY:HH24:MI:SS') as ts,

    (m)[5] as method,
    (m)[6] as path,
    (m)[7] as protocol,

    ((m)[8])::int as status,
    nullif((m)[9], '-')::int as bytes,

    nullif(nullif((m)[10], ''), '-') as referer,
    nullif(nullif((m)[11], ''), '-') as user_agent

  from (
    select
      raw_line,
      regexp_match(
        raw_line,
        $$^([^ ]+)[ ]+([^ ]+)[ ]+([^ ]+)[ ]+\[([^\]]*?)[ ]*\][ ]+"([^ ]+)[ ]+([^ ]+)[ ]+([^"]+)"[ ]+([0-9]{3})[ ]+([0-9]+|-)[ ]+"([^"]*)"[ ]+"([^"]*)"[ ]*$ $$
      ) as m
    from src
  ) x
  where m is not null
)

select
  event_hash,
  ip,
  ident,
  username,
  ts,
  method,
  path,
  protocol,
  status,
  bytes,
  referer,
  user_agent,
  now() as ingested_at
from parsed


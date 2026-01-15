
      
        
        
        delete from "postgres"."PROD"."SILVER_LOGS" as DBT_INTERNAL_DEST
        where (event_hash) in (
            select distinct event_hash
            from "SILVER_LOGS__dbt_tmp091002797738" as DBT_INTERNAL_SOURCE
        );

    

    insert into "postgres"."PROD"."SILVER_LOGS" ("event_hash", "ip", "username", "ts_visite", "method", "path_page", "protocol", "status_visite", "bytes", "referer", "user_agent", "ingested_at")
    (
        select "event_hash", "ip", "username", "ts_visite", "method", "path_page", "protocol", "status_visite", "bytes", "referer", "user_agent", "ingested_at"
        from "SILVER_LOGS__dbt_tmp091002797738"
    )
  
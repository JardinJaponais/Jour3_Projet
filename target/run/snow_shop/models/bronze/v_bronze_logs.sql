
  create view "postgres"."PROD"."v_bronze_logs__dbt_tmp"
    
    
  as (
    

select
    *
from "postgres"."PROD"."BRONZE_LOGS"
  );

  
    

  create  table "postgres"."PROD"."silver__dbt_tmp"
  
  
    as
  
  (
    SELECT * FROM 'access_2026-01-14_14-20-01.log';
  );
  
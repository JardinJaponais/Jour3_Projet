with silver_logs as (

    select * from {{ sources('prod', 'SILVER_LOGS') }}
    
),

renamed as (

    Select 
        ROW_NUMBER() OVER (ORDER BY path_page) AS page_id,
        path_page,
        bytes as taille_page
    from(
        select distinct path_page
        from silver_logs
    ) 

)

select * from renamed
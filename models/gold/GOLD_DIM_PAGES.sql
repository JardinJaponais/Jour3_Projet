with silver_logs as (

    select * from {{ ref('SILVER_LOGS') }}
    
),

renamed as (

    Select 
        ROW_NUMBER() OVER (ORDER BY path_page) AS page_id,
        path_page,
        bytes as taille_page_moyenne
    from(
        select distinct path_page, cast(avg(bytes) as int) as bytes
        from silver_logs
        group by path_page
    ) 

)

select * from renamed
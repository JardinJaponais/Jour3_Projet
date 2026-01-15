with silver_logs as (

    select * from {{ ref('SILVER_LOGS') }}
    
),

dim_pages as (

    select * from {{ ref('GOLD_DIM_PAGES') }}
    
),

renamed as (

    select
        event_hash as Visite_id,
        -- ip,
        -- ident,
        username,
        {{ get_date('ts_visite') }} as Date_Visite,
        {{ get_hms('ts_visite') }} as HMS_Visite,
        {{ get_hour('ts_visite') }} as Heure_Visite,
        -- method,
        page_id,
        -- protocol,
        status_visite as statut_id,
        {{ is_code('status_visite',200) }} as Erreur_Oui_Non,
        -- bytes,
        referer,
        {{ ua_support('user_agent') }} as Support,
        {{ ua_os('user_agent') }} as os,
        {{ ua_browser('user_agent') }} as navigateur,
        ingested_at as date_ajout_ligne
    
    from silver_logs as s

    Left Join dim_pages as p
    ON p.path_page = s.path_page
)

select * from renamed
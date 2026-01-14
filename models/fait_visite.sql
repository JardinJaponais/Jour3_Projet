with silver_logs as (

    select * from {{ sources('postgres_silver', 'silver_logs') }}
    
),


renamed as (

    select
        raw_line as Visite_id,
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
        user_agent, -- traiter 
        ingested_at as date_ajout_ligne
    
    from silver_logs as s

    Left Join dim_pages as p
    ON p.path_page = s.path_page
)

select * from renamed
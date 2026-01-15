with silver_logs as (

    select * from {{ sources('postgres_silver', 'silver_logs') }}
    
),

mapping_statut as (

    select * from {{ ref('mapping_statut') }}
    
),

renamed as (

    Select 
        s.status_visite AS statut_id,
        m.libelle as libelle_statut,
        m.categorie as categorie_staut
    from(
        select distinct status_visite
        from silver_logs
    ) as s
    left join mapping_statut as m
    ON m.code = s.status_visite

)

select * from renamed
-- renvoie la date année mois jour
{% macro get_date(champ_date) %}
    to_timestamp({{ champ_date }}, 'DD/Mon/YYYY:HH24:MI:SS')::date
{% endmacro %}

-- renvoie l'année
{% macro get_year(champ_date) %}
    EXTRACT(
        year FROM to_timestamp({{ champ_date }}, 'DD/Mon/YYYY:HH24:MI:SS')
    )
{% endmacro %}

-- renvoie l'heure
{% macro get_hour(champ_date) %}
    EXTRACT(
        hour FROM to_timestamp({{ champ_date }}, 'DD/Mon/YYYY:HH24:MI:SS')
    )
{% endmacro %}

-- renvoie heure minutes secondes   
{% macro get_hms(champ_date) %}
    to_char(
        to_timestamp({{ champ_date }}, 'DD/Mon/YYYY:HH24:MI:SS'),
        'HH24:MI:SS'
    )
{% endmacro %}
{% macro get_date(champ_date) %}
  ({{ champ_date }}::date)
{% endmacro %}

{% macro get_year(champ_date) %}
  extract(year from {{ champ_date }})
{% endmacro %}

{% macro get_hour(champ_date) %}
  extract(hour from {{ champ_date }})
{% endmacro %}

{% macro get_hms(champ_date) %}
  to_char({{ champ_date }}, 'HH24:MI:SS')
{% endmacro %}

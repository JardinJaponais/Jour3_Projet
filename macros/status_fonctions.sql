-- Fonction pour avoir code erreur ou non 
{% macro is_code(champ_code, value) %}
    CASE
        WHEN {{ champ_code }} = {{ value }} THEN true
        ELSE false
    END
{% endmacro %}
-- Fonction pour obtenir le support
{% macro ua_support(champ_useragent) %}
    case
        when {{ champ_useragent }} ilike '%mobile%'
          or {{ champ_useragent }} ilike '%android%'
          or {{ champ_useragent }} ilike '%iphone%'
          or {{ champ_useragent }} ilike '%ipad%'
            then 'Mobile'
        else 'Desktop'
    end
{% endmacro %}

-- Fonction pour obtenir l'OS
{% macro ua_os(champ_ua) %}
    case
        when {{ champ_ua }} ilike '%windows%' then 'Windows'
        when {{ champ_ua }} ilike '%macintosh%' then 'MacOS'
        when {{ champ_ua }} ilike '%linux%' then 'Linux'
        when {{ champ_ua }} ilike '%android%' then 'Android'
        when {{ champ_ua }} ilike '%iphone%'
          or {{ champ_ua }} ilike '%ipad%' then 'iOS'
        else 'Other'
    end
{% endmacro %}

-- Fonction pour obtenir le navigateur
{% macro ua_browser(champ_ua) %}
    case
        when {{ champ_ua }} ilike '%edg/%' then 'Edge'
        when {{ champ_ua }} ilike '%opr/%'
          or {{ champ_ua }} ilike '%opera%' then 'Opera'
        when {{ champ_ua }} ilike '%chrome/%' then 'Chrome'
        when {{ champ_ua }} ilike '%firefox/%' then 'Firefox'
        when {{ champ_ua }} ilike '%safari%'
          and {{ champ_ua }} not ilike '%chrome%' then 'Safari'
        else 'Other'
    end
{% endmacro %}
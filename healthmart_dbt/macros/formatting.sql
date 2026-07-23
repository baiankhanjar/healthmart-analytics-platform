{% macro safe_percentage(numerator, denominator) %}

round(
    safe_divide(
        {{ numerator }},
        {{ denominator }}
    ) * 100,
    2
)

{% endmacro %}
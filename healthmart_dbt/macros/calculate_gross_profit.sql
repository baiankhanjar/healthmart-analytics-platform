{% macro calculate_gross_profit(line_total, quantity, cost_price) %}

    round(
        {{ line_total }} - ({{ quantity }} * {{ cost_price }}),
        2
    )

{% endmacro %}
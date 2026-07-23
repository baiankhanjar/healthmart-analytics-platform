{% macro sale_category(sales_amount) %}

case
    when {{ sales_amount }} < 20 then 'Small Sale'
    when {{ sales_amount }} <= 100 then 'Medium Sale'
    else 'Large Sale'
end

{% endmacro %}
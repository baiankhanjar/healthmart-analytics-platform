{% test accepted_list_values(model, column_name, allowed_values) %}

select *
from {{ model }}
where {{ column_name }} is not null
  and {{ column_name }} not in (
      {% for value in allowed_values %}
          '{{ value }}'{% if not loop.last %}, {% endif %}
      {% endfor %}
  )

{% endtest %}
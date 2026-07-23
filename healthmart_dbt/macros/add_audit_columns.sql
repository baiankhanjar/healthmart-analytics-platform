{% macro add_audit_columns() %}

current_timestamp() as loaded_at,
'healthmart' as source_system

{% endmacro %}
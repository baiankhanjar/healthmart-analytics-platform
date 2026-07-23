{% snapshot product_snapshot %}

{{
    config(
        target_schema='healthmart_snapshots',
        unique_key='product_id',
        strategy='check',
        check_cols=['cost_price', 'unit_price', 'active_status']
    )
}}

select
    product_id,
    product_name,
    category,
    brand,
    supplier_id,
    cost_price,
    unit_price,
    active_status
from {{ ref('stg_products') }}

{% endsnapshot %}
{{ config(materialized='ephemeral') }}

select
    product_id,
    product_name,
    category,
    brand,
    cost_price,
    unit_price,

    round(unit_price - cost_price, 2) as unit_profit,

    {{ safe_percentage("unit_price - cost_price", "unit_price") }}
    as profit_margin_percentage

from {{ ref('stg_products') }}
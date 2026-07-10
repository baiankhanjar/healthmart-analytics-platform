select
    {{ dbt_utils.generate_surrogate_key(['product_id']) }} as product_key,
    product_id,
    product_name,
    category,
    brand,
    supplier_id,
    cost_price,
    unit_price,
    active_status
from {{ ref('stg_products') }}
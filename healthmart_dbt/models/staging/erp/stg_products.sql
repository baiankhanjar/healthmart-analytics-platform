select
    product_id,
    product_name,
    category,
    brand,
    supplier_id,
    cost_price,
    unit_price,
    active_status
from {{ source('healthmart_raw', 'products') }}
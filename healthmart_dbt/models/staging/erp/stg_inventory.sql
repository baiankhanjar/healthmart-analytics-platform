select
    inventory_id,
    store_id,
    product_id,
    quantity_on_hand,
    reorder_level,
    last_updated_date
from {{ source('healthmart_raw', 'inventory') }}
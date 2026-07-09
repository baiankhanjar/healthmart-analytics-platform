select
    transaction_item_id,
    transaction_id,
    product_id,
    quantity,
    unit_price,
    line_total
from {{ source('healthmart_raw', 'transaction_items') }}
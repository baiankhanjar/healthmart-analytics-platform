select
    transaction_id,
    customer_id,
    store_id,
    transaction_date,
    loaded_at,
    payment_method,
    transaction_total
from {{ source('healthmart_raw', 'transactions') }}
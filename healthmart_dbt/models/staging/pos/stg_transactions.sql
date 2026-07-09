select
    transaction_id,
    customer_id,
    store_id,
    transaction_date,
    payment_method,
    transaction_total
from {{ source('healthmart_raw', 'transactions') }}
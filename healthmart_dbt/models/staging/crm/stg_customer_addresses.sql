select
    address_id,
    customer_id,
    address_type,
    street_address,
    city,
    state,
    zip_code
from {{ source('healthmart_raw', 'customer_addresses') }}
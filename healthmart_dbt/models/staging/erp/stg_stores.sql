select
    store_id,
    store_name,
    city,
    state,
    region,
    store_type,
    open_date,
    active_status
from {{ source('healthmart_raw', 'stores') }}
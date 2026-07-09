select
    supplier_id,
    supplier_name,
    supplier_type,
    country,
    state,
    city,
    contact_email,
    phone,
    active_status
from {{ source('healthmart_raw', 'suppliers') }}
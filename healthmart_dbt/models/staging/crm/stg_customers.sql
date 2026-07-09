select
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    gender,
    birth_date,
    signup_date
from {{ source('healthmart_raw', 'customers') }}
select
    {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_key,
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    gender,
    birth_date,
    signup_date
from {{ ref('stg_customers') }}
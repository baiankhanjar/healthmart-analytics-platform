select
    {{ dbt_utils.generate_surrogate_key(['store_id']) }} as store_key,
    store_id,
    store_name,
    city,
    state,
    region,
    store_type,
    open_date,
    active_status
from {{ ref('stg_stores') }}
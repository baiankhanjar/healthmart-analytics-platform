select
    loyalty_id,
    customer_id,
    loyalty_tier,
    points_balance,
    enrollment_date,
    account_status
from {{ source('healthmart_raw', 'loyalty_accounts') }}
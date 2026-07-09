select
    preference_id,
    customer_id,
    email_opt_in,
    sms_opt_in,
    preferred_language,
    preferred_channel,
    last_updated_date
from {{ source('healthmart_raw', 'customer_preferences') }}
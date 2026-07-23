

select
    {{ dbt_utils.generate_surrogate_key(['sales.transaction_item_id']) }} as sales_key,

    sales.transaction_item_id,
    sales.transaction_id,

    dates.date_key,
    customers.customer_key,
    stores.store_key,
    products.product_key,

    sales.quantity,
    sales.unit_price,
    sales.line_total as sales_amount,
    round(sales.quantity * sales.cost_price, 2) as cost_amount,
    sales.gross_profit

from {{ ref('int_transaction_items_enriched') }} as sales



left join {{ ref('dim_date') }} as dates
    on sales.transaction_date = dates.full_date

left join {{ ref('dim_customers') }} as customers
    on sales.customer_id = customers.customer_id

left join {{ ref('dim_stores') }} as stores
    on sales.store_id = stores.store_id

left join {{ ref('dim_products') }} as products
    on sales.product_id = products.product_id
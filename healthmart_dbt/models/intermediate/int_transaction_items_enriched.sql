select
    ti.transaction_item_id,
    ti.transaction_id,
    t.customer_id,
    t.store_id,
    t.transaction_date,
    ti.product_id,
    p.product_name,
    p.category,
    p.brand,
    ti.quantity,
    ti.unit_price,
    p.cost_price,
    ti.line_total,
    round(ti.line_total - (ti.quantity * p.cost_price), 2) as gross_profit
from {{ ref('stg_transaction_items') }} ti
left join {{ ref('stg_transactions') }} t
    on ti.transaction_id = t.transaction_id
left join {{ ref('stg_products') }} p
    on ti.product_id = p.product_id
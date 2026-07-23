with item_totals as (

    select
        transaction_id,
        round(sum(line_total), 2) as calculated_transaction_total
    from {{ ref('stg_transaction_items') }}
    group by transaction_id

)

select
    transactions.transaction_id,
    transactions.transaction_total,
    item_totals.calculated_transaction_total

from {{ ref('stg_transactions') }} as transactions

left join item_totals
    on transactions.transaction_id = item_totals.transaction_id

where round(transactions.transaction_total, 2)
      != item_totals.calculated_transaction_total
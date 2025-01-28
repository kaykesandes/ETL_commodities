-- models/staging/stg_movimentacao_commodities.sql

with source as (
    select
        data,
        symbol,
        action,
        quantity
    from
        {{source("commodities",'movimentacao_commodities')}}
),

renamed as (
    select
        cast(data as date) as data,
        symbol as simbolo,
        action as acao,
        quantity as quantidade
    from source
)

select * from renamed
# Bookstore

* users

| UserId  | HasStore | UserName | Fund | Password |
| ------- | -------- | -------- | ---- | -------- |
| Primary |          |          |      |          |

* 商铺

| StoreId | UserId      | balance  |
| ------- | ----------- | -------- |
| Primary | Foreign key | 商户余额 |

| StoreId | BookId  | bookinfo 中的一系列单值属性 | tag  | count |
| ------- | ------- | --------------------------- | ---- | ----- |
| Primary | Primary |                             |      |       |

| BookId  | StoreId | picture |
| ------- | ------- | ------- |
| Primary | Primary |         |

上述，那么所有的书都有不同的ID

* 订单

| OrderId | UserId | StoreId | status                                     |
| ------- | ------ | ------- | ------------------------------------------ |
| Primary |        |         | 已下单、已付款、已发货、已确认收货、订单失败 |

| order_id | book_id | count |
| -------- | ------- | ----- |
| Primary  |         |       |

# 是否需要考虑将图片另存
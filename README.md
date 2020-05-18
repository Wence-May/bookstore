

[TOC]



# 基于PostgreSQL的线上书城

## 功能简介

本项目是一个基于PostgreSQL+SqlAlchemy的线上书城网站后端，可供多人在线交易。网站支持书商在上面开商店，购买者可通过网站搜索、购买；买家和买家都可以注册自己的用户账号，一个用户可以开一个或多个网上商店；买家可以为自已的账户充值，在任意商店购买图书，购买支持”下单->付款->发货->收货“流程。应用场景如下：

1. 用户进行注册、登录、登出、注销，在登入时系统为用户产生标记身份、登入时长的token；

2. 买家用户可以进行充值、下单、付款的操作，订单创建后后超时未付款将自动关闭；

3. 卖家可创建（多家）店铺、填加书籍信息及描述、增加库存，为已付款的订单发货；

4. 买家可对已发货的订单确认收货，确认收货后的订单报酬进入商店的账户；

5. 卖家可以将其名下所有商店账户的资金转入个人账户；

6. 用户可以通过关键字搜索，参数化的搜索方式； 如搜索范围包括，题目，标签，目录，内容；全站搜索或是当前店铺搜索。 如果显示结果较大，需要分页 (使用全文索引优化查找)；

7. 用户可以查看自已的历史订单，查看某个订单状态，用户也可以取消订单。

   

1. 激活环境

   ```shell
   . venv/bin/activate
   ```

2. 初始化数据库

   运行`app/models/create_db.py`文件

   ！每次测试前都需要删除数据库然后重新用`create_db.py` 初始化

3. 运行游戏

   ```python
   python3 main.py
   ```

4. 测试

   ```shell
   # 运行测试并生成覆盖率报告
   bash script/test.sh
   ```

## 项目结构

```python
|bookstore
	|----app
            |----static
                    |--	pictures	#静态存储图片
            |----model
                    |------	_init_.py
                    |------	buyer.py
                    |------	seller.py
                    |------	order.py
                    |------	search.py
                    |------	create_db.py# 初始化数据库内容（每次测试前都需要运行）
                    |------	error.py
                    |------	Global.py
                    |------	insert_db.py
                    |------	
            |----view
                    |------	_init_.py
                    |------	auth.py
                    |------	buyer.py
                    |------	seller.py
                    |------	search.py
            |------	config.py
            |------	main.py 		
    |----fe								# 路由接收请求+对数据库操作的定义
            |----access
        			|------	_init_.py
            		|------	auth.py
                	|------	book.py
                    |------	buyer.py
                    |------	seller.py
                    |------	order.py
                    |------	new_buyer.py
                    |------	new_seller.py
            |----bench
            |----data
            |----test
                    |------	_init_.py
                	|------	gen_book_data.py
                    |------	test_add_book.py
                    |------	test_add_funds.py
                   	|------ ......
            |------conftest.py						# 配置测试服务器
            |------conf.py
	|----scripts
    		|----html
        	|------test.sh
```

## 数据库设计

### ER图

### ![image-20191231003246537](C:/Users/lenovo/Documents/WeChat Files/Mjy_1138208075/FileStorage/File/2019-12/第二次作业实验报告 耿岱琳.assets/image-20191231003246537.png)

### 关系模式

#### ER图直接衍生关系模式

ER图直接衍生出的关系图由表**Books，Oders，Stores，Buyers，Sellers**构成，每个表的属性如上图所示。

其中，**Books**是**Stores**的弱实体类，售卖关系是识别联系，他们构成独占联系。这是因为每个商店里面有很多本书，但书的id并不包含商店id，不同店铺可能有相同的书。所以book_id不足以作为书籍的码，而需要依赖于store_id来唯一地识别书籍。

**Buyers**和**Sellers**是用户的ISA子类，它们拥有相同的属性：user_id, balance, password。由于是ISA子类，{**Buyers**} $\cap$ {**Sellers**} $\neq 0 $，卖家和买家有身份重合的情况，这契合”用户可自行注册商店进行营业“的功能。



#### 对关系模式进行优化

根据功能对关系模式进行优化：

1. 

   

优化后的数据库schema如下，

![image-20191231022512350](数据库final6#348.assets/image-20191231022512350.png)

用ER图表示为：![image-20191231024908414](数据库final6#348.assets/image-20191231024908414.png)

**Users**：

| UserId      | UserName | HaveStore | Balance | Password | Terminal |
| ----------- | -------- | --------- | ------- | -------- | -------- |
| primary key |          |           |         |          |          |



**Stores**：

|   StoreId   |   UserId    | Balance |
| :---------: | :---------: | :-----: |
| primary key | foreign key |         |



**StoreBooks**：

|   StoreId   | Stock |
| :---------: | :---: |
| foreign key |       |

| BookId      | Title | Author | Publisher | OriginalTitle | Translator | PubYear | Pages |
| ----------- | :---: | ------ | --------- | ------------- | ---------- | ------- | ----- |
| primary key |       |        |           |               |            |         |       |

| Price | Binding | Isbn | AuthorIntro | BookIntro | Content | Tags | PictureId |
| ----- | ------- | ---- | ----------- | --------- | ------- | ---- | --------- |
|       |         |      |             |           |         |      |           |

**BookPictures**：

| PictureId   | BookId | Address                       |
| ----------- | ------ | ----------------------------- |
| Primary key |        | 图片命名：userId + 上传时间戳 |

**Orders**：

|   OderId    |   StoreId   |   UserId    | Status | Amount | Deadline |
| :---------: | :---------: | :---------: | :----: | :----: | :------: |
| primary key | foreign key | foreign key |        |        |          |

**OrderBooks**：

|   OrderId   | BookId | Count |
| :---------: | :----: | :---: |
| foreign key |        |       |



共同主键：uid, tid, tnum

wearing：记录用户是否佩戴宝物Treasure: tvalue

price：默认值为-1，即未被出售的宝物的price属性为-1

### 索引

1. Treasure.tname

   后面可以看到，对宝物的操作基本上都是包含 根据宝物名称`tname`查询宝物id`tid`这一步，而如果把宝物信息全部合并进入Own表的话，由于一种宝物可能会被非常多个用户拥有，会产生大量的冗余，所以可以在`Treasure.tname`上建立索引，因为通过该属性进行地查询非常频繁，且对Treasure表的修改很少。

2. Treasure.tvalue

   寻宝时需要根据用户的“运气”`uluck`寻找对应价值的宝物，而寻宝是每日任务，该查询很频繁，而对宝物库的修改相比之下非常少，所以在`Treasure.tvalue`上建索引。

## 对数据库的操作


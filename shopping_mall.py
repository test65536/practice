salary = input('Input your salary:')
if salary.isdigit():
    salary = int(salary)
else:
    exit('Invalid data type!')

welcome_msg = 'Welecome to Alxe Shopping Mall'.center(50,'-')
print(welcome_msg)

exit_flag = False
product_list = [
    ('iPhone 7', 3899),
    ('iPhone 8', 5099),
    ('Mac Pro', 21700),
    ('iMac', 10200),
    ('Mac mini', 8899),
    ('iPad mini', 8099),
]

shop_car = []
while not exit_flag:
    print('product list'.center(50,'-'))
    for item in enumerate(product_list):
        index = item[0]
        product_name = item[1][0]
        product_price = item[1][1]
        print(index, ':', product_name, product_price)

    user_choice = input('Which product do you want to buy?[q=quit,c=check]')
    if user_choice.isdigit(): # 是否是商品代码
        user_choice = int(user_choice)
        if user_choice < len(product_list):
            product_item = product_list[user_choice]
            if product_item[1] <= salary:  # 钱够了
                shop_car.append(product_item)  # 放入购物车
                salary -= product_item[1]  # 扣钱
                print('[%s] is added into your shop car, your balance is [%s]'%
                      (product_item, salary))
            else:  # 买不起
                print('Your balance is \033[31;1m[%s]\033[0m, cannot afford this!' % salary)
        else:
            if user_choice == 'q' or user_choice == 'quit':
                print('Your item is as below'.center(50,'*'))
                for item in shop_car:
                    print(item)
                print('END'.center(40, '*'))
                print('Your balance is [%s]' % salary)
                print('GOOD BYE')
                exit_flag = True
            elif user_choice == 'c' or user_choice == 'check':
                print('Your item is as below'.center(50,'*'))
                for item in shop_car:
                    print(item)
                print('END'.center(40, '*'))
                print('Your balance is \033[41;1m[%s]\033[0m' % salary)
                print('GOOD BYE')

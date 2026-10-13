#замыкания
def outer():
    num = 5

    def inner ():
        nonlocal num
        num +=1
        print(num)

    return inner

fu = outer()

fu()
fu()
fu()
fu()
fu()
fu()
fu()
fu()

#задача написать робота пицемейкера
# робот должен принимать заказ от пользователя (учитывать что пользователь может придти не один)
# робот должен предоставить разное меню для разновозрастных пользователей, после идентификации
# пользователя и определения тех позиций которые пользователь хочет купить робот должен спросить,
# как будет проходить оплата (наличнкой или кртой) в случии налички
# пользователь вводит число боле суммы, а робот выдает сдачу

def robot_cash_register():
    total = 0
    def add_money(amount):
        nonlocal total
        total += amount
        print(f"[Касса] +{amount} руб. Итого: {total} руб.")
        return total
    return add_money

update_cash = robot_cash_register()

def get_menu(age):
    if age <= 12:
        print("\nДетское меню:")
        return {"1": ("Мини-Маргарита", 150), "2": ("Мини-Пепперони", 180), "3": ("Сладкая", 200)}
    print("\nВзрослое меню:")
    return {"1": ("Пепперони", 450), "2": ("Маргарита", 400), "3": ("4 Сыра", 500), "4": ("Мясная", 550)}

def pizza_robot():
    print("Привет! Я робот-пицмейкер.")
    while True:
        try:
            guests = int(input("Сколько вас? "))
            if guests > 0: break
        except ValueError: pass

    total_bill = 0
    for i in range(1, guests + 1):
        print(f"\n--- Гость {i} ---")
        while True:
            try:
                age = int(input("Ваш возраст: "))
                if age > 0: break
            except ValueError: pass

        menu = get_menu(age)
        for k, (n, p) in menu.items():
            print(f"  {k}. {n} - {p} руб.")

        guest_total = 0
        while True:
            c = input("Заказ (номер или 0 - конец): ")
            if c == '0':
                if guest_total == 0: continue
                break
            if c in menu:
                n, p = menu[c]
                guest_total += p
                print(f"Добавлено: {n} ({p} руб.)")
            else:
                print("Нет такого пункта.")
        print(f"Итог по гостю {i}: {guest_total} руб.")
        total_bill += guest_total

    print(f"\nОбщий счет: {total_bill} руб.")
    while True:
        pay = input("Оплата (наличные/карта): ").strip().lower()
        if pay in ['наличные', 'нал']: is_cash = True; break
        if pay in ['карта', 'картой']: is_cash = False; break

    if is_cash:
        while True:
            try:
                given = float(input(f"Внесите сумму (не менее {total_bill}): "))
                if given >= total_bill:
                    print(f"Сдача: {given - total_bill} руб.")
                    update_cash(total_bill)
                    break
            except ValueError: pass
    else:
        print("Оплата картой принята.")
        update_cash(total_bill)

    print("Спасибо! Пицца готовится.")

pizza_robot()

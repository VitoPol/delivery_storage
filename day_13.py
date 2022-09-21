from abc import ABC, abstractmethod
from re import search


class Storage(ABC):
    """
    Абстрактный класс для помещения
    """

    def __init__(self, items: dict, capacity: int):
        self._items = items
        self._capacity = capacity

    @abstractmethod
    def add(self, item: str, quantity: int) -> bool:
        """
        Добавляет товар, если это возможно
        :param item: товар
        :param quantity: количество
        :return: Успешность добавления
        """
        if self._get_free_space() < quantity:
            return False
        elif not self._items.get(item):
            self._items.update({item: quantity})
        else:
            self._items[item] += quantity
        return True

    @abstractmethod
    def remove(self, item: str, quantity: int) -> bool:
        """
        Удаляет товар, если это возможно
        :param item: товар
        :param quantity: количество
        :return: Успешность удаления
        """
        try:
            if self._items[item] >= quantity:
                self._items[item] -= quantity
                if self._items[item] == 0:
                    self._items.pop(item)
                return True
        finally:
            return False

    def _get_free_space(self) -> int:
        """
        Считает количество свободных мест
        :return: Возвращает количество свободных мест
        """
        summ = 0
        for quantity in self._items.values():
            summ += quantity
        return self._capacity - summ

    @property
    def items(self) -> dict:
        """
        :return: возвращает сожержание склада в словаре {товар: количество}
        """
        return self._items

    def _get_unique_items_count(self) -> int:
        """
        :return: возвращает количество уникальных товаров
        """
        return len(self._items.keys())


class Store(Storage):  # Склад
    """
    Класс склада
    """

    def __init__(self, items: dict = {}, capacity: int = 100):
        super().__init__(items, capacity)

    def add(self, item: str, quantity: int) -> bool:
        """
        Добавляет товар, если это возможно
        :param item: товар
        :param quantity: количество
        :return: Успешность добавления
        """
        return super().add(item, quantity)

    def remove(self, item: str, quantity: int) -> bool:
        """
        Удаляет товар, если это возможно
        :param item: товар
        :param quantity: количество
        :return: Успешность удаления
        """
        return super().remove(item, quantity)


class Shop(Storage):  # Магазин
    """
    Класс магазина
    """

    def __init__(self, items: dict = {}, capacity: int = 20):
        super().__init__(items, capacity)

    def remove(self, item: str, quantity: int) -> bool:
        """
        Удаляет товар, если это возможно
        :param item: товар
        :param quantity: количество
        :return: Успешность удаления
        """
        return super().remove(item, quantity)

    def add(self, item: str, quantity: int) -> bool:
        """
        Добавляет товар, если это возможно
        :param item: товар
        :param quantity: количество
        :return: Успешность добавления
        """
        if self._get_unique_items_count() == 5 and not self._items.get(item):
            return False
        return super().add(item, quantity)


class Request():
    """
    Класс запросов
    """

    def __init__(self, text: str):
        self._quantity, self._product, self._from_, self._to = self.search_text(text)

    def __repr__(self):
        return repr(f'Доставить {self._quantity} {self._product} из {self._from_} в {self._to}')

    @property
    def quantity(self) -> int:
        """
        :return: Возвращает количество товаров
        """
        return self._quantity

    @property
    def product(self) -> str:
        """
        :return: Возвращает наименование продукта
        """
        return self._product

    @property
    def from_(self) -> str:
        """
        :return: Возвращает наименование хранилища откуда идёт товар
        """
        return self._from_

    @property
    def to(self) -> str:
        """
        :return: Возвращает наименование хранилища куда идёт товар
        """
        return self._to

    def search_text(self, text: str) -> tuple:
        """
        С помощью регулярного выражения выбирает нужные слова
        :param text: Текст вводимый пользователем
        :return: Возвращает количество товара, наименование товара, с какого хранилища и на какое
        """
        match = search(r'^доставить (\d+) ([а-я]+) из ([а-я]+) в ([а-я]+)$', text)
        return int(match[1]), match[2], match[3], match[4]


def choise(from_: str, to: str, store: Store, shop: Shop) -> tuple:
    """
    Опередяет откуда и куда везётся товар
    :param from_: Откуда
    :param to: Куда
    :param store: Объект склада
    :param shop: Объект магазин
    :return: Возвращает кортеж
    """
    if from_ == 'склад' and to == 'магазин':
        return store, shop
    elif from_ == 'магазин' and to == 'склад':
        return shop, store
    else:
        return None, None


def main():
    goods_in_store = {'печеньки': 3, 'собака': 4, 'коробка': 5, 'яблоко': 6, 'дерево': 59, 'апельсин': 20}
    goods_in_shop = {'печеньки': 2, 'собака': 5}
    store = Store(goods_in_store)
    shop = Shop(goods_in_shop)
    print('Если хотите остановить перемещения, то напишите "стоп"')
    while True:
        print('\nНа складе сейчас имеется:')
        [print(k, v) for k, v in store.items.items()]
        print('\nВ магазине сейчас имеется:')
        [print(k, v) for k, v in shop.items.items()]
        text = input('\nВведите запрос в формате, "Доставить 3 печеньки из склад в магазин"\n').lower().strip()
        if text == 'стоп':
            break
        try:
            request = Request(text)
        except:
            print('Не верный запрос, напишите заново\n')
            continue
        from_storage, to_storage = choise(request.from_, request.to, store, shop)
        if not from_storage or not to_storage:
            print('Не верный запрос, напишите заново\n')
            continue
        print(f'Курьер идёт за {request.quantity} {request.product} из {request.from_}')
        if not from_storage.remove(request.product, request.quantity):
            print('Такого товара нет или не хватает')
            continue
        print(f'Курьер везёт {request.quantity} {request.product} с {request.from_} в {request.to}')
        if not to_storage.add(request.product, request.quantity):
            print('Товар не поместился :(\nКурьер отвёз его обратно')
            from_storage.add(request.product, request.quantity)
            continue
        print(f'Курьер доставил {request.quantity} {request.product} в {request.to}')


if __name__ == '__main__':
    main()

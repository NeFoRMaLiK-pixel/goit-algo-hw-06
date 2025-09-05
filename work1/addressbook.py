from collections import UserDict
import re

# Базовый класс для полей
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Поле для имени контакта
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Имя не может быть пустым.")
        super().__init__(value)


# Поле для телефона (10 цифр)
class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Номер телефона должен содержать 10 цифр.")
        super().__init__(value)


# Запись контакта (имя и телефоны)
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))  # Добавление телефона

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Телефон {phone} не найден.")

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            try:
                self.add_phone(new_phone)  # Проверка валидности нового номера
                self.remove_phone(old_phone)
            except ValueError as e:
                raise ValueError(f"Ошибка при замене телефона: {e}")
        else:
            raise ValueError(f"Телефон {old_phone} не найден.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join([p.value for p in self.phones])
        return f"Имя: {self.name.value}, Телефоны: {phones}"


# Адресная книга (коллекция записей)
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record  # Добавление записи

    def find(self, name):
        return self.data.get(name, None)  # Поиск записи

    def delete(self, name):
        if name in self.data:
            del self.data[name]  # Удаление записи
        else:
            raise ValueError(f"Контакт {name} не найден.")

    def __str__(self):
        return "\n".join([str(record) for record in self.data.values()])


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print("\nАдресная книга:")
    print(book)

    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")
    print("\nОбновленная запись Джона:")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"\nНайденный телефон: {found_phone}")

    book.delete("Jane")
    print("\nАдресная книга после удаления Джейн:")
    print(book)
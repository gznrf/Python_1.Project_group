## init_storage() — создай файл, если его нет;
## add_record(record) — добавь новую запись;
## get_all_records() — получи список всех записей;
## update_record(id, new_data) — обнови запись по id;
## delete_record(id) — удали запись по id;
## (Дополнительно) find_by_type(type) — получи все записи определённого типа
import os.path
import json



class Storage:
    PATH = "../repository/storage.json"

    def init_storage(self):
        if os.path.exists(self.PATH):
            return False
        try:
            storage = open("../repository/storage.json", "x")
        except:
            return False
        return True

    def add_record(self, record):
        try:
            with open(self.PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

            data.append(record)

            with open(self.PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except:
            return False
        
        return True

    def get_all_records(self):
        try:
            with open(self.PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
        except: 
            return ""
        
        return data

    def update_record(id, new_data):
        return 0

    def delete_record(id):
        return 0

    def find_by_type(type):
        return 0

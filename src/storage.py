import os.path
import json

class Storage:
    __PATH = "../repository/storage.json"

    ## Проверяет существует ли файл хранилище
    def __is_exists(self):
        if os.path.exists(self.PATH):
            return True
        return False
    
    # получение всех данных из файла
    def __get_all_data(self):
        with open(self.__PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    
    # сохранение всех файлов в файле
    def __save_data(self, data):
        with open(self.__PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    ## init_storage() — создай файл, если его нет;
    def init_storage(self):
        if self.__is_exists():
            return True
        try:
            storage = open(self.__PATH, "x")
        except:
            return False
        return True

    ## add_record(record) — добавь новую запись;
    def add_record(self, record):
        if not self.__is_exists():
            return False
        try:
            data = self.__get_all_data()

            data.append(record)

            self.__save_data()
        except:
            return False
        
        return True

    ## get_all_records() — получи список всех записей;
    def get_all_records(self):
        if not self.__is_exists():
            return ""
        try:
            data = self.__get_all_data()
        except: 
            return ""
        
        return data

    ## update_record(id, new_data) — обнови запись по id;
    def update_record(id, new_data, self):
        if not self.__is_exists():
            return False
        
        data = self.__get_all_data()
        
        if not id in data:
            return False
        
        try:
            data[id] = new_data

            self.__save_data()
        except:
            return False

        return True

    ## delete_record(id) — удали запись по id;
    def delete_record(id, self):
        if not self.__is_exists():
            return False
        
        data = self.__get_all_data()

        if not id in data:
            return False
        
        try:
            del data[id]
            self.__save_data()
        except:
            return False

        return True
        

    ## (Дополнительно) find_by_type(type) — получи все записи определённого типа
    def find_by_type(type, self):
        if not self.__is_exists():
            return False
        
        data = self.__get_all_data()

        records_with_curr_type = {
            record_id: record
            for record_id, record in data.items()
            if record.get("type") == type
        }

        return records_with_curr_type
    ## Очищает хранилище
    def clear(self):
        with open(self.__PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)



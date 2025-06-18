import storage

class test:

    storage_obj = storage.Storage()

    def first_test(self):
        id = "123"
        record = {
            "123":{
                "type": "annuity",
                "input": {"sum": 250000, "rate": 0.11, "term": 24},
                "result": 300000,
                "date": "2024-06-06",
                "comment": "Платёж по ипотеке"
            },
        }
        new_record = {
            "123":{
                "type": "annuity",
                "input": {"sum": 250000, "rate": 0.11, "term": 24},
                "result": 300000,
                "date": "2024-06-06",
                "comment": "Платёж по ипотеке"
            },
        }

        type = "qwe"

        first_record_with_type_qwe = {
            "123":{
                "type": "qwe",
                "input": {"sum": 250000, "rate": 0.11, "term": 24},
                "result": 300000,
                "date": "2024-06-06",
                "comment": "Платёж по ипотеке"
            },
        }
        second_record_with_type_qwe = {
            "123":{
                "type": "qwe",
                "input": {"sum": 250000, "rate": 0.11, "term": 24},
                "result": 300000,
                "date": "2024-06-06",
                "comment": "Платёж по ипотеке"
            },
        }


        if not self.storage_obj.add_record(record):
            return "first test failed"
        if self.storage_obj.get_all_records() == "":
            return "first test failed"
        if not self.storage_obj.update_record(new_record):
            return "first test failed" 
        if not self.storage_obj.delete_record(id):
            return "first test failed" 
        
        self.storage_obj.add_record(first_record_with_type_qwe)
        self.storage_obj.add_record(second_record_with_type_qwe)

        if not self.storage_obj.find_by_type(type):
            return "first test failed"  
        
        self.storage_obj.clear()

        return "first test passed"
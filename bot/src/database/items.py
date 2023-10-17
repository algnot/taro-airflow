from .base import Base
from .pokemon import Pokemon
from random import randint, random


class Items (Base):
    _name = "Items"
    
    def __init__(self):
        super().__init__()
        
    def get_daily_rate_item(self):
        return self.execute("""
            SELECT *
            FROM public.daily_rate_table
            WHERE active = TRUE
            ORDER BY RANDOM() * rate DESC
            LIMIT 1;
        """)[0]
        
    def get_abilities_of_item(self, name:str):
        return self.execute(f"""
            SELECT *
            FROM public.item_abilities_rate_table
            WHERE item_key = '{name}'
        """)
        
    def map_and_sum_items(self, item_list):
        item_mapping = {}
        
        for item in item_list:
            key = (item["item_key"], item["increse_table"], item["increse_key"])
            if key not in item_mapping:
                item_mapping[key] = item.copy()
                item_mapping[key]["value"] = 0
            
            item_mapping[key]["value"] += item["value"]
        
        return list(item_mapping.values())
    
    def get_random_abilities_of_item(self, name:str, amout: int):
        item_abilities = self.get_abilities_of_item(name)
        
        result = []
        
        for _ in range(amout):
            for abilitie in item_abilities:
                chance = abilitie["chance"]
                
                if chance <= randint(1, 100):
                    continue
                
                value = self.random_float(abilitie["min_value"], abilitie["max_value"])
                
                result.append({
                    "item_key": abilitie["item_key"],
                    "increse_table": abilitie["increse_table"],
                    "increse_key": abilitie["increse_key"],
                    "value": value,
                    "amount": amout
                })
            
        return self.map_and_sum_items(result)
    
    def random_float(self, min, max, digit=4):
        return round(random() * (max - min) + min, digit)

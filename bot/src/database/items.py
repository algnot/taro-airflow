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
        
    def get_random_abilities_of_item(self, name:str, amout: int):
        item_abilities = self.get_abilities_of_item(name)
        
        result = []
        for abilitie in item_abilities:
            chance = abilitie["chance"]
            if chance <= randint(1, 100):
                continue
            result.append({
                "item_key": abilitie["item_key"],
                "increse_table": abilitie["increse_table"],
                "increse_key": abilitie["increse_key"],
                "value": self.random_float(abilitie["min_value"], abilitie["max_value"]) * amout,
                "amount": amout
            })
            
        return result
    
    def random_float(self, min, max, digit=2):
        return round(random() * (max - min) + min, digit)

from .base import Base
from .pokemon import Pokemon


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


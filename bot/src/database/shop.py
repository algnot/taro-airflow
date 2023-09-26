from .base import Base


class Shop(Base):
    
    def __init__(self):
      super().__init__()
      
    def get_shop_items(self):
        return self.execute("""
            SELECT *
            FROM public.shop_table
            WHERE active = TRUE
        """)
        
    def get_shop_item(self, item_key):
        return self.execute(f"""
            SELECT *
            FROM public.shop_table
            WHERE item_key = '{item_key}' AND active = TRUE
        """)
        
    def buy_item(self, user_id, item_key, total_amount, coin):
        self.execute(f"""
            UPDATE public.user_inventory_table
            SET {item_key} = {item_key} + {total_amount},
                coin = coin - {coin}
            WHERE user_id = {user_id}
        """)       
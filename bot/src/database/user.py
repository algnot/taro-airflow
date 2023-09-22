from .base import Base
from .pokemon import Pokemon


class User (Base):
    _name = "Pokemon"
    user_id = None
    user_info = {}
    
    def __init__(self, user_id:int):
        super().__init__()
        self.user_id = user_id
        self.user_info = self.get_user_info()
        
    def get_user_info(self):
        return self.execute(f"""
            SELECT * FROM public.users_table ut
            INNER JOIN public.user_inventory_table uit 
            ON uit.user_id = ut.user_id
            WHERE ut.user_id = {self.user_id}
        """)[0]
        
    def get_user_pokemon(self):
        pokemon = self.execute(f"""
            SELECT * FROM public.pokemon_exp_table pxt
            WHERE pxt.user_id = {self.user_id} AND pxt.active = TRUE
            LIMIT 1
        """)
        if not pokemon:
            return None
        return pokemon[0]
    
    def action_use_pokeball(self, number:int=0):
        self.execute(f"""
            UPDATE public.user_inventory_table
            SET pokeball = pokeball - {number}
            WHERE user_id = {self.user_id}
        """)
    
    def action_get_random_pokemon(self):
        pokemon = Pokemon()
        self.action_use_pokeball(1)
        
        random_pokemon = pokemon.get_random_no_evo_pokemon()
        pokemon.create_pokemon(self.user_id, random_pokemon)
        
        return random_pokemon
    
    def action_release_pokemon(self):
        self.execute(f"""
            UPDATE public.pokemon_exp_table
            SET active = FALSE
            WHERE user_id = {self.user_id}
        """)

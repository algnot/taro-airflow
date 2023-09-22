from .base import Base


class Pokemon (Base):
    _name = "Pokemon"
    
    def __init__(self):
        super().__init__()
      
    def get_random_no_evo_pokemon(self):
        return self.execute("SELECT * FROM public.pokemon_table WHERE evo_from_id = -1 ORDER BY RANDOM() LIMIT 1")[0]
        
    def get_pokemon_by_id(self, pokemon_id:int):
        return self.execute(f"SELECT * FROM public.pokemon_table WHERE id = {pokemon_id}")[0]
    
    def create_pokemon(self, user_id:int, pokemon_data:any):
        self.execute(f"""
            INSERT INTO public.pokemon_exp_table (user_id, pokemon_id, exp, level, active, weight, height)
            VALUES ({user_id}, {pokemon_data['id']}, 0, 1, TRUE, {pokemon_data['weight']}, {pokemon_data['height']});
            UPDATE public.users_table
            SET pokemon_id = {pokemon_data['id']}
            WHERE user_id = {user_id};
        """)
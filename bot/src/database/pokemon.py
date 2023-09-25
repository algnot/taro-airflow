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
        
    def increse_abilities(self, user_id:int, pokemon_id:int, abilities:any):
        abilities["value"] = round(abilities["value"], 2)
        self.execute(f"""
            UPDATE public.{abilities['increse_table']}
            SET {abilities['increse_key']} = {abilities['increse_key']} + {abilities['value']}
            WHERE user_id = {user_id} AND pokemon_id = {pokemon_id} AND active = TRUE;
        """)
        
    def handle_level_up(self, user_id:int):
        return self.execute(f"""
            SELECT *
            FROM (
                SELECT pxt.exp,
                pxt.level as old_level,
                lspt.level as new_level,
                SUM(lspt.step_to_next_level) OVER (ORDER BY lspt.level) as want_exp
                FROM public.pokemon_exp_table pxt
                INNER JOIN public.level_step_pokemon_table lspt
                ON lspt.level > pxt.level
                WHERE pxt.user_id={user_id} AND 
                      pxt.active = TRUE
                ) as result_table 
            WHERE result_table.exp >= result_table.want_exp
            ORDER BY result_table.want_exp DESC
            LIMIT 1
        """);
        
    def action_level_up(self, user_id:int, new_level:int, use_exp:int):
        use_exp = round(use_exp, 2)
        self.execute(f"""
            UPDATE public.pokemon_exp_table
            SET level = {new_level}, exp = exp - {use_exp}
            WHERE user_id = {user_id} AND active = TRUE;
        """)
        
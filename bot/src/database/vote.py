from .base import Base


class Vote (Base):
    _name = "Vote"
    vote_id = None
    topic = None
    description = None
    create_by = None
    choices = []
    
    def __init__(self, vote_id:int):
        super().__init__()
        self.vote_id = vote_id
        self.get()
        
    def create(self, topic:str, description:str, choices:list, create_by:int=None):
        self.topic = topic
        self.description = description
        self.choices = choices
        self.create_by = create_by
        self.execute(f"""
            INSERT INTO vote_table (id, topic, description, create_by)
            VALUES ({self.vote_id}, '{topic}', '{description}', {create_by})
        """)
        
        for index, choice in enumerate(choices):
            self.execute(f"""
                INSERT INTO choice_table (vote_id, index, name)
                VALUES ({self.vote_id}, {index + 1}, '{choice['name']}')
            """)
        return self
        
    def get(self):
        result = self.execute(f"""
            SELECT * FROM vote_table
            WHERE id = {self.vote_id}
            LIMIT 1
        """)
        
        if not result:
            return None
        
        choices = self.execute(f"""
            SELECT * FROM choice_table
            WHERE vote_id = {self.vote_id}
            ORDER BY index ASC
        """) 
        
        self.topic = result[0]["topic"]
        self.description = result[0]["description"]
        self.choices = choices
        self.create_by = result[0]["create_by"]
        return self    
    
    def get_choice_id(self, choice_name:str):
        result = self.execute(f"""
            SELECT * FROM choice_table
            WHERE vote_id = {self.vote_id} AND name = '{choice_name}'
            LIMIT 1
        """)
        
        if not result:
            return None
        
        return result[0]["id"]
    
    def on_vote(self, user_id:int, choice_name:str):
        result = self.execute(f"""
            SELECT * FROM vote_user_table
            WHERE user_id = {user_id} AND vote_id = {self.vote_id}
            LIMIT 1
        """)
        
        if result:
            self.execute(f"""
                UPDATE choice_table
                SET count = count - 1
                WHERE vote_id = {self.vote_id} AND 
                      id = {result[0]["choice_id"]};
                      
                UPDATE choice_table
                SET count = count + 1
                WHERE vote_id = {self.vote_id} AND name = '{choice_name}';
                
                UPDATE vote_user_table
                SET choice_id = {self.get_choice_id(choice_name)}
                WHERE user_id = {user_id} AND vote_id = {self.vote_id};
            """)
            
        else:
            self.execute(f"""
                INSERT INTO vote_user_table (user_id, vote_id, choice_id)
                VALUES ({user_id}, {self.vote_id}, {self.get_choice_id(choice_name)});
                
                UPDATE choice_table
                SET count = count + 1
                WHERE vote_id = {self.vote_id} AND name = '{choice_name}';
            """)
            
        self.get()
        return self
            

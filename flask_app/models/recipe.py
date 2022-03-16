from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under30 = data['under30']
        self.user_id=data['user_id']
    
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def valida_receta(formulario):
        es_valido=True
        if len (formulario['name'])<3:
            flash('El nombre de la receta debe twener al menos 3 caracteres',"receta")
            es_valido=False
        if len (formulario['description'])<3:
            flash('La descripcion de la receta debe twener al menos 3 caracteres',"receta")
            es_valido=False
        if len (formulario['instructions'])<3:
            flash('Las instrucciones de la receta debe twener al menos 3 caracteres',"receta")
            es_valido=False
        if len (formulario['date_made'])=="":
            flash('Ingrese una fecha',"receta")
            es_valido=False
        
        return es_valido
    @classmethod
    def save (cls,data):
        query="INSERT INTO recipes (name, under30,description,instructions,date_made,user_id) VALUES (%(name)s,%(under30)s,%(description)s,%(instructions)s,%(date_made)s,%(user_id)s)"
        nuevoId= connectToMySQL('esquema_recetas').query_db(query,data)
        return nuevoId

    @classmethod
    def get_all(cls):
        query="SELECT * FROM recipes"
        results = connectToMySQL('esquema_recetas').query_db(query)
        recetas=[]
        for receta in results:
            rec=cls(receta)
            recetas.append(rec)
        return recetas
    @classmethod
    def get_by_id (cls,data):
        query ="SELECT * FROM recipes WHERE id =%(id)s"
        result =connectToMySQL('esquema_recetas').query_db(query,data)
        recipe =cls(result[0])
        return recipe
    @classmethod
    def update (cls,data):
        query ="UPDATE recipes set name=%(name)s,description=%(description)s,instructions=%(instructions)s,under30=%(under30)s,date_made=%(date_made)s WHERE (id= %(id)s)"
        result =connectToMySQL('esquema_recetas').query_db(query,data)
        return result

    @classmethod
    def delete (cls,data):
        query ="DELETE FROM recipes WHERE id =%(id)s"
        return connectToMySQL('esquema_recetas').query_db(query,data)


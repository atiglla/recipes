from flask_app.config.mysqlconnection import connectToMySQL
import re #Importamos expresiones regulares

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash

class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    
        
    
    @classmethod
    def save(cls, formulario):
        #formulario ={
        # 'first_name': 'elene'
        # 'last_name': 'de troya'
        # 'email': 'elenita'@mail.com
        # 'password': 'password'}
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        nuevoId = connectToMySQL('esquema_recetas').query_db(query, formulario)
        return nuevoId

    @staticmethod
    def valida_usuario(user):
        # user = {
        #     "first_name": "Emilio",
        #     "last_name": "Navejas",
        #     "email": "emilio@codingdojo.com"
        # }

        es_valido = True

        #Validar que mi nombre sea mayor a 2 caracteres
        if len(user['first_name']) < 2:
            flash('Nombre debe de tener al menos 2 caracteres', 'muro')
            es_valido = False
        #Validar que mi apellido sea mayor a 2 caracteres
        if len(user['last_name']) < 2:
            flash('Apellido debe de tener al menos 2 caracteres', 'muro')
            es_valido = False
        #Valido email con expresiones regulares
        if not EMAIL_REGEX.match(user['email']):
            flash('E-mail inválido', 'muro')
            es_valido = False
        if len(user['password']) < 8:
            flash('Contraseña debe tener al menos 6 caracteres', 'muro')
            es_valido = False
        if user['password'] != user['confirm']:
            flash('Contraseñas no coinciden', 'muro')
            es_valido = False
        
        #Consulta si ya existe ese correo
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_recetas').query_db(query, user)
        if len(results) >= 1:
            flash('E-mail registrado previamente', 'muro')
            es_valido = False

        return es_valido

    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('esquema_recetas').query_db(query, data)
        usr = result[0]
        user = cls(usr)
        return user
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('esquema_recetas').query_db(query, data)
        if len(result) < 1:
            return False
        else :
            usr = result[0]
            user = cls(usr)
            return user

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('esquema_recetas').query_db(query)
        users=[]
        for user in results:
            users.append(cls(user))
        return users
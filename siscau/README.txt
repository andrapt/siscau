powerbi@seades


// Configura o ambiente virtual para o projeto
python -m venv venv

// Ativa o ambiente virtual do projeto
.\venv\Scripts\activate


// Instlação do Django
pip install Django

// Criação do projeto em Django
django-admin startproject siscau .

// Roda o servidor web 
python manage.py runserver

// Criação do APP de fertilizantes
 python manage.py startapp fertilizantes

// Após criar as classes no Model, executar o seguinte comandfo
python manage.py makemigrations

//Logo após, executar o seguinte comando para a criação das tabelas na bas e de dados
python manage.py migrate

// Cria o usuário para administrar o admin do django
python manage.py createsuperuser
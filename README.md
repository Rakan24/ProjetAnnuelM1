# ProjetAnnuelM1


1) Cloner le projet


2) Faire dans un terminal à la racine du projet : 

	docker-compose down               
	docker-compose up --build 


Migrations : (predictions)
3) docker-compose exec backend python manage.py makemigrations predictions
docker-compose exec backend python manage.py migrate

Ensuite on se connecte sur : http://localhost:3000/

Se connecter avec : 

user : 

mail = user@gmail.com

password = 1234

Admin : 

mail = admin@gmail.com

password = 1234




a faire : 

corriger route pour admin et threshold
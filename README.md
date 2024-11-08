# backend-technical-test

## Objectif

Construire une API RESTful pour une application de gestion de lieux touristiques. L'API doit permettre de créer, lire, mettre à jour et supprimer des lieux, ainsi que de rechercher des lieux à proximité d'une position géographique donnée. L'application doit utiliser Django, Django REST Framework (DRF) et GeoDjango pour les fonctionnalités géospatiales.

Ajouter une suite de tests avec unittest et django-test

Un plus serait d'utiliser Celery pour gérer des tâches en arrière-plan, et configurer une tache d'envoi de rapport par email.

## Exigences

### Django:

Créez un modèle Lieu avec les champs suivants :
  - nom (CharField)
  - description (TextField)
  - location (PointField de GeoDjango)
  - date_added (DateTimeField)

Nous vous conseillons d'utiliser un backend spatialite

### API Django REST Framework:

Implémentez les vues et les sérialiseurs pour l'API RESTful permettant les opérations CRUD sur les lieux (via un ModelViewSet)
  
### Recherche Géospatiale:

Ajoutez un endpoint à l'API qui permet de rechercher des lieux à proximité d'une position donnée. Utilisez les capacités de GeoDjango pour effectuer cette recherche.
- `api/lieux/search/?lat=1&lng=1`

### Tests Unitaires:

Écrivez des tests unitaires pour les vues de l'API en utilisant unittest de Django.

### Tâches Asynchrones avec Celery:

Implémentez une tâche Celery qui s'exécute toutes les heures pour envoyer un rapport par email contenant le nombre de lieux ajoutés dans la dernière heure.
Nous vous conseillons d'utiliser un backend sqlite pour celery, et l'`EMAIL_BACKEND django.core.mail.backends.filebased.EmailBackend` pour envoyer les emails dans un dossier local 

## Critères d'Évaluation

Clarté et Structure du Code: Le candidat doit écrire du code lisible et bien structuré.

Approche Pythonique: Le code doit suivre les bonnes pratiques de Python.

Connaissance des Outils: Le candidat doit démontrer une bonne compréhension de Django, DRF, Celery et GeoDjango.

## Remarques

Nous vous conseillons d'utiliser la dernière version de Django.
Nous avons utilisé SQLAlchemy pour le brocker celery.

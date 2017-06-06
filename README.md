# Gemaracard

This app allows users to create (and later edit) flashcards for individual words in the Gemara and link them to uploaded texts. Flashcards are generated through a form that forces users to organize the parsing of each word (part of speech, language, gender, number, aspect, stem, etc.). Viewing the text also displays a list of hyperlinked flashcards so users can review vocabulary as they read through a text.

## To run
- $python3 manage.py runserver

## Migrations
- $python3 gemaracard/manage.py makemigration
- $python3 gemaracard/manage.py migrate

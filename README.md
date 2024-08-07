Exercitiu

Creati un endpoint de tip POST care primeste urmatoarele informatii
despre o persoana in body: nume, prenume, varsta, ocupatie. Acest
endpoint va salva informatiile acestea intr-un fisier .json numit de forma
“{nume}_{prenume}”. Pe langa informatiile din body, in fisierul JSON
va fi adaugata si perechea “create_time” cu valoarea timestampul curent.

Creati un endpoint GET care intoarce toate numele de persoane ca
JSON. Acest endpoint primeste un parametru de query care permite
filtrarea dupa varsta.

Creati un endpoint GET care include numele si prenumele in url (de
forma “nume-prenume” ca parametru de

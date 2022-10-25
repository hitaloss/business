# Komercio Generic Views

## Para rodar a aplicação, inicie o ambiente virtual "venv":

```
python -m venv venv
```

#

## Para entrar no ambiente virtual:

- Linux:

```
  source venv/bin/activate
```

- Windows:
  **(terminal bash)**

```
  source venv/Scripts/activate
```

- Windows:
  **(terminal powershell)**

```
  .\venv\scripts\activate
```

#

## A seguir, baixe todas as dependências rodando o comando:

```
pip freeze -r requirements.txt
```

#

## Execute as migrações para criar o db.sqlite e fazer persistência de dados:

- Linux:

```
  ./manage.py migrate
```

- Windows:
  **(terminal bash)**

```
  python manage.py migrate
```

- Windows:
  **(terminal powershell)**

```
  .\manage.py migrate
```

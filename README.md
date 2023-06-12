# Komercio Generic Views

## Instruções:

<br/>

### Crie o ambiente virtual

```
python -m venv venv
```

### Ative o venv

```bash
# linux:

source venv/bin/activate

```

### Instale as dependências

```
pip install -r requirements.txt
```

### Execute as migrações

```
python manage.py migrate
```

## Rodar os testes:

<br/>

### Para rodar os testes utilize um dos comandos abaixo:

```python
./manage.py test
```

ou para mais detalhes

```
./manage.py test -v2
```

### Rodar os testes com coverage

```
coverage run ./manage.py test
```

### Exibir o relatório

```
coverage report
```

## Carregar a fixture

<br/>

```
./manage.py loaddata komercio.json
```

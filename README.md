# python-edi-parser
Python/Django REST Framework positional flat file reader API

## Documentation

https://developercielo.github.io/tutorial/edi

## Inconsistências da Documentação

- Campo 26 do registro de detalhe é do tipo numérico, mas nos comentários diz para preencher com brancos

## Testes

```
(env) > python .\manage.py test
```

```
(env) > coverage run --source='flatparser' .\manage.py test flatparser
```

```
(env) > coverage report
```

or

```
(env) > coverage html
```
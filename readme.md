## Запуск сервиса todo через Docker

### Предварительные требования

Убедитесь, что у вас установлен Docker.
### Шаги для запуска

1. Склонируйте репозиторий и перейдите в папку сервиса:
```
git clone https://github.com/traf-and/MS.git
git switch development
cd MS/todo_service
```
2. Соберите Docker-образ:

```
sudo docker build -t todo .
```

3. Запустите контейнер:
```
sudo docker run -d -v todo_data:/app/data --name todo -p 80:80 todo
```

4. После этого вы сможете получить доступ к API по адресу [http://127.0.0.1:80](http://127.0.0.1:80).


Автоматическая документация по сервису находится по ссыле
[http://127.0.0.1:80/docs](http://127.0.0.1:80/docs).

## Запуск сервиса short_url через Docker

### Предварительные требования

Убедитесь, что у вас установлен Docker.
### Шаги для запуска

1. Склонируйте репозиторий и перейдите в папку сервиса:
```
git clone https://github.com/traf-and/MS.git
git switch development
cd MS/short_URL
```
2. Соберите Docker-образ:

```
sudo docker build -t short_URL .
```

3. Запустите контейнер:
```
sudo docker run -d -v short_URL:/app/data --name short_URL -p 80:80 short_URL
```

4. После этого вы сможете получить доступ к API по адресу [http://127.0.0.1:80](http://127.0.0.1:80).

Автоматическая документация по сервису находится по ссыле
[http://127.0.0.1:80/docs](http://127.0.0.1:80/docs).

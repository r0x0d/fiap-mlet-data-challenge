# FIAP Datathon 

## Rodando o projeto: 

Instalando as dependências 

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Inicializando o mlflow

```bash
$ podman-compose up -d mlflow
```

Treinando o modelo para teste:
```bash
$ make train 
# ou
$ python train_model.py
```

Para rodar a API, use o comando:

```bash
$ fastapi run app/main.py
```

Para rodar o app streamlit, use o comando:

```bash
$ streamlit run streamlit_app.py
```
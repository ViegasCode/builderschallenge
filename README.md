# Builders Challenge - Movie API (OMDb integration)

## Overview
API REST em FastAPI que consome a OMDb API para enriquecer os dados de filmes ao cadastrar.
Ao fazer `POST /movies` com `{ "title": "The Matrix" }`, a API busca os dados completos
na OMDb, persiste em banco e retorna o registro salvo, criado também um catálogo no "/" para exibir
os filmes incluídos via API Rest. ;)

## Setup (local)
1. Crie e ative um virtualenv:
```bash
python -m venv .venv
# mac/linux
source .venv/bin/activate
# windows (PowerShell)
.venv\Scripts\Activate.ps1
```

2. Instale dependências:
```bash
pip install -r requirements.txt
```

3. Crie `.env` na raiz com sua chave OMDb.
```
OMDB_API_KEY=your_api_key_here
```

4. Rode o servidor:
```bash
uvicorn main:app --reload
Obs.: Se estiver no diretório buildersch, rodar com:
uvicorn buildbox_challenge_final.main:app --reload
```

5. Acesse a docs para requisições:
http://127.0.0.1:8000/docs

6. Acesse o catálogo que espelha os filmes cadastrados: http://127.0.0.1:8000/

## Endpoints
- `POST /movies` → body: `{ "title": "The Matrix" }` (apenas título).
- `GET /movies` → lista todos os filmes salvos.
- `GET /movies/{id}` → busca um filme por id.

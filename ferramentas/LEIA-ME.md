# Ferramentas de áudio

| Pasta | O que é | Licença |
| --- | --- | --- |
| `sfx-kit/` | 320 efeitos sonoros prontos (WAV 48 kHz) com catálogo e guia de uso (`GUIDE.md`, `catalogue.md`, `sounds.json`) | CC0 |
| `earshot/` | "Ouvidos" para o agente: descreve, compara e avalia sons e filmes (CLI `earshot`) | MIT |
| `openverse/buscar.py` | Busca e baixa áudio/imagens livres pela API pública do Openverse (WordPress) | API pública; respeite a licença de cada item |

Os skills do earshot (`earshot`, `real-sound`) estão em `.claude/skills/`.

## Instalar o earshot (uma vez por máquina)

```bash
python3 -m venv ferramentas/.venv
ferramentas/.venv/bin/pip install --extra-index-url https://download.pytorch.org/whl/cpu -e "ferramentas/earshot[mcp]"
ferramentas/.venv/bin/earshot describe caminho/do/som.wav
ferramentas/.venv/bin/earshot critique video/comerciais/bravos-brasa-motion.mp4
```

## Openverse

```bash
python3 ferramentas/openverse/buscar.py audio "whoosh" --licenca cc0 -n 5 --baixar saida/
python3 ferramentas/openverse/buscar.py images "barbearia" --licenca cc0,by -n 5
```

Só o cliente de busca foi incluído. O repositório completo do Openverse (WordPress/openverse) é a aplicação
inteira do buscador (Django, Airflow, Nuxt, Docker, ~245 MB) e não faz sentido dentro deste projeto.
Itens com licença diferente de CC0 pedem crédito ao autor: guarde o `.json` que o script grava ao lado do arquivo.

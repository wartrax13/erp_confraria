# ERP Confraria

Projeto criado para sistematizar e facilitar processos relacionados a entrega e recebimentos de doações.

# Dependencias do sistema

```bash
sudo apt install python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

# Pip tools:
pip-compile --generate-hashes requirements-dev.in
pip-sync requirements-dev.txt

# Migrate
python manage.py migrate

# Criar superusuario
python manage.py createsuperuser

# Rodar script para a lista de Cadastros Pessoa Física
Entre em contato para obter o arquivo necessário em Excel (teste_cadastro.xlsx)
Coloque o arquivo dentro da pasta backup/teste_cadastro.xlsx e em seguida:

python manage.py shell
from backup import script_cadastros

# Rodar
python manage.py runserver
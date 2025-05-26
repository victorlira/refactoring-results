import re
import json
import shutil

# 1) Caminhos
input_file  = 'refactor-result.json'
backup_file = input_file + '.bak'

# 2) Backup
shutil.copyfile(input_file, backup_file)

# 3) Lê todo o JSON (quebrado) como texto
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 4) Escapa tabs LITERALS dentro de strings JSON (entre aspas)
def escape_tabs_in_string_literal(match):
    literal = match.group(0)         # inclui as aspas externas
    inner = literal[1:-1]            # conteúdo dentro das aspas
    inner = inner.replace('\t', '\\t')
    return f'"{inner}"'

content = re.sub(
    r'"(?:\\.|[^"\\])*"',           # corresponde a qualquer string JSON (com escapes)
    escape_tabs_in_string_literal,
    content
)

# 5) Remove outros control-chars proibidos fora de strings
content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', content)

# 6) Envolve em aspas os valores de `tool` sem aspas
content = re.sub(
    r'("tool"\s*:\s*)([A-Za-z0-9_]+)(\s*(?:,|\}))',
    lambda m: f'{m.group(1)}\"{m.group(2)}\"{m.group(3)}',
    content
)

# 7) Carrega em JSON (strict=False permite control-chars escapados)
data = json.loads(content, strict=False)

# 8) Sobrescreve o original, já formatado
with open(input_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'✔ "{input_file}" corrigido! Backup em "{backup_file}".')


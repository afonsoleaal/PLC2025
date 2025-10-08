import re

conteudo = """
# Exemplo
## Exemplo
### Exemplo
Este é um **exemplo** ...
Este é um *exemplo* ...
1. Primeiro item
2. Segundo item
3. Terceiro item
Como pode ser consultado em [página da UC](http://www.uc.pt)
Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com) ...
"""

def converter(texto):
    # Cabeçalhos
    def cabecalho(m):
        nivel = len(m.group(1))
        return f"<h{nivel}>{m.group(2)}</h{nivel}>"
    html = re.sub(r'^(#{1,3})\s+(.*)$', cabecalho, texto, flags=re.MULTILINE)

    # Negrito
    html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html)

    # Itálico
    html = re.sub(r'\*(.+?)\*', r'<i>\1</i>', html)

    # Listas numeradas
    html = re.sub(r'^\d+\.\s+(.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'((?:<li>.*?</li>\s*)+)', r'<ol>\n\1</ol>\n', html)

    # Links e imagens
    def substituir(m):
        if m.group('img'):
            return f'<img src="{m.group("url")}" alt="{m.group("texto")}"/>'
        else:
            return f'<a href="{m.group("url")}">{m.group("texto")}</a>'


    html = re.sub(r'(?P<img>!)?\[(?P<texto>[^\]]+)\]\((?P<url>[^)]+)\)', substituir, html)

    print(html)

converter(conteudo)

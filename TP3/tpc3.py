import re

# Lista de padrões de tokens (cada um com um nome e uma expressão regular)
token_spec = [
    ("COMMENT",   r"#.*"),                               # Comentários
    ("KEYWORD",   r"(?i)\b(select|where|limit|a)\b"),    # Palavras-chave (case-insensitive)
    ("VAR",       r"\?[A-Za-z_]\w*"),                    # Variáveis 
    ("IDENT",     r"[A-Za-z_][\w-]*:[A-Za-z_][\w-]*"),   # Identificadores 
    ("STRING",    r'"[^"]*"(?:@[a-z]+)?'),               # Strings 
    ("NUMBER",    r"\d+"),                               # Números 
    ("SYMBOL",    r"[{}.;]"),                            # Símbolos isolados
    ("WHITESPACE",r"[ \t\n]+"),                          # Espaços e \n's
]


master_pattern = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec))

def lex(text):
    """Função que analisa o texto e devolve a lista de tokens"""
    tokens = []
    for match in master_pattern.finditer(text):
        kind = match.lastgroup  
        value = match.group()   
        if kind == "WHITESPACE" or kind == "COMMENT":
            continue  
        tokens.append((kind, value))
    return tokens


# Exemplo de teste com a query dada
query = """# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
"""

# Mostra os tokens encontrados
for tok in lex(query):
    print(tok)

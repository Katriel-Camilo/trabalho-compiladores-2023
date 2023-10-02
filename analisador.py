\\ Trabalho -  reconhecedor HTML 
\\Unipinhal 2023
import re
from termcolor import colored

html_content = """
<html>
<head>
   <title> Compiladores </title>
</head>
<body>
  <p style="color: red; background: blue; font-family:verdana; color: yellow;" id="abc"> Unipinhal </p>
  <br>
</body>
</html>
"""

def extrair_tags(conteudo_html):
    tags = re.findall(r'<\s*([a-zA-Z0-9]+)\s*(.*?)\s*>|</\s*([a-zA-Z0-9]+)\s*>|<\s*([a-zA-Z0-9]+)\s*/\s*>|([^<]*)', conteudo_html)
    return tags

def analisar_html(conteudo_html):
    tags = extrair_tags(conteudo_html)
    pilha_de_tags = []
    
    for tag in tags:
        tag_abertura, atributos, tag_fechamento, tag_self_closing, conteudo_interno = tag
        if tag_abertura or tag_self_closing:
            nivel = len(pilha_de_tags)
            tag_name = tag_abertura if tag_abertura else tag_self_closing
            tag_obj = {
                "name": tag_name,
                "level": nivel,
                "attributes": re.findall(r'([a-zA-Z0-9-]+)="(.*?)"', atributos),
                "inner_html": [],
            }
            if not tag_self_closing:
                pilha_de_tags.append(tag_obj)
            recuo = '  ' * nivel
            print(colored(f"Tag de Abertura:", 'blue'), colored(f"<{tag_name}>", 'yellow'), colored(f"- Nível {nivel}", 'white'))
            for attr in tag_obj["attributes"]:
                attr_name, attr_value = attr
                print(f"{recuo}  \033[32mAtributo de Tag:\033[0m ({attr_name})")
                valores = attr_value.split(';')
                valor_numero = 1  # Inicializa o número do valor
                for valor in valores:
                    if valor.strip():  # Verifica se o valor não está vazio
                        if ':' in valor:
                            nome_valor, valor_valor = valor.strip().split(':')
                            print(f"{recuo}    \033[31mConteúdo {valor_numero} do ({attr_name}): ({nome_valor})")
                            print(f"{recuo}    \033[31mValor conteúdo ({nome_valor}): ({valor_valor.strip()})")
                            valor_numero += 1  # Incrementa o número do valor
                        else:
                            if valor_numero == 1:
                                print(f"{recuo}    \033[31mValor atributo {attr_name}: ({valor.strip()})")
                            else:
                                print(f"{recuo}    \033[31mValor conteúdo ({attr_name}): ({valor.strip()})")
                            valor_numero += 1  # Incrementa o número do valor
        elif tag_fechamento:
            while pilha_de_tags:
                last_tag = pilha_de_tags.pop()
                if last_tag["name"] == tag_fechamento:
                    recuo = '  ' * last_tag['level']
                    for inner in last_tag["inner_html"]:
                        print(f"{recuo}  \033[35mConteúdo da Tag:\033[0m {inner.strip()}")
                    print(colored(f"Tag de Fechamento:", 'blue'), colored(f"</{tag_fechamento}>", 'yellow'))
                    break
        elif conteudo_interno.strip():
            if pilha_de_tags:
                pilha_de_tags[-1]["inner_html"].append(conteudo_interno.strip())

print("=========================================")
print("\033[33mAnálise do Código HTML:\033[0m")
print("=========================================")
analisar_html(html_content)
print("===============================================")
print("\033[33mCódigo Análisado com Sucesso!\033[0m")
print("===============================================")

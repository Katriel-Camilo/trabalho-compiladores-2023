# Importa o módulo 're' para trabalhar com expressões regulares
# e o módulo 'termcolor' para colorir a saída no terminal.
import re
from termcolor import colored

# Conteúdo HTML de exemplo.
html_content = """
<html>
<head>
   <title> Compiladores </title>
</head>
<body>
  <p style="color: red; background: blue; font-family:verdana; color: yellow;" id="slogan"> Nova UniPinhal, como você sempre quis! </p>
  <br>
</body>
</html>
"""

# Função para extrair todas as tags HTML e conteúdo interno do HTML.
def extrair_tags(conteudo_html):
    # Usa expressões regulares para encontrar tags de abertura, fechamento,
    # auto-fechamento e conteúdo dentro do HTML.
    tags = re.findall(r'<\s*([a-zA-Z0-9]+)\s*(.*?)\s*>|</\s*([a-zA-Z0-9]+)\s*>|<\s*([a-zA-Z0-9]+)\s*/\s*>|([^<]*)', conteudo_html)
    return tags

# Função principal para analisar e imprimir informações das tags HTML.
def analisar_html(conteudo_html):
    # Chama a função para extrair as tags do HTML.
    tags = extrair_tags(conteudo_html)
    # Cria uma pilha de tags para rastrear as tags aninhadas.
    pilha_de_tags = []
    
    # Itera sobre as tags encontradas.
    for tag in tags:
        tag_abertura, atributos, tag_fechamento, tag_self_closing, conteudo_interno = tag
        if tag_abertura or tag_self_closing:
            nivel = len(pilha_de_tags)
            tag_name = tag_abertura if tag_abertura else tag_self_closing
            # Cria um objeto para armazenar informações da tag.
            tag_obj = {
                "name": tag_name,
                "level": nivel,
                "attributes": re.findall(r'([a-zA-Z0-9-]+)="(.*?)"', atributos),
                "inner_html": [],
            }
            # Se a tag não for de auto-fechamento, a adiciona à pilha.
            if not tag_self_closing:
                pilha_de_tags.append(tag_obj)
            recuo = '  ' * nivel
            # Imprime informações da tag de abertura formatadas com cores.
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
                            # Imprime informações dos atributos de estilo.
                            print(f"{recuo}    \033[31mConteúdo {valor_numero} do ({attr_name}): ({nome_valor})")
                            print(f"{recuo}    \033[31mValor conteúdo ({nome_valor}): ({valor_valor.strip()})")
                            valor_numero += 1  # Incrementa o número do valor
                        else:
                            if valor_numero == 1:
                                # Imprime informações do primeiro valor do atributo.
                                print(f"{recuo}    \033[31mValor atributo {attr_name}: ({valor.strip()})")
                            else:
                                # Imprime informações dos valores subsequentes do atributo.
                                print(f"{recuo}    \033[31mValor conteúdo ({attr_name}): ({valor.strip()})")
                            valor_numero += 1  # Incrementa o número do valor
        elif tag_fechamento:
            while pilha_de_tags:
                last_tag = pilha_de_tags.pop()
                if last_tag["name"] == tag_fechamento:
                    recuo = '  ' * last_tag['level']
                    for inner in last_tag["inner_html"]:
                        # Imprime conteúdo interno da tag.
                        print(f"{recuo}  \033[35mConteúdo da Tag:\033[0m {inner.strip()}")
                    # Imprime informações da tag de fechamento formatadas com cores.
                    print(colored(f"Tag de Fechamento:", 'blue'), colored(f"</{tag_fechamento}>", 'yellow'))
                    break
        elif conteudo_interno.strip():
            if pilha_de_tags:
                # Adiciona conteúdo interno à tag no topo da pilha.
                pilha_de_tags[-1]["inner_html"].append(conteudo_interno.strip())

# Imprime cabeçalho informativo.
print("=========================================")
print("\033[33mAnálise do Código HTML:\033[0m")
print("=========================================")
# Chama a função para analisar o HTML.
analisar_html(html_content)
# Imprime mensagem de conclusão.
print("===============================================")
print("\033[33mCódigo Análisado com Sucesso!\033[0m")
print("===============================================")

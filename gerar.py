import requests
import json
import os
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def obter_dados_do_segredo():
    segredo = os.environ.get("MEUS_LINKS")
    if not segredo:
        print("❌ Segredo não encontrado.")
        return []
    
    lista_formatada = []
    # Separa por vírgula (cada item é "Nome|Link")
    itens = segredo.split(',')
    
    for item in itens:
        # Separa por barra vertical
        partes = item.strip().split('|')
        if len(partes) == 2:
            nome_custom = partes[0].strip()
            url = partes[1].strip()
            lista_formatada.append((nome_custom, url))
        else:
            # Se não tiver o nome, tenta usar só a url
            url_limpa = item.strip()
            if url_limpa:
                lista_formatada.append(("Desconhecido", url_limpa))
                
    print(f"✅ Carregados {len(lista_formatada)} itens para monitoramento.")
    return lista_formatada

def formatar_data(timestamp):
    if not timestamp: return "---"
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')
    except: return "Indefinido"

def analisar_links(lista_itens):
    print("Iniciando verificação...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    dados_finais = []

    for nome_custom, url in lista_itens:
        # Aqui definimos que o 'usuario' a ser exibido é o NOME DA FONTE
        nome_exibicao = nome_custom 
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    u_info = data.get('user_info', {})
                    
                    if not u_info:
                        dados_finais.append([nome_exibicao, "-", "-", "Erro Login"])
                    else:
                        # Pegamos os dados técnicos, mas mantemos o nome Fonte XX
                        status = u_info.get('status', 'Unknown')
                        expira = formatar_data(u_info.get('exp_date'))
                        ativos = u_info.get('active_cons', '0')
                        maximos = u_info.get('max_connections', '0')
                        
                        dados_finais.append([nome_exibicao, expira, f"{ativos}/{maximos}", status])
                except:
                    dados_finais.append([nome_exibicao, "-", "-", "Erro JSON"])
            elif response.status_code == 403:
                dados_finais.append([nome_exibicao, "-", "-", "Bloqueado"])
            elif response.status_code == 404:
                dados_finais.append([nome_exibicao, "-", "-", "Não Achou"])
            else:
                dados_finais.append([nome_exibicao, "-", "-", f"Erro {response.status_code}"])

        except requests.exceptions.ConnectTimeout:
            dados_finais.append([nome_exibicao, "-", "-", "Timeout"])
        except:
            dados_finais.append([nome_exibicao, "-", "-", "Offline"])
            
    return dados_finais

def gerar_imagem(dados):
    print("Gerando imagem...")
    largura = 900
    altura_linha = 40
    altura_cabecalho = 120
    altura_total = altura_cabecalho + (len(dados) * altura_linha) + 40
    
    img = Image.new('RGB', (largura, altura_total), color=(18, 18, 24))
    d = ImageDraw.Draw(img)
    
    try:
        caminho_fonte = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        caminho_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font_padrao = ImageFont.truetype(caminho_fonte, 15)
        font_bold = ImageFont.truetype(caminho_bold, 15)
        font_titulo = ImageFont.truetype(caminho_bold, 24)
        font_sub = ImageFont.truetype(caminho_fonte, 12)
    except:
        font_padrao = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_titulo = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Cabeçalho
    d.rectangle([(0, 0), (largura, 90)], fill=(30, 30, 40))
    agora = datetime.now().strftime("%d/%m/%Y - %H:%M (Brasília)")
    
    d.text((30, 20), "MONITORAMENTO IPTV", fill=(0, 200, 255), font=font_titulo)
    d.text((30, 55), f"Atualizado: {agora}", fill=(150, 150, 150), font=font_sub)
    
    # Colunas (Mudei de USUÁRIO para FONTE)
    y_col = 100
    colunas = [("FONTE", 30), ("VENCIMENTO", 300), ("CONEXÕES", 550), ("STATUS", 750)]
    for nome, x in colunas:
        d.text((x, y_col), nome, fill=(100, 255, 100), font=font_bold)
    
    d.line([(30, y_col + 25), (largura-30, y_col + 25)], fill=(80, 80, 80), width=1)

    # Linhas
    y = y_col + 40
    for i, linha in enumerate(dados):
        nome, vence, conexoes, status = linha
        
        if i % 2 == 0: d.rectangle([(10, y-5), (largura-10, y+30)], fill=(25, 25, 35))

        cor = (220, 220, 220)
        cor_st = (255, 50, 50) # Vermelho
        
        if status == "Active": cor_st = (50, 255, 50) # Verde
        elif status == "Expiring Soon": cor_st = (255, 165, 0) # Laranja

        d.text((30, y), str(nome), fill=cor, font=font_padrao)
        d.text((300, y), str(vence), fill=cor, font=font_padrao)
        d.text((550, y), str(conexoes), fill=cor, font=font_padrao)
        d.text((750, y), str(status), fill=cor_st, font=font_bold)
        y += altura_linha

    img.save("status.png")

def criar_video():
    print("Renderizando vídeo...")
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", "status.png", 
        "-c:v", "libx264", "-t", "10", "-pix_fmt", "yuv420p", 
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "video_status.mp4"
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    lista = obter_dados_do_segredo()
    if lista:
        dados = analisar_links(lista)
        gerar_imagem(dados)
        criar_video()
    else:
        print("Nenhum dado para processar.")

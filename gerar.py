import requests
import json
import os
import subprocess
import platform
import math
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# SEUS LINKS (HARDCODED)
# ==========================================
MEUS_LINKS_TEXTO = "Fonte 16|http://7voahoje.top:80/player_api.php?username=7csplay&password=seven2022,Fonte 14|http://play.dnsrot.vip/player_api.php?username=5550388689&password=simpleiptv,Fonte 15|http://play.dnsrot.vip/player_api.php?&username=Marcosfp05&password=nlybdft6fml,Fonte 18|http://7voahoje.top:8080/player_api.php?username=delcio&password=99118656,Fonte 25|http://megaxc.ca/player_api.php?username=ialwg1&password=iao8wo,Fonte 26|http://cdnrez.xyz:80/player_api.php?username=241555307&password=106251943,Fonte 27|http://play.dnsrot.vip/player_api.php?username=nena6194sala&password=mqtavfrtyl,Fonte 28|http://play.dnsrot.vip/player_api.php?username=tomoko11&password=14n11oi50oc,Fonte 29|http://play.dnsrot.vip/player_api.php?username=vanessanook&password=vinr390x8y,Fonte 30|http://play.dnsrot.vip/player_api.php?username=huhenz&password=fa7kum6q4bm,Fonte 31|http://play.dnsrot.vip/player_api.php?username=zQ4qeGkNrQ&password=factoryiptv,Fonte 32|http://play.dnsrot.vip/player_api.php?username=7RRjPTu5d6&password=factoryiptv,Fonte 33|http://nymcsus.autos:80/player_api.php?username=022282&password=ETr1Pb,Fonte 34|http://nymcsus.autos:80/player_api.php?username=010794&password=FXz1sY,Fonte 35|http://pernalonga.cc/player_api.php?username=454266&password=gU8vEr,Fonte 36|http://nymcsus.autos:80/player_api.php?username=022125&password=ytH8dH,Fonte 37|http://pernalonga.cc/player_api.php?username=876683&password=npZ6T6,Fonte 38|http://case2.lat/player_api.php?&username=593812776&password=876362759,Fonte 39|http://case2.lat/player_api.php?&username=374897485&password=789272274,Fonte 40|http://case2.lat/player_api.php?&username=961386894&password=118897421,Fonte 41|http://case2.lat/player_api.php?&username=718423457&password=539143340,Fonte 42|http://case2.lat/player_api.php?&username=175473583&password=643238922,Fonte 43|http://case2.lat/player_api.php?&username=587142841&password=619556956,Fonte 44|http://case2.lat/player_api.php?&username=753685114&password=689268878,Fonte 45|http://case2.lat/player_api.php?&username=648866758&password=722737417,Fonte 46|http://case2.lat/player_api.php?&username=399392844&password=784365638,Fonte 47|http://case2.lat/player_api.php?&username=858257510&password=975651644,Fonte 48|http://case2.lat/player_api.php?&username=223141736&password=496767276,Fonte 49|http://case2.lat/player_api.php?&username=777951153&password=939114817,Fonte 50|http://case2.lat/player_api.php?&username=971812357&password=246137274,Fonte 51|http://case2.lat/player_api.php?&username=988493659&password=241861732,Fonte 52|http://case2.lat/player_api.php?&username=943285414&password=493936454,Fonte 53|http://case2.lat/player_api.php?&username=872689987&password=824513989,Fonte 54|http://case2.lat/player_api.php?&username=338365128&password=769491152,Fonte 55|http://case2.lat/player_api.php?&username=754551879&password=531553919,Fonte 56|http://case2.lat/player_api.php?&username=11283886&password=65967277"

def obter_lista_links():
    lista_formatada = []
    itens = MEUS_LINKS_TEXTO.split(',')
    
    for item in itens:
        partes = item.strip().split('|')
        if len(partes) == 2:
            nome_custom = partes[0].strip()
            url = partes[1].strip()
            lista_formatada.append((nome_custom, url))
        else:
            url_limpa = item.strip()
            if url_limpa:
                lista_formatada.append(("Desconhecido", url_limpa))
                
    print(f"✅ Carregados {len(lista_formatada)} itens da lista.")
    return lista_formatada

def formatar_data(timestamp):
    if not timestamp: return "---"
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')
    except: return "Indefinido"

def analisar_links(lista_itens):
    print("\n🔎 Iniciando verificação de status...\n")
    
    # Headers para emular navegador e evitar erro 406
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive'
    }

    dados_finais = []

    for nome_custom, url in lista_itens:
        nome_exibicao = nome_custom 
        print(f"Verificando: {nome_exibicao}...", end=" ")
        
        try:
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    u_info = data.get('user_info', {})
                    
                    if not u_info:
                        print("❌ Erro Login")
                        dados_finais.append([nome_exibicao, "-", "-", "-", "Erro Login"])
                    else:
                        status = u_info.get('status', 'Unknown')
                        criado = formatar_data(u_info.get('created_at'))
                        expira = formatar_data(u_info.get('exp_date'))
                        ativos = u_info.get('active_cons', '0')
                        maximos = u_info.get('max_connections', '0')
                        
                        print(f"✅ OK ({status})")
                        dados_finais.append([nome_exibicao, criado, expira, f"{ativos}/{maximos}", status])
                except:
                    print(f"⚠️ Erro JSON")
                    dados_finais.append([nome_exibicao, "-", "-", "-", "Erro JSON"])
            
            elif response.status_code == 403:
                print("🚫 Bloqueado (IP)")
                dados_finais.append([nome_exibicao, "-", "-", "-", "Bloq. IP"])
            elif response.status_code == 404:
                print("❓ Não encontrado")
                dados_finais.append([nome_exibicao, "-", "-", "-", "Não Achou"])
            else:
                print(f"⚠️ Erro {response.status_code}")
                dados_finais.append([nome_exibicao, "-", "-", "-", f"Erro {response.status_code}"])

        except:
             print("🔌 Falha Conexão")
             dados_finais.append([nome_exibicao, "-", "-", "-", "Offline"])
            
    return dados_finais

def carregar_fontes():
    """Carrega fontes ajustadas para modo compacto (mais linhas)."""
    fontes = {}
    try:
        sistema = platform.system()
        # Tamanhos reduzidos para caber mais linhas (Compact Mode)
        base_size = 19   
        title_size = 36  
        
        if sistema == "Windows":
            fontes['padrao'] = ImageFont.truetype("arial.ttf", base_size)
            fontes['bold'] = ImageFont.truetype("arialbd.ttf", base_size)
            fontes['titulo'] = ImageFont.truetype("arialbd.ttf", title_size)
            fontes['sub'] = ImageFont.truetype("arial.ttf", 16)
        else:
            # Caminhos Linux
            path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            path_b = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            fontes['padrao'] = ImageFont.truetype(path, base_size)
            fontes['bold'] = ImageFont.truetype(path_b, base_size)
            fontes['titulo'] = ImageFont.truetype(path_b, title_size)
            fontes['sub'] = ImageFont.truetype(path, 16)
    except:
        fontes['padrao'] = ImageFont.load_default()
        fontes['bold'] = ImageFont.load_default()
        fontes['titulo'] = ImageFont.load_default()
        fontes['sub'] = ImageFont.load_default()
    
    return fontes

def gerar_imagens_paginadas(dados):
    print("\n🎨 Gerando imagens (Modo Compacto - Alta Densidade)...")
    
    # Configurações de Layout
    LARGURA = 1920
    ALTURA = 1080
    MARGEM_X = 50
    
    # AJUSTES PARA CABER MAIS LINHAS
    Y_INICIAL = 140       # Começa a tabela mais para cima
    ALTURA_LINHA = 34     # Linha mais fina (antes era 60)
    ALTURA_RODAPE = 40
    
    # Calcular quantos itens cabem por página
    espaco_disponivel = ALTURA - Y_INICIAL - ALTURA_RODAPE
    itens_por_pagina = espaco_disponivel // ALTURA_LINHA
    
    print(f"ℹ️  Capacidade por página: {itens_por_pagina} linhas.")
    
    # Paginação
    total_paginas = math.ceil(len(dados) / itens_por_pagina)
    fontes = carregar_fontes()
    
    nomes_arquivos = []

    # Configuração de Data e Hora
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    agora = datetime.now(fuso_horario).strftime("%d/%m/%Y - %H:%M")

    for pagina in range(total_paginas):
        img = Image.new('RGB', (LARGURA, ALTURA), color=(15, 15, 25))
        d = ImageDraw.Draw(img)
        
        # Cabeçalho Geral
        d.rectangle([(0, 0), (LARGURA, 90)], fill=(30, 30, 50)) 
        d.text((MARGEM_X, 20), "MONITORAMENTO IPTV", fill=(0, 255, 255), font=fontes['titulo'])
        d.text((MARGEM_X, 65), f"Atualizado: {agora} | Pág {pagina + 1}/{total_paginas}", fill=(200, 200, 200), font=fontes['sub'])

        # Cabeçalho da Tabela (Colunas)
        colunas_x = [50, 600, 900, 1200, 1500] 
        titulos = ["FONTE / SERVIDOR", "CRIADO", "VENCE", "CONEX", "STATUS"]
        
        y_header = 100
        d.rectangle([(MARGEM_X, y_header), (LARGURA - MARGEM_X, y_header + 30)], fill=(50, 50, 70))
        
        for i, titulo in enumerate(titulos):
            d.text((colunas_x[i], y_header + 5), titulo, fill=(255, 215, 0), font=fontes['bold'])

        # Dados da Página Atual
        inicio = pagina * itens_por_pagina
        fim = inicio + itens_por_pagina
        dados_pagina = dados[inicio:fim]

        y = Y_INICIAL
        for i, linha in enumerate(dados_pagina):
            nome, criado, vence, conexoes, status = linha
            
            # Fundo zebrado para facilitar a leitura com linhas finas
            if i % 2 == 0:
                d.rectangle([(MARGEM_X, y), (LARGURA - MARGEM_X, y + ALTURA_LINHA)], fill=(22, 22, 32))
            else:
                d.rectangle([(MARGEM_X, y), (LARGURA - MARGEM_X, y + ALTURA_LINHA)], fill=(28, 28, 38))
            
            # Cores do Status
            cor_texto = (230, 230, 230)
            cor_status = (255, 50, 50) # Vermelho
            
            status_lower = str(status).lower()
            if "active" in status_lower: cor_status = (50, 255, 50) # Verde Neon
            elif "expiring" in status_lower: cor_status = (255, 165, 0) # Laranja
            elif "bloq" in status_lower or "403" in status_lower: cor_status = (200, 0, 0) # Vermelho Escuro

            # Centralizar texto verticalmente na linha
            offset_y = 6 

            d.text((colunas_x[0], y + offset_y), str(nome), fill=cor_texto, font=fontes['padrao'])
            d.text((colunas_x[1], y + offset_y), str(criado), fill=cor_texto, font=fontes['padrao'])
            d.text((colunas_x[2], y + offset_y), str(vence), fill=cor_texto, font=fontes['padrao'])
            d.text((colunas_x[3], y + offset_y), str(conexoes), fill=cor_texto, font=fontes['padrao'])
            d.text((colunas_x[4], y + offset_y), str(status), fill=cor_status, font=fontes['bold'])
            
            y += ALTURA_LINHA

        # Salvar frame
        nome_arquivo = f"status_{pagina}.png"
        img.save(nome_arquivo)
        nomes_arquivos.append(nome_arquivo)
        print(f"🖼️  Slide {pagina+1} gerado: {nome_arquivo}")

    return nomes_arquivos

def criar_video_slideshow(imagens):
    if not imagens: return
    
    print("🎬 Gerando vídeo slideshow (1920x1080)...")
    
    # Tempo de exibição por página (segundos)
    tempo_por_slide = "10" 
    
    try:
        # Cria vídeo compatível com qualquer player (yuv420p)
        cmd = [
            "ffmpeg", "-y", 
            "-framerate", f"1/{tempo_por_slide}", 
            "-i", "status_%d.png",                 
            "-c:v", "libx264", 
            "-r", "30",                            
            "-pix_fmt", "yuv420p",                 
            "video_status.mp4"
        ]
        
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Vídeo 'video_status.mp4' criado com sucesso!")
            
    except FileNotFoundError:
        print("⚠️  FFmpeg não instalado. Apenas as imagens foram geradas.")
    except Exception as e:
        print(f"⚠️  Erro ao gerar vídeo: {e}")

if __name__ == "__main__":
    lista = obter_lista_links()
    if lista:
        dados = analisar_links(lista)
        arquivos = gerar_imagens_paginadas(dados)
        criar_video_slideshow(arquivos)
    else:
        print("Nenhum dado para processar.")

import requests
import json
import os
import subprocess
import platform
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# SEUS LINKS ESTÃO AQUI AGORA (HARDCODED)
# ==========================================
MEUS_LINKS_TEXTO = "Fonte 16|http://7vnx.xyz:80/player_api.php?username=7csplay&password=seven2022,Fonte 14|http://play.dnsrot.vip/player_api.php?username=5550388689&password=simpleiptv,Fonte 15|http://play.dnsrot.vip/player_api.php?&username=Marcosfp05&password=nlybdft6fml,Fonte 18|http://7vnx.xyz:8080/player_api.php?username=delcio&password=99118656,Fonte 25|http://megaxc.ca/player_api.php?username=ialwg1&password=iao8wo,Fonte 26|http://cdnrez.xyz:80/player_api.php?username=241555307&password=106251943,Fonte 27|http://play.dnsrot.vip/player_api.php?username=nena6194sala&password=mqtavfrtyl,Fonte 28|http://play.dnsrot.vip/player_api.php?username=tomoko11&password=14n11oi50oc,Fonte 29|http://play.dnsrot.vip/player_api.php?username=vanessanook&password=vinr390x8y,Fonte 30|http://play.dnsrot.vip/player_api.php?username=huhenz&password=fa7kum6q4bm,Fonte 31|http://play.dnsrot.vip/player_api.php?username=zQ4qeGkNrQ&password=factoryiptv,Fonte 32|http://play.dnsrot.vip/player_api.php?username=7RRjPTu5d6&password=factoryiptv"

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
                
    print(f"✅ Carregados {len(lista_formatada)} itens da lista interna.")
    return lista_formatada

def formatar_data(timestamp):
    if not timestamp: return "---"
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')
    except: return "Indefinido"

def analisar_links(lista_itens):
    print("\n🔎 Iniciando verificação de status...\n")
    
    # MUDANÇA IMPORTANTE: User-Agent que imita um app de IPTV real para evitar bloqueios
    headers = {
        'User-Agent': 'IPTVSmartersPro/1.1.1 (iPad; iOS 12.0; Scale/2.00)',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    dados_finais = []

    for nome_custom, url in lista_itens:
        nome_exibicao = nome_custom 
        print(f"Verificando: {nome_exibicao}...", end=" ")
        
        try:
            # Timeout um pouco maior para conexões lentas
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    u_info = data.get('user_info', {})
                    
                    if not u_info:
                        print("❌ Erro Login/Dados vazios")
                        dados_finais.append([nome_exibicao, "-", "-", "-", "Erro Login"])
                    else:
                        status = u_info.get('status', 'Unknown')
                        criado = formatar_data(u_info.get('created_at'))
                        expira = formatar_data(u_info.get('exp_date'))
                        ativos = u_info.get('active_cons', '0')
                        maximos = u_info.get('max_connections', '0')
                        
                        print(f"✅ OK ({status})")
                        dados_finais.append([nome_exibicao, criado, expira, f"{ativos}/{maximos}", status])
                except Exception as e:
                    print("⚠️ Erro JSON")
                    dados_finais.append([nome_exibicao, "-", "-", "-", "Erro JSON"])
            elif response.status_code == 403:
                print("🚫 Bloqueado (403)")
                dados_finais.append([nome_exibicao, "-", "-", "-", "Bloqueado"])
            elif response.status_code == 404:
                print("❓ Não encontrado (404)")
                dados_finais.append([nome_exibicao, "-", "-", "-", "Não Achou"])
            else:
                print(f"⚠️ Erro {response.status_code}")
                dados_finais.append([nome_exibicao, "-", "-", "-", f"Erro {response.status_code}"])

        except requests.exceptions.ConnectTimeout:
            print("⏰ Timeout")
            dados_finais.append([nome_exibicao, "-", "-", "-", "Timeout"])
        except requests.exceptions.ConnectionError:
             print("🔌 Falha Conexão")
             dados_finais.append([nome_exibicao, "-", "-", "-", "Offline"])
        except Exception as e:
            print(f"💥 Erro: {e}")
            dados_finais.append([nome_exibicao, "-", "-", "-", "Erro Geral"])
            
    return dados_finais

def gerar_imagem(dados):
    print("\n🎨 Gerando imagem 'status.png'...")
    largura = 1100 
    altura_linha = 40
    altura_cabecalho = 120
    altura_total = altura_cabecalho + (len(dados) * altura_linha) + 40
    
    img = Image.new('RGB', (largura, altura_total), color=(18, 18, 24))
    d = ImageDraw.Draw(img)
    
    # Lógica para carregar fontes tanto no Windows quanto no Linux
    try:
        sistema = platform.system()
        if sistema == "Windows":
            font_padrao = ImageFont.truetype("arial.ttf", 15)
            font_bold = ImageFont.truetype("arialbd.ttf", 15)
            font_titulo = ImageFont.truetype("arialbd.ttf", 24)
            font_sub = ImageFont.truetype("arial.ttf", 12)
        else:
            # Caminhos Linux (GitHub Actions / Ubuntu)
            caminho_fonte = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            caminho_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            font_padrao = ImageFont.truetype(caminho_fonte, 15)
            font_bold = ImageFont.truetype(caminho_bold, 15)
            font_titulo = ImageFont.truetype(caminho_bold, 24)
            font_sub = ImageFont.truetype(caminho_fonte, 12)
    except:
        # Fallback se não achar nada
        font_padrao = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_titulo = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Cabeçalho
    d.rectangle([(0, 0), (largura, 90)], fill=(30, 30, 40))
    
    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    data_hora_brasil = datetime.now(fuso_horario)
    agora = data_hora_brasil.strftime("%d/%m/%Y - %H:%M (Brasília)")
    
    d.text((30, 20), "MONITORAMENTO IPTV", fill=(0, 200, 255), font=font_titulo)
    d.text((30, 55), f"Atualizado: {agora}", fill=(150, 150, 150), font=font_sub)
    
    # Colunas
    y_col = 100
    colunas = [
        ("FONTE", 30), 
        ("CRIADO EM", 280),
        ("VENCIMENTO", 480), 
        ("CONEXÕES", 700), 
        ("STATUS", 900)
    ]
    
    for nome, x in colunas:
        d.text((x, y_col), nome, fill=(100, 255, 100), font=font_bold)
    
    d.line([(30, y_col + 25), (largura-30, y_col + 25)], fill=(80, 80, 80), width=1)

    # Linhas
    y = y_col + 40
    for i, linha in enumerate(dados):
        nome, criado, vence, conexoes, status = linha
        
        if i % 2 == 0: d.rectangle([(10, y-5), (largura-10, y+30)], fill=(25, 25, 35))

        cor = (220, 220, 220)
        cor_st = (255, 50, 50) # Vermelho padrão
        
        if status == "Active": cor_st = (50, 255, 50)
        elif status == "Expiring Soon": cor_st = (255, 165, 0)
        elif status == "Bloqueado": cor_st = (255, 0, 0)

        d.text((30, y), str(nome), fill=cor, font=font_padrao)
        d.text((280, y), str(criado), fill=cor, font=font_padrao)
        d.text((480, y), str(vence), fill=cor, font=font_padrao)
        d.text((700, y), str(conexoes), fill=cor, font=font_padrao)
        d.text((900, y), str(status), fill=cor_st, font=font_bold)
        y += altura_linha

    img.save("status.png")
    print("🖼️  Imagem salva com sucesso.")

def criar_video():
    print("🎬 Tentando gerar vídeo...")
    # Verifica se o ffmpeg está disponível
    try:
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", "status.png", 
            "-c:v", "libx264", "-t", "10", "-pix_fmt", "yuv420p", 
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "video_status.mp4"
        ]
        # Redireciona a saída para devnull para não poluir o terminal, exceto se der erro
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Vídeo 'video_status.mp4' gerado com sucesso!")
    except FileNotFoundError:
        print("⚠️  FFmpeg não encontrado no sistema. Apenas a imagem foi gerada.")
    except subprocess.CalledProcessError:
        print("⚠️  Erro ao executar o FFmpeg.")
    except Exception as e:
        print(f"⚠️  Não foi possível gerar vídeo: {e}")

if __name__ == "__main__":
    lista = obter_lista_links()
    if lista:
        dados = analisar_links(lista)
        gerar_imagem(dados)
        criar_video()
    else:
        print("Nenhum dado para processar.")

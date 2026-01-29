import requests
import json
import os
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Lendo os links do Segredo do GitHub
links_secret = os.environ.get("MEUS_LINKS")
if links_secret:
    urls = [link.strip() for link in links_secret.split(',')]
else:
    print("ERRO: Segredo MEUS_LINKS não encontrado!")
    urls = []

def formatar_data(timestamp):
    if not timestamp: return "N/A"
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')
    except: return "Erro"

def obter_dados():
    resultados = []
    for url in urls:
        if not url: continue
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                u_info = data.get('user_info', {})
                usuario = u_info.get('username', 'Desconhecido')
                expira = formatar_data(u_info.get('exp_date'))
                ativos = u_info.get('active_cons', '0')
                maximos = u_info.get('max_connections', '0')
                status = u_info.get('status', 'Off')
                resultados.append([usuario, expira, f"{ativos}/{maximos}", status])
            else:
                resultados.append(["Erro Conexão", "-", "-", "Erro"])
        except:
            resultados.append(["Erro Link", "-", "-", "Falha"])
    return resultados

def criar_imagem(dados):
    W, H = 800, 600 # Tamanho do vídeo
    img = Image.new('RGB', (W, H), color=(15, 15, 20))
    d = ImageDraw.Draw(img)
    
    # Fontes
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
        font_title = ImageFont.load_default()

    # Título
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    d.text((20, 20), f"Painel IPTV - {agora}", fill=(255, 200, 0), font=font_title)

    # Cabeçalho
    y = 80
    d.text((20, y), "USUÁRIO", fill=(0, 255, 255), font=font)
    d.text((250, y), "VENCIMENTO", fill=(0, 255, 255), font=font)
    d.text((450, y), "CONEXÕES", fill=(0, 255, 255), font=font)
    d.text((600, y), "STATUS", fill=(0, 255, 255), font=font)
    
    # Linha divisória
    d.line([(20, y+25), (780, y+25)], fill=(100,100,100), width=2)

    # Lista
    y += 40
    for linha in dados:
        cor = (255, 255, 255)
        if linha[3] != "Active": cor = (255, 80, 80) # Vermelho se não ativo
        
        d.text((20, y), str(linha[0]), fill=cor, font=font)
        d.text((250, y), str(linha[1]), fill=cor, font=font)
        d.text((450, y), str(linha[2]), fill=cor, font=font)
        d.text((600, y), str(linha[3]), fill=cor, font=font)
        y += 30

    img.save("status.png")

def criar_video():
    # Cria vídeo de 10 segundos
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", "status.png", 
        "-c:v", "libx264", "-t", "10", "-pix_fmt", "yuv420p", 
        "-vf", "scale=800:600", "video_status.mp4"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    dados = obter_dados()
    criar_imagem(dados)
    criar_video()

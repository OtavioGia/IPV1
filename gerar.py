import requests
import json
import os
import subprocess
import platform
import math
import time
import traceback
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# SEUS LINKS (HARDCODED)
# ==========================================
MEUS_LINKS_TEXTO = """
F14M2|http://play.dnsrot.vip/player_api.php?username=5550388689&password=simpleiptv,
F15M2|http://play.dnsrot.vip/player_api.php?&username=Marcosfp05&password=nlybdft6fml,
F25M3|http://megaxc.ca/player_api.php?&username=ialwg1&password=iao8wo,
F27M1|http://play.dnsrot.vip/player_api.php?&username=nena6194sala&password=mqtavfrtyl,
F28M1|http://play.dnsrot.vip/player_api.php?&username=tomoko11&password=14n11oi50oc,
F29M3|http://play.dnsrot.vip/player_api.php?&username=vanessanook&password=vinr390x8y,
F30M3|http://play.dnsrot.vip/player_api.php?&username=huhenz&password=fa7kum6q4bm,
F31M2|http://play.dnsrot.vip/player_api.php?&username=zQ4qeGkNrQ&password=factoryiptv,
F32M2|http://play.dnsrot.vip/player_api.php?&username=7RRjPTu5d6&password=factoryiptv,
F57M10|http://agkcl2.cc/player_api.php?&username=719065&password=r12xvZ,
F61M5|http://agkcl2.cc/player_api.php?&username=318284&password=pgJqrm,
F64M5|http://agkcl2.cc/player_api.php?&username=882170&password=A3FHej,
F65M5|http://agkcl2.cc/player_api.php?&username=888647&password=xjfFUu,
F67M5|http://cavalo.cc/player_api.php?&username=671409&password=f3UQjJ,
F68M5|http://cavalo.cc/player_api.php?&username=988060&password=zd7YEw,
F69M5|http://cavalo.cc/player_api.php?&username=525656&password=7UDTt9,
F70M5|http://cavalo.cc/player_api.php?&username=544119&password=87XJCZ,
F71M5|http://cavalo.cc/player_api.php?&username=671409&password=f3UQjJ,
F72M5|http://cavalo.cc/player_api.php?&username=166691&password=SqEdeF,
F74M5|http://cavalo.cc/player_api.php?&username=392157&password=fs8w4W,
F75M5|http://cavalo.cc/player_api.php?&username=393747&password=PEHcPC,
F76M5|http://cavalo.cc/player_api.php?&username=563593&password=vGfUjy,
F77M5|http://cavalo.cc/player_api.php?&username=296115&password=bn2aGw,
F78M5|http://cavalo.cc/player_api.php?&username=166691&password=SqEdeF,
F79M5|http://cavalo.cc/player_api.php?&username=146336&password=zF39KA,
F80M5|http://cavalo.cc/player_api.php?&username=393747&password=PEHcPC,
F81M5|http://cavalo.cc/player_api.php?&username=965893&password=Rx5Vau,
F82M5|http://cavalo.cc/player_api.php?&username=544119&password=87XJCZ,
F84M5|http://cavalo.cc/player_api.php?&username=985028&password=Stj27w,
F85M5|http://cavalo.cc/player_api.php?&username=563593&password=vGfUjy,
F86M5|http://cavalo.cc/player_api.php?&username=525656&password=7UDTt9,
F87M5|http://cavalo.cc/player_api.php?&username=258275&password=GWDsuf,
F88M5|http://cavalo.cc/player_api.php?&username=023629&password=Gw91WV,
F89M5|http://cavalo.cc/player_api.php?&username=939041&password=8SA9sh,
F90M5|http://cavalo.cc/player_api.php?&username=241804&password=x27GNr,
F91M5|http://cavalo.cc/player_api.php?&username=146336&password=zF39KA,
F92M5|http://cavalo.cc/player_api.php?&username=965893&password=Rx5Vau,
F93M5|http://cavalo.cc/player_api.php?&username=258275&password=GWDsuf,
F94M5|http://cavalo.cc/player_api.php?&username=296115&password=bn2aGw,
F95M5|http://cavalo.cc/player_api.php?&username=939041&password=8SA9sh,
F96M5|http://cavalo.cc/player_api.php?&username=023629&password=Gw91WV,
F97M5|http://cavalo.cc/player_api.php?&username=392157&password=fs8w4W,
F98M5|http://cavalo.cc/player_api.php?&username=988060&password=zd7YEw,
Fonte U38|http://case2.lat/player_api.php?&username=593812776&password=876362759,
Fonte U39|http://case2.lat/player_api.php?&username=374897485&password=789272274,
Fonte U40|http://case2.lat/player_api.php?&username=961386894&password=118897421,
Fonte U41|http://case2.lat/player_api.php?&username=718423457&password=539143340,
Fonte U42|http://case2.lat/player_api.php?&username=175473583&password=643238922,
Fonte U43|http://case2.lat/player_api.php?&username=587142841&password=619556956,
Fonte U44|http://case2.lat/player_api.php?&username=753685114&password=689268878,
Fonte U45|http://case2.lat/player_api.php?&username=648866758&password=722737417,
Fonte U46|http://case2.lat/player_api.php?&username=399392844&password=784365638,
Fonte U47|http://case2.lat/player_api.php?&username=858257510&password=975651644,
Fonte U48|http://case2.lat/player_api.php?&username=223141736&password=496767276,
Fonte U49|http://case2.lat/player_api.php?&username=777951153&password=939114817,
Fonte U50|http://case2.lat/player_api.php?&username=971812357&password=246137274,
Fonte U51|http://case2.lat/player_api.php?&username=988493659&password=241861732,
Fonte U52|http://case2.lat/player_api.php?&username=943285414&password=493936454,
Fonte U53|http://case2.lat/player_api.php?&username=872689987&password=824513989,
Fonte U54|http://case2.lat/player_api.php?&username=338365128&password=769491152,
Fonte U55|http://case2.lat/player_api.php?&username=754551879&password=531553919
"""

# Nome do arquivo de debug
DEBUG_FILE = "debug_relatorio.txt"


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
    if not timestamp:
        return "---"
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')
    except Exception:
        return "Indefinido"


def analisar_links(lista_itens):
    print("\n🔎 Iniciando verificação de status...\n")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive'
    }

    dados_finais = []
    debug_entries = []  # cada item: dict com todos os detalhes daquela fonte

    for idx, (nome_custom, url) in enumerate(lista_itens, start=1):
        nome_exibicao = nome_custom
        print(f"Verificando: {nome_exibicao}...", end=" ")

        debug = {
            "indice": idx,
            "nome": nome_exibicao,
            "url": url,
            "inicio_ts": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "tempo_resposta": None,
            "http_status": None,
            "content_type": None,
            "tamanho_bytes": None,
            "raw_preview": None,
            "json_keys": None,
            "user_info_keys": None,
            "status_final": None,
            "exception_tipo": None,
            "exception_msg": None,
            "traceback": None,
            "observacoes": []
        }

        t0 = time.time()
        try:
            response = requests.get(url, headers=headers, timeout=20)
            debug["tempo_resposta"] = round(time.time() - t0, 2)
            debug["http_status"] = response.status_code
            debug["content_type"] = response.headers.get('Content-Type', 'N/A')
            debug["tamanho_bytes"] = len(response.content)

            if response.status_code == 200:
                debug["raw_preview"] = response.text[:800]
                try:
                    data = response.json()
                    debug["json_keys"] = list(data.keys())
                    u_info = data.get('user_info', {})

                    if not u_info:
                        print("❌ Erro Login")
                        debug["status_final"] = "Erro Login"
                        debug["observacoes"].append(
                            "user_info veio vazio/ausente no JSON. Corpo completo (limitado a 1500 chars): "
                            + json.dumps(data, ensure_ascii=False)[:1500]
                        )
                        dados_finais.append([nome_exibicao, "-", "-", "-", "Erro Login"])
                    else:
                        debug["user_info_keys"] = list(u_info.keys())
                        status = u_info.get('status', 'Unknown')
                        criado = formatar_data(u_info.get('created_at'))
                        expira = formatar_data(u_info.get('exp_date'))
                        ativos = u_info.get('active_cons', '0')
                        maximos = u_info.get('max_connections', '0')

                        print(f"✅ OK ({status})")
                        debug["status_final"] = status
                        debug["observacoes"].append(
                            f"created_at={u_info.get('created_at')} | exp_date={u_info.get('exp_date')} | "
                            f"active_cons={ativos} | max_connections={maximos}"
                        )
                        dados_finais.append([nome_exibicao, criado, expira, f"{ativos}/{maximos}", status])
                except Exception as e_json:
                    print("⚠️ Erro JSON")
                    debug["status_final"] = "Erro JSON"
                    debug["exception_tipo"] = type(e_json).__name__
                    debug["exception_msg"] = str(e_json)
                    debug["traceback"] = traceback.format_exc()
                    dados_finais.append([nome_exibicao, "-", "-", "-", "Erro JSON"])

            elif response.status_code == 403:
                print("🚫 Bloqueado (IP)")
                debug["status_final"] = "Bloq. IP"
                debug["raw_preview"] = response.text[:800]
                dados_finais.append([nome_exibicao, "-", "-", "-", "Bloq. IP"])
            elif response.status_code == 404:
                print("❓ Não encontrado")
                debug["status_final"] = "Não Achou"
                debug["raw_preview"] = response.text[:800]
                dados_finais.append([nome_exibicao, "-", "-", "-", "Não Achou"])
            else:
                print(f"⚠️ Erro {response.status_code}")
                debug["status_final"] = f"Erro {response.status_code}"
                debug["raw_preview"] = response.text[:800]
                dados_finais.append([nome_exibicao, "-", "-", "-", f"Erro {response.status_code}"])

        except requests.exceptions.Timeout as e:
            print("🔌 Falha Conexão (Timeout)")
            debug["tempo_resposta"] = round(time.time() - t0, 2)
            debug["status_final"] = "Offline"
            debug["exception_tipo"] = "Timeout"
            debug["exception_msg"] = str(e)
            debug["traceback"] = traceback.format_exc()
            dados_finais.append([nome_exibicao, "-", "-", "-", "Offline"])

        except requests.exceptions.ConnectionError as e:
            print("🔌 Falha Conexão (ConnectionError)")
            debug["tempo_resposta"] = round(time.time() - t0, 2)
            debug["status_final"] = "Offline"
            debug["exception_tipo"] = "ConnectionError"
            debug["exception_msg"] = str(e)
            debug["traceback"] = traceback.format_exc()
            dados_finais.append([nome_exibicao, "-", "-", "-", "Offline"])

        except Exception as e:
            print("🔌 Falha Conexão")
            debug["tempo_resposta"] = round(time.time() - t0, 2)
            debug["status_final"] = "Offline"
            debug["exception_tipo"] = type(e).__name__
            debug["exception_msg"] = str(e)
            debug["traceback"] = traceback.format_exc()
            dados_finais.append([nome_exibicao, "-", "-", "-", "Offline"])

        debug_entries.append(debug)

    # Gera o relatório de debug em txt (não interfere na geração de imagem/vídeo)
    gerar_debug_txt(debug_entries)

    return dados_finais


def gerar_debug_txt(debug_entries):
    print(f"\n📝 Gerando relatório de debug detalhado: {DEBUG_FILE}")

    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    agora = datetime.now(fuso_horario).strftime("%d/%m/%Y - %H:%M:%S")

    # Resumo por status_final
    resumo = {}
    for d in debug_entries:
        chave = d["status_final"] or "Indefinido"
        resumo[chave] = resumo.get(chave, 0) + 1

    linhas = []
    linhas.append("=" * 100)
    linhas.append("RELATÓRIO DE DEBUG - MONITORAMENTO IPTV")
    linhas.append(f"Execução em: {agora}")
    linhas.append(f"Total de fontes verificadas: {len(debug_entries)}")
    linhas.append("=" * 100)
    linhas.append("")
    linhas.append("RESUMO POR STATUS:")
    for status, qtd in sorted(resumo.items(), key=lambda x: -x[1]):
        linhas.append(f"  - {status}: {qtd}")
    linhas.append("")
    linhas.append("=" * 100)
    linhas.append("DETALHE POR FONTE")
    linhas.append("=" * 100)

    for d in debug_entries:
        linhas.append("")
        linhas.append("-" * 100)
        linhas.append(f"[{d['indice']}/{len(debug_entries)}] FONTE: {d['nome']}")
        linhas.append(f"URL: {d['url']}")
        linhas.append(f"Início da checagem: {d['inicio_ts']}")
        linhas.append(f"Tempo de resposta: {d['tempo_resposta']}s" if d['tempo_resposta'] is not None else "Tempo de resposta: N/A")
        linhas.append(f"HTTP Status Code: {d['http_status']}")
        linhas.append(f"Content-Type: {d['content_type']}")
        linhas.append(f"Tamanho da resposta: {d['tamanho_bytes']} bytes" if d['tamanho_bytes'] is not None else "Tamanho da resposta: N/A")
        linhas.append(f"STATUS FINAL ATRIBUÍDO: {d['status_final']}")

        if d["json_keys"] is not None:
            linhas.append(f"Chaves no JSON raiz: {d['json_keys']}")
        if d["user_info_keys"] is not None:
            linhas.append(f"Chaves em user_info: {d['user_info_keys']}")

        for obs in d["observacoes"]:
            linhas.append(f"Observação: {obs}")

        if d["exception_tipo"]:
            linhas.append(f"❌ EXCEÇÃO: {d['exception_tipo']} -> {d['exception_msg']}")
            linhas.append("Traceback completo:")
            linhas.append(d["traceback"])

        if d["raw_preview"]:
            linhas.append("Resposta bruta (preview, até 800 caracteres):")
            linhas.append(d["raw_preview"])

    linhas.append("")
    linhas.append("=" * 100)
    linhas.append("FIM DO RELATÓRIO")
    linhas.append("=" * 100)

    try:
        with open(DEBUG_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas))
        print(f"✅ Relatório de debug salvo em '{DEBUG_FILE}'")
    except Exception as e:
        print(f"⚠️ Falha ao salvar relatório de debug: {e}")


def carregar_fontes():
    """Carrega fontes ajustadas para modo compacto (mais linhas)."""
    fontes = {}
    try:
        sistema = platform.system()
        base_size = 19
        title_size = 36

        if sistema == "Windows":
            fontes['padrao'] = ImageFont.truetype("arial.ttf", base_size)
            fontes['bold'] = ImageFont.truetype("arialbd.ttf", base_size)
            fontes['titulo'] = ImageFont.truetype("arialbd.ttf", title_size)
            fontes['sub'] = ImageFont.truetype("arial.ttf", 16)
        else:
            path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            path_b = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            fontes['padrao'] = ImageFont.truetype(path, base_size)
            fontes['bold'] = ImageFont.truetype(path_b, base_size)
            fontes['titulo'] = ImageFont.truetype(path_b, title_size)
            fontes['sub'] = ImageFont.truetype(path, 16)
    except Exception:
        fontes['padrao'] = ImageFont.load_default()
        fontes['bold'] = ImageFont.load_default()
        fontes['titulo'] = ImageFont.load_default()
        fontes['sub'] = ImageFont.load_default()

    return fontes


def gerar_imagens_paginadas(dados):
    print("\n🎨 Gerando imagens (Modo Compacto - Alta Densidade)...")

    LARGURA = 1920
    ALTURA = 1080
    MARGEM_X = 50

    Y_INICIAL = 140
    ALTURA_LINHA = 34
    ALTURA_RODAPE = 40

    espaco_disponivel = ALTURA - Y_INICIAL - ALTURA_RODAPE
    itens_por_pagina = espaco_disponivel // ALTURA_LINHA

    print(f"ℹ️  Capacidade por página: {itens_por_pagina} linhas.")

    total_paginas = math.ceil(len(dados) / itens_por_pagina)
    fontes = carregar_fontes()

    nomes_arquivos = []

    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    agora = datetime.now(fuso_horario).strftime("%d/%m/%Y - %H:%M")

    for pagina in range(total_paginas):
        img = Image.new('RGB', (LARGURA, ALTURA), color=(15, 15, 25))
        d = ImageDraw.Draw(img)

        d.rectangle([(0, 0), (LARGURA, 90)], fill=(30, 30, 50))
        d.text((MARGEM_X, 20), "MONITORAMENTO IPTV", fill=(0, 255, 255), font=fontes['titulo'])
        d.text((MARGEM_X, 65), f"Atualizado: {agora} | Pág {pagina + 1}/{total_paginas}", fill=(200, 200, 200), font=fontes['sub'])

        colunas_x = [50, 600, 900, 1200, 1500]
        titulos = ["FONTE / SERVIDOR", "CRIADO", "VENCE", "CONEX", "STATUS"]

        y_header = 100
        d.rectangle([(MARGEM_X, y_header), (LARGURA - MARGEM_X, y_header + 30)], fill=(50, 50, 70))

        for i, titulo in enumerate(titulos):
            d.text((colunas_x[i], y_header + 5), titulo, fill=(255, 215, 0), font=fontes['bold'])

        inicio = pagina * itens_por_pagina
        fim = inicio + itens_por_pagina
        dados_pagina = dados[inicio:fim]

        y = Y_INICIAL
        for i, linha in enumerate(dados_pagina):
            nome, criado, vence, conexoes, status = linha

            if i % 2 == 0:
                d.rectangle([(MARGEM_X, y), (LARGURA - MARGEM_X, y + ALTURA_LINHA)], fill=(22, 22, 32))
            else:
                d.rectangle([(MARGEM_X, y), (LARGURA - MARGEM_X, y + ALTURA_LINHA)], fill=(28, 28, 38))

            cor_texto = (230, 230, 230)
            cor_status = (255, 50, 50)

            status_lower = str(status).lower()
            if "active" in status_lower:
                cor_status = (50, 255, 50)
            elif "expiring" in status_lower:
                cor_status = (255, 165, 0)
            elif "bloq" in status_lower or "403" in status_lower:
                cor_status = (200, 0, 0)

            offset_y = 6

            d.text((colunas_x[0], y + offset_y), str(nome), fill=cor_texto, font=fontes['padrao'])
            d.text((colunas_x[1], y + offset_y), str(criado), fill=cor_texto, font=fontes['padrao'])
            d.text((colunas_x[2], y + offset_y), str(vence), fill=cor_texto, font=fontes['padrao'])
            d.text((colunas_x[3], y + offset_y), str(conexoes), fill=cor_texto, font=fontes['padrao'])
            d.text((colunas_x[4], y + offset_y), str(status), fill=cor_status, font=fontes['bold'])

            y += ALTURA_LINHA

        nome_arquivo = f"status_{pagina}.png"
        img.save(nome_arquivo)
        nomes_arquivos.append(nome_arquivo)
        print(f"🖼️  Slide {pagina+1} gerado: {nome_arquivo}")

    return nomes_arquivos


def criar_video_slideshow(imagens):
    if not imagens:
        return

    print("🎬 Gerando vídeo slideshow (1920x1080)...")

    tempo_por_slide = "10"

    try:
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

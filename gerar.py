import requests
from requests.adapters import HTTPAdapter
try:
    from urllib3.util.retry import Retry
except ImportError:
    from requests.packages.urllib3.util.retry import Retry
import json
import os
import subprocess
import platform
import math
import time
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlsplit, urlunsplit
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

# Assinaturas conhecidas de página padrão do nginx (host sem vhost/API configurada)
ASSINATURAS_NGINX_DEFAULT = [
    "Welcome to nginx!",
    "welcome to nginx",
]

# ==========================================
# CONFIG DE VELOCIDADE / REDE
# ==========================================
MAX_WORKERS = 15          # quantas fontes verificar em paralelo
TIMEOUT_PRINCIPAL = 12     # timeout (s) da tentativa principal
TIMEOUT_ALTERNATIVO = 5    # timeout (s) de cada tentativa alternativa (https / portas extras)
ESPERA_RETRY_404 = 0.8     # espera (s) antes de repetir um 404 (possível falha transitória)

# ==========================================
# PROXY / VPN OPCIONAL (acesso "do Brasil")
# ==========================================
# CONFIRMADO no debug: agkcl2.cc e cavalo.cc funcionam no navegador (IP do Brasil)
# mas não funcionam rodando no GitHub Actions (IP de datacenter fora do Brasil).
# Isso é bloqueio por geolocalização de IP no servidor — não tem como contornar
# só com headers, PRECISA sair de um IP brasileiro (proxy/VPN pago).
#
# Preencha a URL do proxy aqui (ex: "http://usuario:senha@ip_do_proxy:porta").
# Deixe "" (vazio) para não usar proxy nenhum.
IPTV_PROXY = "45.224.240.53:1080"  # <<< PREENCHA AQUI SE QUISER USAR PROXY, OU DEIXE VAZIO

# Opcional: se quiser usar o proxy SÓ em alguns hosts (economiza tráfego pago),
# liste os domínios aqui. Deixe a lista VAZIA para usar o proxy em TUDO.
# Exemplo: PROXY_SOMENTE_HOSTS = ["agkcl2.cc", "cavalo.cc"]
PROXY_SOMENTE_HOSTS = []

IPTV_PROXY = IPTV_PROXY.strip()
PROXIES = {"http": IPTV_PROXY, "https": IPTV_PROXY} if IPTV_PROXY else None


def proxy_para_url(url):
    """Decide se essa URL específica deve usar o proxy configurado."""
    if not PROXIES:
        return None
    if not PROXY_SOMENTE_HOSTS:
        return PROXIES
    host = (urlsplit(url).hostname or "").lower()
    for alvo in PROXY_SOMENTE_HOSTS:
        if alvo.lower() in host:
            return PROXIES
    return None


_thread_local = threading.local()
_print_lock = threading.Lock()

# Cabeçalhos completos, imitando um Chrome real (ajuda em bot-fight-mode simples
# baseado só em headers; NÃO resolve bloqueio por geolocalização de IP).
HEADERS_NAVEGADOR = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    # NÃO anunciar suporte a Brotli ('br') aqui: o ambiente do GitHub Actions não
    # tem a lib de descompressão Brotli instalada. Se o servidor responder
    # comprimido em Brotli e o requests não conseguir descomprimir, o resultado
    # é lixo binário no lugar do JSON — foi exatamente isso que quebrou o
    # case2.lat (que antes funcionava 100%) numa rodada anterior deste script.
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}


def aquecer_sessao_se_necessario(sessao, url, proxies):
    """Visita a home do host antes da API, como um navegador faria ao abrir o
    site pela primeira vez. Ajuda em proteções simples baseadas em cookie/JS
    challenge leve. Roda no máximo 1 vez por host por thread."""
    aquecidos = getattr(_thread_local, "hosts_aquecidos", None)
    if aquecidos is None:
        aquecidos = set()
        _thread_local.hosts_aquecidos = aquecidos

    partes = urlsplit(url)
    host_key = f"{partes.scheme}://{partes.netloc}"
    if host_key in aquecidos:
        return
    aquecidos.add(host_key)

    try:
        sessao.get(host_key + "/", headers=HEADERS_NAVEGADOR, timeout=6, proxies=proxies)
    except Exception:
        pass  # aquecimento é best-effort; se falhar, segue pro request real mesmo assim


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
    if PROXIES:
        print("🌐 Proxy configurado via IPTV_PROXY — todas as requisições vão passar por ele.")
    else:
        print("ℹ️  Nenhum proxy configurado (variável IPTV_PROXY vazia). Requisições diretas.")

    vistos = {}
    for nome, url in lista_formatada:
        vistos.setdefault(url, []).append(nome)
    duplicados = {url: nomes for url, nomes in vistos.items() if len(nomes) > 1}
    if duplicados:
        print(f"⚠️  Atenção: {len(duplicados)} URL(s) duplicada(s) na lista (mesma conta usada em múltiplos nomes):")
        for url, nomes in duplicados.items():
            print(f"    {', '.join(nomes)} -> {url}")

    return lista_formatada


def formatar_data(timestamp):
    if not timestamp:
        return "---"
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')
    except Exception:
        return "Indefinido"


def eh_pagina_nginx_default(texto, content_type):
    if not texto:
        return False
    if content_type and 'json' in content_type.lower():
        return False
    texto_lower = texto.lower()
    for assinatura in ASSINATURAS_NGINX_DEFAULT:
        if assinatura.lower() in texto_lower:
            return True
    return False


# Portas comumente usadas por painéis Xtream Codes além da porta original
PORTAS_ALTERNATIVAS = [8080, 8880, 2095, 2052, 2082, 2086]


def gerar_urls_alternativas(url_original):
    alternativas = []
    partes = urlsplit(url_original)

    if partes.scheme == "http":
        https_url = urlunsplit(("https",) + partes[1:])
        alternativas.append(("HTTPS (mesma porta)", https_url))

    host_sem_porta = partes.hostname or ""
    if host_sem_porta:
        for porta in PORTAS_ALTERNATIVAS:
            if partes.port == porta:
                continue
            netloc = f"{host_sem_porta}:{porta}"
            url_alt = urlunsplit((partes.scheme, netloc, partes.path, partes.query, partes.fragment))
            alternativas.append((f"Porta {porta}", url_alt))

    return alternativas


def _criar_retry_seguro(total):
    """Cria um objeto Retry que NUNCA obedece o header 'Retry-After' do servidor.

    Motivo: alguns hosts atrás de Cloudflare (cavalo.cc, case2.lat, etc.) respondem
    521 (origem fora do ar) e às vezes mandam 'Retry-After: 120'. Por padrão o
    urllib3 obedece isso e literalmente PARA a thread por 2 minutos — foi essa a
    causa dos travamentos gigantes no relatório anterior. Aqui a gente desliga
    esse comportamento e limita qualquer backoff a poucos segundos.
    """
    retry = Retry(
        total=total,
        connect=total,
        read=total,
        backoff_factor=0.3,
        status_forcelist=[429, 500, 502, 503, 504, 520, 521, 522, 523, 524],
        allowed_methods=frozenset(['GET']),
        respect_retry_after_header=False,  # <-- ESSENCIAL: ignora "espere 120s"
    )
    # Limita o teto do backoff exponencial, cobrindo versões antigas e novas do urllib3.
    try:
        retry.backoff_max = 3
    except Exception:
        pass
    try:
        retry.BACKOFF_MAX = 3
    except Exception:
        pass
    return retry


def obter_sessao_da_thread():
    """Sessão 'principal' de cada thread: tem 1 retry automático para falhas
    transitórias reais (5xx passageiro), mas nunca trava por Retry-After."""
    sessao = getattr(_thread_local, "sessao", None)
    if sessao is None:
        sessao = requests.Session()
        adapter = HTTPAdapter(
            max_retries=_criar_retry_seguro(total=1),
            pool_connections=MAX_WORKERS,
            pool_maxsize=MAX_WORKERS,
        )
        sessao.mount("http://", adapter)
        sessao.mount("https://", adapter)
        _thread_local.sessao = sessao
    return sessao


def obter_sessao_exploratoria_da_thread():
    """Sessão usada só para tentativas alternativas (https, portas extras).
    Zero retries automáticos aqui: se falhar, a gente mesmo decide o próximo
    passo — assim nenhuma dessas tentativas "de sorte" pode travar o pool."""
    sessao = getattr(_thread_local, "sessao_exploratoria", None)
    if sessao is None:
        sessao = requests.Session()
        adapter = HTTPAdapter(
            max_retries=_criar_retry_seguro(total=0),
            pool_connections=MAX_WORKERS,
            pool_maxsize=MAX_WORKERS,
        )
        sessao.mount("http://", adapter)
        sessao.mount("https://", adapter)
        _thread_local.sessao_exploratoria = sessao
    return sessao


def parece_binario_nao_decodificado(response):
    """Detecta o sintoma de conteúdo comprimido (ex: Brotli) que o requests não
    conseguiu descomprimir: texto cheio de bytes de controle/não-imprimíveis,
    normalmente sem nenhuma chance de ser JSON de verdade."""
    texto = response.text[:200] if response.text else ""
    if not texto:
        return False
    nao_imprimiveis = sum(1 for c in texto if ord(c) < 32 and c not in "\r\n\t")
    nao_imprimiveis += sum(1 for c in texto if ord(c) > 126)
    return (nao_imprimiveis / max(len(texto), 1)) > 0.25


def processar_resposta_json(response, debug):
    if parece_binario_nao_decodificado(response):
        debug["status_final"] = "Erro Decodificação (binário)"
        debug["observacoes"].append(
            "Resposta veio como bytes não-imprimíveis, típico de conteúdo comprimido "
            "(ex: Brotli) que o requests não conseguiu descomprimir nesse ambiente. "
            f"Content-Encoding do servidor: {response.headers.get('Content-Encoding', 'N/A')}."
        )
        return False, None
    try:
        data = response.json()
        debug["json_keys"] = list(data.keys())
        u_info = data.get('user_info', {})

        if not u_info:
            debug["status_final"] = "Erro Login"
            debug["observacoes"].append(
                "user_info veio vazio/ausente no JSON. Corpo completo (limitado a 1500 chars): "
                + json.dumps(data, ensure_ascii=False)[:1500]
            )
            return True, ["-", "-", "-", "Erro Login"]

        debug["user_info_keys"] = list(u_info.keys())
        status = u_info.get('status', 'Unknown')
        criado = formatar_data(u_info.get('created_at'))
        expira = formatar_data(u_info.get('exp_date'))
        ativos = u_info.get('active_cons', '0')
        maximos = u_info.get('max_connections', '0')

        debug["status_final"] = status
        debug["observacoes"].append(
            f"created_at={u_info.get('created_at')} | exp_date={u_info.get('exp_date')} | "
            f"active_cons={ativos} | max_connections={maximos}"
        )
        return True, [criado, expira, f"{ativos}/{maximos}", status]

    except Exception as e_json:
        debug["exception_tipo"] = type(e_json).__name__
        debug["exception_msg"] = str(e_json)
        debug["traceback"] = traceback.format_exc()
        return False, None


def verificar_fonte(idx, nome_custom, url, headers):
    """Verifica uma única fonte. Roda dentro de uma thread do pool."""
    sessao = obter_sessao_da_thread()

    debug = {
        "indice": idx,
        "nome": nome_custom,
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
        "observacoes": [],
        "tentativas": []
    }

    t0 = time.time()
    linha_resultado = None
    msg_console = None
    proxy_desta_url = proxy_para_url(url)

    aquecer_sessao_se_necessario(sessao, url, proxy_desta_url)

    try:
        response = sessao.get(url, headers=headers, timeout=TIMEOUT_PRINCIPAL, proxies=proxy_desta_url)
        debug["tempo_resposta"] = round(time.time() - t0, 2)
        debug["http_status"] = response.status_code
        debug["content_type"] = response.headers.get('Content-Type', 'N/A')
        debug["tamanho_bytes"] = len(response.content)
        debug["tentativas"].append({"url": url, "resultado": f"HTTP {response.status_code}"})

        if response.status_code == 200:
            debug["raw_preview"] = response.text[:800]

            if eh_pagina_nginx_default(response.text, debug["content_type"]):
                debug["observacoes"].append(
                    "Resposta inicial era página padrão do nginx (sem vhost/API configurada). Tentando URLs alternativas..."
                )
                sessao_exp = obter_sessao_exploratoria_da_thread()
                sucesso_alt = False
                for label, url_alt in gerar_urls_alternativas(url):
                    try:
                        proxy_alt = proxy_para_url(url_alt)
                        resp_alt = sessao_exp.get(url_alt, headers=headers, timeout=TIMEOUT_ALTERNATIVO, proxies=proxy_alt)
                        ct_alt = resp_alt.headers.get('Content-Type', 'N/A')
                        if resp_alt.status_code == 200 and not eh_pagina_nginx_default(resp_alt.text, ct_alt):
                            ok, linha = processar_resposta_json(resp_alt, debug)
                            debug["tentativas"].append({
                                "url": url_alt,
                                "resultado": f"{label} -> HTTP {resp_alt.status_code}, JSON OK" if ok else f"{label} -> HTTP {resp_alt.status_code}, falhou parse JSON"
                            })
                            if ok:
                                debug["raw_preview"] = resp_alt.text[:800]
                                debug["http_status"] = resp_alt.status_code
                                debug["content_type"] = ct_alt
                                linha_resultado = linha
                                sucesso_alt = True
                                msg_console = f"✅ OK via {label} ({linha[-1]})"
                                break
                        else:
                            debug["tentativas"].append({
                                "url": url_alt,
                                "resultado": f"{label} -> HTTP {resp_alt.status_code}, ainda nginx/sem API"
                            })
                    except Exception as e_alt:
                        debug["tentativas"].append({
                            "url": url_alt,
                            "resultado": f"{label} -> falhou: {type(e_alt).__name__}: {e_alt}"
                        })

                if not sucesso_alt:
                    msg_console = "🌐 Painel Offline (Nginx)"
                    debug["status_final"] = "Painel Offline (Nginx)"
                    debug["observacoes"].append(
                        "Nenhuma variação de URL (https, porta 8080) retornou API válida."
                    )
                    linha_resultado = ["-", "-", "-", "Painel Offline (Nginx)"]

            else:
                ok, linha = processar_resposta_json(response, debug)
                if ok:
                    status_txt = linha[-1]
                    if status_txt == "Erro Login":
                        msg_console = "❌ Erro Login"
                    else:
                        msg_console = f"✅ OK ({status_txt})"
                    linha_resultado = linha
                else:
                    status_ja_definido = debug.get("status_final")
                    status_final = status_ja_definido or "Erro JSON"
                    debug["status_final"] = status_final
                    if status_final == "Erro Decodificação (binário)":
                        msg_console = "🧩 Erro Decodificação (binário)"
                    else:
                        msg_console = "⚠️ Erro JSON"
                    linha_resultado = ["-", "-", "-", status_final]

        elif response.status_code == 403:
            msg_console = "🚫 Bloqueado (IP)"
            debug["status_final"] = "Bloq. IP"
            debug["raw_preview"] = response.text[:800]
            linha_resultado = ["-", "-", "-", "Bloq. IP"]

        elif response.status_code == 404:
            time.sleep(ESPERA_RETRY_404)
            try:
                resp_retry = obter_sessao_exploratoria_da_thread().get(
                    url, headers=headers, timeout=TIMEOUT_ALTERNATIVO, proxies=proxy_desta_url
                )
                debug["tentativas"].append({"url": url, "resultado": f"Retry 404 -> HTTP {resp_retry.status_code}"})
                if resp_retry.status_code == 200 and not eh_pagina_nginx_default(
                    resp_retry.text, resp_retry.headers.get('Content-Type', 'N/A')
                ):
                    ok, linha = processar_resposta_json(resp_retry, debug)
                    if ok:
                        debug["raw_preview"] = resp_retry.text[:800]
                        debug["http_status"] = resp_retry.status_code
                        debug["content_type"] = resp_retry.headers.get('Content-Type', 'N/A')
                        msg_console = f"✅ OK no retry ({linha[-1]})"
                        linha_resultado = linha
                if linha_resultado is None:
                    msg_console = "❓ Não encontrado"
                    debug["status_final"] = "Não Achou"
                    debug["raw_preview"] = response.text[:800]
                    linha_resultado = ["-", "-", "-", "Não Achou"]
            except Exception:
                msg_console = "❓ Não encontrado"
                debug["status_final"] = "Não Achou"
                debug["raw_preview"] = response.text[:800]
                linha_resultado = ["-", "-", "-", "Não Achou"]

        else:
            msg_console = f"⚠️ Erro {response.status_code}"
            debug["status_final"] = f"Erro {response.status_code}"
            debug["raw_preview"] = response.text[:800]
            linha_resultado = ["-", "-", "-", f"Erro {response.status_code}"]

    except requests.exceptions.Timeout as e:
        msg_console = "🔌 Falha Conexão (Timeout)"
        debug["tempo_resposta"] = round(time.time() - t0, 2)
        debug["status_final"] = "Offline"
        debug["exception_tipo"] = "Timeout"
        debug["exception_msg"] = str(e)
        debug["traceback"] = traceback.format_exc()
        linha_resultado = ["-", "-", "-", "Offline"]

    except requests.exceptions.ConnectionError as e:
        msg_console = "🔌 Falha Conexão (ConnectionError)"
        debug["tempo_resposta"] = round(time.time() - t0, 2)
        debug["status_final"] = "Offline"
        debug["exception_tipo"] = "ConnectionError"
        debug["exception_msg"] = str(e)
        debug["traceback"] = traceback.format_exc()
        linha_resultado = ["-", "-", "-", "Offline"]

    except Exception as e:
        msg_console = "🔌 Falha Conexão"
        debug["tempo_resposta"] = round(time.time() - t0, 2)
        debug["status_final"] = "Offline"
        debug["exception_tipo"] = type(e).__name__
        debug["exception_msg"] = str(e)
        debug["traceback"] = traceback.format_exc()
        linha_resultado = ["-", "-", "-", "Offline"]

    with _print_lock:
        print(f"[{idx:02d}] {nome_custom}: {msg_console}")

    return idx, nome_custom, linha_resultado, debug


def analisar_links(lista_itens):
    print(f"\n🔎 Iniciando verificação de status (paralelo, {MAX_WORKERS} por vez)...\n")

    headers = HEADERS_NAVEGADOR

    resultados = {}
    debug_entries = {}

    inicio_total = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(verificar_fonte, idx, nome, url, headers): idx
            for idx, (nome, url) in enumerate(lista_itens, start=1)
        }
        for future in as_completed(futures):
            idx, nome_custom, linha_resultado, debug = future.result()
            resultados[idx] = [nome_custom] + linha_resultado
            debug_entries[idx] = debug

    duracao_total = round(time.time() - inicio_total, 1)
    print(f"\n⏱️  Verificação concluída em {duracao_total}s.")

    # Reordena pelo índice original (a lista chega fora de ordem por causa do paralelismo)
    dados_finais = [resultados[i] for i in sorted(resultados.keys())]
    debug_ordenado = [debug_entries[i] for i in sorted(debug_entries.keys())]

    gerar_debug_txt(debug_ordenado, duracao_total)

    return dados_finais


def gerar_debug_txt(debug_entries, duracao_total=None):
    print(f"\n📝 Gerando relatório de debug detalhado: {DEBUG_FILE}")

    diferenca = timedelta(hours=-3)
    fuso_horario = timezone(diferenca)
    agora = datetime.now(fuso_horario).strftime("%d/%m/%Y - %H:%M:%S")

    resumo = {}
    for d in debug_entries:
        chave = d["status_final"] or "Indefinido"
        resumo[chave] = resumo.get(chave, 0) + 1

    linhas = []
    linhas.append("=" * 100)
    linhas.append("RELATÓRIO DE DEBUG - MONITORAMENTO IPTV")
    linhas.append(f"Execução em: {agora}")
    linhas.append(f"Total de fontes verificadas: {len(debug_entries)}")
    if duracao_total is not None:
        linhas.append(f"Tempo total de verificação (paralelo): {duracao_total}s")
    linhas.append(f"Proxy utilizado: {'Sim (IPTV_PROXY definido)' if PROXIES else 'Não'}")
    if PROXIES and PROXY_SOMENTE_HOSTS:
        linhas.append(f"Proxy aplicado apenas aos hosts: {', '.join(PROXY_SOMENTE_HOSTS)}")
    elif PROXIES:
        linhas.append("Proxy aplicado a TODAS as fontes.")
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

        if d["tentativas"]:
            linhas.append("Tentativas realizadas:")
            for t in d["tentativas"]:
                linhas.append(f"  - {t['url']} => {t['resultado']}")

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
            elif "offline" in status_lower or "nginx" in status_lower:
                cor_status = (150, 150, 150)

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

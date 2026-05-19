import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="RD Logistics & Material Técnico")

# =====================================================================
# BANCO DE DADOS EM MEMÓRIA (GERIDO PELO PAINEL ADMIN)
# =====================================================================
CONFIGURACOES = {
    "titulo": "RD Logistics & Distribuição",
    "descricao": "Distribuição de materiais técnicos para construção a seco e soluções logísticas.",
    "whatsapp": "351910000000",
    "cor_secundaria": "#00d2ff"
}

MERCADORIAS = [
    {
        "id": 1, 
        "nome": "Placa Pladur Standard", 
        "preco": 12.50, 
        "unidade": "un",
        "imagem": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?q=80&w=300&auto=format&fit=crop"
    },
    {
        "id": 2, 
        "nome": "Perfil Montante 45mm", 
        "preco": 3.80, 
        "unidade": "m",
        "imagem": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?q=80&w=300&auto=format&fit=crop"
    }
]

ADMIN_USER = "admin"
ADMIN_PASS = "rd_2026_secure"

# =====================================================================
# INTERFACE PÚBLICA (DESIGN ATUALIZADO)
# =====================================================================
@app.get("/", response_class=HTMLResponse)
async def home():
    itens_html = ""
    for item in MERCADORIAS:
        itens_html += f"""
        <div style="background:#0a0a0a; border:1px solid #111; padding:20px; border-radius:8px; text-align:center;">
            <img src="{item['imagem']}" style="width:100%; height:150px; object-fit:cover; border-radius:6px; margin-bottom:15px;">
            <h3 style="font-family:'Orbitron', sans-serif; font-size:1.1rem; color:#fff; margin:10px 0;">{item['nome']}</h3>
            <p style="color:{CONFIGURACOES['cor_secundaria']}; font-weight:bold; font-size:1.3rem; margin:5px 0;">{item['preco']:.2f}€ <span style="font-size:0.9rem; color:#888;">/ {item['unidade']}</span></p>
            <input type="number" value="1" min="1" id="qtd-{item['id']}" style="width:50px; background:#111; color:#fff; border:1px solid #333; padding:5px; text-align:center; margin-bottom:15px; border-radius:4px;"><br>
            <a href="https://wa.me/{CONFIGURACOES['whatsapp']}?text=Olá,+gostaria+de+encomendar+{item['nome']}" target="_blank" style="display:block; background:#000; color:{CONFIGURACOES['cor_secundaria']}; border:1px solid {CONFIGURACOES['cor_secundaria']}; text-decoration:none; padding:10px; border-radius:4px; font-family:'Orbitron'; font-weight:bold; font-size:0.85rem;">ADICIONAR</a>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="pt-pt">
    <head>
        <meta charset="UTF-8">
        <title>{CONFIGURACOES['titulo']}</title>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Urbanist:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {{ background:#000; color:#fff; font-family:'Urbanist', sans-serif; margin:0; padding-top:100px; }}
            header {{ position:fixed; top:0; left:0; width:100%; background:rgba(0,0,0,0.95); padding:15px 0; border-bottom:1px solid #111; z-index:100; }}
            .nav-box {{ max-width:1200px; margin:auto; display:flex; justify-content:space-between; align-items:center; padding:0 20px; }}
            .container {{ max-width:1200px; margin:auto; padding:20px; display:grid; grid-template-columns: 1fr 320px; gap:40px; }}
            .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap:25px; }}
            .checkout-box {{ background:#050505; border:1px solid #111; padding:20px; border-radius:8px; height:fit-content; }}
            .btn-checkout {{ display:block; width:100%; text-align:center; background:{CONFIGURACOES['cor_secundaria']}; color:#000; text-decoration:none; padding:12px 0; border-radius:4px; font-family:'Orbitron'; font-weight:bold; margin-top:15px; }}
            a.admin-link {{ color:#666; text-decoration:none; font-size:0.8rem; font-family:'Orbitron'; }}
        </style>
    </head>
    <body>
        <header>
            <div class="nav-box">
                <div style="font-family:'Orbitron'; font-weight:bold; color:#fff; font-size:1.4rem;">RD <span style="color:{CONFIGURACOES['cor_secundaria']}">LOGISTICS</span></div>
                <a href="/admin" class="admin-link">PAINEL CONTROL</a>
            </div>
        </header>
        
        <div class="container">
            <div>
                <div style="margin-bottom:40px;">
                    <h1 style="font-family:'Orbitron'; font-size:2.4rem; margin:0 0 10px 0;">{CONFIGURACOES['titulo']}</h1>
                    <p style="color:#aaa; font-size:1.1rem; margin:0;">{CONFIGURACOES['descricao']}</p>
                </div>
                <div class="grid">{itens_html}</div>
            </div>
            
            <div class="checkout-box">
                <h3 style="font-family:'Orbitron'; margin-top:0; border-bottom:1px solid #111; padding-bottom:10px;">TOTAL A PAGAR: <span style="color:red;">0.00€</span></h3>
                <a href="#" class="btn-checkout">AVANÇAR PARA CHECKOUT</a>
                <div style="margin-top:30px; background:#0a0a0a; border:1px solid #111; padding:15px; border-radius:6px;">
                    <h5 style="margin:0 0 10px 0; color:#aaa;">📍 Localização da Carga Viva</h5>
                    <p style="font-size:0.85rem; color:#666; margin:0;">Destino: Não definido (Preencha no Checkout)</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

# =====================================================================
# GESTÃO OPERACIONAL (AUTENTICAÇÃO & ACÇÕES)
# =====================================================================
def verificar_cookie(request: Request):
    if request.cookies.get("rd_session_token") != "active_authorized":
        raise HTTPException(status_code=401)
    return True

@app.get("/admin/login", response_class=HTMLResponse)
async def login_page():
    return f"""
    <body style="background:#000; color:#fff; font-family:sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
        <form action="/admin/login" method="POST" style="background:#050505; padding:40px; border-radius:8px; border:1px solid #111; width:300px;">
            <h2 style="color:{CONFIGURACOES['cor_secundaria']}; font-family:'Orbitron'; text-align:center; margin-top:0;">RD BACKOFFICE</h2>
            <input type="text" name="u" placeholder="Utilizador" style="display:block; width:100%; margin:15px 0; padding:12px; background:#000; border:1px solid #222; color:#fff;" required>
            <input type="password" name="p" placeholder="Palavra-passe" style="display:block; width:100%; margin:15px 0; padding:12px; background:#000; border:1px solid #222; color:#fff;" required>
            <button style="width:100%; padding:12px; background:{CONFIGURACOES['cor_secundaria']}; color:black; border:none; font-weight:bold; cursor:pointer; font-family:'Orbitron';">ENTRAR</button>
        </form>
    </body>
    """

@app.post("/admin/login")
async def login_action(u: str = Form(...), p: str = Form(...)):
    if u == ADMIN_USER and p == ADMIN_PASS:
        resp = RedirectResponse(url="/admin", status_code=303)
        resp.set_cookie(key="rd_session_token", value="active_authorized", httponly=True)
        return resp
    return RedirectResponse(url="/admin/login", status_code=303)

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, auth: bool = Depends(verificar_cookie)):
    linhas_produtos = "".join([f"""
    <tr style="border-bottom:1px solid #111;">
        <td style="padding:10px;"><img src="{item['imagem']}" style="width:40px; height:40px; object-fit:cover; border-radius:4px;"></td>
        <td style="padding:10px;">{item['nome']}</td>
        <td style="padding:10px; color:{CONFIGURACOES['cor_secundaria']}; font-weight:bold;">{item['preco']:.2f}€ / {item['unidade']}</td>
        <td style="padding:10px;"><a href="/admin/remover/{item['id']}" style="color:#ff3333; text-decoration:none; font-weight:bold;">[Remover]</a></td>
    </tr>""" for item in MERCADORIAS])

    return f"""
    <body style="background:#000; color:#fff; font-family:sans-serif; padding:40px;">
        <div style="display:flex; justify-content:space-between; align-items:center; max-width:1200px; margin:auto;">
            <h1 style="font-family:'Orbitron'; color:{CONFIGURACOES['cor_secundaria']};">🎛️ PAINEL ADMINISTRATIVO RD</h1>
            <a href="/" style="color:#fff; text-decoration:none; border:1px solid #333; padding:8px 15px; border-radius:4px;">Visualizar Site Público →</a>
        </div>
        <hr style="border-color:#111; margin:20px 0 40px 0;">
        
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:40px; max-width:1200px; margin:auto;">
            <div style="background:#050505; padding:25px; border-radius:8px; border:1px solid #111;">
                <h3 style="color:#ffc107; margin-top:0; font-family:'Orbitron';">🎨 Editar Textos Principais</h3>
                <form action="/admin/atualizar-site" method="POST">
                    Título: <input type="text" name="t" value="{CONFIGURACOES['titulo']}" style="width:100%; padding:10px; background:#000; border:1px solid #222; color:#fff; margin:5px 0 15px 0;"><br>
                    Descrição: <textarea name="d" style="width:100%; height:80px; padding:10px; background:#000; border:1px solid #222; color:#fff; margin:5px 0 15px 0;">{CONFIGURACOES['descricao']}</textarea><br>
                    WhatsApp: <input type="text" name="w" value="{CONFIGURACOES['whatsapp']}" style="width:100%; padding:10px; background:#000; border:1px solid #222; color:#fff; margin:5px 0 15px 0;"><br>
                    <button type="submit" style="background:green; color:white; padding:12px 20px; border:none; cursor:pointer; font-weight:bold; border-radius:4px;">Gravar Alterações</button>
                </form>
            </div>
            
            <div style="background:#050505; padding:25px; border-radius:8px; border:1px solid #111;">
                <h3 style="color:#28a745; margin-top:0; font-family:'Orbitron';">➕ Adicionar Nova Mercadoria</h3>
                <form action="/admin/adicionar-item" method="POST">
                    Nome: <input type="text" name="n" style="width:100%; padding:10px; background:#000; border:1px solid #222; color:#fff; margin:5px 0 15px 0;" required><br>
                    Preço (€): <input type="number" step="0.01" name="pr" style="width:100%; padding:10px; background:#000; border:1px solid #222; color:#fff; margin:5px 0 15px 0;" required><br>
                    Unidade (ex: un, m, kg): <input type="text" name="uni" value="un" style="width:100%; padding:10px; background:#000; border:1px solid #222; color:#fff; margin:5px 0 15px 0;" required><br>
                    Link Imagem: <input type="text" name="img" placeholder="https://..." style="width:100%; padding:10px; background:#000; border:1px solid #222; color:#fff; margin:5px 0 15px 0;" required><br>
                    <button type="submit" style="background:blue; color:white; padding:12px 20px; border:none; cursor:pointer; font-weight:bold; border-radius:4px;">Inserir na Montra</button>
                </form>
            </div>
        </div>

        <div style="max-width:1200px; margin:40px auto 0 auto; background:#050505; padding:25px; border-radius:8px; border:1px solid #111;">
            <h3 style="margin-top:0; font-family:'Orbitron';">📋 Mercadorias em Exibição</h3>
            <table style="width:100%; border-collapse:collapse; text-align:left;">
                <thead>
                    <tr style="border-bottom:2px solid #222; color:#aaa;">
                        <th style="padding:10px;">Foto</th>
                        <th style="padding:10px;">Nome</th>
                        <th style="padding:10px;">Preço/Unidade</th>
                        <th style="padding:10px;">Ação</th>
                    </tr>
                </thead>
                <tbody>{linhas_produtos}</tbody>
            </table>
        </div>
    </body>
    """

@app.post("/admin/atualizar-site")
async def atualizar_site(t: str = Form(...), d: str = Form(...), w: str = Form(...), auth: bool = Depends(verificar_cookie)):
    CONFIGURACOES["titulo"], CONFIGURACOES["descricao"], CONFIGURACOES["whatsapp"] = t, d, w
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/admin/adicionar-item")
async def adicionar_item(n: str = Form(...), pr: float = Form(...), uni: str = Form(...), img: str = Form(...), auth: bool = Depends(verificar_cookie)):
    novo_id = max([p["id"] for p in MERCADORIAS]) + 1 if MERCADORIAS else 1
    MERCADORIAS.append({"id": novo_id, "nome": n, "preco": pr, "unidade": uni, "imagem": img})
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/admin/remover/{item_id}")
async def remover_item(item_id: int, auth: bool = Depends(verificar_cookie)):
    global MERCADORIAS
    MERCADORIAS = [p for p in MERCADORIAS if p["id"] != item_id]
    return RedirectResponse(url="/admin", status_code=303)

@app.exception_handler(401)
async def custom_401_handler(request, exc): return RedirectResponse(url="/admin/login")

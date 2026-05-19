# ---- ROTA 3: PÁGINA EXCLUSIVA DE CHECKOUT OTIMIZADA ----
@app.get("/pagamento", response_class=HTMLResponse)
async def read_checkout():
    html_pay = f"""
    <!DOCTYPE html>
    <html lang="pt-pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RD Logistics | Pagamento Seguro</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Urbanist:wght@400;600;700&display=swap" rel="stylesheet">
        <script src="https://js.stripe.com/v3/"></script>
        <style>
            :root {{ --rd-red: #FF0000; --nexus-blue: #00d2ff; --dark-bg: #000000; }}
            body {{ margin: 0; background: var(--dark-bg); color: white; font-family: 'Urbanist', sans-serif; padding-top: 110px; }}
            
            /* Header síncrono integrado diretamente */
            header {{ position:fixed; top:0; left:0; width:100%; background:rgba(0,0,0,0.95); padding:15px 0; border-bottom:1px solid #111; z-index:100; }}
            .nav-box {{ max-width:1200px; margin:auto; display:flex; justify-content:space-between; align-items:center; padding:0 20px; }}
            
            .checkout-container {{ display: grid; grid-template-columns: 1.2fr 1.8fr; gap: 40px; max-width: 1200px; margin: auto; padding: 20px; }}
            .box-billing {{ background: #0a0a0a; border: 1px solid #222; border-radius: 12px; padding: 30px; }}
            .box-billing h3 {{ font-family: 'Orbitron'; margin-top: 0; color: var(--nexus-blue); border-bottom: 1px solid #1c1c1c; padding-bottom: 10px; }}
            
            .payment-methods {{ display: flex; gap: 20px; margin: 20px 0; }}
            .method-btn {{ flex: 1; background: #0f0f0f; border: 1px solid #222; color: white; padding: 18px 15px; border-radius: 8px; font-family: 'Orbitron'; font-weight: bold; cursor: pointer; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; transition: all 0.2s ease; position: relative; }}
            .method-btn.active {{ border-color: var(--rd-red); background: rgba(255, 0, 0, 0.05); box-shadow: 0 0 15px rgba(255,0,0,0.1); }}
            
            .logos-row {{ display: flex; gap: 8px; justify-content: center; align-items: center; }}
            .form-group {{ margin-bottom: 20px; }}
            .form-group label {{ display: block; font-size: 0.85rem; color: #888; font-family: 'Orbitron'; margin-bottom: 8px; }}
            .form-input {{ width: 100%; padding: 14px; background: #111; border: 1px solid #333; color: white; border-radius: 6px; font-size:1rem; box-sizing: border-box; }}
            .btn-pay-execute {{ width: 100%; background: #25D366; color: white; border: none; padding: 16px; border-radius: 6px; font-family: 'Orbitron'; font-weight: bold; cursor: pointer; font-size: 1.1rem; text-transform: uppercase; }}
            .btn-pay-execute:disabled {{ background: #333; color: #777; cursor: not-allowed; }}
            .order-item {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #1c1c1c; font-size: 0.95rem; }}
            #stripe-card-element {{ background: #111; padding: 16px; border-radius: 6px; border: 1px solid #333; margin-top: 5px; }}
        </style>
    </head>
    <body>
        
        <header>
            <div class="nav-box">
                <div style="font-family:'Orbitron'; font-weight:bold; color:#fff; font-size:1.4rem;">RD <span style="color:var(--nexus-blue)">LOGISTICS</span></div>
                <a href="/" style="color:#666; text-decoration:none; font-size:0.85rem; font-family:'Orbitron';" id="nav-pay">← VOLTAR À VITRINE</a>
            </div>
        </header>

        <div class="checkout-container">
            <div class="box-billing">
                <h3><i class="fa-solid fa-receipt"></i> Resumo Consolidado</h3>
                <div id="lista-checkout-itens" style="margin: 20px 0;"></div>
                <div style="display:flex; justify-content:space-between; font-family:'Orbitron'; font-size:1.3rem; font-weight:bold; color:var(--rd-red); border-top:1px dashed #333; padding-top:15px;">
                    <span>TOTAL A PAGAR:</span>
                    <span id="total-checkout-val">0.00€</span>
                </div>
            </div>
            
            <div class="box-billing">
                <h3><i class="fa-solid fa-shield-halved"></i> Gateway de Pagamento Seguro</h3>
                <div class="form-group">
                    <label><i class="fa-solid fa-map-pin" style="color:var(--rd-red);"></i> MORADA DE DESPACHO E ENTREGA</label>
                    <input type="text" id="rd-morada" class="form-input" placeholder="

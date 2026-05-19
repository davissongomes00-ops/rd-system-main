/* Continuação dos estilos da animação da carrinha */
            .truck-cabin::after { content: ''; position: absolute; top: 3px; right: 2px; width: 7px; height: 8px; background: #00d2ff; border-radius: 0 4px 0 0; }
            .truck-wheel { width: 10px; height: 10px; background: #333; border: 2px solid #555; border-radius: 50%; position: absolute; bottom: -5px; animation: spinWheel 0.5s infinite linear; }
            .wheel1 { left: 8px; } .wheel2 { right: 12px; }
            .truck-glow { position: absolute; right: -5px; bottom: 8px; width: 15px; height: 6px; background: rgba(0, 210, 255, 0.8); filter: blur(4px); border-radius: 50%; }
            @keyframes driveTruck { 0% { left: -100px; } 100% { left: 100%; } }
            @keyframes spinWheel { 100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
    """ + HEADER_HTML + """
        <div class="container">
            <div class="software-card">
                <h2 style="font-family:'Orbitron'; margin-top:0;"><i class="fa-solid fa-calculator"></i> Dimensionamento Técnico de Pladur</h2>
                <p style="color:#777; font-size:0.95rem;">Insira a área total da parede ou teto para calcular automaticamente os insumos necessários.</p>
                
                <label style="font-family:'Orbitron'; font-size:0.85rem; color:#aaa;">ÁREA TOTAL DA ESTRUTURA (M²):</label>
                <input type="number" id="areaM2" value="0" min="0" oninput="executarCalculoLogistico()">

                <table class="budget-table">
                    <thead>
                        <tr>
                            <th>Insumo Estrutural</th>
                            <th>Qtd Estimada</th>
                            <th>Preço Unit.</th>
                            <th style="text-align:right;">Subtotal</th>
                        </tr>
                    </thead>
                    <tbody id="linhas-tabela-calculo">
                        <tr><td colspan="4" style="color:#555; text-align:center; padding:30px;">Aguardando inserção de área m²...</td></tr>
                    </tbody>
                </table>

                <div class="highway-container">
                    <div class="delivery-truck">
                        <div class="truck-body">
                            <div class="truck-wheel wheel1"></div>
                            <div class="truck-wheel wheel2"></div>
                        </div>
                        <div class="truck-cabin">
                            <div class="truck-glow"></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="sidebar-summary">
                <h3 style="font-family:'Orbitron'; margin-top:0; color:var(--nexus-blue);">Resumo Técnico</h3>
                <div style="display:flex; justify-content:space-between; margin:15px 0; font-size:0.95rem; color:#aaa;">
                    <span>Cubagem estimada de Carga:</span>
                    <strong id="cubagemDisplay" style="color:white; font-family:'Orbitron';">0.00 m³</strong>
                </div>
                <div style="border-top:1px solid #222; padding-top:15px;">
                    <div style="font-size:0.8rem; color:#666; font-family:'Orbitron';">ORÇAMENTO DE ESTRUTURA</div>
                    <div id="totalOrcamento" style="font-size:2rem; font-family:'Orbitron'; font-weight:bold; color:var(--rd-red); margin-top:5px;">0.00€</div>
                </div>
                <button class="btn-whatsapp-calc" onclick="enviarOrcamentoWhatsApp()"><i class="fa-brands fa-whatsapp"></i> Exportar para WhatsApp</button>
            </div>
        </div>

        <script>
            const tabelaPrecos = { placa: 12.50, montante: 3.80, parafuso: 0.05, massa: 4.20 };

            function executarCalculoLogistico() {
                const area = parseFloat(document.getElementById("areaM2").value) || 0;
                if(area <= 0) {
                    document.getElementById("linhas-tabela-calculo").innerHTML = '<tr><td colspan="4" style="color:#555; text-align:center; padding:30px;">Aguardando inserção de área m²...</td></tr>';
                    document.getElementById("totalOrcamento").innerText = "0.00€";
                    document.getElementById("cubagemDisplay").innerText = "0.00 m³";
                    return;
                }

                // Fórmulas técnicas base por m²
                const qtdPlacas = Math.ceil(area * 0.35);
                const qtdMontantes = Math.ceil(area * 0.9);
                const qtdParafusos = Math.ceil(area * 16);
                const qtdMassa = Math.ceil(area * 0.6);

                const subPlaca = qtdPlacas * tabelaPrecos.placa;
                const subMontante = qtdMontantes * tabelaPrecos.montante;
                const subParafuso = qtdParafusos * tabelaPrecos.parafuso;
                const subMassa = qtdMassa * tabelaPrecos.massa;
                const total = subPlaca + subMontante + subParafuso + subMassa;
                const cubagem = area * 0.018;

                document.getElementById("linhas-tabela-calculo").innerHTML = `
                    <tr><td>Placa Pladur Standard (un)</td><td>${qtdPlacas}</td><td>${tabelaPrecos.placa.toFixed(2)}€</td><td style="text-align:right;">${subPlaca.toFixed(2)}€</td></tr>
                    <tr><td>Perfil Montante 45mm (m)</td><td>${qtdMontantes}</td><td>${tabelaPrecos.montante.toFixed(2)}€</td><td style="text-align:right;">${subMontante.toFixed(2)}€</td></tr>
                    <tr><td>Parafusos PM 25 (un)</td><td>${qtdParafusos}</td><td>${tabelaPrecos.parafuso.toFixed(2)}€</td><td style="text-align:right;">${subParafuso.toFixed(2)}€</td></tr>
                    <tr><td>Massa de Juntas (kg)</td><td>${qtdMassa}</td><td>${tabelaPrecos.massa.toFixed(2)}€</td><td style="text-align:right;">${subMassa.toFixed(2)}€</td></tr>
                    <tr class="total-row"><td colspan="3">VALOR TOTAL ESTIMADO</td><td style="text-align:right;">${total.toFixed(2)}€</td></tr>
                `;
                
                document.getElementById("totalOrcamento").innerText = total.toFixed(2) + "€";
                document.getElementById("cubagemDisplay").innerText = cubagem.toFixed(2) + " m³";
                localStorage.setItem("rd_calculo_total", total.toFixed(2));
            }

            function enviarOrcamentoWhatsApp() {
                const area = document.getElementById("areaM2").value;
                const total = document.getElementById("totalOrcamento").innerText;
                if(parseFloat(area) <= 0) return alert("Insira uma área válida para gerar o pedido.");
                const msg = encodeURIComponent(`*RD LOGISTICS - ORÇAMENTO TÉCNICO*\n\nÁrea informada: ${area} m²\nValor Total Estimado: ${total}\n\nGostaria de validar esta cubagem de materiais para entrega no meu endereço.`);
                window.open(`https://api.whatsapp.com/send?phone=351910000000&text=${msg}`, '_blank');
            }
        </script>
    """ + FOOTER_HTML + """
    </body>
    </html>
    """
    return HTMLResponse(content=html_calc)

# ---- ROTA 3: PÁGINA DE PAGAMENTO (CHECKOUT INTEGRADO) ----
@app.get("/pagamento", response_class=HTMLResponse)
def read_pagamento():
    html_pay = """
    <!DOCTYPE html>
    <html lang="pt-pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RD Logistics | Checkout Seguro</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Urbanist:wght@300;600;700&display=swap" rel="stylesheet">
        <script src="https://js.stripe.com/v3/"></script>
        <style>
            :root { --rd-red: #FF0000; --dark-bg: #000000; }
            body { margin: 0; background: var(--dark-bg); color: white; font-family: 'Urbanist', sans-serif; padding-top: 110px; }
            .pay-container { max-width: 700px; margin: auto; background: #0a0a0a; border: 1px solid #222; padding: 40px; border-radius: 12px; border-top: 5px solid var(--rd-red); box-shadow: 0 0 20px rgba(0,0,0,0.8); }
            input[type="text"] { width: 100%; padding: 14px; margin-bottom: 20px; background: #111; border: 1px solid #333; color: white; border-radius: 6px; font-size: 1rem; }
            #stripe-card-element { background: #111; padding: 16px; border: 1px solid #333; border-radius: 6px; margin-bottom: 25px; }
            .btn-submit-pay { width: 100%; background: var(--rd-red); color: white; font-family:'Orbitron'; font-weight:bold; border: none; padding: 16px; border-radius: 6px; font-size: 1.1rem; cursor: pointer; text-transform: uppercase; }
            .btn-submit-pay:disabled { background: #444; cursor: not-allowed; }
            #erro-pagamento { color: #FF0000; margin-top: 15px; font-family: 'Orbitron'; font-size: 0.9rem; text-align: center; }
        </style>
    </head>
    <body>
    """ + HEADER_HTML + """
        <div class="pay-container">
            <h2 style="font-family:'Orbitron'; margin-top:0; text-align:center;"><i class="fa-solid fa-shield-halved"></i> Terminal de Checkout Seguro</h2>
            <p style="text-align:center; color:#666; margin-bottom:30px;">Processamento de chaves encriptadas via Stripe Engine.</p>
            
            <div style="background:#111; padding:15px; border-radius:6px; margin-bottom:25px; display:flex; justify-content:space-between; align-items:center;">
                <span style="font-family:'Orbitron'; font-size:0.9rem; color:#aaa;">MONTANTE GLOBAL A LIQUIDAR:</span>
                <strong id="valorTotalLiquidar" style="font-family:'Orbitron'; font-size:1.5rem; color:#00d2ff;">0.00€</strong>
            </div>

            <form id="formulario-checkout" onsubmit="processarFluxoPagamentoReal(event)">
                <label style="font-size:0.85rem; color:#aaa; font-family:'Orbitron'; display:block; margin-bottom:5px;">NOME COMPLETO DO TITULAR</label>
                <input type="text" id="nomeTitular" placeholder="Ex: Gabriel Rodrigues" required>

                <label style="font-size:0.85rem; color:#aaa; font-family:'Orbitron'; display:block; margin-bottom:5px;">MORADA DE ENTREGA DA CARGA</label>
                <input type="text" id="moradaCliente" placeholder="Ex: Av. dos Aliados, Porto" required onchange="salvarMoradaLocal(this.value)">

                <label style="font-size:0.85rem; color:#aaa; font-family:'Orbitron'; display:block; margin-bottom:5px;">DADOS DO CARTÃO (STRIPE EMULATOR)</label>
                <div id="stripe-card-element"></div>

                <button type="submit" id="btnDispararPay" class="btn-submit-pay">EFETUAR LIQUIDAÇÃO SEGURA</button>
                <div id="erro-pagamento"></div>
            </form>
        </div>

        <script>
            // Substitua pela sua chave pública real do painel Stripe se necessário
            const stripe = Stripe('pk_test_51P...SUA_CHAVE_PUBLICA_AQUI...'); 
            const elements = stripe.elements();
            const elementoCartao = elements.create('card', {
                style: { base: { color: '#ffffff', fontSize: '16px', '::placeholder': { color: '#555555' } } }
            });
            elementoCartao.mount('#stripe-card-element');

            const totalVitrine = parseFloat(localStorage.getItem("rd_carrinho_total")) || 0;
            const totalCalculadora = parseFloat(localStorage.getItem("rd_calculo_total")) || 0;
            const montanteFinal = totalVitrine > 0 ? totalVitrine : totalCalculadora;
            
            document.getElementById("valorTotalLiquidar").innerText = montanteFinal.toFixed(2) + "€";

            function salvarMoradaLocal(valor) {
                localStorage.setItem("rd_morada_cliente", valor);
            }

            async function processarFluxoPagamentoReal(event) {
                event.preventDefault();
                const btn = document.getElementById("btnDispararPay");
                const caixaErro = document.getElementById("erro-pagamento");
                btn.disabled = true;
                btn.innerText = "PROCESSANDO TRANSAÇÃO...";
                caixaErro.innerText = "";

                if(montanteFinal <= 0) {
                    caixaErro.innerText = "ERRO: O valor do carrinho está zerado.";
                    btn.disabled = false; btn.innerText = "EFETUAR LIQUIDAÇÃO SEGURA";
                    return;
                }

                try {
                    const resposta = await fetch('/api/criar-pagamento', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ total: montanteFinal })
                    });
                    const dadosServidor = await resposta.json();

                    if (dadosServidor.error) { throw new Error(dadosServidor.error); }

                    const resultadoStripe = await stripe.confirmCardPayment(dadosServidor.clientSecret, {
                        payment_method: {
                            card: elementoCartao,
                            billing_details: { name: document.getElementById("nomeTitular").value }
                        }
                    });

                    if (resultadoStripe.error) {
                        caixaErro.innerText = resultadoStripe.error.message;
                        btn.disabled = false; btn.innerText = "EFETUAR LIQUIDAÇÃO SEGURA";
                    } else if (resultadoStripe.paymentIntent.status === 'succeeded') {
                        alert("PAGAMENTO CONCLUÍDO COM SUCESSO! Sistema Logístico Acionado.");
                        localStorage.setItem("rd_selecionados", JSON.stringify([]));
                        localStorage.setItem("rd_carrinho_total", "0.00");
                        window.location.href = "/";
                    }
                } catch (e) {
                    caixaErro.innerText = e.message;
                    btn.disabled = false; btn.innerText = "EFETUAR LIQUIDAÇÃO SEGURA";
                }
            }
        </script>
    """ + FOOTER_HTML + """
    </body>
    </html>
    """
    return HTMLResponse(content=html_pay)

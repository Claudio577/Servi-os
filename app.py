import streamlit as st
from datetime import datetime
import json
import uuid

DB_PATH = "data/db.json"

# -----------------------------
# Funções de banco de dados
# -----------------------------
def load_db():
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

db = load_db()

# -----------------------------
# Funções simuladoras
# -----------------------------
def registrar_transacao(tipo, valor, descricao):
    transacao = {
        "id": str(uuid.uuid4()),
        "tipo": tipo,
        "valor": valor,
        "descricao": descricao,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    db["transacoes"].append(transacao)
    db["saldo"] += valor
    save_db(db)

# PIX
def enviar_pix(chave, valor):
    if db["saldo"] < valor:
        return False, "Saldo insuficiente."
    registrar_transacao("PIX enviado", -valor, f"Envio para {chave}")
    return True, "PIX enviado com sucesso!"

# Pagamento
def pagar_boleto(cod_barras, valor):
    if db["saldo"] < valor:
        return False, "Saldo insuficiente."
    registrar_transacao("Pagamento", -valor, f"Boleto {cod_barras}")
    return True, "Pagamento realizado!"

# Recarga
def fazer_recarga(numero, operadora, valor):
    registrar_transacao("Recarga", -valor, f"{operadora} - {numero}")
    return True, "Recarga efetuada!"

# Empréstimos
def contratar_emprestimo(valor, juros=0.08):
    total = valor * (1 + juros)
    registrar_transacao("Empréstimo", valor, "Crédito contratado")
    return True, f"Empréstimo aprovado! Total a pagar: R$ {total:.2f}"

# -----------------------------
# Interface Streamlit
# -----------------------------
st.set_page_config(page_title="Hub Financeiro IA", layout="wide")

st.title("💸 Hub Financeiro Móvel com IA")

menu = st.sidebar.radio("Menu", ["Dashboard", "PIX", "Pagamentos", "Recargas", "Empréstimos"])

# Dashboard
if menu == "Dashboard":
    st.header("📊 Dashboard Financeiro")
    st.metric("Saldo", f"R$ {db['saldo']:,.2f}")

    st.subheader("Últimas transações")
    for t in reversed(db["transacoes"][-5:]):
        st.write(f"**{t['tipo']}** | {t['descricao']} | R$ {t['valor']:.2f} | _{t['data']}_")

# PIX
elif menu == "PIX":
    st.header("⚡ Fazer PIX")

    chave = st.text_input("Chave PIX")
    valor = st.number_input("Valor", min_value=1.0)

    if st.button("Enviar PIX"):
        ok, msg = enviar_pix(chave, valor)
        st.success(msg) if ok else st.error(msg)

# Pagamentos
elif menu == "Pagamentos":
    st.header("💳 Pagamento de Boletos")

    codigo = st.text_input("Código de barras")
    valor = st.number_input("Valor do boleto", min_value=1.0)

    if st.button("Pagar"):
        ok, msg = pagar_boleto(codigo, valor)
        st.success(msg) if ok else st.error(msg)

# Recargas
elif menu == "Recargas":
    st.header("📱 Recarga de Celular")

    numero = st.text_input("Número")
    op = st.selectbox("Operadora", ["Vivo", "Claro", "TIM", "Oi"])
    valor = st.number_input("Valor", min_value=1.0)

    if st.button("Recarregar"):
        ok, msg = fazer_recarga(numero, op, valor)
        st.success(msg)

# Empréstimos
elif menu == "Empréstimos":
    st.header("🏦 Simulação de Empréstimo")

    valor = st.number_input("Valor desejado", min_value=100.0)

    if st.button("Contratar"):
        ok, msg = contratar_emprestimo(valor)
        st.success(msg)

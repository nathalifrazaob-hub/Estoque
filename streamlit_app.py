import streamlit as st
import pandas as pd
import os

# --------------------------------------------
# CONFIGURAÇÃO GERAL
# --------------------------------------------
st.set_page_config(page_title="Controle de Estoque", page_icon="📦", layout="wide")
st.title("Controle de Estoque")
st.markdown("Controle o estoque de itens de segurança e uniformes de forma simples e organizada.")

# --------------------------------------------
# ARQUIVOS BASE
# --------------------------------------------
estoque_arquivo = "estoque.csv"
retirada_arquivo = "retiradas.csv"

# Carregar estoque
if os.path.exists(estoque_arquivo):
    df = pd.read_csv(estoque_arquivo)
else:
    df = pd.DataFrame(columns=["Tipo", "Descrição", "Tamanho", "Quantidade", "Data"])

# Carregar retiradas
if os.path.exists(retirada_arquivo):
    df_retiradas = pd.read_csv(retirada_arquivo)
else:
    df_retiradas = pd.DataFrame(columns=["Colaborador", "Item", "Tamanho", "Quantidade", "Data"])

# --------------------------------------------
# MENU LATERAL
# --------------------------------------------
st.sidebar.title("📋 Menu de Navegação")
aba = st.sidebar.radio("Selecione uma opção:", ["Cadastrar item", "Consultar estoque", "Retirada"])

# --------------------------------------------
# ABA 1 - CADASTRAR ITEM
# --------------------------------------------
if aba == "Cadastrar item":
    st.subheader("📦 Cadastro de Itens no Estoque")

    col1, col2 = st.columns(2)
    with col1:
        tipo = st.selectbox("Tipo", ["Uniformes", "EPI", "Escritório"])
        descricao = st.text_input("Descrição (ex: Calça, Camisa, Botina)")
        tamanho = st.text_input("Tamanho (ex: P, M, G, Único)")
    with col2:
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        data = st.date_input("Data de Entrada")

    if st.button("Salvar item"):
        novo = pd.DataFrame([[tipo, descricao, tamanho, quantidade, data]], columns=df.columns)
        df = pd.concat([df, novo], ignore_index=True)
        df.to_csv(estoque_arquivo, index=False)
        st.success("✅ Item adicionado com sucesso!")

# --------------------------------------------
# ABA 2 - CONSULTAR ESTOQUE (tabela + ⚙️ menu discreto)
# --------------------------------------------
elif aba == "Consultar estoque":
    st.subheader("🔍 Consulta de Itens no Estoque por Categoria")

    categorias = ["CALÇA", "CAMISA", "BOTINA", "CAPACETE", "LUVA"]

    if df.empty:
        st.info("Nenhum item cadastrado ainda.")
    else:
        for categoria in categorias:
            df_cat = df[df["Descrição"].str.upper().str.contains(categoria, na=False)]

            if not df_cat.empty:
                st.markdown(f"### {categoria.title()}s no Estoque")

                # Cabeçalho
                header_cols = st.columns([2, 1, 1, 1, 1])
                header_cols[0].write("**Descrição**")
                header_cols[1].write("**Tamanho**")
                header_cols[2].write("**Quantidade**")
                header_cols[3].write("**Data**")
                header_cols[4].write("**Ações**")

                for i, row in df_cat.iterrows():
                    cols = st.columns([2, 1, 1, 1, 1])
                    cols[0].write(row["Descrição"])
                    cols[1].write(row["Tamanho"])
                    cols[2].write(row["Quantidade"])
                    cols[3].write(str(row["Data"]))

                    with cols[4]:
                        with st.popover("⚙", use_container_width=False):
                            st.markdown(f"**{row['Descrição']} ({row['Tamanho']})**")
                            nova_qtd = st.number_input(
                                "Quantidade", min_value=1,
                                value=int(row["Quantidade"]),
                                step=1, key=f"qtd_{i}"
                            )
                            nova_data = st.date_input(
                                "Data", pd.to_datetime(row["Data"]),
                                key=f"data_{i}"
                            )

                            if st.button("💾 Salvar", key=f"salvar_{i}"):
                                df.at[i, "Quantidade"] = nova_qtd
                                df.at[i, "Data"] = nova_data
                                df.to_csv(estoque_arquivo, index=False)
                                st.success("Alterações salvas com sucesso!")
                                st.rerun()

                            if st.button("🗑️ Excluir", key=f"excluir_{i}"):
                                df = df.drop(i)
                                df.to_csv(estoque_arquivo, index=False)
                                st.warning(f"Item '{row['Descrição']}' excluído.")
                                st.rerun()

                total = df_cat["Quantidade"].sum()
                st.markdown(f"**Total de {categoria.lower()}s:** {total}")
                st.markdown("---")

        # Outros
        outros = df[~df["Descrição"].str.upper().str.contains("|".join(categorias), na=False)]
        if not outros.empty:
            st.markdown("### Outros Itens no Estoque")
            header_cols = st.columns([2, 1, 1, 1, 1])
            header_cols[0].write("**Descrição**")
            header_cols[1].write("**Tamanho**")
            header_cols[2].write("**Quantidade**")
            header_cols[3].write("**Data**")
            header_cols[4].write("**Ações**")

            for i, row in outros.iterrows():
                cols = st.columns([2, 1, 1, 1, 1])
                cols[0].write(row["Descrição"])
                cols[1].write(row["Tamanho"])
                cols[2].write(row["Quantidade"])
                cols[3].write(str(row["Data"]))

                with cols[4]:
                    with st.popover("⚙", use_container_width=False):

                        st.markdown(f"**{row['Descrição']} ({row['Tamanho']})**")
                        nova_qtd = st.number_input(
                            "Quantidade", min_value=1,
                            value=int(row["Quantidade"]),
                            step=1, key=f"qtd_outro_{i}"
                        )
                        nova_data = st.date_input(
                            "Data", pd.to_datetime(row["Data"]),
                            key=f"data_outro_{i}"
                        )

                        if st.button("💾 Salvar", key=f"salvar_outro_{i}"):
                            df.at[i, "Quantidade"] = nova_qtd
                            df.at[i, "Data"] = nova_data
                            df.to_csv(estoque_arquivo, index=False)
                            st.success("Alterações salvas com sucesso!")
                            st.rerun()

                        if st.button("🗑️ Excluir", key=f"excluir_outro_{i}"):
                            df = df.drop(i)
                            df.to_csv(estoque_arquivo, index=False)
                            st.warning(f"Item '{row['Descrição']}' excluído.")
                            st.rerun()

# --------------------------------------------
# ABA 3 - RETIRADA
# --------------------------------------------
elif aba == "Retirada":
    st.subheader("🧾 Registro de Retirada de Itens do Estoque")

    col1, col2, col3 = st.columns(3)
    with col1:
        colaborador = st.text_input("Nome do Colaborador")
    with col2:
        item = st.selectbox("Item Retirado", df["Descrição"].unique() if not df.empty else [])
    with col3:
        tamanho = st.selectbox("Tamanho", df["Tamanho"].unique() if not df.empty else [])

    if item and tamanho:
        filtro = df[(df["Descrição"] == item) & (df["Tamanho"] == tamanho)]
        if not filtro.empty:
            qtd_disp = int(filtro.iloc[0]["Quantidade"])
            st.info(f"💡 Estoque atual: **{qtd_disp} unidades**")
        else:
            qtd_disp = 0
    else:
        qtd_disp = 0

    col4, col5 = st.columns(2)
    with col4:
        quantidade = st.number_input("Quantidade Retirada", min_value=1, step=1)
    with col5:
        data = st.date_input("Data da Retirada")

    if st.button("Registrar Retirada"):
        if colaborador and item and tamanho:
            index = df[(df["Descrição"] == item) & (df["Tamanho"] == tamanho)].index
            if len(index) > 0:
                idx = index[0]
                qtd_atual = int(df.at[idx, "Quantidade"])
                if quantidade > qtd_atual:
                    st.error("❌ Quantidade maior que o disponível em estoque.")
                else:
                    df.at[idx, "Quantidade"] = qtd_atual - quantidade
                    df.to_csv(estoque_arquivo, index=False)

                    nova = pd.DataFrame([[colaborador, item, tamanho, quantidade, data]], columns=df_retiradas.columns)
                    df_retiradas = pd.concat([df_retiradas, nova], ignore_index=True)
                    df_retiradas.to_csv(retirada_arquivo, index=False)
                    st.success(f"✅ Retirada de {quantidade}x {item} registrada com sucesso!")
                    st.rerun()
            else:
                st.warning("⚠️ Item não encontrado no estoque.")
        else:
            st.warning("⚠️ Preencha todos os campos antes de registrar.")

    st.markdown("---")
    st.subheader("📋 Histórico de Retiradas")
    if not df_retiradas.empty:
        st.dataframe(df_retiradas, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma retirada registrada ainda.")

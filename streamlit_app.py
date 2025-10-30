import streamlit as st
import pandas as pd
import os

# --------------------------------------------
# CONFIGURAÇÃO GERAL DO SISTEMA
# --------------------------------------------
st.set_page_config(
    page_title="CONTROLE DE ESTOQUE",
    page_icon="📦",
    layout="wide"
)

st.title("CONTROLE DE ESTOQUE")
st.markdown("Controle o estoque de itens de segurança e uniformes de forma simples e organizada.")

# --------------------------------------------
# ARQUIVO BASE DE DADOS
# --------------------------------------------
arquivo = "estoque.csv"

if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)
else:
    df = pd.DataFrame(columns=["Tipo", "Descrição", "Tamanho", "Quantidade", "Data"])

# --------------------------------------------
# MENU LATERAL
# --------------------------------------------
aba = st.sidebar.radio("Menu", ["Cadastrar item", "Consultar estoque"])

# --------------------------------------------
# ABA 1 - CADASTRO
# --------------------------------------------
if aba == "Cadastrar item":
    st.subheader("📦 Cadastro de Itens no Estoque")
    st.write("Preencha os dados abaixo para registrar um novo item no estoque:")

    col1, col2 = st.columns(2)
    with col1:
        tipo = st.selectbox("Tipo", ["UNIFORME", "EPI", "ESCRITÓRIO"])
        descricao = st.text_input("Descrição (ex: Calça, Camisa, Botina)")
        tamanho = st.text_input("Tamanho (ex: P, M, G, Único)")
    with col2:
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        data = st.date_input("Data de Entrada")

    if st.button("Salvar item"):
        novo = pd.DataFrame([[tipo, descricao, tamanho, quantidade, data]], columns=df.columns)
        df = pd.concat([df, novo], ignore_index=True)
        df.to_csv(arquivo, index=False)
        st.success("✅ Item adicionado com sucesso!")

# --------------------------------------------
# ABA 2 - CONSULTA
# --------------------------------------------
elif aba == "Consultar estoque":
    st.subheader("🔍 Consulta de Itens no Estoque por Categoria")

    # Categorias fixas (pode editar essa lista à vontade)
    categorias = ["CALÇA", "CAMISA", "BOTINA", "CAPACETE", "LUVA"]

    if df.empty:
        st.info("Nenhum item cadastrado ainda.")
    else:
        # Mostra as categorias encontradas no estoque
        for categoria in categorias:
            # Filtra pela palavra da categoria
            df_cat = df[df["Descrição"].str.upper().str.contains(categoria, na=False)]

            if not df_cat.empty:
                st.markdown(f"### 🟦 {categoria.title()}s no Estoque")

                # Agrupa por tamanho e soma as quantidades
                df_cat_group = df_cat.groupby(["Tamanho"], as_index=False)["Quantidade"].sum()

                # Exibe a tabela com estilo
                st.dataframe(
                    df_cat_group.style.set_properties(**{
                        "text-align": "center",
                        "background-color": "#f9f9f9",
                        "border-color": "#ddd"
                    }),
                    use_container_width=True,
                    hide_index=True
                )

                total = df_cat_group["Quantidade"].sum()
                st.markdown(f"**Total de {categoria.lower()}s no estoque:** {total}")
                st.markdown("---")

        # Itens que não estão nas categorias fixas
        outros = df[
            ~df["Descrição"].str.upper().str.contains("|".join(categorias), na=False)
        ]

        if not outros.empty:
            st.markdown("### 📦 Outros Itens no Estoque")
            st.dataframe(
                outros[["Descrição", "Tipo", "Tamanho", "Quantidade", "Data"]],
                use_container_width=True,
                hide_index=True
            )


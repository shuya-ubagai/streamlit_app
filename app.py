import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df_niigata = pd.read_csv("FEH_00500209_260126084514.csv", encoding="shift-jis") # 新潟県のデータベース
df_nagano = pd.read_csv("FEH_00500209_260126103754.csv", encoding="shift-jis") # 長野県のデータベース

common_cat02 = sorted(
    set(df_niigata["cat02_code"]) & set(df_nagano["cat02_code"]))

cat01_table = df_niigata[["cat01_code", "cat01"]].drop_duplicates()
cat02_table = df_niigata[["cat02_code", "cat02"]].drop_duplicates()

st.title("新潟県の農林業経営体数 比較アプリ")

with st.sidebar:
    st.header("条件選択")

    st.markdown("### 地域の選択")
    col1, col2 = st.columns(2)

    with col1:
        region_niigata = st.multiselect("新潟県",
                                    df_niigata["(J315-02-2-001)新潟県地域"].unique())
    with col2:                       
        region_nagano = st.multiselect("長野県",
                                   df_nagano["(J320-02-2-001)長野県地域"].unique())
    st.markdown("### 経営体系")
    keitai = st.radio("経営体系の選択",
                         df_niigata["cat01_code"].unique())
    
    st.markdown("### 経営内容")
    naiyou = st.selectbox("経営内容の選択",
                            df_niigata["cat02_code"].unique())

df_niigata["cat02_code"] = df_niigata["cat02_code"].astype(str)
df_nagano["cat02_code"] = df_nagano["cat02_code"].astype(str)
naiyou = str(naiyou)

df_n = df_niigata[
    (df_niigata["(J315-02-2-001)新潟県地域"].isin(region_niigata)) &
    (df_niigata["cat01_code"] == keitai) &
    (df_niigata["cat02_code"] == naiyou)
]  # 授業と違い、2つ同時に定義

df_h = df_nagano[
    (df_nagano["(J320-02-2-001)長野県地域"].isin(region_nagano)) &
    (df_nagano["(J301-02-1-001)農林業経営体数"] == keitai) &
    (df_nagano["cat02_code"] == naiyou)
    ]


st.subheader("新潟県")
df_n.set_index("(J315-02-2-001)新潟県地域", inplace=True)
st.dataframe(df_n, width=800, height=200)

st.subheader("長野県")
df_h.set_index("(J320-02-2-001)長野県地域", inplace=True)
st.dataframe(df_h, width=800, height=200)

if not df_n.empty and not df_h.empty:
    value_niigata = df_n["value"].sum()
    value_nagano = df_h["value"].sum()

    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(["新潟県", "長野県"],
        [value_niigata, value_nagano],
        color=["#1f77b4", "#ff7f0e"])
    ax.set_ylabel("経営体数")
    ax.set.title("経営体数比較")

    st.pyplot(fig)

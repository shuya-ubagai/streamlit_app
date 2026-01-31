import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df_niigata = pd.read_csv("FEH_00500209_260126084514.csv", encoding="shift-jis")
df_nagano = pd.read_csv("FEH_00500209_260126103754.csv", encoding="shift-jis")

plt.rcParams['font.family'] = 'MS Gothic'

df_style = pd.concat([df_niigata, df_nagano], ignore_index=True)

with st.sidebar.expander("抽出条件を設定する", expanded=True):

    # 地域選択
    local1 = st.selectbox(
        "新潟県地域",
        df_niigata["(J315-02-2-001)新潟県地域"].unique()
    )
    local2 = st.selectbox(
        "長野県地域",
        df_nagano["(J320-02-2-001)長野県地域"].unique()
    )

    style = st.radio(
        "経営体系の選択",
        df_style["(J301-02-1-001)農林業経営体数"].unique()
    )


df_niigata_sel = df_niigata[
    (df_niigata["(J315-02-2-001)新潟県地域"] == local1) &
    (df_niigata["(J301-02-1-001)農林業経営体数"] == style)
]

df_nagano_sel = df_nagano[
    (df_nagano["(J320-02-2-001)長野県地域"] == local2) &
    (df_nagano["(J301-02-1-001)農林業経営体数"] == style)
]

if df_niigata_sel.empty or df_nagano_sel.empty:
    st.error("選択した条件に一致するデータがありません")
    st.write("新潟側抽出結果：", df_niigata_sel)
    st.write("長野側抽出結果：", df_nagano_sel)
else:
    
    value_niigata = pd.to_numeric(df_niigata_sel["value"].iloc[0], errors="coerce")
    value_nagano = pd.to_numeric(df_nagano_sel["value"].iloc[0], errors="coerce")

    
    st.metric("新潟県の値：", value_niigata)
    st.metric("長野県の値：", value_nagano)

    
    fig, ax = plt.subplots()
    ax.bar(["新潟県", "長野県"], [value_niigata, value_nagano],
           color=["skyblue", "lightgreen"])
    ax.set_ylabel("農林経営体数")
    ax.set_title(f"{style} の比較（{local1} vs {local2}）")

    detail = st.toggle("ON/OFF")
    
    if detail:
        st.pyplot(fig)
import streamlit as st

with st.form(key='profile_form'):
        #テキストボックス
        name = st.text_input('名前')
        address = st.text_input('住所')

        #セレクトボックス
        age_category = st.radio(
            '年齢層',
            (('子ども（18歳未満）'), '大人（18歳以上）')
        )

        #複数選択
        hobby = st.multiselect(
            '趣味',
            ('スポーツ', '読書', 'プログラミング', 'アニメ', '映画', '釣り', '料理')
        )



        #ボタン
        submit_btn = st.form_submit_button('送信')
        cancel_btn = st.form_submit_button('キャンセル')
        if submit_btn:
            st.text(f'ようこそ！{name}さん、{address}に書簡を送りました。')
            st.text(f'年齢層: {age_category}')
            st.text(f'趣味: {",".join(hobby)}')
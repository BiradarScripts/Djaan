import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/search"

st.set_page_config(page_title="AI Search Engine", layout="wide")
st.title("🔍 Multi-document Embedding Search")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Number of Results", 1, 10, 5)
    use_expansion = st.checkbox("Use Query Expansion (Bonus)", value=False)

query = st.text_input("Enter your search query:", "space exploration")

if st.button("Search"):
    if query:
        payload = {"query": query, "top_k": top_k, "use_expansion": use_expansion}
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                for res in results:
                    with st.container():
                        st.subheader(f"📄 {res['doc_id']} (Score: {res['score']})")
                        st.markdown(f"**Preview:** _{res['preview']}_")
                        
                        with st.expander("Why this result?"):
                            expl = res['explanation']
                            st.write(f"**Relevance:** {expl['relevance_summary']}")
                            st.write(f"**Word Overlap:** {expl['overlap_ratio']}")
                            st.write(f"**Matching Terms:** {', '.join(expl['common_words'])}")
                        st.divider()
            else:
                st.error("Error communicating with API")
        except Exception as e:
            st.error(f"Connection failed: {e}")
    else:
        st.warning("Please enter a query.")
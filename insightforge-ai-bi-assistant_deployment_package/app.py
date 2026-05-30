
import os
import pandas as pd
import streamlit as st

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma

st.set_page_config(
    page_title="InsightForge BI Assistant",
    layout="wide"
)

st.title("InsightForge — AI-Powered Business Intelligence Assistant")
st.write(
    "Upload a CSV dataset or use the included sample dataset to generate "
    "business insights with RAG, LangChain, ChromaDB, and an LLM."
)

# ---------------------------------------------------
# API KEY HANDLING — PUBLIC GITHUB / STREAMLIT SAFE
# ---------------------------------------------------
st.sidebar.header("API Key Setup")

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state.OPENAI_API_KEY = ""

user_api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key",
    type="password",
    placeholder="sk-..."
)

if user_api_key:
    st.session_state.OPENAI_API_KEY = user_api_key

if not st.session_state.OPENAI_API_KEY:
    st.sidebar.warning("OpenAI API key required.")
    st.info("Enter your OpenAI API key in the sidebar to begin.")
    st.caption("Your key is used only during this active session and is not stored in GitHub.")
    st.stop()

os.environ["OPENAI_API_KEY"] = st.session_state.OPENAI_API_KEY

st.sidebar.success("API key loaded for this session.")
st.sidebar.caption("No API key is stored in this repository.")

# ---------------------------------------------------
# MODEL CONFIG
# ---------------------------------------------------
CHAT_MODEL = "gpt-4.1-mini"
TEMPERATURE = 0.2
TOP_K = 6

llm = ChatOpenAI(model=CHAT_MODEL, temperature=TEMPERATURE)
embeddings = OpenAIEmbeddings()
parser = StrOutputParser()

# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------
def detect_column(df, candidates):
    lower_map = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    return None


def build_metrics(df):
    sales_col = detect_column(
        df,
        ["sales", "sales_amount", "amount", "revenue", "total_sales", "price", "value"]
    )

    date_col = detect_column(
        df,
        ["date", "order_date", "transaction_date", "datetime", "timestamp", "time"]
    )

    product_col = detect_column(
        df,
        ["product", "item", "sku", "product_name", "item_name", "category"]
    )

    region_col = detect_column(
        df,
        ["region", "state", "country", "city", "store", "location", "branch"]
    )

    if not sales_col:
        raise ValueError(
            "No sales/revenue column found. Include a column named sales, revenue, "
            "amount, total_sales, price, or value."
        )

    df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce")

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    sales_series = df[sales_col].dropna()

    global_stats = {
        "count": int(sales_series.shape[0]),
        "sum": float(sales_series.sum()) if len(sales_series) else 0.0,
        "mean": float(sales_series.mean()) if len(sales_series) else 0.0,
        "median": float(sales_series.median()) if len(sales_series) else 0.0,
        "std": float(sales_series.std(ddof=1)) if len(sales_series) > 1 else 0.0,
        "min": float(sales_series.min()) if len(sales_series) else 0.0,
        "max": float(sales_series.max()) if len(sales_series) else 0.0,
    }

    time_tables = {}

    if date_col and df[date_col].notna().any():
        temp = df.dropna(subset=[date_col]).copy()

        temp["month"] = temp[date_col].dt.to_period("M").astype(str)
        temp["quarter"] = temp[date_col].dt.to_period("Q").astype(str)
        temp["year"] = temp[date_col].dt.year

        time_tables["monthly"] = temp.groupby("month")[sales_col].sum().sort_index()
        time_tables["quarterly"] = temp.groupby("quarter")[sales_col].sum().sort_index()
        time_tables["yearly"] = temp.groupby("year")[sales_col].sum().sort_index()

    slice_tables = {}

    if product_col:
        slice_tables["product_sales"] = (
            df.groupby(product_col)[sales_col]
            .sum()
            .sort_values(ascending=False)
        )

    if region_col:
        slice_tables["region_sales"] = (
            df.groupby(region_col)[sales_col]
            .sum()
            .sort_values(ascending=False)
        )

    detected = {
        "sales_col": sales_col,
        "date_col": date_col,
        "product_col": product_col,
        "region_col": region_col,
    }

    return global_stats, time_tables, slice_tables, detected


def series_to_doc(title, series, section, top_n=30):
    lines = []

    for idx, val in series.head(top_n).items():
        try:
            val = float(val)
        except Exception:
            pass

        lines.append(f"{idx}: {val}")

    return Document(
        page_content=title + "\n" + "\n".join(lines),
        metadata={"section": section}
    )


def build_documents(global_stats, time_tables, slice_tables):
    docs = []

    global_text = (
        "GLOBAL BUSINESS METRICS\n"
        f"count={global_stats['count']}\n"
        f"sum={global_stats['sum']}\n"
        f"mean={global_stats['mean']}\n"
        f"median={global_stats['median']}\n"
        f"std={global_stats['std']}\n"
        f"min={global_stats['min']}\n"
        f"max={global_stats['max']}\n"
    )

    docs.append(
        Document(
            page_content=global_text,
            metadata={"section": "global_stats"}
        )
    )

    for name, series in time_tables.items():
        docs.append(
            series_to_doc(
                f"SALES BY {name.upper()}",
                series,
                f"time_{name}",
                36
            )
        )

    for name, series in slice_tables.items():
        docs.append(
            series_to_doc(
                name.upper(),
                series,
                name,
                30
            )
        )

    return docs


def format_docs(found_docs):
    return "\n\n---\n\n".join([d.page_content for d in found_docs])


SYSTEM_RULES = """
You are InsightForge, a Business Intelligence Assistant.

You must base your answer on the retrieved business context.
If a requested metric is unavailable, explain what is missing.

Always respond with:
1) Key Findings
2) Supporting Evidence
3) Recommendations
4) Suggested Visualization(s)

Be concise, specific, and business-oriented.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_RULES),
    (
        "human",
        "Conversation so far:\n{history}\n\n"
        "User question:\n{question}\n\n"
        "Retrieved context:\n{context}"
    )
])

# ---------------------------------------------------
# DATA LOADING
# ---------------------------------------------------
DEFAULT_DATA_PATH = "sample_data/sales_data.csv"

uploaded_file = st.file_uploader(
    "Upload a CSV business dataset",
    type=["csv"]
)

df = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Uploaded dataset loaded.")

elif os.path.exists(DEFAULT_DATA_PATH):
    df = pd.read_csv(DEFAULT_DATA_PATH)
    st.info("Using included sample dataset.")

else:
    st.info("Upload a CSV file to begin.")
    st.stop()

# ---------------------------------------------------
# APP BODY
# ---------------------------------------------------
st.subheader("Dataset Preview")
st.dataframe(df.head())

try:
    global_stats, time_tables, slice_tables, detected = build_metrics(df)

    st.subheader("Detected Columns")
    st.json(detected)

    st.subheader("Global Metrics")
    st.json(global_stats)

    docs = build_documents(global_stats, time_tables, slice_tables)

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def history_text(max_turns=8):
        turns = st.session_state.messages[-(max_turns * 2):]
        lines = []

        for m in turns:
            role = "User" if m["role"] == "user" else "Assistant"
            lines.append(f"{role}: {m['content']}")

        return "\n".join(lines)

    st.subheader("Ask InsightForge")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask about sales trends, products, regions, or business performance..."
    )

    if question:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        found_docs = retriever.invoke(question)
        context = format_docs(found_docs)

        chain = prompt | llm | parser

        answer = chain.invoke({
            "history": history_text(),
            "question": question,
            "context": context
        })

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

    st.subheader("Visualizations")

    if "monthly" in time_tables:
        st.write("Monthly Sales Trend")
        st.line_chart(time_tables["monthly"])

    if "product_sales" in slice_tables:
        st.write("Top Product Sales")
        st.bar_chart(slice_tables["product_sales"].head(15))

    if "region_sales" in slice_tables:
        st.write("Top Regional Sales")
        st.bar_chart(slice_tables["region_sales"].head(15))

except Exception as e:
    st.error(f"Error processing dataset: {e}")

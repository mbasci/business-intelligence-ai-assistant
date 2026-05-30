# InsightForge — AI-Powered Business Intelligence Assistant

InsightForge is an AI-powered Business Intelligence Assistant that helps users analyze structured business datasets using Retrieval-Augmented Generation, LangChain, ChromaDB, OpenAI models, pandas, and Streamlit.

## Project Purpose

Many organizations collect large amounts of business data but struggle to convert that data into clear, actionable insights. InsightForge allows users to upload a CSV dataset and ask business intelligence questions in natural language.

The app automatically detects key business columns, calculates summary statistics, builds a retrieval-based knowledge layer, and uses an LLM to generate structured insights and recommendations.

## Key Features

- CSV dataset upload
- Optional included sample dataset
- Automatic column detection
- Sales/revenue summary statistics
- Monthly, quarterly, and yearly trend analysis
- Product performance analysis
- Regional performance analysis
- Retrieval-Augmented Generation with LangChain
- ChromaDB vector retrieval
- Conversational memory using Streamlit session state
- Streamlit visualizations
- Public API-key input through the app sidebar

## API Key Security

This public version does not store an API key in GitHub.

Each user must provide their own OpenAI API key in the Streamlit sidebar.

The key is used only during the active session.

Do not commit API keys, .env files, or Streamlit secrets to GitHub.

## Technologies Used

- Python
- Streamlit
- OpenAI
- LangChain
- ChromaDB
- pandas
- NumPy
- matplotlib
- scikit-learn

## Project Architecture

1. User opens the Streamlit app
2. User enters their OpenAI API key in the sidebar
3. User uploads a CSV file or uses the included sample dataset
4. pandas detects key columns and calculates business metrics
5. Metrics are converted into LangChain documents
6. ChromaDB creates a vector retrieval layer
7. The user asks a question
8. Relevant business context is retrieved
9. The LLM generates structured business insights
10. Streamlit displays answers and visualizations

## Example Questions

- What are the key business trends?
- Which products are performing best?
- Which regions generate the most sales?
- What are the major recommendations?
- What visualizations should management review?
- What does the monthly sales trend show?

## Installation

Run:

    pip install -r requirements.txt

## Run Locally

Run:

    streamlit run app.py

## Streamlit Cloud Deployment

1. Upload this project to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app.
4. Select this GitHub repository.
5. Select app.py as the main file.
6. Deploy.

No Streamlit secret is required for the public version because each user enters their own OpenAI API key.

## Suggested Repository Structure

insightforge-ai-bi-assistant/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
├── packages.txt
├── sample_data/
│   └── sales_data.csv
├── screenshots/
├── notebooks/
└── .streamlit/
    └── secrets.example.toml

## Notes on Data

Only use public, synthetic, anonymized, or non-sensitive demo data.

Do not upload confidential client data, personal data, protected health information, or proprietary business datasets to a public repository.

## Dataset Requirements

InsightForge works best with clean, structured business datasets in CSV format.

### Required Columns

The dataset must contain at least one numeric business metric column such as:

- sales
- revenue
- amount
- total_sales
- price
- value

These columns are used to calculate business metrics and generate insights.

### Recommended Columns

| Purpose | Example Column Names |
|---|---|
| Date / Time | date, order_date, transaction_date |
| Product / Category | product, item, sku, category |
| Region / Location | region, state, country, city |
| Customer Identifier | customer_id |
| Demographics | gender, age_group, income_band |

### Recommended Data Quality

- Use clean, structured tabular data
- Remove duplicate rows where appropriate
- Avoid heavily missing or corrupted values
- Ensure numeric columns contain numeric values
- Use consistent date formats
- Avoid mixing currencies or units without normalization

### File Format

- Supported format: CSV
- UTF-8 encoding recommended

### Important Notes

The quality of the generated insights depends heavily on the quality, cleanliness, and consistency of the uploaded dataset.

## Future Improvements

- Add downloadable business reports
- Add PDF and Word report export
- Add forecasting models
- Add user-controlled column mapping
- Add persistent vector database storage
- Add model evaluation dashboard
- Add authentication for enterprise users
- Add support for Excel files
- Add multi-file analysis

## Author

Mark Anderson, PhD

AI Tools and Innovation with Purpose
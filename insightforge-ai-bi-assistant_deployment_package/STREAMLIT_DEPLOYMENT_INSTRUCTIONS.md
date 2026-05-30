# Streamlit Cloud Deployment Instructions

## App Name

InsightForge — AI-Powered Business Intelligence Assistant

## Main File

app.py

## Deployment Steps

1. Go to Streamlit Community Cloud.
2. Select "New app."
3. Connect your GitHub account.
4. Select the repository:

   insightforge-ai-bi-assistant

5. Set the main file path:

   app.py

6. Click Deploy.

## API Key Behavior

This public version asks users to enter their own OpenAI API key in the Streamlit sidebar.

No OpenAI API key is stored in GitHub.

No Streamlit secret is required for basic public deployment.

## Testing After Deployment

After deployment:

1. Open the Streamlit app link.
2. Enter your OpenAI API key in the sidebar.
3. Upload a CSV file or use the sample dataset.
4. Ask:

   What are the key business trends?

5. Confirm the app returns:

   - Key Findings
   - Supporting Evidence
   - Recommendations
   - Suggested Visualizations

## Suggested Demo Question

What are the main sales trends and what should management do next?
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from firecrawl import FirecrawlApp

# ---------------- Load Environment ----------------
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

if not OPENROUTER_API_KEY or not FIRECRAWL_API_KEY:
    st.error("❌ Missing API keys in .env file")
    st.stop()

# ---------------- LLM ----------------
llm = ChatOpenAI(
    model="x-ai/grok-4-fast",
    temperature=0.3,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ---------------- Firecrawl ----------------
firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

def firecrawl_search(query: str) -> str:
    result = firecrawl.search(query=query, limit=5)
    return str(result)

# ---------------- Prompts ----------------
competitor_prompt = PromptTemplate(
    input_variables=["company"],
    template="""
You are a senior GTM strategist.

Analyze recent product launches by {company}.
Provide:
1. Market positioning
2. Launch strengths with evidence
3. Launch weaknesses with evidence
4. Strategic takeaways

End with a Sources section.
"""
)

sentiment_prompt = PromptTemplate(
    input_variables=["company"],
    template="""
You are a market sentiment analyst.

Analyze public sentiment for {company} based on reviews, forums, and social media.
Provide:
- Positive sentiment drivers
- Negative sentiment drivers
- Overall sentiment summary

End with a Sources section.
"""
)

metrics_prompt = PromptTemplate(
    input_variables=["company"],
    template="""
You are a launch performance analyst.

Analyze public KPIs for recent product launches by {company}.
Include:
- Adoption signals
- Engagement metrics
- Revenue or growth indicators
- Press coverage

End with a Sources section.
"""
)

# ---------------- Analysis Runner ----------------
def run_analysis(company: str, analysis_type: str) -> str:
    if analysis_type == "Competitor Analysis":
        prompt_text = competitor_prompt.format(company=company)
    elif analysis_type == "Sentiment Analysis":
        prompt_text = sentiment_prompt.format(company=company)
    elif analysis_type == "Launch Metrics":
        prompt_text = metrics_prompt.format(company=company)
    else:
        return "Invalid analysis type"

    response = llm.invoke(prompt_text)
    return response.content

# ---------------- Streamlit UI ----------------
st.set_page_config(
    page_title="AI Product Launch Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .main-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Analysis cards */
    .analysis-card {
        background: white;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .analysis-card:hover {
        border-color: #6366f1;
        box-shadow: 0 8px 20px rgba(99,102,241,0.15);
        transform: translateY(-2px);
    }
    
    .analysis-card.selected {
        border-color: #6366f1;
        background: linear-gradient(135deg, rgba(99,102,241,0.05) 0%, rgba(139,92,246,0.05) 100%);
    }
    
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .card-description {
        color: #6b7280;
        font-size: 0.95rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 0.5rem;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102,126,234,0.4);
    }
    
    /* Results container */
    .results-container {
        background: white;
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-top: 2rem;
    }
    
    /* Metrics boxes */
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f9fafb;
    }
    
    /* Info boxes */
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🚀 AI Product Launch Intelligence</h1>
    <p class="main-subtitle">Powered by Advanced AI • Real-time Market Insights • Strategic Analysis</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 About This Tool")
    st.markdown("""
    This AI-powered platform provides:
    
    - **Competitor Analysis** - Market positioning & launch strategies
    - **Sentiment Tracking** - Public perception analysis
    - **Performance Metrics** - KPIs & growth indicators
    
    ---
    """)
    
    
    
    st.markdown("---")
    st.markdown("### ⚡ Powered By")
    st.markdown("• Grok-4 AI Model\n• Firecrawl Web Search\n• LangChain Framework")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🏢 Company Information")
    company = st.text_input(
        "Enter Company Name",
        placeholder="e.g., OpenAI, Tesla, Spotify, Anthropic",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### ")
    st.markdown("")  # Spacing

# Analysis Type Selection
st.markdown("### 📈 Select Analysis Type")

col1, col2, col3 = st.columns(3)

analysis_options = {
    "Competitor Analysis": {
        "icon": "🎯",
        "description": "Market positioning & strategic insights",
        "color": "#667eea"
    },
    "Sentiment Analysis": {
        "icon": "💭",
        "description": "Public perception & customer feedback",
        "color": "#8b5cf6"
    },
    "Launch Metrics": {
        "icon": "📊",
        "description": "KPIs, adoption & performance data",
        "color": "#ec4899"
    }
}

# Store selected analysis in session state
if 'selected_analysis' not in st.session_state:
    st.session_state.selected_analysis = "Competitor Analysis"

with col1:
    if st.button("🎯 Competitor Analysis", use_container_width=True):
        st.session_state.selected_analysis = "Competitor Analysis"
    st.markdown('<p style="text-align: center; color: #6b7280; font-size: 0.85rem;">Market positioning & strategy</p>', unsafe_allow_html=True)

with col2:
    if st.button("💭 Sentiment Analysis", use_container_width=True):
        st.session_state.selected_analysis = "Sentiment Analysis"
    st.markdown('<p style="text-align: center; color: #6b7280; font-size: 0.85rem;">Public perception tracking</p>', unsafe_allow_html=True)

with col3:
    if st.button("📊 Launch Metrics", use_container_width=True):
        st.session_state.selected_analysis = "Launch Metrics"
    st.markdown('<p style="text-align: center; color: #6b7280; font-size: 0.85rem;">Performance & KPI analysis</p>', unsafe_allow_html=True)

# Show selected analysis
st.info(f"**Selected:** {st.session_state.selected_analysis}")

st.markdown("---")

# Run Analysis Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_button = st.button("🔍 Run Analysis", use_container_width=True, type="primary")

# Execute Analysis
if run_button:
    if not company:
        st.error("⚠️ Please enter a company name to proceed")
    else:
        with st.spinner(f"🔄 Analyzing {company}... This may take a moment"):
            try:
                # Progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Initializing analysis...")
                progress_bar.progress(25)
                
                status_text.text("Gathering market intelligence...")
                progress_bar.progress(50)
                
                # Run the actual analysis
                output = run_analysis(company, st.session_state.selected_analysis)
                
                status_text.text("Processing insights...")
                progress_bar.progress(75)
                
                status_text.text("Finalizing report...")
                progress_bar.progress(100)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display success message
                st.success(f"✅ Analysis complete for **{company}**")
                
                # Display results in a nice container
                st.markdown("---")
                st.markdown(f"## 📄 {st.session_state.selected_analysis} Report")
                
                # Results container
                with st.container():
                    st.markdown(output)
                
                # Download button
                st.download_button(
                    label="📥 Download Report",
                    data=output,
                    file_name=f"{company}_{st.session_state.selected_analysis.replace(' ', '_')}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"❌ Error occurred: {str(e)}")
                st.markdown("""
                <div class="info-box">
                    <strong>💡 Troubleshooting Tips:</strong>
                    <ul>
                        <li>Check your API keys in the .env file</li>
                        <li>Ensure you have internet connectivity</li>
                        <li>Try a different company name</li>
                        <li>Verify API rate limits haven't been exceeded</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem 0;">
    <p style="margin: 0;">Built with ❤️ using Streamlit • LangChain • Grok-4</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">© 2024 AI Product Launch Intelligence</p>
</div>
""", unsafe_allow_html=True)
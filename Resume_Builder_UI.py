import streamlit as st
import time
import base64
import random
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Intelligent Resume Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states for persistent data
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'analyzed_skills' not in st.session_state:
    st.session_state.analyzed_skills = []
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

# Custom styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem !important;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 0.5rem;
        padding-top: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    .card {
        border-radius: 0.7rem;
        background-color: #f8f9fa;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1E88E5;
    }
    .keyword-tag {
        display: inline-block;
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 0.3rem 0.6rem;
        border-radius: 1rem;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
    .missing-keyword-tag {
        display: inline-block;
        background-color: #ffebee;
        color: #c62828;
        padding: 0.3rem 0.6rem;
        border-radius: 1rem;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: bold;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        color: #0d47a1;
    }
    .tip-box {
        background-color: #e8f5e9;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #2e7d32;
    }
    .highlight {
        background-color: #fff176;
        padding: 0 0.2rem;
        border-radius: 0.2rem;
    }
    .stButton > button {
        font-weight: bold;
        height: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with tips and information
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/resume.png", width=80)
    st.markdown("## Guide & Tips")
    
    with st.expander("About ATS Systems", expanded=False):
        st.markdown("""
        **Applicant Tracking Systems (ATS)** scan your resume before a human ever sees it.
        
        Key points:
        - 75% of resumes are rejected by ATS before reaching a recruiter
        - Simple formatting increases your chances
        - Keyword matching is crucial for passing ATS filters
        """)
    
    with st.expander("Resume Best Practices", expanded=False):
        st.markdown("""
        1. **Be Specific**: Use numbers and metrics to quantify achievements
        2. **Customize**: Tailor your resume for each job application
        3. **Format Properly**: Use consistent headers and bullet points
        4. **Focus on Relevance**: Prioritize relevant experience
        5. **Check for Typos**: Spelling and grammar errors create poor impressions
        """)
    
    with st.expander("Keyword Optimization Tips", expanded=True):
        st.markdown("""
        ✅ Include technical skills mentioned in the job description
        
        ✅ Match the exact phrasing used in the listing
        
        ✅ Include both acronyms and spelled-out versions (e.g., "UI/UX" and "User Interface")
        
        ✅ Use industry-standard terminology
        
        ✅ Include soft skills that match the company culture
        """)
    
    st.markdown("---")
    st.markdown("### Need help?")
    help_option = st.selectbox(
        "Choose an option:",
        ["Select", "Common Resume Mistakes", "What to Include", "ATS Compatibility Issues"]
    )
    
    if help_option == "Common Resume Mistakes":
        st.info("""
        - **Too generic**: Not tailoring to specific job
        - **Wall of text**: Poor formatting and readability
        - **Missing keywords**: Not including terms from job description
        - **Too long**: Exceeding 2 pages for most roles
        - **Focusing on duties**: Not highlighting accomplishments
        """)
    elif help_option == "What to Include":
        st.info("""
        - **Professional summary**: 2-3 sentences highlighting your value
        - **Relevant skills**: Both technical and soft skills
        - **Work experience**: Focus on achievements, not just responsibilities
        - **Education**: Degrees, certifications, relevant coursework
        - **Projects**: Highlight relevant work with measurable outcomes
        """)
    elif help_option == "ATS Compatibility Issues":
        st.info("""
        - **Complex formatting**: Tables, headers, footers, columns
        - **Images & graphics**: Most ATS can't read these
        - **Non-standard section headings**: Stick to conventional titles
        - **PDF compatibility**: Ensure PDFs are text-based, not scanned
        - **File naming**: Use simple names (FirstName_LastName_Resume.pdf)
        """)

# Main content
st.markdown('<p class="main-title">INTELLIGENT RESUME BUILDER</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Build an ATS-optimized resume tailored to your target job</p>', unsafe_allow_html=True)

# Main sections with tabs
tab1, tab2, tab3 = st.tabs(["📝 Input Details", "🔄 Analyze & Optimize", "📄 Results & Download"])

# Tab 1: Input Details
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">Job Information</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        job_role = st.text_input(
            "Enter Job Role",
            placeholder="e.g., Data Scientist, Software Engineer",
            help="Be specific about the exact role you're applying for"
        )
    
    with col2:
        company_name = st.text_input(
            "Company Name (Optional)",
            placeholder="e.g., Google, Amazon",
            help="Including the company name helps personalize your resume"
        )
    
    job_description = st.text_area(
        "Paste Job Description",
        height=200,
        placeholder="Paste the complete job description here for best results...",
        help="The more complete the job description, the better the analysis"
    )
    
    
    # Resume upload section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">Upload Your Current Resume</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Please upload your current resume in PDF format (Max 10MB)"
    )
    
    if uploaded_file is not None:
        file_size_kb = uploaded_file.size / 1024
        st.session_state.file_uploaded = True
        
        # Success message with file details
        st.success(f"✅ Resume uploaded: {uploaded_file.name} ({file_size_kb:.1f} KB)")
        
        # Preview toggle
        if st.checkbox("Show Resume Preview", value=True):
            try:
                # Display PDF
                base64_pdf = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error previewing PDF: {e}")
    else:
        # Resume template options if no file is uploaded
        st.info("Don't have a resume? Select a template to start with:")
        template_col1, template_col2, template_col3 = st.columns(3)
        with template_col1:
            st.button("Basic Template")
        with template_col2:
            st.button("Professional Template")
        with template_col3:
            st.button("Modern Template")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Optimization options
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">Optimization Settings</p>', unsafe_allow_html=True)
    
    opt_col1, opt_col2 = st.columns(2)
    
    with opt_col1:
        optimization_level = st.select_slider(
            "Optimization Level",
            options=["Light", "Moderate", "Comprehensive"],
            value="Moderate",
            help="How extensively should we modify your resume"
        )
        
        focus_areas = st.multiselect(
            "Focus Areas",
            ["Technical Skills", "Experience Descriptions", "Projects", "Professional Summary", "Education", "Certifications"],
            default=["Technical Skills", "Experience Descriptions", "Professional Summary"],
            help="Select areas to prioritize for optimization"
        )
    
    with opt_col2:
        st.markdown("##### Format Options")
        ats_format = st.checkbox("Optimize for ATS compatibility", value=True)
        highlight_keywords = st.checkbox("Highlight matching keywords", value=True)
        add_missing_skills = st.checkbox("Add missing relevant skills", value=True)
        reorder_sections = st.checkbox("Reorder sections by relevance", value=True)
    
    # Continue button to next tab
    if st.button("Continue to Analysis", type="primary", use_container_width=True, disabled=not st.session_state.file_uploaded):
        if job_description.strip() == "":
            st.error("⚠️ Please enter a job description before continuing")
        else:
            st.switch_page("tab2")  # This would need a custom mechanism in actual Streamlit
            
    st.markdown("</div>", unsafe_allow_html=True)

# Tab 2: Analysis & Optimization
with tab2:
    if not st.session_state.file_uploaded:
        st.warning("Please upload your resume in the Input Details tab first")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="section-header">Resume Analysis</p>', unsafe_allow_html=True)
        
        if st.button("Start Analysis", type="primary", use_container_width=True):
            with st.spinner("Analyzing your resume and job description..."):
                # Simulated analysis with progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate different analysis stages
                for i, stage in enumerate([
                    "Extracting text from resume...",
                    "Identifying skills and experience...",
                    "Comparing with job requirements...",
                    "Finding optimization opportunities...",
                    "Preparing recommendations..."
                ]):
                    status_text.text(stage)
                    progress_value = (i + 1) * 20
                    progress_bar.progress(progress_value)
                    time.sleep(0.8)  # Simulate processing time
                
                status_text.text("Analysis complete!")
                st.session_state.processing_complete = True
                
                # Generate sample skills for demo
                st.session_state.analyzed_skills = {
                    "matching": ["Python", "Data Analysis", "SQL", "Communication", "Problem Solving"],
                    "missing": ["TensorFlow", "AWS", "Docker", "Agile Methodology", "CI/CD"],
                    "irrelevant": ["Microsoft Word", "Photography", "Social Media Management"]
                }
        
        if st.session_state.processing_complete:
            # Display analysis results
            st.success("✅ Analysis completed successfully!")
            
            # Metric scores
            met_col1, met_col2, met_col3, met_col4 = st.columns(4)
            
            match_score = random.randint(65, 85)
            with met_col1:
                st.metric("Overall Match", f"{match_score}%", help="How well your resume matches the job requirements")
            
            keyword_score = random.randint(60, 80)
            with met_col2:
                st.metric("Keyword Match", f"{keyword_score}%", help="Percentage of job keywords found in your resume")
            
            ats_score = random.randint(70, 90)
            with met_col3:
                st.metric("ATS Compatibility", f"{ats_score}%", help="How likely your resume is to pass ATS systems")
            
            relevance_score = random.randint(65, 85)
            with met_col4:
                st.metric("Content Relevance", f"{relevance_score}%", help="How relevant your experience is to the job")
            
            # Skills analysis
            st.markdown("##### Skills Analysis")
            
            skill_col1, skill_col2 = st.columns(2)
            
            with skill_col1:
                st.markdown("**Matching Skills**")
                matching_skills_html = ""
                for skill in st.session_state.analyzed_skills["matching"]:
                    matching_skills_html += f'<span class="keyword-tag">✓ {skill}</span>'
                st.markdown(matching_skills_html, unsafe_allow_html=True)
                
                st.markdown("**Missing Skills**")
                missing_skills_html = ""
                for skill in st.session_state.analyzed_skills["missing"]:
                    missing_skills_html += f'<span class="missing-keyword-tag">+ {skill}</span>'
                st.markdown(missing_skills_html, unsafe_allow_html=True)
            
            with skill_col2:
                # Simple bar chart for visualization
                fig, ax = plt.subplots(figsize=(5, 3))
                labels = ['Matching', 'Missing', 'Irrelevant']
                values = [len(st.session_state.analyzed_skills["matching"]), 
                          len(st.session_state.analyzed_skills["missing"]),
                          len(st.session_state.analyzed_skills["irrelevant"])]
                
                colors = ['#4CAF50', '#FFC107', '#F44336']
                ax.bar(labels, values, color=colors)
                ax.set_ylabel('Number of Skills')
                ax.set_title('Skills Distribution')
                
                # Display the matplotlib figure in Streamlit
                st.pyplot(fig)
            
            # Improvement recommendations
            st.markdown("##### Recommended Improvements")
            
            recommendations = [
                "Add missing skills like TensorFlow and Docker to your Skills section",
                "Quantify achievements in your work experience (add numbers and metrics)",
                "Improve your Professional Summary to better match job requirements",
                "Use more action verbs at the beginning of your bullet points",
                "Add more industry-specific keywords throughout your resume"
            ]
            
            for i, rec in enumerate(recommendations):
                st.markdown(f"{i+1}. {rec}")
            
            # Continue button
            if st.button("Optimize My Resume", type="primary", use_container_width=True):
                st.switch_page("tab3")  # This would need a custom mechanism in actual Streamlit
        
        st.markdown("</div>", unsafe_allow_html=True)

# Tab 3: Results and Download
with tab3:
    if not st.session_state.processing_complete:
        st.warning("Please complete the analysis in the previous tab first")
    else:
        # Simulated optimization process
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<p class="section-header">Your Optimized Resume</p>', unsafe_allow_html=True)
        
        with st.spinner("Generating your optimized resume..."):
            # Simulate optimization process
            time.sleep(2)
        
        st.success("🎉 Your resume has been successfully optimized!")
        
        # Before/After comparison option
        if st.checkbox("Show Before/After Comparison", value=True):
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                st.markdown("##### Original Resume")
                if uploaded_file:
                    base64_pdf = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
            
            with comp_col2:
                st.markdown("##### Optimized Resume")
                # In a real app, this would be the optimized PDF
                # For demo, we'll just use the same PDF
                if uploaded_file:
                    base64_pdf = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Highlight changes
        with st.expander("Key Changes Made", expanded=True):
            changes = [
                "Added 5 missing keywords from the job description",
                "Reordered sections to prioritize relevant experience",
                "Enhanced professional summary to better match job requirements",
                "Reformatted bullet points for better ATS readability",
                "Added quantifiable achievements to work experience",
                "Removed irrelevant skills and experiences",
                "Updated header format for better ATS compatibility"
            ]
            
            for change in changes:
                st.markdown(f"✅ {change}")
        
        # Download options
        st.markdown("##### Download Options")
        download_col1, download_col2, download_col3 = st.columns(3)
        
        with download_col1:
            st.download_button(
                "Download as PDF",
                data=uploaded_file.getvalue() if uploaded_file else b"",  # In a real app, this would be the optimized PDF
                file_name="ATS_Optimized_Resume.pdf",
                mime="application/pdf"
            )
        
        with download_col2:
            # In a real app, this would be a DOCX conversion
            st.download_button(
                "Download as DOCX",
                data=uploaded_file.getvalue() if uploaded_file else b"",
                file_name="ATS_Optimized_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        
        with download_col3:
            # In a real app, this would be a plain text version
            st.download_button(
                "Download as TXT",
                data=b"This is a text version of your resume" if uploaded_file else b"",
                file_name="ATS_Optimized_Resume.txt",
                mime="text/plain"
            )
        
        # Next steps and advice
        st.markdown("##### Next Steps")
        
        next_steps_html = """
        <div class="tip-box">
            <h4>Pro Tips for Your Application</h4>
            <ul>
                <li><strong>Customize cover letter:</strong> Use the same keywords in your cover letter</li>
                <li><strong>Follow up:</strong> Send a follow-up email 3-5 days after applying</li>
                <li><strong>Prepare for interview:</strong> Research common questions for this role</li>
                <li><strong>LinkedIn profile:</strong> Update your LinkedIn to match your optimized resume</li>
            </ul>
        </div>
        """
        st.markdown(next_steps_html, unsafe_allow_html=True)
        
        # Feedback option
        st.markdown("##### Was this helpful?")
        feedback_col1, feedback_col2, feedback_col3 = st.columns(3)
        with feedback_col1:
            st.button("👍 Very Helpful")
        with feedback_col2:
            st.button("🤔 Somewhat Helpful")
        with feedback_col3:
            st.button("👎 Not Helpful")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")

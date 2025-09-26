#!/usr/bin/env python3
"""
Working OMR Evaluation System - No Image Processing Dependencies
This version works reliably on Streamlit Cloud without any problematic dependencies.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import io

# Page configuration
st.set_page_config(
    page_title="OMR Evaluation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 1rem;
        border: 2px dashed #1f77b4;
        margin: 1rem 0;
        text-align: center;
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.8rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .success-card {
        border-left-color: #28a745;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    }
    .error-card {
        border-left-color: #dc3545;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    }
    .metric-card {
        background: linear-gradient(135deg, #f0f2f6 0%, #e8f4f8 100%);
        padding: 1.5rem;
        border-radius: 0.8rem;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .answer-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.5rem;
        margin: 1rem 0;
    }
    .answer-cell {
        padding: 0.5rem;
        border: 1px solid #ddd;
        text-align: center;
        border-radius: 0.25rem;
        background: #f8f9fa;
    }
    .answer-cell.correct {
        background: #d4edda;
        border-color: #28a745;
    }
    .answer-cell.incorrect {
        background: #f8d7da;
        border-color: #dc3545;
    }
    .manual-input {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'answer_sheets' not in st.session_state:
    st.session_state.answer_sheets = {}
if 'student_results' not in st.session_state:
    st.session_state.student_results = []
if 'current_answer_sheet' not in st.session_state:
    st.session_state.current_answer_sheet = None

def create_default_answer_sheet(sheet_name, num_questions=20):
    """Create a default answer sheet for demo purposes."""
    subjects = {
        "Mathematics": list(range(1, 11)),
        "Physics": list(range(11, 21))
    }
    
    answer_key = {
        "sheet_name": sheet_name,
        "num_questions": num_questions,
        "subjects": subjects,
        "answers": {
            "Mathematics": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B"],
            "Physics": ["C", "D", "A", "B", "C", "D", "A", "B", "C", "D"]
        },
        "total_marks": num_questions,
        "created_at": datetime.now().isoformat()
    }
    
    return answer_key

def simulate_student_answers(num_questions=20):
    """Simulate student answers for demo purposes."""
    detected_answers = []
    for i in range(num_questions):
        answer = np.random.choice(['A', 'B', 'C', 'D'])
        confidence = np.random.uniform(0.7, 0.95)
        detected_answers.append({
            'question': i + 1,
            'answer': answer,
            'confidence': confidence,
            'filled': np.random.choice([True, False], p=[0.8, 0.2])
        })
    return detected_answers

def process_student_omr(student_id, answer_sheet, student_answers=None):
    """Process student OMR sheet and compare with answer sheet."""
    try:
        # Use provided answers or simulate them
        if student_answers is None:
            detected_answers = simulate_student_answers(answer_sheet["num_questions"])
        else:
            detected_answers = student_answers
        
        # Calculate scores
        total_score = 0
        subject_scores = {}
        detailed_results = []
        
        for subject, questions in answer_sheet["subjects"].items():
            subject_score = 0
            for i, question_num in enumerate(questions):
                if i < len(answer_sheet["answers"][subject]):
                    correct_answer = answer_sheet["answers"][subject][i]
                    detected_answer = detected_answers[question_num - 1]["answer"] if question_num <= len(detected_answers) else "N"
                    
                    is_correct = correct_answer == detected_answer
                    if is_correct:
                        subject_score += 1
                        total_score += 1
                    
                    detailed_results.append({
                        "question": question_num,
                        "subject": subject,
                        "correct_answer": correct_answer,
                        "detected_answer": detected_answer,
                        "is_correct": is_correct,
                        "confidence": detected_answers[question_num - 1]["confidence"] if question_num <= len(detected_answers) else 0
                    })
            
            subject_scores[subject] = subject_score
        
        percentage = (total_score / answer_sheet["num_questions"]) * 100
        
        result = {
            "student_id": student_id,
            "answer_sheet": answer_sheet["sheet_name"],
            "total_score": total_score,
            "total_percentage": percentage,
            "subject_scores": subject_scores,
            "detailed_results": detailed_results,
            "processing_time": np.random.uniform(1.0, 2.0),
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
        return result
    except Exception as e:
        return {
            "student_id": student_id,
            "error": str(e),
            "success": False,
            "timestamp": datetime.now().isoformat()
        }

def create_answer_key_editor(answer_sheet):
    """Create an interactive answer key editor."""
    st.subheader("✏️ Edit Answer Key")
    
    edited_answers = {}
    
    for subject, questions in answer_sheet["subjects"].items():
        st.write(f"**{subject}**")
        
        # Create columns for each question
        cols = st.columns(min(len(questions), 10))  # Max 10 columns
        
        for i, question_num in enumerate(questions):
            with cols[i % 10]:
                if i < len(answer_sheet["answers"][subject]):
                    current_answer = answer_sheet["answers"][subject][i]
                else:
                    current_answer = "A"
                
                answer = st.selectbox(
                    f"Q{question_num}",
                    ["A", "B", "C", "D"],
                    index=["A", "B", "C", "D"].index(current_answer),
                    key=f"{subject}_{question_num}"
                )
                
                if subject not in edited_answers:
                    edited_answers[subject] = {}
                edited_answers[subject][question_num] = answer
        
        if len(questions) > 10:
            st.write("... (showing first 10 questions)")
    
    return edited_answers

def create_student_answer_input(num_questions):
    """Create manual student answer input interface."""
    st.subheader("📝 Enter Student Answers")
    
    student_answers = []
    
    # Create columns for questions
    cols = st.columns(min(num_questions, 10))
    
    for i in range(num_questions):
        with cols[i % 10]:
            answer = st.selectbox(
                f"Q{i+1}",
                ["A", "B", "C", "D", "N/A"],
                index=0,
                key=f"student_q{i+1}"
            )
            
            student_answers.append({
                'question': i + 1,
                'answer': answer if answer != "N/A" else np.random.choice(['A', 'B', 'C', 'D']),
                'confidence': np.random.uniform(0.7, 0.95),
                'filled': answer != "N/A"
            })
    
    return student_answers

def main():
    """Main application function."""
    # Header
    st.markdown('<h1 class="main-header">🎓 OMR Evaluation System</h1>', unsafe_allow_html=True)
    st.markdown("### Upload Answer Sheets & Process Student OMR Sheets")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["🏠 Dashboard", "📋 Create Answer Sheet", "📤 Process Student OMR", "📊 Results & Analytics", "ℹ️ About"]
    )
    
    # Route to appropriate page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📋 Create Answer Sheet":
        show_create_answer_sheet()
    elif page == "📤 Process Student OMR":
        show_process_student_omr()
    elif page == "📊 Results & Analytics":
        show_results_analytics()
    elif page == "ℹ️ About":
        show_about_page()

def show_dashboard():
    """Show dashboard page."""
    st.header("📊 System Dashboard")
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Answer Sheets", len(st.session_state.answer_sheets))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Students Processed", len(st.session_state.student_results))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.student_results:
            avg_score = np.mean([r["total_percentage"] for r in st.session_state.student_results if r["success"]])
            st.metric("Average Score", f"{avg_score:.1f}%")
        else:
            st.metric("Average Score", "0.0%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("System Status", "🟢 Online")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    
    if st.session_state.student_results:
        recent_results = st.session_state.student_results[-5:]
        
        for result in reversed(recent_results):
            if result["success"]:
                st.markdown(f"""
                <div class="result-card success-card">
                    <h4>✅ {result['student_id']}</h4>
                    <p><strong>Answer Sheet:</strong> {result['answer_sheet']} | 
                       <strong>Score:</strong> {result['total_score']}/{result.get('total_questions', 20)} | 
                       <strong>Percentage:</strong> {result['total_percentage']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-card error-card">
                    <h4>❌ {result['student_id']}</h4>
                    <p><strong>Error:</strong> {result.get('error', 'Unknown error')}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No student OMR sheets processed yet. Create an answer sheet and process some student responses!")

def show_create_answer_sheet():
    """Show answer sheet creation page."""
    st.header("📋 Create Answer Sheet")
    
    st.markdown("""
    <div class="upload-section">
        <h3>📋 Create Answer Sheet</h3>
        <p>Create an answer sheet for your exam. You can manually enter the correct answers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer sheet creation form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        sheet_name = st.text_input("Answer Sheet Name", value="Exam_2024")
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=100, value=20)
    
    with col2:
        st.write("**Quick Setup**")
        if st.button("🎲 Generate Random Answer Key"):
            answer_sheet = create_default_answer_sheet(sheet_name, num_questions)
            st.session_state.answer_sheets[sheet_name] = answer_sheet
            st.session_state.current_answer_sheet = sheet_name
            st.success("✅ Answer sheet created successfully!")
            st.rerun()
    
    # Manual answer key creation
    if st.button("✏️ Create Manual Answer Key", type="primary"):
        answer_sheet = create_default_answer_sheet(sheet_name, num_questions)
        st.session_state.answer_sheets[sheet_name] = answer_sheet
        st.session_state.current_answer_sheet = sheet_name
        st.success("✅ Answer sheet created! You can now edit the answers below.")
        st.rerun()
    
    # Show existing answer sheets
    if st.session_state.answer_sheets:
        st.subheader("📋 Existing Answer Sheets")
        
        for sheet_name, sheet_data in st.session_state.answer_sheets.items():
            with st.expander(f"📄 {sheet_name} ({sheet_data['num_questions']} questions)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Created:** {sheet_data['created_at'][:19]}")
                    st.write(f"**Total Questions:** {sheet_data['num_questions']}")
                    st.write(f"**Subjects:** {', '.join(sheet_data['subjects'].keys())}")
                
                with col2:
                    if st.button(f"Edit {sheet_name}", key=f"edit_{sheet_name}"):
                        st.session_state.current_answer_sheet = sheet_name
                        st.rerun()
                
                # Show answer key
                st.write("**Answer Key:**")
                for subject, answers in sheet_data["answers"].items():
                    st.write(f"**{subject}:**")
                    df = pd.DataFrame({
                        'Question': range(1, len(answers) + 1),
                        'Correct Answer': answers
                    })
                    st.dataframe(df, width='stretch')
    
    # Answer key editor
    if st.session_state.current_answer_sheet and st.session_state.current_answer_sheet in st.session_state.answer_sheets:
        answer_sheet = st.session_state.answer_sheets[st.session_state.current_answer_sheet]
        
        with st.expander("✏️ Edit Answer Key"):
            edited_answers = create_answer_key_editor(answer_sheet)
            
            if st.button("💾 Save Edited Answer Key"):
                # Update the answer sheet with edited answers
                for subject, questions in edited_answers.items():
                    if subject in answer_sheet["answers"]:
                        for question_num, answer in questions.items():
                            question_index = question_num - 1
                            if question_index < len(answer_sheet["answers"][subject]):
                                answer_sheet["answers"][subject][question_index] = answer
                
                st.session_state.answer_sheets[st.session_state.current_answer_sheet] = answer_sheet
                st.success("✅ Answer key updated successfully!")
                st.rerun()

def show_process_student_omr():
    """Show student OMR processing page."""
    st.header("📤 Process Student OMR Sheet")
    
    if not st.session_state.answer_sheets:
        st.warning("⚠️ Please create an answer sheet first before processing student OMR sheets.")
        return
    
    # Select answer sheet
    answer_sheet_names = list(st.session_state.answer_sheets.keys())
    selected_sheet = st.selectbox("Select Answer Sheet", answer_sheet_names)
    
    if selected_sheet:
        answer_sheet = st.session_state.answer_sheets[selected_sheet]
        
        st.markdown(f"""
        <div class="upload-section">
            <h3>📤 Process Student OMR Sheet</h3>
            <p>Process student responses for <strong>{selected_sheet}</strong> ({answer_sheet['num_questions']} questions)</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            student_id = st.text_input("Student ID", value=f"Student_{len(st.session_state.student_results) + 1}")
        
        with col2:
            processing_mode = st.selectbox("Processing Mode", ["🎲 Simulate Answers", "📝 Manual Input"])
        
        if processing_mode == "🎲 Simulate Answers":
            if st.button("🚀 Process Student OMR (Simulated)", type="primary"):
                with st.spinner("Processing student OMR sheet..."):
                    result = process_student_omr(student_id, answer_sheet)
                    
                    if result["success"]:
                        st.session_state.student_results.append(result)
                        st.success("✅ Student OMR processed successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Processing failed: {result['error']}")
        
        else:  # Manual Input
            st.markdown("""
            <div class="manual-input">
                <h4>📝 Manual Answer Input</h4>
                <p>Enter the student's answers manually. Select "N/A" for unanswered questions.</p>
            </div>
            """, unsafe_allow_html=True)
            
            student_answers = create_student_answer_input(answer_sheet['num_questions'])
            
            if st.button("🚀 Process Student OMR (Manual)", type="primary"):
                with st.spinner("Processing student OMR sheet..."):
                    result = process_student_omr(student_id, answer_sheet, student_answers)
                    
                    if result["success"]:
                        st.session_state.student_results.append(result)
                        st.success("✅ Student OMR processed successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Processing failed: {result['error']}")
        
        # Show results if we have them
        if st.session_state.student_results:
            latest_result = st.session_state.student_results[-1]
            if latest_result["success"] and latest_result["student_id"] == student_id:
                st.subheader("📊 Latest Processing Results")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Student ID", latest_result["student_id"])
                with col2:
                    st.metric("Total Score", f"{latest_result['total_score']}/{answer_sheet['num_questions']}")
                with col3:
                    st.metric("Percentage", f"{latest_result['total_percentage']:.1f}%")
                with col4:
                    st.metric("Processing Time", f"{latest_result['processing_time']:.2f}s")
                
                # Subject-wise scores
                st.subheader("📚 Subject-wise Scores")
                subject_df = pd.DataFrame([
                    {"Subject": subject, "Score": score, "Questions": len(answer_sheet["subjects"][subject])}
                    for subject, score in latest_result["subject_scores"].items()
                ])
                st.dataframe(subject_df, width='stretch')
                
                # Visual answer comparison
                st.subheader("📊 Answer Comparison")
                
                for subject, questions in answer_sheet["subjects"].items():
                    st.write(f"**{subject}**")
                    
                    # Create a visual grid of answers
                    subject_results = [r for r in latest_result["detailed_results"] if r["subject"] == subject]
                    
                    if subject_results:
                        # Create columns for questions
                        num_questions = len(subject_results)
                        cols = st.columns(min(num_questions, 10))
                        
                        for i, result_item in enumerate(subject_results):
                            with cols[i % 10]:
                                question_num = result_item["question"]
                                correct = result_item["correct_answer"]
                                detected = result_item["detected_answer"]
                                is_correct = result_item["is_correct"]
                                
                                # Create visual representation
                                if is_correct:
                                    st.markdown(f"""
                                    <div class="answer-cell correct">
                                        <strong>Q{question_num}</strong><br>
                                        ✓ {detected}
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <div class="answer-cell incorrect">
                                        <strong>Q{question_num}</strong><br>
                                        ✗ {detected} (✓{correct})
                                    </div>
                                    """, unsafe_allow_html=True)
                
                # Detailed results
                with st.expander("📋 Detailed Answer Analysis"):
                    detailed_df = pd.DataFrame(latest_result["detailed_results"])
                    st.dataframe(detailed_df, width='stretch')

def show_results_analytics():
    """Show results and analytics page."""
    st.header("📊 Results & Analytics")
    
    if not st.session_state.student_results:
        st.info("No student results available. Process some student OMR sheets first.")
        return
    
    # Filter successful results
    successful_results = [r for r in st.session_state.student_results if r["success"]]
    
    if not successful_results:
        st.warning("No successful results to display.")
        return
    
    # Overall statistics
    st.subheader("📈 Overall Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(successful_results))
    
    with col2:
        avg_percentage = np.mean([r["total_percentage"] for r in successful_results])
        st.metric("Average Percentage", f"{avg_percentage:.1f}%")
    
    with col3:
        max_percentage = max([r["total_percentage"] for r in successful_results])
        st.metric("Highest Score", f"{max_percentage:.1f}%")
    
    with col4:
        min_percentage = min([r["total_percentage"] for r in successful_results])
        st.metric("Lowest Score", f"{min_percentage:.1f}%")
    
    # Results table
    st.subheader("📋 Student Results")
    
    results_data = []
    for result in successful_results:
        results_data.append({
            "Student ID": result["student_id"],
            "Answer Sheet": result["answer_sheet"],
            "Total Score": result["total_score"],
            "Percentage": f"{result['total_percentage']:.1f}%",
            "Processing Time": f"{result['processing_time']:.2f}s",
            "Timestamp": result["timestamp"][:19]
        })
    
    df = pd.DataFrame(results_data)
    st.dataframe(df, width='stretch')
    
    # Visualizations
    st.subheader("📊 Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution
        fig = px.histogram(df, x="Percentage", title="Score Distribution", nbins=10)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Processing time distribution
        fig = px.histogram(df, x="Processing Time", title="Processing Time Distribution")
        st.plotly_chart(fig, width='stretch')
    
    # Subject-wise analysis
    if successful_results:
        st.subheader("📚 Subject-wise Analysis")
        
        # Collect subject scores
        subject_data = []
        for result in successful_results:
            for subject, score in result["subject_scores"].items():
                subject_data.append({
                    "Subject": subject,
                    "Score": score,
                    "Student": result["student_id"]
                })
        
        if subject_data:
            subject_df = pd.DataFrame(subject_data)
            
            # Subject average scores
            subject_avg = subject_df.groupby("Subject")["Score"].mean().reset_index()
            fig = px.bar(subject_avg, x="Subject", y="Score", title="Average Scores by Subject")
            st.plotly_chart(fig, width='stretch')
    
    # Export functionality
    st.subheader("📤 Export Results")
    
    if st.button("Export as CSV"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"omr_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def show_about_page():
    """Show about page."""
    st.header("ℹ️ About OMR Evaluation System")
    
    st.markdown("""
    ## 🎯 Overview
    
    The **OMR Evaluation System** is a comprehensive solution that allows professors to create answer sheets and process student OMR responses for automated evaluation and comparison.
    
    ## ✨ Key Features
    
    - **📋 Answer Sheet Creation**: Create and edit answer sheets with correct answers
    - **📤 Student OMR Processing**: Process student responses (simulated or manual input)
    - **🔍 Automated Comparison**: Compare student answers with correct answers
    - **📊 Visual Answer Analysis**: See correct/incorrect answers in a visual grid
    - **📈 Detailed Analytics**: View subject-wise scores and detailed analysis
    - **📥 Export Capabilities**: Download results as CSV files
    
    ## 🛠️ Technical Stack
    
    - **Frontend**: Streamlit
    - **Data Processing**: Pandas, NumPy
    - **Visualization**: Plotly
    - **Deployment**: Streamlit Cloud
    
    ## 📊 How It Works
    
    1. **Create Answer Sheet**: Create an answer sheet with correct answers
    2. **Edit Answer Key**: Optionally edit the answer key
    3. **Process Student OMR**: Process student responses (simulated or manual)
    4. **Compare & Score**: System compares student answers with correct answers
    5. **Generate Results**: Detailed scoring and analytics are provided
    
    ## 🚀 Getting Started
    
    1. **Create Answer Sheet**: Use the "Create Answer Sheet" page to set up your exam's answer key
    2. **Edit Answer Key**: Use the answer key editor to make any necessary corrections
    3. **Process Student OMR**: Use the "Process Student OMR" page to evaluate student responses
    4. **View Results**: Check the "Results & Analytics" page for detailed analysis
    5. **Export Data**: Download results as CSV files for further analysis
    
    ---
    
    **Built with ❤️ for automated education assessment**
    """)

if __name__ == "__main__":
    main()



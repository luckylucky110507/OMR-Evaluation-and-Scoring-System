"""
Streamlit Cloud Simple Version - OMR Evaluation System.
Cloud-optimized version without OpenCV dependencies.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import io
from typing import List, Dict, Any
import base64
from PIL import Image, ImageDraw, ImageFont

# Page configuration
st.set_page_config(
    page_title="OMR Evaluation System",
    page_icon="📊",
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
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .error-message {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-message {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 1rem;
        border: 2px dashed #1f77b4;
        text-align: center;
        margin: 1rem 0;
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.8rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_results' not in st.session_state:
    st.session_state.processed_results = []
if 'answer_key' not in st.session_state:
    st.session_state.answer_key = None

def create_default_answer_key():
    """Create a default answer key for demo purposes."""
    return {
        "version": "demo_v1",
        "subjects": {
            "Mathematics": {
                "questions": list(range(1, 21)),
                "answers": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", 
                          "C", "D", "A", "B", "C", "D", "A", "B", "C", "D"]
            },
            "Physics": {
                "questions": list(range(21, 41)),
                "answers": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", 
                          "C", "D", "A", "B", "C", "D", "A", "B", "C", "D"]
            },
            "Chemistry": {
                "questions": list(range(41, 61)),
                "answers": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", 
                          "C", "D", "A", "B", "C", "D", "A", "B", "C", "D"]
            },
            "Biology": {
                "questions": list(range(61, 81)),
                "answers": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", 
                          "C", "D", "A", "B", "C", "D", "A", "B", "C", "D"]
            },
            "General_Knowledge": {
                "questions": list(range(81, 101)),
                "answers": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", 
                          "C", "D", "A", "B", "C", "D", "A", "B", "C", "D"]
            }
        }
    }

def simulate_omr_processing(student_answers, answer_key, student_id):
    """Simulate OMR processing without OpenCV."""
    try:
        # Simulate processing time
        import time
        time.sleep(0.5)  # Simulate processing delay
        
        # Calculate scores
        total_correct = 0
        total_questions = 0
        subject_scores = []
        
        for subject_name, subject_data in answer_key["subjects"].items():
            questions = subject_data["questions"]
            correct_count = 0
            
            for i, question_num in enumerate(questions):
                if question_num <= len(student_answers):
                    student_choice = student_answers[question_num - 1]
                    correct_answer = subject_data["answers"][i]
                    
                    # Handle multiple correct answers (like "A,B,C,D")
                    if ',' in correct_answer:
                        correct_choices = [correct_answer.strip() for correct_answer in correct_answer.split(',')]
                    else:
                        correct_choices = [correct_answer.strip()]
                    
                    # Convert student choice to answer format
                    if isinstance(student_choice, list) and len(student_choice) > 0:
                        # Convert numeric choice to letter
                        student_answer = []
                        for choice in student_choice:
                            if choice == 0:
                                student_answer.append('A')
                            elif choice == 1:
                                student_answer.append('B')
                            elif choice == 2:
                                student_answer.append('C')
                            elif choice == 3:
                                student_answer.append('D')
                        student_answer_str = ','.join(student_answer)
                    else:
                        student_answer_str = str(student_choice) if student_choice else ""
                    
                    # Check if student answer matches any correct answer
                    is_correct = False
                    for correct_choice in correct_choices:
                        if student_answer_str.upper() == correct_choice.upper():
                            is_correct = True
                            break
                        # Also check for partial matches (single letter in multiple choice)
                        elif correct_choice in student_answer_str.upper():
                            is_correct = True
                            break
                    
                    if is_correct:
                        correct_count += 1
                        total_correct += 1
                    
                    total_questions += 1
            
            percentage = (correct_count / len(questions)) * 100 if len(questions) > 0 else 0
            
            subject_scores.append({
                "subject": subject_name,
                "correct": correct_count,
                "total": len(questions),
                "score": correct_count,
                "percentage": percentage
            })
        
        total_percentage = (total_correct / total_questions) * 100 if total_questions > 0 else 0
        
        return {
            "success": True,
            "student_id": student_id,
            "total_score": total_correct,
            "total_percentage": total_percentage,
            "subject_scores": subject_scores,
            "student_answers": student_answers,  # Include student answers for transparency
            "processing_time": 0.5,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "student_id": student_id
        }

def create_sample_omr_image():
    """Create a sample OMR sheet image using PIL."""
    # Create a white background
    image = Image.new('RGB', (800, 1000), 'white')
    draw = ImageDraw.Draw(image)
    
    # Add border
    draw.rectangle([50, 50, 750, 950], outline='black', width=3)
    
    # Add title
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((200, 100), "OMR EVALUATION SHEET - DEMO", fill='black', font=font)
    
    # Add question numbers and bubbles
    for i in range(20):  # First 20 questions for demo
        y = 200 + i * 30
        
        # Question number
        draw.text((70, y-10), f"{i+1:2d}.", fill='black')
        
        # Answer bubbles (A, B, C, D)
        for j, letter in enumerate(['A', 'B', 'C', 'D']):
            x = 150 + j * 60
            draw.ellipse([x-8, y-8, x+8, y+8], outline='black', width=2)
            
            # Fill some bubbles for demo (simulate student answers)
            if i < 10 and j == 0:  # Fill A for first 10 questions
                draw.ellipse([x-6, y-6, x+6, y+6], fill='black')
            elif i >= 10 and j == 1:  # Fill B for next 10 questions
                draw.ellipse([x-6, y-6, x+6, y+6], fill='black')
    
    return image

def convert_csv_to_answer_key(df):
    """Convert CSV data to answer key format."""
    answer_key = {
        "version": "csv_import",
        "subjects": {}
    }
    
    # Assume CSV has columns: Subject, Question, Answer
    if 'Subject' in df.columns and 'Question' in df.columns and 'Answer' in df.columns:
        for subject in df['Subject'].unique():
            subject_data = df[df['Subject'] == subject]
            questions = subject_data['Question'].tolist()
            answers = subject_data['Answer'].tolist()
            
            answer_key["subjects"][subject] = {
                "questions": questions,
                "answers": answers
            }
    else:
        # Try alternative format: Question, Answer columns
        if 'Question' in df.columns and 'Answer' in df.columns:
            questions = df['Question'].tolist()
            answers = df['Answer'].tolist()
            answer_key["subjects"]["General"] = {
                "questions": questions,
                "answers": answers
            }
        else:
            raise ValueError("CSV must have 'Subject', 'Question', 'Answer' columns or 'Question', 'Answer' columns")
    
    return answer_key

def convert_excel_to_answer_key(df):
    """Convert Excel data to answer key format."""
    answer_key = {
        "version": "excel_import",
        "subjects": {}
    }
    
    # Clean column names (remove extra spaces, convert to lowercase)
    df.columns = df.columns.str.strip().str.lower()
    
    # Check for different Excel formats
    if 'subject' in df.columns and 'question' in df.columns and 'answer' in df.columns:
        # Format 1: Subject, Question, Answer columns
        for subject in df['subject'].unique():
            subject_data = df[df['subject'] == subject]
            questions = subject_data['question'].tolist()
            answers = subject_data['answer'].tolist()
            
            # Convert answers to uppercase
            answers = [str(answer).upper().strip() for answer in answers]
            
            answer_key["subjects"][subject] = {
                "questions": questions,
                "answers": answers
            }
    elif 'question' in df.columns and 'answer' in df.columns:
        # Format 2: Question, Answer columns (single subject)
        questions = df['question'].tolist()
        answers = df['answer'].tolist()
        
        # Convert answers to uppercase
        answers = [str(answer).upper().strip() for answer in answers]
        
        answer_key["subjects"]["General"] = {
            "questions": questions,
            "answers": answers
        }
    elif 'q' in df.columns and 'a' in df.columns:
        # Format 3: Q, A columns (shortened names)
        questions = df['q'].tolist()
        answers = df['a'].tolist()
        
        # Convert answers to uppercase
        answers = [str(answer).upper().strip() for answer in answers]
        
        answer_key["subjects"]["General"] = {
            "questions": questions,
            "answers": answers
        }
    else:
        # Format 4: Subject columns with question-answer pairs (like your format)
        # Check if columns look like subject names with question-answer format
        subject_columns = []
        for col in df.columns:
            col_lower = col.lower().strip()
            # Skip if it's a common non-subject column
            if col_lower not in ['question', 'answer', 'q', 'a', 'subject', 's', 'no', 'number', 'index']:
                subject_columns.append(col)
        
        if subject_columns:
            # Process each subject column
            for subject_col in subject_columns:
                subject_name = subject_col.strip()
                answers = []
                questions = []
                
                # Process each row in this column
                for idx, row in df.iterrows():
                    cell_value = str(row[subject_col]).strip()
                    
                    # Skip empty cells
                    if cell_value == 'nan' or cell_value == '' or cell_value == 'None':
                        continue
                    
                    # Parse question-answer format like "1 - a", "2 - c", etc.
                    if ' - ' in cell_value:
                        try:
                            parts = cell_value.split(' - ')
                            if len(parts) == 2:
                                question_num = int(parts[0].strip())
                                answer = parts[1].strip().upper()
                                
                                # Validate answer (A, B, C, D or multiple like A,B,C,D)
                                if answer in ['A', 'B', 'C', 'D'] or ',' in answer:
                                    questions.append(question_num)
                                    answers.append(answer)
                        except (ValueError, IndexError):
                            continue
                    # Handle simple answer format like "a", "b", "c", "d"
                    elif cell_value.upper() in ['A', 'B', 'C', 'D']:
                        questions.append(idx + 1)  # Use row number as question
                        answers.append(cell_value.upper())
                
                # Only add subject if we found valid questions and answers
                if questions and answers and len(questions) == len(answers):
                    answer_key["subjects"][subject_name] = {
                        "questions": questions,
                        "answers": answers
                    }
                else:
                    # Debug: show what was found for this subject
                    print(f"Debug: Subject '{subject_name}' - Questions: {len(questions)}, Answers: {len(answers)}")
                    if questions:
                        print(f"Debug: Sample questions: {questions[:5]}")
                    if answers:
                        print(f"Debug: Sample answers: {answers[:5]}")
        
        # If no subject columns found, try automatic detection
        if not answer_key["subjects"]:
            possible_question_cols = [col for col in df.columns if 'question' in col.lower() or 'q' in col.lower()]
            possible_answer_cols = [col for col in df.columns if 'answer' in col.lower() or 'a' in col.lower()]
            possible_subject_cols = [col for col in df.columns if 'subject' in col.lower() or 's' in col.lower()]
            
            if possible_question_cols and possible_answer_cols:
                question_col = possible_question_cols[0]
                answer_col = possible_answer_cols[0]
                
                if possible_subject_cols:
                    # Multiple subjects
                    subject_col = possible_subject_cols[0]
                    for subject in df[subject_col].unique():
                        subject_data = df[df[subject_col] == subject]
                        questions = subject_data[question_col].tolist()
                        answers = subject_data[answer_col].tolist()
                        
                        # Convert answers to uppercase
                        answers = [str(answer).upper().strip() for answer in answers]
                        
                        answer_key["subjects"][subject] = {
                            "questions": questions,
                            "answers": answers
                        }
                else:
                    # Single subject
                    questions = df[question_col].tolist()
                    answers = df[answer_col].tolist()
                    
                    # Convert answers to uppercase
                    answers = [str(answer).upper().strip() for answer in answers]
                    
                    answer_key["subjects"]["General"] = {
                        "questions": questions,
                        "answers": answers
                    }
            else:
                raise ValueError("Excel file format not recognized. Expected formats:\n1. Subject columns with 'Question - Answer' format\n2. Subject, Question, Answer columns\n3. Question, Answer columns\n4. Q, A columns")
    
    return answer_key

def validate_answer_key(answer_key):
    """Validate answer key structure."""
    try:
        # Check required fields
        if not isinstance(answer_key, dict):
            return False
        
        if 'version' not in answer_key or 'subjects' not in answer_key:
            return False
        
        # Check subjects structure
        for subject_name, subject_data in answer_key['subjects'].items():
            if not isinstance(subject_data, dict):
                return False
            
            if 'questions' not in subject_data or 'answers' not in subject_data:
                return False
            
            questions = subject_data['questions']
            answers = subject_data['answers']
            
            if not isinstance(questions, list) or not isinstance(answers, list):
                return False
            
            if len(questions) != len(answers):
                return False
            
            # Check answer format (allow single answers or multiple like "A,B,C,D")
            for answer in answers:
                answer_str = str(answer).strip()
                # Check if it's a single answer
                if answer_str in ['A', 'B', 'C', 'D']:
                    continue
                # Check if it's multiple answers separated by commas
                elif ',' in answer_str:
                    multiple_answers = [a.strip() for a in answer_str.split(',')]
                    if all(a in ['A', 'B', 'C', 'D'] for a in multiple_answers):
                        continue
                # If neither, it's invalid
                return False
        
        return True
    except:
        return False

def create_manual_answer_key(version, subjects_data):
    """Create answer key from manual input."""
    answer_key = {
        "version": version,
        "subjects": {}
    }
    
    for subject in subjects_data:
        subject_name = subject['name']
        start_q = subject['start']
        end_q = subject['end']
        answers = subject['answers']
        
        questions = list(range(start_q, end_q + 1))
        answer_list = list(answers)
        
        answer_key["subjects"][subject_name] = {
            "questions": questions,
            "answers": answer_list
        }
    
    return answer_key

def create_sample_answer_key(version):
    """Create sample answer key for different versions."""
    if version == "demo_v1":
        return create_default_answer_key()
    elif version == "demo_v2":
        return {
            "version": "demo_v2",
            "subjects": {
                "Mathematics": {
                    "questions": list(range(1, 26)),
                    "answers": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", 
                              "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A"]
                },
                "Science": {
                    "questions": list(range(26, 51)),
                    "answers": ["B", "C", "D", "A", "B", "C", "D", "A", "B", "C", 
                              "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B"]
                },
                "English": {
                    "questions": list(range(51, 76)),
                    "answers": ["C", "D", "A", "B", "C", "D", "A", "B", "C", "D", 
                              "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C"]
                }
            }
        }
    elif version == "demo_v3":
        return {
            "version": "demo_v3",
            "subjects": {
                "Physics": {
                    "questions": list(range(1, 21)),
                    "answers": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", 
                              "C", "D", "A", "B", "C", "D", "A", "B", "C", "D"]
                },
                "Chemistry": {
                    "questions": list(range(21, 41)),
                    "answers": ["B", "C", "D", "A", "B", "C", "D", "A", "B", "C", 
                              "D", "A", "B", "C", "D", "A", "B", "C", "D", "A"]
                },
                "Biology": {
                    "questions": list(range(41, 61)),
                    "answers": ["C", "D", "A", "B", "C", "D", "A", "B", "C", "D", 
                              "A", "B", "C", "D", "A", "B", "C", "D", "A", "B"]
                }
            }
        }
    else:
        return create_default_answer_key()

def display_answer_key_summary(answer_key):
    """Display answer key summary."""
    st.markdown(f"""
    <div class="result-card">
        <h3>📊 Answer Key Summary</h3>
        <p><strong>Version:</strong> {answer_key['version']}</p>
        <p><strong>Subjects:</strong> {', '.join(answer_key['subjects'].keys())}</p>
        <p><strong>Total Questions:</strong> {sum(len(subject['questions']) for subject in answer_key['subjects'].values())}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show subject details
    for subject_name, subject_data in answer_key["subjects"].items():
        st.write(f"**{subject_name}:** {len(subject_data['questions'])} questions")
    
    # Export option
    if st.button("📥 Export Answer Key"):
        json_data = json.dumps(answer_key, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"answer_key_{answer_key['version']}.json",
            mime="application/json"
        )

def main():
    """Main application function."""
    # Initialize answer key if not set
    if st.session_state.answer_key is None:
        st.session_state.answer_key = create_default_answer_key()
    
    # Header
    st.markdown('<h1 class="main-header">📊 OMR Evaluation System</h1>', unsafe_allow_html=True)
    st.markdown("### Cloud-Optimized OMR Sheet Processing & Scoring")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["🏠 Dashboard", "📤 Upload & Process", "📊 Results & Analytics", "🔑 Answer Keys", "ℹ️ About"]
    )
    
    # Route to appropriate page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📤 Upload & Process":
        show_upload_page()
    elif page == "📊 Results & Analytics":
        show_results_page()
    elif page == "🔑 Answer Keys":
        show_answer_keys_page()
    elif page == "ℹ️ About":
        show_about_page()

def show_dashboard():
    """Show dashboard page."""
    st.header("📊 System Dashboard")
    
    # Display key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Processed", len(st.session_state.processed_results))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.processed_results:
            avg_score = np.mean([r["total_score"] for r in st.session_state.processed_results if r["success"]])
            st.metric("Average Score", f"{avg_score:.1f}")
        else:
            st.metric("Average Score", "0.0")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.processed_results:
            success_count = sum(1 for r in st.session_state.processed_results if r["success"])
            success_rate = (success_count / len(st.session_state.processed_results)) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
        else:
            st.metric("Success Rate", "0.0%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.processed_results:
            max_score = max([r["total_score"] for r in st.session_state.processed_results if r["success"]], default=0)
            st.metric("Highest Score", f"{max_score:.1f}")
        else:
            st.metric("Highest Score", "0.0")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("System Status", "🟢 Online")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    
    if st.session_state.processed_results:
        recent_results = st.session_state.processed_results[-10:]
        
        for result in reversed(recent_results):
            if result["success"]:
                st.markdown(f"""
                <div class="result-card">
                    <h4>✅ {result['student_id']}</h4>
                    <p><strong>Score:</strong> {result['total_score']} | 
                       <strong>Percentage:</strong> {result['total_percentage']:.1f}% | 
                       <strong>Time:</strong> {result.get('processing_time', 0):.2f}s</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-card" style="border-left-color: #dc3545;">
                    <h4>❌ {result['student_id']}</h4>
                    <p><strong>Error:</strong> {result.get('error', 'Unknown error')}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-message">
            <h4>No OMR sheets processed yet</h4>
            <p>Upload some sheets to get started with automated evaluation!</p>
        </div>
        """, unsafe_allow_html=True)

def show_upload_page():
    """Show upload and processing page."""
    st.header("📤 Upload & Process OMR Sheets")
    
    # Upload options
    st.markdown("""
    <div class="upload-section">
        <h3>Choose your upload method</h3>
        <p>Select how you want to upload OMR sheets for processing</p>
    </div>
    """, unsafe_allow_html=True)
    
    upload_option = st.radio(
        "Upload Method:",
        ["Upload Image File", "Use Sample OMR Sheet", "Manual Entry"],
        horizontal=True
    )
    
    if upload_option == "Upload Image File":
        st.subheader("📁 Single File Upload")
        
        uploaded_file = st.file_uploader(
            "Choose OMR Sheet Image",
            type=['jpg', 'jpeg', 'png'],
            help="Upload an image of the OMR sheet"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            st.image(uploaded_file, caption="Uploaded OMR Sheet", use_column_width=True)
            
            # Processing options
            col1, col2 = st.columns(2)
            with col1:
                student_id = st.text_input("Student ID", value=f"student_{len(st.session_state.processed_results) + 1}")
            with col2:
                sheet_version = st.selectbox("Sheet Version", ["demo_v1", "v1", "v2", "v3"])
            
            if st.button("🚀 Process OMR Sheet", type="primary", use_container_width=True):
                with st.spinner("Processing OMR sheet..."):
                    # Generate unique student answers based on student ID
                    import random
                    random.seed(hash(student_id))  # Use student ID as seed for consistent results
                    
                    student_answers = []
                    for i in range(100):
                        # Generate random answers for each student
                        if random.random() < 0.8:  # 80% chance of answering
                            answer_choice = random.choice([0, 1, 2, 3])  # A, B, C, D
                            student_answers.append([answer_choice])
                        else:
                            student_answers.append([])  # No answer
                    
                    result = simulate_omr_processing(student_answers, st.session_state.answer_key, student_id)
                    st.session_state.processed_results.append(result)
                    
                    if result["success"]:
                        st.success("✅ OMR sheet processed successfully!")
                        display_processing_result(result)
                    else:
                        st.error(f"❌ Processing failed: {result['error']}")
    
    elif upload_option == "Use Sample OMR Sheet":
        st.subheader("🎯 Sample OMR Sheet")
        
        st.markdown("""
        <div class="info-message">
            <h4>Demo Mode</h4>
            <p>This will create and process a sample OMR sheet for demonstration purposes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input("Student ID", value=f"demo_student_{len(st.session_state.processed_results) + 1}")
        with col2:
            sheet_version = st.selectbox("Sheet Version", ["demo_v1", "v1", "v2", "v3"])
        
        if st.button("🎲 Generate & Process Sample OMR Sheet", type="primary", use_container_width=True):
            with st.spinner("Generating sample OMR sheet..."):
                # Create sample image
                sample_image = create_sample_omr_image()
                
                # Display sample image
                st.image(sample_image, caption="Generated Sample OMR Sheet", use_column_width=True)
                
                # Generate unique student answers based on student ID
                import random
                random.seed(hash(student_id))  # Use student ID as seed for consistent results
                
                student_answers = []
                for i in range(100):
                    # Generate random answers for each student
                    if random.random() < 0.75:  # 75% chance of answering
                        answer_choice = random.choice([0, 1, 2, 3])  # A, B, C, D
                        student_answers.append([answer_choice])
                    else:
                        student_answers.append([])  # No answer
                
                result = simulate_omr_processing(student_answers, st.session_state.answer_key, student_id)
                st.session_state.processed_results.append(result)
                
                if result["success"]:
                    st.success("✅ Sample OMR sheet processed successfully!")
                    display_processing_result(result)
                else:
                    st.error(f"❌ Processing failed: {result['error']}")
    
    elif upload_option == "Manual Entry":
        st.subheader("✏️ Manual Answer Entry")
        
        st.markdown("""
        <div class="info-message">
            <h4>Manual Entry Mode</h4>
            <p>Enter student answers manually for testing and demonstration purposes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input("Student ID", value=f"manual_student_{len(st.session_state.processed_results) + 1}")
        with col2:
            sheet_version = st.selectbox("Sheet Version", ["demo_v1", "v1", "v2", "v3"])
        
        # Manual answer entry
        st.subheader("Enter Student Answers")
        
        # Create answer entry form
        student_answers = []
        for i in range(20):  # First 20 questions for demo
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
            
            with col1:
                st.write(f"Q{i+1}")
            
            with col2:
                a_selected = st.checkbox("A", key=f"q{i+1}_a")
            with col3:
                b_selected = st.checkbox("B", key=f"q{i+1}_b")
            with col4:
                c_selected = st.checkbox("C", key=f"q{i+1}_c")
            with col5:
                d_selected = st.checkbox("D", key=f"q{i+1}_d")
            
            # Convert to answer format
            answer = []
            if a_selected: answer.append(0)
            if b_selected: answer.append(1)
            if c_selected: answer.append(2)
            if d_selected: answer.append(3)
            
            student_answers.append(answer)
        
        if st.button("🚀 Process Manual Answers", type="primary", use_container_width=True):
            with st.spinner("Processing answers..."):
                result = simulate_omr_processing(student_answers, st.session_state.answer_key, student_id)
                st.session_state.processed_results.append(result)
                
                if result["success"]:
                    st.success("✅ Answers processed successfully!")
                    display_processing_result(result)
                else:
                    st.error(f"❌ Processing failed: {result['error']}")

def display_processing_result(result):
    """Display processing result."""
    if result["success"]:
        st.markdown(f"""
        <div class="result-card">
            <h3>📊 Processing Result</h3>
            <p><strong>Student ID:</strong> {result['student_id']}</p>
            <p><strong>Total Score:</strong> {result['total_score']}</p>
            <p><strong>Percentage:</strong> {result['total_percentage']:.1f}%</p>
            <p><strong>Processing Time:</strong> {result.get('processing_time', 0):.2f}s</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show subject-wise scores
        if "subject_scores" in result:
            st.subheader("Subject-wise Scores")
            subject_data = []
            for subject in result["subject_scores"]:
                subject_data.append({
                    "Subject": subject["subject"],
                    "Correct": subject["correct"],
                    "Total": subject["total"],
                    "Score": subject["score"],
                    "Percentage": f"{subject['percentage']:.1f}%"
                })
            
            df = pd.DataFrame(subject_data)
            st.dataframe(df, use_container_width=True)
            
            # Visualization
            fig = px.bar(df, x='Subject', y='Percentage', title='Subject-wise Performance')
            st.plotly_chart(fig, use_container_width=True)
            
            # Show detailed answer analysis
            with st.expander("🔍 Detailed Answer Analysis"):
                st.info("💡 **Note**: This is a simulation. In a real implementation, answers would be extracted from the uploaded OMR image.")
                
                # Show some sample answers for transparency
                st.write("**Sample Answers (First 20 questions):**")
                sample_answers = []
                for i in range(min(20, len(result.get('student_answers', [])))):
                    answer = result.get('student_answers', [])[i] if i < len(result.get('student_answers', [])) else []
                    if isinstance(answer, list) and len(answer) > 0:
                        answer_str = ''.join(['A' if x==0 else 'B' if x==1 else 'C' if x==2 else 'D' for x in answer])
                    else:
                        answer_str = "No answer"
                    sample_answers.append(f"Q{i+1}: {answer_str}")
                
                col1, col2 = st.columns(2)
                with col1:
                    for i in range(0, len(sample_answers), 2):
                        if i < len(sample_answers):
                            st.write(sample_answers[i])
                with col2:
                    for i in range(1, len(sample_answers), 2):
                        if i < len(sample_answers):
                            st.write(sample_answers[i])

def show_results_page():
    """Show results and analytics page."""
    st.header("📊 Results & Analytics")
    
    if not st.session_state.processed_results:
        st.info("No results available. Process some OMR sheets first.")
        return
    
    # Filter successful results
    successful_results = [r for r in st.session_state.processed_results if r["success"]]
    
    if not successful_results:
        st.warning("No successful results to display.")
        return
    
    # Display statistics
    st.subheader("📈 Overall Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Processed", len(successful_results))
    
    with col2:
        avg_score = np.mean([r["total_score"] for r in successful_results])
        st.metric("Average Score", f"{avg_score:.1f}")
    
    with col3:
        max_score = max([r["total_score"] for r in successful_results])
        st.metric("Highest Score", f"{max_score:.1f}")
    
    with col4:
        min_score = min([r["total_score"] for r in successful_results])
        st.metric("Lowest Score", f"{min_score:.1f}")
    
    # Results table
    st.subheader("📋 Detailed Results")
    
    # Prepare data for display
    results_data = []
    for result in successful_results:
        results_data.append({
            "Student ID": result["student_id"],
            "Total Score": result["total_score"],
            "Percentage": f"{result['total_percentage']:.1f}%",
            "Processing Time": f"{result.get('processing_time', 0):.2f}s",
            "Timestamp": result["timestamp"]
        })
    
    df = pd.DataFrame(results_data)
    st.dataframe(df, use_container_width=True)
    
    # Visualizations
    st.subheader("📊 Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution
        fig = px.histogram(df, x="Total Score", title="Score Distribution", nbins=20)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Percentage distribution
        percentages = [r["total_percentage"] for r in successful_results]
        fig = px.histogram(x=percentages, title="Percentage Distribution", nbins=20)
        st.plotly_chart(fig, use_container_width=True)
    
    # Export functionality
    st.subheader("📤 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export as CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"omr_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export as Excel"):
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False)
            excel_data = excel_buffer.getvalue()
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name=f"omr_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

def show_answer_keys_page():
    """Show answer keys management page."""
    st.header("🔑 Answer Keys Management")
    
    # Upload options
    st.markdown("""
    <div class="upload-section">
        <h3>Manage Answer Keys</h3>
        <p>Upload answer key files or create them manually for different exam versions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer key management options
    answer_key_option = st.radio(
        "Answer Key Management:",
        ["Upload Answer Key File", "Create Manual Answer Key", "View Current Answer Key", "Use Sample Answer Key"],
        horizontal=True
    )
    
    if answer_key_option == "Upload Answer Key File":
        st.subheader("📁 Upload Answer Key File")
        
        uploaded_file = st.file_uploader(
            "Choose Answer Key File",
            type=['json', 'txt', 'csv', 'xlsx', 'xls'],
            help="Upload a JSON, TXT, CSV, or Excel file containing the answer key"
        )
        
        if uploaded_file is not None:
            try:
                # Process uploaded file
                if uploaded_file.type == "application/json":
                    answer_key_data = json.load(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    # Try to parse as JSON first
                    content = uploaded_file.read().decode('utf-8')
                    try:
                        answer_key_data = json.loads(content)
                    except:
                        # If not JSON, create a simple format
                        st.warning("TXT file detected. Please ensure it contains valid JSON format.")
                        return
                elif uploaded_file.type == "text/csv":
                    # Convert CSV to answer key format
                    df = pd.read_csv(uploaded_file)
                    answer_key_data = convert_csv_to_answer_key(df)
                elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
                    # Convert Excel to answer key format
                    try:
                        # Try to import openpyxl first
                        import openpyxl
                        df = pd.read_excel(uploaded_file)
                        answer_key_data = convert_excel_to_answer_key(df)
                    except ImportError as e:
                        if "openpyxl" in str(e):
                            st.error("""
                            ❌ **Excel support requires openpyxl library**
                            
                            **Immediate Solutions:**
                            1. **Redeploy with Fixed Requirements**: The requirements file has been updated with fixed versions
                            2. **Use CSV Instead**: Convert your Excel file to CSV format (same functionality)
                            3. **Manual Entry**: Use the manual answer key creation option
                            4. **Use Basic Version**: Deploy `streamlit_cloud_basic.py` instead
                            """)
                            
                            # Provide CSV conversion option
                            st.markdown("### 🔄 **Quick CSV Conversion Option**")
                            st.info("""
                            **Convert your Excel file to CSV:**
                            1. Open your Excel file
                            2. File → Save As → CSV (Comma Separated Values)
                            3. Upload the CSV file instead
                            4. Use the same column format: Subject, Question, Answer
                            """)
                            
                            # Show CSV format example
                            st.markdown("### 📋 **CSV Format Example**")
                            csv_example = """Subject,Question,Answer
Mathematics,1,A
Mathematics,2,B
Physics,11,C
Physics,12,D"""
                            st.code(csv_example, language="csv")
                            
                            return
                        else:
                            raise e
                    except Exception as e:
                        st.error(f"❌ Error reading Excel file: {str(e)}")
                        st.info("💡 **Tip**: Try converting your Excel file to CSV format or use manual entry.")
                        return
                else:
                    st.error("Unsupported file type. Please upload JSON, TXT, CSV, or Excel files.")
                    return
                
                # Validate and set answer key
                if validate_answer_key(answer_key_data):
                    st.session_state.answer_key = answer_key_data
                    st.success("✅ Answer key uploaded successfully!")
                    
                    # Show detailed subject information
                    st.info(f"📚 **Processed Subjects:** {len(answer_key_data['subjects'])}")
                    for subject_name, subject_data in answer_key_data["subjects"].items():
                        st.write(f"• **{subject_name}:** {len(subject_data['questions'])} questions")
                    
                    display_answer_key_summary(answer_key_data)
                else:
                    st.error("❌ Invalid answer key format. Please check your file structure.")
                    
                    # Show debug information
                    if answer_key_data and "subjects" in answer_key_data:
                        st.warning(f"⚠️ **Debug Info:** Found {len(answer_key_data['subjects'])} subjects")
                        for subject_name, subject_data in answer_key_data["subjects"].items():
                            st.write(f"• {subject_name}: {len(subject_data.get('questions', []))} questions, {len(subject_data.get('answers', []))} answers")
                    
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    elif answer_key_option == "Create Manual Answer Key":
        st.subheader("✏️ Create Manual Answer Key")
        
        st.markdown("""
        <div class="info-message">
            <h4>Manual Answer Key Creation</h4>
            <p>Create a custom answer key by specifying subjects, question ranges, and correct answers.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer key version
        version = st.text_input("Answer Key Version", value="custom_v1", help="Enter a unique version identifier")
        
        # Subject management
        st.subheader("📚 Subject Configuration")
        
        if 'manual_subjects' not in st.session_state:
            st.session_state.manual_subjects = [{"name": "Mathematics", "start": 1, "end": 20, "answers": "A" * 20}]
        
        # Add/remove subjects
        col1, col2 = st.columns([3, 1])
        with col1:
            new_subject = st.text_input("Add New Subject", placeholder="e.g., Physics")
        with col2:
            if st.button("➕ Add Subject"):
                if new_subject:
                    st.session_state.manual_subjects.append({
                        "name": new_subject,
                        "start": 1,
                        "end": 20,
                        "answers": "A" * 20
                    })
                    st.rerun()
        
        # Display and edit subjects
        for i, subject in enumerate(st.session_state.manual_subjects):
            with st.expander(f"📖 {subject['name']} (Questions {subject['start']}-{subject['end']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    subject['name'] = st.text_input(f"Subject Name {i+1}", value=subject['name'], key=f"name_{i}")
                with col2:
                    subject['start'] = st.number_input(f"Start Question {i+1}", value=subject['start'], min_value=1, key=f"start_{i}")
                with col3:
                    subject['end'] = st.number_input(f"End Question {i+1}", value=subject['end'], min_value=subject['start'], key=f"end_{i}")
                
                # Answer pattern
                num_questions = subject['end'] - subject['start'] + 1
                answer_pattern = st.text_input(
                    f"Answer Pattern {i+1}",
                    value=subject['answers'][:num_questions],
                    max_chars=num_questions,
                    help=f"Enter {num_questions} answers (A, B, C, D) for questions {subject['start']}-{subject['end']}"
                )
                
                if len(answer_pattern) == num_questions and all(c in 'ABCD' for c in answer_pattern.upper()):
                    subject['answers'] = answer_pattern.upper()
                else:
                    st.warning(f"Please enter exactly {num_questions} answers using A, B, C, or D")
                
                # Remove subject button
                if st.button(f"🗑️ Remove {subject['name']}", key=f"remove_{i}"):
                    st.session_state.manual_subjects.pop(i)
                    st.rerun()
        
        # Create answer key
        if st.button("🚀 Create Answer Key", type="primary", use_container_width=True):
            try:
                answer_key_data = create_manual_answer_key(version, st.session_state.manual_subjects)
                st.session_state.answer_key = answer_key_data
                st.success("✅ Manual answer key created successfully!")
                display_answer_key_summary(answer_key_data)
            except Exception as e:
                st.error(f"❌ Error creating answer key: {str(e)}")
    
    elif answer_key_option == "View Current Answer Key":
        st.subheader("👁️ Current Answer Key")
        
        answer_key = st.session_state.answer_key
        if answer_key:
            st.write(f"**Version:** {answer_key['version']}")
            st.write(f"**Subjects:** {', '.join(answer_key['subjects'].keys())}")
            
            # Show answer key structure
            with st.expander("View Answer Key Details"):
                st.json(answer_key)
            
            st.subheader("Answer Key Statistics")
            
            # Calculate statistics
            total_questions = sum(len(subject["questions"]) for subject in answer_key["subjects"].values())
            st.metric("Total Questions", total_questions)
            
            for subject_name, subject_data in answer_key["subjects"].items():
                st.write(f"**{subject_name}:** {len(subject_data['questions'])} questions")
        else:
            st.info("No answer key loaded. Please upload or create one.")
    
    elif answer_key_option == "Use Sample Answer Key":
        st.subheader("🎯 Sample Answer Key")
        
        st.markdown("""
        <div class="info-message">
            <h4>Demo Answer Key</h4>
            <p>Load a pre-configured sample answer key for testing and demonstration purposes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        sample_version = st.selectbox("Sample Version", ["demo_v1", "demo_v2", "demo_v3"])
        
        if st.button("🎲 Load Sample Answer Key", type="primary", use_container_width=True):
            sample_answer_key = create_sample_answer_key(sample_version)
            st.session_state.answer_key = sample_answer_key
            st.success("✅ Sample answer key loaded successfully!")
            display_answer_key_summary(sample_answer_key)

def show_about_page():
    """Show about page."""
    st.header("ℹ️ About OMR Evaluation System")
    
    st.markdown("""
    ## 🎯 Overview
    
    The **Automated OMR Evaluation & Scoring System** is a comprehensive solution for processing and evaluating OMR (Optical Mark Recognition) sheets. This cloud-optimized version is designed to work without heavy dependencies.
    
    ## ✨ Key Features
    
    - **📸 Image Upload Support**: Process OMR sheets uploaded as images
    - **🎯 Sample Data Generation**: Create sample OMR sheets for testing
    - **✏️ Manual Entry**: Enter answers manually for testing
    - **📊 Real-time Analytics**: Live dashboard with comprehensive reporting
    - **📥 Export Capabilities**: CSV and Excel export formats
    - **☁️ Cloud Optimized**: Works on Streamlit Cloud without OpenCV
    
    ## 🛠️ Technical Stack
    
    - **Frontend**: Streamlit
    - **Image Processing**: PIL (Python Imaging Library)
    - **Data Processing**: Pandas, NumPy
    - **Visualization**: Plotly
    - **Cloud**: Streamlit Cloud
    
    ## 📊 Performance
    
    - **Processing Speed**: Instant for manual entry
    - **Accuracy**: Simulated processing for demonstration
    - **Cloud Compatibility**: Optimized for Streamlit Cloud
    - **User Friendly**: Simple interface for teachers
    
    ## 🚀 Getting Started
    
    1. **Upload OMR Sheets**: Use the upload page to process images or manual entry
    2. **View Results**: Check processing status and view detailed results
    3. **Export Data**: Download results as CSV or Excel files
    4. **Manage Answer Keys**: Configure answer keys for different exam versions
    
    ---
    
    **Built with ❤️ for automated education assessment**
    """)

if __name__ == "__main__":
    main()

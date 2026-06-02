import streamlit as st
import cv2
import pandas as pd
from ultralytics import YOLO
import database
import time

# Initialize database
database.init_db()

# Page Config
st.set_page_config(page_title="Garbage Sorting AI", page_icon="♻️", layout="wide")

# Custom Modern CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Hide default Streamlit headers/footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Glassmorphism Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Primary Button Styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(45deg, #00C9FF, #92FE9D);
        color: black;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button[kind="primary"]:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 201, 255, 0.4);
    }
    
    /* Sidebar modern look */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("♻️ Smart Bin AI")
page = st.sidebar.radio("Navigation", ["Live Camera", "Analytics Dashboard"])

@st.cache_resource
def load_model():
    # Load custom YOLO model
    try:
        return YOLO("best.pt")
    except Exception as e:
        st.error(f"Error loading custom model: {e}. Falling back to default.")
        return YOLO("yolov8n.pt")

model = load_model()

if page == "Live Camera":
    st.title("🎥 Live Garbage Detection")
    st.markdown("Show a piece of garbage to the webcam to classify it.")
    
    # We use a session state to control the webcam loop
    if 'run_webcam' not in st.session_state:
        st.session_state.run_webcam = False

    col1, col2 = st.columns([3, 1])
    
    with col1:
        stframe = st.empty()
    
    with col2:
        st.markdown("### Controls")
        start_button = st.button("Start Camera", type="primary")
        stop_button = st.button("Stop Camera")
        
        st.markdown("### Current Session Stats")
        stats_placeholder = st.empty()

    if start_button:
        st.session_state.run_webcam = True
    if stop_button:
        st.session_state.run_webcam = False

    if st.session_state.run_webcam:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        session_counts = {}
        counted_ids = set()
        sorting_line_x = 320 # Vertical line at X=320 (middle)
        servo_alert_active = False
        servo_alert_end_time = 0
        activated_class = ""
        
        while st.session_state.run_webcam:
            success, frame = cap.read()
            if not success:
                st.error("Failed to access webcam.")
                break
                
            height, width, _ = frame.shape
            line_x = min(sorting_line_x, width - 50)
                
            # Run YOLO inference
            results = model.track(frame, persist=True, verbose=False)
            annotated_frame = results[0].plot()
            
            # Log detections only when they cross the virtual line
            if results[0].boxes is not None and len(results[0].boxes) > 0 and results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                track_ids = results[0].boxes.id.int().cpu().numpy()
                class_ids = results[0].boxes.cls.int().cpu().numpy()
                
                for box, track_id, cls_id in zip(boxes, track_ids, class_ids):
                    # Calculate centroid
                    x1, y1, x2, y2 = box
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)
                    
                    # Draw centroid
                    cv2.circle(annotated_frame, (cx, cy), 5, (255, 0, 0), -1)
                    
                    class_name = model.names[cls_id]
                    
                    if cx >= line_x and track_id not in counted_ids:
                        counted_ids.add(track_id)
                        
                        # Attempt to log to database
                        if database.log_detection(class_name, track_id):
                            if class_name in session_counts:
                                session_counts[class_name] += 1
                            else:
                                session_counts[class_name] = 1
                                
                        # Trigger Servo Simulation
                        servo_alert_active = True
                        servo_alert_end_time = time.time() + 1.5
                        activated_class = class_name
            
            # Draw Vertical Virtual Sorting Line
            cv2.line(annotated_frame, (line_x, 0), (line_x, height), (255, 0, 0), 2)
            cv2.putText(annotated_frame, "Sorting Line", (line_x + 10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                        
            # Draw Flashing Servo Alert
            if servo_alert_active:
                if time.time() < servo_alert_end_time:
                    if int(time.time() * 6) % 2 == 0:
                        alert_text = f"[🔴 SERVO ACTIVATED FOR: {activated_class.upper()}]"
                        (tw, th), _ = cv2.getTextSize(alert_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                        cv2.rectangle(annotated_frame, (width//2 - tw//2 - 10, 40), (width//2 + tw//2 + 10, 40 + th + 10), (0, 0, 0), -1)
                        cv2.putText(annotated_frame, alert_text, (width//2 - tw//2, 40 + th), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                else:
                    servo_alert_active = False

            # Convert BGR to RGB for Streamlit
            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            stframe.image(rgb_frame, channels="RGB", use_container_width=True)
            
            # Update session stats UI
            with stats_placeholder.container():
                for cls, count in session_counts.items():
                    st.metric(label=cls.capitalize(), value=count)
                    
            # Small sleep to yield execution and prevent freezing
            time.sleep(0.01)
            
        cap.release()

elif page == "Analytics Dashboard":
    st.title("📊 Garbage Analytics Dashboard")
    
    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()
        
    st.markdown("### Today's Statistics")
    df_today = database.get_today_stats()
    
    if df_today.empty:
        st.info("No items sorted today yet.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(df_today.set_index("class_name"))
        with col2:
            st.dataframe(df_today, use_container_width=True)
            
    st.markdown("---")
    
    st.markdown("### All-Time Statistics")
    df_all = database.get_all_time_stats()
    
    if df_all.empty:
        st.info("No items sorted all-time.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(df_all.set_index("class_name"))
        with col2:
            st.dataframe(df_all, use_container_width=True)

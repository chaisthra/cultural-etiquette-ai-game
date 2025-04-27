import streamlit as st
import random
import time

class CulturalEtiquetteGame:
    def __init__(self):
        self.countries = {
            "Japan": {
                "greetings": ["Bow instead of handshake", "Business cards are exchanged with both hands", "Remove shoes when entering homes"],
                "dining": ["Slurping noodles is acceptable and shows appreciation", "Don't stick chopsticks upright in rice", "It's polite to pour drinks for others, not yourself"],
                "business": ["Punctuality is extremely important", "Business cards should be received with both hands", "Group consensus is valued over individual decisions"]
            },
            "India": {
                "greetings": ["The Namaste gesture is a common greeting", "Physical contact between genders may be limited", "Elders are greeted first as a sign of respect"],
                "dining": ["Eating with right hand is traditional", "Refusing food can be seen as impolite", "Sharing food from your plate is considered inappropriate"],
                "business": ["Relationships before business transactions", "Hierarchical structures are important", "Decisions may take time as consensus is valued"]
            },
            "Brazil": {
                "greetings": ["Kisses on both cheeks are common", "Handshakes are firm and long", "Personal space is smaller than in Western countries"],
                "dining": ["Being late to dinner is acceptable", "Keep hands visible during meals", "The host serves food to guests first"],
                "business": ["Building personal relationships is crucial", "Meetings may not follow strict schedules", "Direct criticism is avoided in public settings"]
            },
            "Saudi Arabia": {
                "greetings": ["Same-sex handshakes are common", "Greet elders first", "Physical contact between unrelated men and women is avoided"],
                "dining": ["Eat with right hand only", "Declining coffee or tea may be impolite", "Praise the food during the meal"],
                "business": ["Building trust takes time and multiple meetings", "Negotiations may be lengthy", "Decision-making is often hierarchical"]
            },
            "Germany": {
                "greetings": ["Punctuality is highly valued", "Handshakes are firm and direct", "Use formal titles until invited to use first names"],
                "dining": ["Keep hands visible on the table", "Finish everything on your plate", "Don't start eating until the host says 'Guten Appetit'"],
                "business": ["Direct communication is appreciated", "Meetings follow clear agendas", "Decisions are often made methodically with supporting data"]
            }
        }
        
        self.scenarios = [
            "You've been invited to a business dinner in {country}. What would be appropriate etiquette?",
            "You're meeting a potential business partner in {country} for the first time. How should you greet them?",
            "You're attending a formal meeting in {country}. What cultural norms should you be aware of?",
            "You've been invited to someone's home for a meal in {country}. What should you do?",
            "You need to decline an offer in {country} without causing offense. How would you approach this?"
        ]
        
        self.feedback_positive = [
            "Excellent choice! That shows cultural awareness and respect.",
            "Perfect! You've demonstrated good understanding of local customs.",
            "Well done! Your cultural intelligence is impressive.",
            "Great job! That would be well-received in this culture.",
            "Correct! That's exactly what would be expected in this situation."
        ]
        
        self.feedback_negative = [
            "That might cause some discomfort in this cultural context.",
            "This approach could be seen as inappropriate in this setting.",
            "This wouldn't align with local expectations.",
            "This might be misinterpreted in this cultural context.",
            "This could create an awkward situation based on local customs."
        ]
        
        # Game state
        self.score = 0
        self.round = 0
        self.max_rounds = 5
        self.current_country = None
        self.current_scenario = None
        self.current_options = []
        self.correct_option = None
        self.game_over = False
        self.player_name = ""
        self.difficulty = "medium"
        self.time_limit = 30  # seconds
        self.timer_start = None
        
    def start_game(self):
        self.score = 0
        self.round = 0
        self.game_over = False
        self.next_round()
        
    def next_round(self):
        if self.round >= self.max_rounds:
            self.game_over = True
            return
            
        self.round += 1
        self.current_country = random.choice(list(self.countries.keys()))
        scenario_template = random.choice(self.scenarios)
        self.current_scenario = scenario_template.format(country=self.current_country)
        
        # Generate options
        category = random.choice(["greetings", "dining", "business"])
        correct_practices = self.countries[self.current_country][category]
        incorrect_practices = []
        
        # Get incorrect practices from other countries
        for country, categories in self.countries.items():
            if country != self.current_country:
                incorrect_practices.extend(categories[category])
        
        # Select correct option and some incorrect ones
        self.correct_option = random.choice(correct_practices)
        possible_incorrect = random.sample(incorrect_practices, 3)
        
        # Create the options list with correct and incorrect answers
        self.current_options = possible_incorrect + [self.correct_option]
        random.shuffle(self.current_options)
        
        # Start timer
        self.timer_start = time.time()
        
    def check_answer(self, selected_option):
        time_taken = time.time() - self.timer_start
        time_factor = max(0, 1 - (time_taken / (self.time_limit * 2)))
        
        if selected_option == self.correct_option:
            # Base points + time bonus
            points = 100 + int(100 * time_factor)
            self.score += points
            feedback = random.choice(self.feedback_positive)
            return True, feedback, points
        else:
            feedback = random.choice(self.feedback_negative)
            return False, feedback, 0

# Country color themes
country_themes = {
    "Japan": {"primary": "#D0312D", "secondary": "#F3F3F3", "accent": "#2B4162"},
    "India": {"primary": "#FF9933", "secondary": "#FFFFFF", "accent": "#138808"},
    "Brazil": {"primary": "#009c3b", "secondary": "#ffdf00", "accent": "#002776"},
    "Saudi Arabia": {"primary": "#006C35", "secondary": "#FFFFFF", "accent": "#8A1538"},
    "Germany": {"primary": "#000000", "secondary": "#DD0000", "accent": "#FFCE00"}
}

def main():
    st.set_page_config(
        page_title="AI Cultural Adaptation & Etiquette Game",
        page_icon="🌍",
        layout="wide",
    )
    
    # Set the background image first - this will apply to all screens
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://ik.imagekit.io/kr7ylbnd3/culture/Cultural%20Diversity%20Education%20Presentation%20In%20Colorful%20Beige%20Illustrated%20Style.png?updatedAt=1745791222682');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Add a semi-transparent overlay to improve readability of content */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(44, 62, 80, 0.3); /* Semi-transparent overlay */
        z-index: -1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize game in session state if not exists
    if 'game' not in st.session_state:
        st.session_state.game = CulturalEtiquetteGame()
        st.session_state.show_welcome = True
        st.session_state.show_game = False
        st.session_state.show_results = False
        st.session_state.last_feedback = None
        st.session_state.answer_status = None
        st.session_state.points_earned = 0
    
    game = st.session_state.game

    # Get current country theme colors or default colors
    theme = {"primary": "#4527A0", "secondary": "#7B1FA2", "accent": "#1E88E5"}
    if hasattr(game, 'current_country') and game.current_country in country_themes:
        theme = country_themes[game.current_country]
    
    # Ultra-Responsive Design for All Screen Sizes
    st.markdown("""
    <style>
    /* Responsive viewport containers */
    .stApp {
        height: 100vh !important;
        overflow: hidden !important;
    }

    .main .block-container {
        max-width: 100% !important;
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        overflow: hidden !important;
    }

    /* Ultra-compact welcome screen */
    .main-header {
        font-size: clamp(1.5em, 4vw, 2.5em) !important;
        margin-bottom: 0 !important;
        padding: 5px 0 !important;
    }

    .welcome-container {
        padding: 8px !important;
        margin-bottom: 5px !important;
        max-height: none !important;
        overflow: visible !important;
    }

    .welcome-container-text {
        font-size: clamp(0.8em, 2vw, 1.1em) !important;
        margin-bottom: 5px !important;
        line-height: 1.3 !important;
    }

    /* Ultra-compact game screen */
    .score-display {
        font-size: clamp(0.7em, 2vw, 1.1em) !important;
        margin: 2px 0 !important;
        padding: 2px !important;
    }

    .scenario-card {
        padding: 10px !important;
        margin-bottom: 5px !important;
    }

    .country-header {
        font-size: clamp(1em, 2.5vw, 1.5em) !important;
        margin-bottom: 5px !important;
    }

    .scenario-text {
        font-size: clamp(0.8em, 2vw, 1.1em) !important;
        margin-bottom: 5px !important;
        line-height: 1.3 !important;
    }

    .option-button {
        padding: 6px !important;
        margin: 3px 0 !important;
        font-size: clamp(0.8em, 2vw, 1em) !important;
    }

    /* Compact feedback */
    .feedback-positive, .feedback-negative {
        padding: 5px !important;
        margin: 5px 0 !important;
        font-size: clamp(0.7em, 1.8vw, 0.9em) !important;
    }

    /* Make images and fixed elements responsive */
    img, svg {
        max-width: 100% !important;
        height: auto !important;
    }

    /* Compactify results screen */
    .results-container {
        padding: 8px !important;
        margin: 5px 0 !important;
    }

    .results-container div {
        margin-bottom: 5px !important;
    }

    .results-header {
        font-size: clamp(1.3em, 3vw, 1.8em) !important;
        margin-bottom: 5px !important;
    }

    .results-score, .results-level {
        font-size: clamp(1em, 2.5vw, 1.4em) !important;
        margin: 5px 0 !important;
    }

    /* Smaller medal */
    div[style*="width: 120px; height: 120px"] {
        width: clamp(60px, 15vw, 100px) !important;
        height: clamp(60px, 15vw, 100px) !important;
        margin: 8px auto !important;
    }

    div[style*="width: 120px; height: 120px"] span {
        font-size: clamp(1.2em, 3vw, 1.8em) !important;
    }

    /* Ensure all content fits in view */
    .streamlit-expanderHeader {
        padding: 3px !important;
    }

    div[data-testid="stExpander"] {
        margin-top: 3px !important;
        margin-bottom: 3px !important;
    }

    /* Force vertical layout on small screens */
    @media (max-width: 768px) {
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        
        div[data-testid="stVerticalBlock"] {
            gap: 3px !important;
        }
        
        div[data-testid="stForm"] {
            padding: 0 !important;
        }
        
        /* Hide or collapse non-essential elements on very small screens */
        @media (max-height: 600px) {
            .streamlit-expanderContent {
                max-height: 100px !important;
                overflow-y: auto !important;
            }
            
            /* Hide certain elements if screen is too small */
            div.cultural-tip, div[data-testid="stExpander"] {
                display: none !important;
            }
        }
    }

    /* Adjust input elements */
    .stTextInput > div, .stSelectbox > div {
        margin-bottom: 0 !important;
    }

    /* Make buttons super compact */
    .stButton > button {
        padding: clamp(5px, 1.5vw, 10px) clamp(8px, 2vw, 15px) !important;
        font-size: clamp(0.8em, 2vw, 1em) !important;
    }

    /* Hide Streamlit branding for more space */
    .reportview-container .main footer {
        display: none !important;
    }

    footer {
        display: none !important;
    }

    /* Force all elements to stay in viewport */
    .stButton, .stTextInput, .stSelectbox, .stSlider {
        transform: scale(0.95);
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    /* Make progress bars thinner */
    .stProgress > div > div {
        height: 5px !important;
    }

    .timer-bar {
        height: 5px !important;
        margin-bottom: 5px !important;
    }

    /* Enhanced feedback boxes with animation */
    .feedback-positive, .feedback-negative {
        padding: 12px !important;
        margin: 10px 0 !important;
        border-radius: 10px !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.15) !important;
        font-weight: bold !important;
        transform: scale(1);
        animation: pop-in 0.5s ease-out;
        border: 2px solid white;
    }

    .feedback-positive {
        background: linear-gradient(135deg, #a8e063 0%, #56ab2f 100%) !important;
        color: white !important;
    }

    .feedback-negative {
        background: linear-gradient(135deg, #ff9966 0%, #ff5e62 100%) !important;
        color: white !important;
    }

    @keyframes pop-in {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    /* Enhanced Cultural AI Assistant */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 10px 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        border: 2px solid white !important;
    }

    .streamlit-expanderContent {
        border: 2px solid #764ba2 !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }

    /* Cultural tip with more visual appeal */
    .cultural-tip {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1) !important;
        border-top: 5px solid #667eea !important;
    }

    .cultural-tip h4 {
        color: #4a47a3 !important;
        margin-top: 0 !important;
        border-bottom: 2px solid #764ba2 !important;
        padding-bottom: 5px !important;
    }

    /* Cultural facts cards with enhanced styling */
    .cultural-facts-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(240,248,255,0.9) 100%) !important;
        border-radius: 10px !important;
        padding: 12px !important;
        margin: 10px 0 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15) !important;
        border-left: 5px solid #6a11cb !important;
        border-top: 1px solid rgba(255,255,255,0.8) !important;
        border-right: 1px solid rgba(255,255,255,0.8) !important;
        border-bottom: 1px solid rgba(255,255,255,0.8) !important;
    }

    .cultural-facts-card h4 {
        background: linear-gradient(90deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 0 !important;
    }

    /* Custom coloring for each category */
    .greetings-card { border-left-color: #FF6B6B !important; }
    .greetings-card h4 { background: linear-gradient(90deg, #FF6B6B, #FF9E80); -webkit-background-clip: text; }

    .dining-card { border-left-color: #36D1DC !important; }
    .dining-card h4 { background: linear-gradient(90deg, #36D1DC, #5B86E5); -webkit-background-clip: text; }

    .business-card { border-left-color: #8A2387 !important; }
    .business-card h4 { background: linear-gradient(90deg, #8A2387, #E94057); -webkit-background-clip: text; }

    /* Add CSS for Quick Cultural Facts container to make it stand out */
    .quick-facts-container {
        background: linear-gradient(135deg, rgba(25,118,210,0.85) 0%, rgba(66,39,90,0.85) 100%);
        border-radius: 15px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        border: 2px solid rgba(255,255,255,0.5);
        backdrop-filter: blur(5px);
        position: relative;
        overflow: hidden;
    }

    /* Add decorative elements */
    .quick-facts-container::before {
        content: "";
        position: absolute;
        top: -10px;
        right: -10px;
        width: 40px;
        height: 40px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        z-index: 0;
    }

    .quick-facts-container::after {
        content: "";
        position: absolute;
        bottom: -20px;
        left: -20px;
        width: 80px;
        height: 80px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        z-index: 0;
    }

    /* Make category cards stand out more against the container */
    .cultural-facts-card {
        background: rgba(255,255,255,0.95) !important;
        margin: 10px 0 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
        transform: translateZ(0);
        transition: transform 0.2s;
    }

    .cultural-facts-card:hover {
        transform: translateY(-3px) scale(1.01);
    }

    /* Enhance category headings */
    .cultural-facts-card h4 {
        font-weight: bold !important;
        padding: 8px !important;
        margin: 0 !important;
        border-bottom: 2px solid rgba(0,0,0,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Welcome Screen
    if st.session_state.show_welcome:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='main-header'>🌍 Cultural Etiquette AI Challenge 🌍</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class='welcome-container'>
                <div class='welcome-container-text'>
                Test your cultural IQ in our AI challenge! Navigate social situations across cultures.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            name_col, difficulty_col = st.columns([2, 1])
            with name_col:
                st.text_input("Name", key="player_name_input", label_visibility="collapsed", placeholder="Enter your name")
            with difficulty_col:
                difficulty = st.selectbox(
                    "Difficulty",
                    options=["easy", "medium", "hard"],
                    index=1,
                    label_visibility="collapsed"
                )
            
            # Simplified "How to Play" section
            with st.expander("How to Play"):
                st.markdown("""
                <ul style='padding-left: 20px; margin: 5px;'>
                    <li><strong>Scenarios:</strong> Cultural situations from different countries</li>
                    <li><strong>Choose:</strong> Select the most appropriate response</li>
                    <li><strong>Be quick:</strong> Answer quickly for bonus points</li>
                    <li><strong>Learn:</strong> Cultural tips provided throughout the game</li>
                </ul>
                """, unsafe_allow_html=True)
            
            if st.button("Start Game", key="start_button", use_container_width=True):
                if st.session_state.player_name_input:
                    game.player_name = st.session_state.player_name_input
                    game.difficulty = difficulty
                    
                    # Set time limit based on difficulty
                    if difficulty == "easy":
                        game.time_limit = 40
                        game.max_rounds = 5
                    elif difficulty == "medium":
                        game.time_limit = 30
                        game.max_rounds = 7
                    else:  # hard
                        game.time_limit = 20
                        game.max_rounds = 10
                        
                    game.start_game()
                    st.session_state.show_welcome = False
                    st.session_state.show_game = True
                    st.rerun()
                else:
                    st.warning("Please enter your name before starting the game.")
    
    # Game Screen
    elif st.session_state.show_game and not game.game_over:
        # Custom background for the specific country
        if game.current_country in country_themes:
            primary = country_themes[game.current_country]["primary"]
            secondary = country_themes[game.current_country]["secondary"]
            st.markdown(f"""
            <style>
            .stApp::after {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, {primary}40 0%, {secondary}40 100%);
                z-index: -1;
                pointer-events: none;
            }}
            </style>
            """, unsafe_allow_html=True)
        
        # Header area with score and round info
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; margin:0; padding:2px; font-size:0.8em; background:rgba(255,255,255,0.6); border-radius:5px;'>
            <span><b>Score:</b> {game.score}</span>
            <span><b>Round:</b> {game.round}/{game.max_rounds}</span>
            <span><b>Player:</b> {game.player_name}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Timer bar with enhanced animation
        time_elapsed = time.time() - game.timer_start
        time_remaining = max(0, game.time_limit - time_elapsed)
        progress = time_remaining / game.time_limit
        
        # Add pulsing effect when time is running low
        timer_class = "timer-bar"
        if time_remaining < 5:
            timer_class += " time-warning"
            st.markdown(f"""
            <style>
            .time-warning {{
                background: linear-gradient(90deg, #ff9a8b, #ff6a88);
            }}
            </style>
            """, unsafe_allow_html=True)
            
        st.markdown(f"<div class='{timer_class}'></div>", unsafe_allow_html=True)
        st.progress(progress)
        
        # Scenario card
        st.markdown(f"""
        <div class='scenario-card'>
            <div class='country-header'>🌍 {game.current_country}</div>
            <div class='scenario-text'>{game.current_scenario}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Options with enhanced styling
        for i, option in enumerate(game.current_options):
            if st.button(f"{option}", key=f"option_{i}", use_container_width=True):
                is_correct, feedback, points = game.check_answer(option)
                st.session_state.last_feedback = feedback
                st.session_state.answer_status = is_correct
                st.session_state.points_earned = points
                
                # Show feedback immediately
                if is_correct:
                    st.markdown(f"""
                    <div class='feedback-positive'>
                        <div style='display:flex; align-items:center;'>
                            <div style='font-size:1.8em; margin-right:10px;'>✅</div>
                            <div>{feedback} <span style='background:#fff3; padding:2px 5px; border-radius:4px;'>+{points} points</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='feedback-negative'>
                        <div style='display:flex; align-items:center;'>
                            <div style='font-size:1.8em; margin-right:10px;'>❌</div>
                            <div>{feedback} <div style='margin-top:5px; padding:3px; background:rgba(255,255,255,0.2); border-radius:5px;'>
                            Correct answer: {game.correct_option}</div></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Auto-advance after delay
                game.next_round()
                if game.game_over:
                    st.session_state.show_game = False
                    st.session_state.show_results = True
                st.rerun()
        
        # Display last feedback if exists
        if st.session_state.last_feedback:
            if st.session_state.answer_status:
                st.markdown(f"<div class='feedback-positive'>✅ {st.session_state.last_feedback} +{st.session_state.points_earned} points</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='feedback-negative'>❌ {st.session_state.last_feedback}</div>", unsafe_allow_html=True)
        
        # Auto-submit if time runs out
        if time_remaining <= 0:
            st.markdown("<div class='feedback-negative'>⏰ Time's up! Moving to next question.</div>", unsafe_allow_html=True)
            game.next_round()
            if game.game_over:
                st.session_state.show_game = False
                st.session_state.show_results = True
            st.rerun()
        
        # Cultural tip with enhanced UI
        with st.expander("🧠 Cultural AI Assistant"):
            st.markdown(f"""
            <div class='cultural-tip'>
                <h4>✨ AI Cultural Tip for {game.current_country}</h4>
                <p>When in {game.current_country}, being aware of local customs shows respect and helps build stronger relationships. 
                Pay attention to non-verbal communication and local etiquette around greetings, dining, and business interactions.</p>
            </div>
            
            <div class='quick-facts-container'>
                <h3 style='text-align:center; margin:10px 0; color:#fff; text-shadow:1px 1px 3px rgba(0,0,0,0.3);'>Quick Cultural Facts</h3>
            """, unsafe_allow_html=True)
            
            for category, practices in game.countries[game.current_country].items():
                st.markdown(f"""
                <div class='cultural-facts-card {category}-card'>
                    <h4>{category.capitalize()}</h4>
                    <ul style='margin-bottom:5px;'>
                """, unsafe_allow_html=True)
                
                for practice in practices:
                    st.markdown(f"<li>{practice}</li>", unsafe_allow_html=True)
                    
                st.markdown("</ul></div>", unsafe_allow_html=True)
            
            # Close the container div
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Results Screen with enhanced UI
    elif st.session_state.show_results:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='main-header'>Game Complete!</div>", unsafe_allow_html=True)
            
            # Calculate performance level
            max_possible = game.max_rounds * 200  # Maximum possible score
            performance_percent = (game.score / max_possible) * 100
            
            if performance_percent >= 80:
                performance = "Cultural Ambassador 🏆"
                message = "Exceptional cultural intelligence! You would excel in international settings."
                medal_color = "linear-gradient(45deg, #FFD700, #FFA500)"
            elif performance_percent >= 60:
                performance = "Cultural Enthusiast 🌟"
                message = "Great cultural awareness! You navigate most cultural situations well."
                medal_color = "linear-gradient(45deg, #C0C0C0, #A9A9A9)"
            elif performance_percent >= 40:
                performance = "Cultural Learner 📚"
                message = "Good start! With more practice, you'll improve your cultural adaptability."
                medal_color = "linear-gradient(45deg, #CD7F32, #8B4513)"
            else:
                performance = "Cultural Novice 🌱"
                message = "There's room for improvement. Keep learning about different cultures!"
                medal_color = "linear-gradient(45deg, #4682B4, #1E90FF)"
            
            st.markdown(f"""
            <div class='results-container'>
                <div style='text-align: center; margin-bottom: 30px;'>
                    <div style='font-size: 2.2em; margin-bottom: 15px; font-weight: bold;'>{game.player_name}</div>
                    <div class='results-score'>Final Score: {game.score}</div>
                    <div style='width: 120px; height: 120px; border-radius: 60px; background: {medal_color}; 
                         margin: 20px auto; display: flex; align-items: center; justify-content: center; 
                         box-shadow: 0 8px 15px rgba(0,0,0,0.2);'>
                        <span style='font-size: 2em; color: white;'>{int(performance_percent)}%</span>
                    </div>
                    <div class='results-level'>{performance}</div>
                    <div style='font-size: 1.1em; padding: 10px 20px; background: rgba(255,255,255,0.7); 
                         border-radius: 10px; margin: 15px 0;'>{message}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background:rgba(255,255,255,0.8); padding:8px; border-radius:10px; margin-top:10px;">
                <h4 style="margin:0; font-size:1em; text-align:center;">Cultural Intelligence Tips</h4>
                <ul style="margin:3px; padding-left:15px; font-size:0.8em;">
                    <li><b>Observe</b> customs</li>
                    <li><b>Respect</b> differences</li>
                    <li><b>Adapt</b> behavior</li>
                    <li><b>Ask</b> when unsure</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Play Again", use_container_width=True):
                    st.session_state.game = CulturalEtiquetteGame()
                    st.session_state.show_welcome = True
                    st.session_state.show_results = False
                    st.session_state.last_feedback = None
                    st.session_state.answer_status = None
                    st.rerun()
            with col2:
                if st.button("Exit Game", use_container_width=True):
                    st.session_state.show_welcome = True
                    st.session_state.show_results = False
                    st.session_state.last_feedback = None
                    st.session_state.answer_status = None
                    st.rerun()

if __name__ == "__main__":
    main()
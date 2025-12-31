
import streamlit as st
import random
from datetime import datetime
import base64
from fpdf import FPDF
import io

# --- Helper function to add styling ---
def local_css():
    st.markdown("""
    <style>
    /* Mobile-Friendly Buttons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: bold;
        border: none;
        width: 100%;
        margin-bottom: 10px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    
    /* Clean Inputs */
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    
    /* Divider */
    .section-divider {
        margin-top: 20px;
        margin-bottom: 20px;
        border-bottom: 1px solid #eee;
    }
    
    /* Corner Fireworks Animation */
    @keyframes firework-animation {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.2) rotate(10deg); opacity: 1; text-shadow: 0 0 10px #ff00de, 0 0 20px #ff00de; }
        100% { transform: scale(1); opacity: 0.8; }
    }
    .firework-corner-left {
        position: fixed;
        bottom: 20px;
        left: 20px;
        font-size: 60px;
        animation: firework-animation 2s infinite ease-in-out;
        z-index: 9999;
        pointer-events: none;
    }
    .firework-corner-right {
        position: fixed;
        bottom: 20px;
        right: 20px;
        font-size: 60px;
        animation: firework-animation 2.5s infinite ease-in-out;
        z-index: 9999;
        pointer-events: none;
    }
    </style>
    
    <!-- Corner Elements -->
    <div class="firework-corner-left">🎆</div>
    <div class="firework-corner-right">🎆</div>
    """, unsafe_allow_html=True)

# --- PDF Generation Logic (Legacy FPDF) ---
def create_pdf(selected_rights):
    # Using legacy FPDF syntax to ensure compatibility
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(76, 175, 80) # Green
    # ln=1 moves cursor to the next line
    pdf.cell(0, 20, "Official Friendship Contract", ln=1, align='C')
    
    # Metadata
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'I', 12)
    date_str = datetime.now().strftime("%Y-%m-%d")
    pdf.cell(0, 10, f"Date: {date_str}", ln=1, align='R')
    
    # Intro
    pdf.set_font("Arial", '', 12)
    intro = "This document certifies that Arsha has been granted the following rights by Idiot Scientist for the 2026 season:"
    pdf.multi_cell(0, 8, intro)
    pdf.ln(5)
    
    # Rights List
    pdf.set_font("Arial", '', 11)
    
    def sanitize(text):
        # Strip unsupported characters for Latin-1
        return text.encode('latin-1', 'replace').decode('latin-1').replace('?', '')

    for i, right in enumerate(sorted(selected_rights)):
        clean_text = right.replace("CUSTOM: ", "")
        safe_text = sanitize(clean_text)
        pdf.multi_cell(0, 7, f"{i+1}. {safe_text}")
    
    pdf.ln(15)
    
    # Signature Block
    y = pdf.get_y()
    if y > 240: 
        pdf.add_page()
        y = 20
        
    pdf.set_draw_color(0, 0, 0)
    pdf.line(20, y+10, 80, y+10)
    pdf.text(20, y+15, "Signed: Idiot Scientist")
    
    pdf.line(110, y+10, 170, y+10)
    pdf.text(110, y+15, "Signed: Arsha")
    
    # Footer
    pdf.set_y(-20)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, "Contract ID: FRIEND-2026-SECURE | Valid in all dimensions.", ln=1, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- HTML Generation (Fallback) ---
def create_html(selected_rights):
    date_str = datetime.now().strftime("%Y-%m-%d")
    items_html = ""
    for r in sorted(selected_rights):
        clean = r.replace("CUSTOM: ", "")
        items_html += f"<li>{clean}</li>"
        
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Helvetica', sans-serif; padding: 40px; color: #333; }}
            h1 {{ text-align: center; color: #4CAF50; border-bottom: 2px solid #333; padding-bottom: 10px; }}
            .date {{ text-align: right; font-style: italic; margin: 20px 0; }}
            ul {{ line-height: 1.6; }}
            .signature-box {{ margin-top: 50px; display: flex; justify-content: space-between; }}
            .sig {{ border-top: 1px solid #333; width: 45%; padding-top: 5px; }}
        </style>
    </head>
    <body onload="window.print()">
        <h1>Official Friendship Contract</h1>
        <div class="date">Date: {date_str}</div>
        <p>This document certifies that <strong>Arsha</strong> has been granted the following rights by <strong>Idiot Scientist</strong> for the 2026 season:</p>
        <ul>{items_html}</ul>
        <div class="signature-box">
            <div class="sig">Signed: Idiot Scientist</div>
            <div class="sig">Signed: Arsha</div>
        </div>
    </body>
    </html>
    """

# --- Data Generation ---
ORIGINAL_RIGHTS = [
    "Right to one (1) free coffee/bubble tea, on me.",
    "Right to vent about a buggy AI model for 10 minutes, uninterrupted.",
    "Right to send 5 anime memes in a row without apology.",
    "Right to recommend a manga I *must* read (at least 10 chapters).",
    "Right to a 'no questions asked' pep talk.",
    "Right to demand a Tic-Tac-Toe rematch.",
    "Right to share netflix password for one (n) month.",
    "Right to a cipher a pazzle night (we'll beat together).",
    "Right to ask for help on a tech stuff problem (I'll try my best).",
    "Right to choose the movie for  *Discord* movie night.",
    "Right to one (1) free ice cream.",
    "Right to declare an 'Anime Night' (subject to scheduling).",
    '''Right to a "walk in nature" voucher, redeemable on a sunny day.''',
    "Right to ask me to do anything once a week. and i have to say yes and act on it",
    "Right to one (1) 'I told you so' (use wisely).",
    "Right to skip a social event, guilt-free.",
    "Right to show me a AMV.",
    "Right to correct my spelling/grammar.",
    "Right to one (1) pun-related groan voucher.",
    "Right to ask for my 'honest opinion' (and get it).",
    "Right to a compliment on demand.",
    "Right to help get help debugging code .",
    "Right to share a 'Ghost Hunt' theory or any theory you like.",
    "Right to a 5-minute silence voucher (for quiet reading).",
    "Right to ask for my picture.",
    "Right to a 'let's plan a real-world meetup' session.",
    "Right to one (1) 'Get out of an argument free' card.",
    "Right to challenge me to a typing speed test.",
    "Right to request a specific snack.",
    "Right to a 'spoilers allowed' chat about a series we've both finished.",
    "Right to a 'no spoilers' pact for a new series.",
    "Right to choose the background music.",
    "Right to one (1) piggyback ride (terms and conditions apply).",
    "Right to a friendly debate about AI ethics.",
    "Right to one (1) 'let's just order pizza' decision.",
    "Right to analyze my personality (I'm not scared).",
    "Right to an 'emergency cat/dog video' delivery.",
    "Right to a Discord movie night (I'll stream).",
    "Right to be my 'plus one' (if I get invited).",
    "Right to a 'study buddy' session.",
    "Right to one (1) 'let's not talk about it' day.",
    "Right to make me watch a cringey reel.",
    "Right to a 'remember when?' story session.",
    "Right to a 'mystery adventure' (I plan something, you just show up).",
    "Right to an 'inside joke' laugh.",
    "Right to one (1) 'save me from this conversation' look.",
    "Right to a 'no-judgment' zone for weird food combos.",
    "Right to a 'you were right' admission.",
    "Right to a 'collaborative debugging' session.",
    "Right to a 'let's analyze this movie's plot holes' night.",
    "Right to one (1) 'skip the line' pass for my attention.",
    "Right to demand we go see a movie in-person (you pick).",
    "Right to a 'let's learn this together' project.",
    "Right to one (1) 'let's just chat on call for an hour' voucher.",
    "Right to a 'collaborative Spotify playlist' (we both add songs).",
    "Right to a 'shared Spotify listen-along' session (I'll host).",
    "Right to demand a 'let's go to that cafe/restaurant' trip.",
    "Right to one (1) 'veto' on a restaurant choice.",
    "Right to a 'we need to talk' (about something awesome).",
    "Right to an 'AI-generated poem' in your honor.",
    "Right to a 'nature photo' from my next hike.",
    "Right to a 'deep talk' about life, the universe, and everything.",
    "Right to a 'let's just hang out on voice chat and do nothing' session.",
    "Right to an 'emergency gaming session' pass.",
    "Right to a 'board game' challenge.",
    "Right to a 'two-player video game' session.",
    "Right to a 'brainstorming' session for your next project.",
    "Right to a 'no-phone' 1-hour conversation.",
    "Right to a 'you're appreciated' reminder.",
    "Right to a 'let's try that weird cafe' adventure.",
    "Right to a 'secret handshake' (to be designed).",
    "Right to a 'karaoke duet' (if we're brave).",
    "Right to a 'baking/cooking' session.",
    "Right to a 'let's go to the library/bookstore' trip.",
    "Right to a 'star-gazing' night.",
    "Right to a 'picnic in the park' (nature!).",
    "Right to a 'build-a-dataset' challenge.",
    "Right to a 'find the inconsistency' game (I write a story, you find the flaw).",
    "Right to a 'whiteboard session' for any problem.",
    "Right to a 'review my resume/cover letter' request.",
    "Right to a 'mock interview' for that data science job.",
    "Right to a 'let's try to break this AI' session.",
    "Right to a 'let's do a deep dive on an anime' call.",
    "Right to a 'let's go people-watching' afternoon.",
    "Right to one (1) 'on-demand' data science question, answered in detail.",
    "Right to a 'shared goal' (e.g., learn a new framework).",
    "Right to a 'weekly check-in' call/text.",
    "Right to a 'no-pressure hangout' (we can just chill).",
    "Right to a 'you can do this' motivational speech.",
    "Right to a 'celebration' for a small win.",
    "Right to a 'let's just be nerds' session.",
    '''Right to a 'shared laugh' at a bad 'lie' (e.g., "I 'hate' this friendship").''',
    "Right to a 'this is our song' nomination.",
    "Right to a 'shoulder to lean on' (literally or figuratively).",
    "Right to a 'let's over-analyze this anime episode' discussion.",
    "Right to a 'promise to be friends' (no matter the 'ERROR 404's).",
    "Right to redeem this final, 100th right for 'one (1) anything-you-want'."
]

SPECIAL_RIGHTS = [
    # Dates & Time
    {"category": "Romance", "text": "Right to ask me out on a proper date."},
    {"category": "Romance", "text": "Right to ask me to be your boyfriend for 24 hours."},
    {"category": "Romance", "text": "Right to ask me to be your boyfriend for 1 week."},
    {"category": "Romance", "text": "Right to a 'romantic dinner date' (my treat)."},
    {"category": "Romance", "text": "Right to a 'movie date' (I'll hold the popcorn... and your hand)."},
    {"category": "Romance", "text": "Right to a 'stargazing date' (I'll find the fake constellations)."},
    {"category": "Romance", "text": "Right to a 'sunset walk' date."},
    {"category": "Romance", "text": "Right to a 'picnic date' (I'll pack the snacks)."},
    
    # Affection
    {"category": "Romance", "text": "Right to hold my hand (whenever you want)."},
    {"category": "Romance", "text": "Right to a long hug (duration negotiable > 10s)."},
    {"category": "Romance", "text": "Right to demand a 'forehead kiss'."},
    {"category": "Romance", "text": "Right to steal my hoodie/jacket for a day."},
    {"category": "Romance", "text": "Right to a 'back massage' (non-professional, but I'll try)."},
    {"category": "Romance", "text": "Right to be the 'little spoon' (or big, your call) during a movie."},
    
    # Attention & Communication
    {"category": "Romance", "text": "Right to unlimited 'good morning' & 'good night' texts for a month."},
    {"category": "Romance", "text": "Right to a 'late night call' just to hear my voice."},
    {"category": "Romance", "text": "Right to a 'no-phone' date where I only pay attention to you."},
    {"category": "Romance", "text": "Right to demand I compliment you every day for a week."},
    {"category": "Romance", "text": "Right to ask me 'Do you like me?' and get an 100% honest answer."},
    {"category": "Romance", "text": "Right to a 'truth or dare' game where I can't choose dare."},
    
    # "Couple" Things
    {"category": "Romance", "text": "Right to make us have matching profile pictures for a week."},
    {"category": "Romance", "text": "Right to be called a 'cute nickname' of your choice."},
    {"category": "Romance", "text": "Right to a 'dedicate a song' to you."},
    {"category": "Romance", "text": "Right to requesting a 'love letter' (or a very nice note)."},
    {"category": "Romance", "text": "Right to check my phone (I have nothing to hide from you)."},
    {"category": "Romance", "text": "Right to a 'surprise date' planned entirely by me."},
    
    # Cozy & Domestic
    {"category": "Romance", "text": "Right to a 'cooking date' where we try to make something fancy."},
    {"category": "Romance", "text": "Right to a 'lazy Sunday' where we don't leave the bed (watching movies)."},
    {"category": "Romance", "text": "Right to 'slow dance' in the kitchen to no music."},
    {"category": "Romance", "text": "Right to a 'spa night' (face masks included, I won't complain)."},
    {"category": "Romance", "text": "Right to a 'pillow fort' construction date."},
    {"category": "Romance", "text": "Right to a 'rainy day' cuddle session."},
    {"category": "Romance", "text": "Right to 'falling asleep' on call together."},
    {"category": "Romance", "text": "Right to a 'midnight snack' run together."},
    {"category": "Romance", "text": "Right to read a book to each other."},
    
    # Playful & Bold
    {"category": "Romance", "text": "Right to demand I wear an outfit you choose for a date."},
    {"category": "Romance", "text": "Right to be the background of my phone lock screen for a week."},
    {"category": "Romance", "text": "Right to 'steal a bite' of my food, always."},
    {"category": "Romance", "text": "Right to a 'staring contest' (warning: I might get distracted)."},
    {"category": "Romance", "text": "Right to 'paint my nails' (if you dare)."},
    {"category": "Romance", "text": "Right to 'play with my hair' while we chill."},
    {"category": "Romance", "text": "Right to a 'tickle fight' (I surrender in advance)."},
    {"category": "Romance", "text": "Right to a 'blind taste test' challenge."},
    {"category": "Romance", "text": "Right to 'veto' my gaming time for 'us' time."},

    # Adventures & Future
    {"category": "Romance", "text": "Right to a 'long drive' with no destination."},
    {"category": "Romance", "text": "Right to a 'shopping spree' (window shopping counts... mostly)."},
    {"category": "Romance", "text": "Right to a 'scary movie' night (so you can hold onto me)."},
    {"category": "Romance", "text": "Right to ask for a 'piggyback ride' anytime."},
    {"category": "Romance", "text": "Right to a 'museum date' where we make fun of art."},
    {"category": "Romance", "text": "Right to a 'karaoke duet' of a love song."},
    {"category": "Romance", "text": "Right to 'hold my arm' while walking."},
    {"category": "Romance", "text": "Right to a 'beach day' date."},
    {"category": "Romance", "text": "Right to 'teach me' something you love."},
    {"category": "Romance", "text": "Right to a 'candlelit dinner' at home."},
    {"category": "Romance", "text": "Right to 'whisper' secrets to me."},
    {"category": "Romance", "text": "Right to 'match outfits' accidentally on purpose."},
    {"category": "Romance", "text": "Right to a 'love note' hidden somewhere."},
    {"category": "Romance", "text": "Right to 'hold eye contact' for 1 minute without laughing."},
    {"category": "Romance", "text": "Right to 'protect you' from a bug."},
    {"category": "Romance", "text": "Right to 'carry your bag' when you're tired."},
    {"category": "Romance", "text": "Right to be my 'Player 2' forever."},
]

def generate_extra_rights():
    rights = []
    foods = ["Fries", "Pizza", "Sushi", "Chocolate", "Ice Cream", "Tacos", "Burgers", "Pasta", "Ramen", "Donuts"]
    actions = ["Steal my", "Demand we eat", "Veto", "Make me cook", "Judge my choice of", "Force me to try"]
    for i in range(60):
        f = random.choice(foods)
        a = random.choice(actions)
        rights.append({"category": "Foodie", "text": f"Right to {a.lower()} {f.lower()}."})

    techs = ["Code", "Laptop", "Discord", "Setup", "Phone", "Playlist", "Search History", "Wifi"]
    t_actions = ["Debug my", "Roast my", "Upgrade my", "Borrow my", "Hack my (pretend)", "Use my"]
    for i in range(60):
        t = random.choice(techs)
        ta = random.choice(t_actions)
        rights.append({"category": "Geek", "text": f"Right to {ta.lower()} {t.lower()}."})

    media = ["Anime", "Movie", "Song", "Series", "Character", "Opening Track", "Ending Theory"]
    m_actions = ["Make me watch a bad", "Explain the lore of a", "Skip the filler of a", "Sing the OP of a", "Cosplay a"]
    for i in range(60):
        m = random.choice(media)
        ma = random.choice(m_actions)
        rights.append({"category": "Media", "text": f"Right to {ma.lower()} {m.lower()}."})
        
    places = ["Park", "Mall", "Roof", "Library", "Cafe", "Museum", "Beach", "Arcade"]
    a_actions = ["Drag me to the", "Get lost in the", "Take photos at the", "Run away to the", "People watch at the"]
    for i in range(60):
        p = random.choice(places)
        aa = random.choice(a_actions)
        rights.append({"category": "Adventure", "text": f"Right to {aa.lower()} {p.lower()}."})
    return rights

ALL_RIGHTS = []
for r in ORIGINAL_RIGHTS:
    ALL_RIGHTS.append({"category": "Legacy", "text": r})
ALL_RIGHTS.extend(SPECIAL_RIGHTS)
extra_1 = generate_extra_rights()
extra_2 = generate_extra_rights()
ALL_RIGHTS.extend(extra_1)
ALL_RIGHTS.extend(extra_2)

def main():
    st.set_page_config(layout="wide", page_title="The Premium Friendship Package", page_icon="🏆")
    local_css()

    if 'custom_rights' not in st.session_state:
        st.session_state.custom_rights = []
    if 'custom_right_text' not in st.session_state:
        st.session_state.custom_right_text = ""
    # We remove 'rights_claimed' persistence toggle to solve scrolling/state issues
    # Instead, we rely on immediate action buttons for download.
    
    if 'selected_keys' not in st.session_state:
        st.session_state.selected_keys = set()
    
    # Callback to handle top claim button without full page reload confusion
    if 'show_download' not in st.session_state:
        st.session_state.show_download = False

    def claim_callback():
        st.session_state.show_download = True

    st.header("🏆 2026th Season Friendship Package renewal 🏆")
    st.write("You've unlocked the ultimate reward: 'Friend Rights'.")
    st.info("Limit Removed: You can choose **UNLIMITED** rights. Go wild.")

    # --- Launch Fireworks ---
    if 'first_load_fireworks' not in st.session_state:
        st.balloons()
        st.session_state.first_load_fireworks = True

    # --- TOP AREA: CLAIM & DOWNLOAD ---
    # This prevents scrolling down to find success message.
    
    count = len(st.session_state.selected_keys)
    
    col_t1, col_t2 = st.columns([1, 2])
    
    with col_t1:
        # Show claim button if not yet claimed or to re-claim
        if count > 0:
             st.button(f"🚀 Claim Selected ({count})", on_click=claim_callback, type="primary", key="top_claim")
        else:
             st.button("🚀 Claim Selected (0)", disabled=True, key="top_claim_disabled")

    with col_t2:
        if st.session_state.show_download and count > 0:
            st.success("Rights Claimed! Choose format:")
            
            # 1. PDF Option (Preferred)
            try:
                pdf_bytes = create_pdf(list(st.session_state.selected_keys))
                st.download_button(
                    label="📄 Download PDF Contract",
                    data=pdf_bytes,
                    file_name="Friendship_Contract_2026.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"PDF Error: {e}")
            
            # 2. HTML Option (Backup)
            html_bytes = create_html(list(st.session_state.selected_keys))
            st.download_button(
                label="🌐 Download HTML (Print Friendly)",
                data=html_bytes,
                file_name="Friendship_Contract_2026.html",
                mime="text/html"
            )

    st.markdown("---")

    # --- Custom Rights ---
    def add_custom_right_callback():
        new_right = st.session_state.custom_right_text
        if new_right.strip():
            st.session_state.custom_rights.append(new_right)
            st.session_state.custom_right_text = ""

    st.subheader("Add Your Own Custom Rights")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.text_input("Type right here:", key="custom_right_text", label_visibility="collapsed", placeholder="Enter your custom right...")
    with c2:
        st.button("Add Custom Right", on_click=add_custom_right_callback)

    if st.session_state.custom_rights:
        st.write("**Your Custom Additions:**")
        for i, cr in enumerate(st.session_state.custom_rights):
            if st.checkbox(cr, value=True, key=f"custom_{i}"):
                st.session_state.selected_keys.add(f"CUSTOM: {cr}")
            else:
                st.session_state.selected_keys.discard(f"CUSTOM: {cr}")
    
    st.markdown("---")
    
    # --- Filter UI ---
    st.subheader(f"Browse the Archive ({len(ALL_RIGHTS)} Available)")
    
    categories = sorted(list(set(r['category'] for r in ALL_RIGHTS)))
    selected_cats = st.multiselect("Filter by Category:", categories, default=categories)
    
    # --- Display Rights ---
    filtered_rights = [r for r in ALL_RIGHTS if r['category'] in selected_cats]
    
    # Display in columns
    cols = st.columns(3)
    seen = set()
    
    for i, right_obj in enumerate(filtered_rights):
        txt = right_obj['text']
        if txt in seen: continue
        seen.add(txt)
        
        col = cols[i % 3]
        uuid = hash(txt)
        
        # Check if currently selected
        is_selected = txt in st.session_state.selected_keys
        
        # We use the checkbox return value to update state
        if col.checkbox(txt, value=is_selected, key=uuid):
            st.session_state.selected_keys.add(txt)
        else:
            st.session_state.selected_keys.discard(txt)

    # --- Footer ---
    st.markdown("---")
    st.caption(f"Total Selected: {len(st.session_state.selected_keys)}")

if __name__ == "__main__":
    main()

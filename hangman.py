import streamlit as st
import random

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CodeAlpha Hangman",
    page_icon="🎮",
    layout="centered"
)

# --------------------------------------------------
# WORD DATABASE
# --------------------------------------------------

WORD_DATA = {
    "python": "A popular programming language.",
    "computer": "An electronic machine used to process data.",
    "developer": "A person who creates software.",
    "programming": "The process of writing instructions for computers.",
    "internship": "Temporary work experience for students or beginners.",
    "keyboard": "An input device used for typing.",
    "internet": "A global network connecting computers.",
    "software": "Programs and applications used by computers.",
    "algorithm": "A step-by-step procedure for solving a problem.",
    "database": "An organized collection of data.",
    "function": "A reusable block of code.",
    "variable": "A named location used to store data.",
    "streamlit": "A Python framework used to build web apps.",
    "framework": "A structure that helps developers build applications.",
    "debugging": "The process of finding and fixing errors in code."
}


# --------------------------------------------------
# HANGMAN DRAWINGS
# --------------------------------------------------

HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,

    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,

    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,

    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,

    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,

    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,

    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """
]


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "wins" not in st.session_state:
    st.session_state.wins = 0

if "losses" not in st.session_state:
    st.session_state.losses = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"


# --------------------------------------------------
# DIFFICULTY SETTINGS
# --------------------------------------------------

def get_attempts(difficulty):

    if difficulty == "Easy":
        return 8

    elif difficulty == "Medium":
        return 6

    else:
        return 4


# --------------------------------------------------
# START NEW GAME
# --------------------------------------------------

def new_game():

    secret_word = random.choice(list(WORD_DATA.keys()))

    st.session_state.secret_word = secret_word
    st.session_state.guessed_letters = []
    st.session_state.attempts = get_attempts(
        st.session_state.difficulty
    )
    st.session_state.max_attempts = st.session_state.attempts

    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.hint_used = False


# Start first game
if "secret_word" not in st.session_state:
    new_game()


# --------------------------------------------------
# CHECK GAME STATUS
# --------------------------------------------------

def check_win():

    secret_word = st.session_state.secret_word
    guessed_letters = st.session_state.guessed_letters

    return all(
        letter in guessed_letters
        for letter in secret_word
    )


# --------------------------------------------------
# PROCESS GUESS
# --------------------------------------------------

def make_guess(letter):

    if st.session_state.game_over:
        return

    letter = letter.lower()

    # Already guessed
    if letter in st.session_state.guessed_letters:
        return

    st.session_state.guessed_letters.append(letter)

    # Wrong guess
    if letter not in st.session_state.secret_word:

        st.session_state.attempts -= 1

    # Check win
    if check_win():

        st.session_state.game_won = True
        st.session_state.game_over = True

        st.session_state.wins += 1
        st.session_state.streak += 1

        # Score based on remaining attempts
        st.session_state.score += (
            10 + st.session_state.attempts * 2
        )

    # Check loss
    elif st.session_state.attempts <= 0:

        st.session_state.game_over = True
        st.session_state.game_won = False

        st.session_state.losses += 1
        st.session_state.streak = 0


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("🎮 Game Settings")

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"],
        index=["Easy", "Medium", "Hard"].index(
            st.session_state.difficulty
        )
    )

    # Difficulty changed
    if difficulty != st.session_state.difficulty:

        st.session_state.difficulty = difficulty
        new_game()
        st.rerun()

    st.divider()

    st.subheader("📊 Statistics")

    st.metric(
        "Score",
        st.session_state.score
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Wins",
            st.session_state.wins
        )

    with col2:
        st.metric(
            "Losses",
            st.session_state.losses
        )

    st.metric(
        "🔥 Win Streak",
        st.session_state.streak
    )

    st.divider()

    if st.button(
        "🔄 New Game",
        use_container_width=True
    ):

        new_game()
        st.rerun()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎮 CodeAlpha Hangman Game")

st.write(
    "Guess the hidden programming word "
    "one letter at a time."
)


# --------------------------------------------------
# GAME INFORMATION
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "❤️ Lives",
        st.session_state.attempts
    )

with col2:
    st.metric(
        "🎯 Difficulty",
        st.session_state.difficulty
    )

with col3:
    st.metric(
        "🏆 Score",
        st.session_state.score
    )


# --------------------------------------------------
# HANGMAN IMAGE
# --------------------------------------------------

wrong_guesses = (
    st.session_state.max_attempts
    - st.session_state.attempts
)

# Convert different difficulties to 0-6 stage
stage = int(
    (wrong_guesses / st.session_state.max_attempts) * 6
)

stage = min(stage, 6)

st.code(
    HANGMAN_STAGES[stage],
    language=None
)


# --------------------------------------------------
# DISPLAY WORD
# --------------------------------------------------

display_word = []

for letter in st.session_state.secret_word:

    if letter in st.session_state.guessed_letters:
        display_word.append(letter.upper())

    else:
        display_word.append("_")


st.markdown("### 🔤 Guess the Word")

st.markdown(
    f"<h2 style='text-align:center; "
    f"letter-spacing:12px;'>"
    f"{' '.join(display_word)}"
    f"</h2>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# PROGRESS
# --------------------------------------------------

correct_letters = sum(
    1
    for letter in set(st.session_state.secret_word)
    if letter in st.session_state.guessed_letters
)

total_letters = len(
    set(st.session_state.secret_word)
)

progress = correct_letters / total_letters

st.progress(progress)


# --------------------------------------------------
# HINT
# --------------------------------------------------

if not st.session_state.game_over:

    if st.button("💡 Show Hint"):

        st.session_state.hint_used = True


if st.session_state.hint_used:

    st.info(
        "💡 Hint: "
        + WORD_DATA[st.session_state.secret_word]
    )


# --------------------------------------------------
# GUESSED LETTERS
# --------------------------------------------------

if st.session_state.guessed_letters:

    st.write(
        "**Guessed letters:**",
        " ".join(
            letter.upper()
            for letter in st.session_state.guessed_letters
        )
    )


# --------------------------------------------------
# KEYBOARD
# --------------------------------------------------

st.markdown("### ⌨️ Choose a Letter")

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# 4 rows of buttons
rows = [
    alphabet[0:7],
    alphabet[7:14],
    alphabet[14:21],
    alphabet[21:26]
]

for row in rows:

    columns = st.columns(len(row))

    for column, letter in zip(columns, row):

        with column:

            already_guessed = (
                letter.lower()
                in st.session_state.guessed_letters
            )

            disabled = (
                already_guessed
                or st.session_state.game_over
            )

            if st.button(
                letter,
                key=f"letter_{letter}",
                disabled=disabled,
                use_container_width=True
            ):

                make_guess(letter)
                st.rerun()


# --------------------------------------------------
# GAME RESULT
# --------------------------------------------------

if st.session_state.game_over:

    st.divider()

    if st.session_state.game_won:

        st.success(
            f"🎉 Congratulations! "
            f"You guessed **{st.session_state.secret_word.upper()}**!"
        )

        st.balloons()

    else:

        st.error("💀 Game Over!")

        st.write(
            "The correct word was:",
            f"**{st.session_state.secret_word.upper()}**"
        )

    if st.button(
        "🎮 Play Again",
        type="primary",
        use_container_width=True
    ):

        new_game()
        st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "CodeAlpha Hangman Game • Built with Python & Streamlit"
)

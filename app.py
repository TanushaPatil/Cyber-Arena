from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import sqlite3
import os
import re
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

DATABASE = os.path.join(
    app.root_path,
    "database",
    "ctf.db"
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():

    os.makedirs(
        os.path.dirname(DATABASE),
        exist_ok=True
    )

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db():

    conn = get_db()

    # =====================================================
    # USERS
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT DEFAULT 'user',

            points INTEGER DEFAULT 0
        )
    """)

    # =====================================================
    # CHALLENGES
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS challenges (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            category TEXT NOT NULL,

            difficulty TEXT NOT NULL,

            description TEXT NOT NULL,

            points INTEGER NOT NULL,

            flag TEXT NOT NULL,

            active INTEGER DEFAULT 1
        )
    """)

    # =====================================================
    # ADD LAB_URL COLUMN TO OLD DATABASE
    # =====================================================

    columns = [
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(challenges)"
        ).fetchall()
    ]

    if "lab_url" not in columns:

        conn.execute("""
            ALTER TABLE challenges
            ADD COLUMN lab_url TEXT
        """)

    # =====================================================
    # SUBMISSIONS
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS submissions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            challenge_id INTEGER NOT NULL,

            submitted_flag TEXT NOT NULL,

            correct INTEGER DEFAULT 0,

            submitted_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (challenge_id)
                REFERENCES challenges(id)
                ON DELETE CASCADE,

            UNIQUE(
                user_id,
                challenge_id,
                submitted_flag
            )
        )
    """)

    # =====================================================
    # 10 FLAGSHIP CTF CHALLENGES
    # =====================================================

    sample_challenges = [

        # -------------------------------------------------
        # 1. WEB EXPLOITATION
        # -------------------------------------------------

        (
            "The Hidden Admin",

            "Web Exploitation",

            "Medium",

            "A small web application contains an access-control weakness. Investigate how user profiles are requested and find a way to access information belonging to the administrator.",

            250,

            "TECH{hidden_admin_access}",

            "http://127.0.0.1:5001"
        ),

        # -------------------------------------------------
        # 2. CRYPTOGRAPHY
        # -------------------------------------------------

        (
            "The Broken Cipher",

            "Cryptography",

            "Medium",

            "A collection of encrypted messages has been recovered from a suspicious source. Analyze the cipher, identify the weakness, recover the plaintext, and uncover the hidden flag.",

            250,

            "TECH{BROKEN_CIPHER}",

            None
        ),

        # -------------------------------------------------
        # 3. DIGITAL FORENSICS
        # -------------------------------------------------

        (
            "The Missing Evidence",

            "Digital Forensics",

            "Medium",

            "A network capture was recovered after a suspicious transfer. Analyze the traffic, follow the relevant communication, recover the hidden evidence, and find the flag.",

            250,

            "TECH{missing_evidence}",

            None
        ),

        # -------------------------------------------------
        # 4. OSINT
        # -------------------------------------------------

        (
            "The Vanishing Profile",

            "OSINT",

            "Medium",

            "A mysterious profile has disappeared from the internet. Use publicly available information, visual clues, and connected digital traces to identify the hidden profile and recover the flag.",

            250,

            "TECH{vanishing_profile}",

            None
        ),

        # -------------------------------------------------
        # 5. REVERSE ENGINEERING
        # -------------------------------------------------

        (
            "The Broken License",

            "Reverse Engineering",

            "Medium",

            "A suspicious executable performs a hidden license validation routine. Analyze the binary, understand the validation logic, reconstruct the expected input, and recover the flag.",

            200,

            "TECH{reverse_the_blackbox}",

            None
        ),

        # -------------------------------------------------
        # 6. PWN / BINARY
        # -------------------------------------------------

        (
            "Stack Attack",

            "Pwn / Binary",

            "Hard",

            "A vulnerable binary accepts user input without properly checking its size. Analyze the program's memory layout and exploit the vulnerability to reach the hidden win function and retrieve the flag.",

            300,

            "TECH{stack_attack}",

            None
        ),

        # -------------------------------------------------
        # 7. STEGANOGRAPHY
        # -------------------------------------------------

        (
            "The Silent Image",

            "Steganography",

            "Easy",

            "An innocent-looking media file has been recovered. The visible content appears normal, but something is hidden inside the file. Analyze the media carefully and recover the secret flag.",

            150,

            "TECH{silent_image}",

            None
        ),

        # -------------------------------------------------
        # 8. MOBILE SECURITY
        # -------------------------------------------------

        (
            "The Lost APK",

            "Mobile Security",

            "Medium",

            "A suspicious Android application has been recovered. Reverse engineer the APK, inspect its activities and resources, and discover the hidden secret stored inside the application.",

            250,

            "TECH{lost_apk}",

            None
        ),

        # -------------------------------------------------
        # 9. BLOCKCHAIN / WEB3
        # -------------------------------------------------

        (
            "The Vulnerable Vault",

            "Blockchain / Web3",

            "Hard",

            "A smart contract is protecting a valuable digital vault. Analyze the contract logic and identify the weakness in its access-control mechanism to retrieve the hidden flag.",

            300,

            "TECH{vulnerable_vault}",

            None
        ),

        # -------------------------------------------------
        # 10. MISCELLANEOUS
        # -------------------------------------------------

        (
            "The Final Puzzle",

            "Miscellaneous",

            "Easy",

            "Several strange clues have been combined into one final puzzle. Decode the data, identify the pattern, connect the clues, and uncover the final flag.",

            150,

            "TECH{final_puzzle}",

            None
        )
    ]

    # =====================================================
    # INSERT / UPDATE CHALLENGES
    # =====================================================

    for challenge in sample_challenges:

        title = challenge[0]

        existing = conn.execute(
            """
            SELECT id
            FROM challenges
            WHERE title = ?
            """,
            (title,)
        ).fetchone()

        if existing:

            conn.execute(
                """
                UPDATE challenges

                SET
                    category = ?,
                    difficulty = ?,
                    description = ?,
                    points = ?,
                    flag = ?,
                    lab_url = ?,
                    active = 1

                WHERE title = ?
                """,
                (
                    challenge[1],
                    challenge[2],
                    challenge[3],
                    challenge[4],
                    challenge[5],
                    challenge[6],
                    title
                )
            )

        else:

            conn.execute(
                """
                INSERT INTO challenges
                (
                    title,
                    category,
                    difficulty,
                    description,
                    points,
                    flag,
                    lab_url,
                    active
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                """,
                challenge
            )

    # =====================================================
    # DISABLE OLD PLACEHOLDER CHALLENGES
    # =====================================================

    old_challenges = [

        "Hidden Parameter",

        "Caesar's Secret",

        "Lost Evidence",

        "Digital Footprint",

        "Stack Trouble",

        "Invisible Message",

        "Mobile Mystery",

        "Smart Contract",

        "Encoding Chaos"
    ]

    for old_title in old_challenges:

        conn.execute(
            """
            UPDATE challenges

            SET active = 0

            WHERE title = ?
            """,
            (old_title,)
        )

    conn.commit()

    conn.close()


# =========================================================
# LOGIN REQUIRED DECORATOR
# =========================================================

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login first.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        return f(*args, **kwargs)

    return decorated_function


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # -----------------------------------------------
        # VALIDATION
        # -----------------------------------------------

        if not username or not email or not password:

            flash(
                "All fields are required.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        # -----------------------------------------------
        # DATABASE
        # -----------------------------------------------

        conn = get_db()

        existing = conn.execute(
            """
            SELECT id

            FROM users

            WHERE username = ?
               OR email = ?
            """,
            (
                username,
                email
            )
        ).fetchone()

        if existing:

            conn.close()

            flash(
                "Username or email already exists.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        # -----------------------------------------------
        # PASSWORD HASH
        # -----------------------------------------------

        hashed_password = generate_password_hash(
            password
        )

        conn.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password
            )

            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                hashed_password
            )
        )

        conn.commit()

        conn.close()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        conn = get_db()

        user = conn.execute(
            """
            SELECT *

            FROM users

            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["username"] = user["username"]

            session["role"] = user["role"]

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid username or password.",
            "error"
        )

    return render_template(
        "login.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    conn = get_db()

    user = conn.execute(
        """
        SELECT *

        FROM users

        WHERE id = ?
        """,
        (
            session["user_id"],
        )
    ).fetchone()

    # Number of solved challenges

    solved_count = conn.execute(
        """
        SELECT COUNT(*)

        FROM submissions

        WHERE user_id = ?

        AND correct = 1
        """,
        (
            session["user_id"],
        )
    ).fetchone()[0]

    # Total challenges

    total_challenges = conn.execute(
        """
        SELECT COUNT(*)

        FROM challenges

        WHERE active = 1
        """
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        user=user,
        solved_count=solved_count,
        total_challenges=total_challenges
    )


# =========================================================
# ALL CHALLENGE DOMAINS
# =========================================================
@app.route(
    "/challenge/<path:category_name>"
)
@login_required
def challenge_by_domain(category_name):

    conn = get_db()

    challenge = conn.execute(
        """
        SELECT
            id,
            title,
            category,
            difficulty,
            description,
            points,
            lab_url
        FROM challenges
        WHERE category = ?
        AND active = 1
        LIMIT 1
        """,
        (category_name,)
    ).fetchone()

    if not challenge:
        conn.close()

        flash(
            "Challenge not found.",
            "error"
        )

        return redirect(
            url_for("challenges")
        )

    solved = conn.execute(
        """
        SELECT id
        FROM submissions
        WHERE user_id = ?
        AND challenge_id = ?
        AND correct = 1
        LIMIT 1
        """,
        (
            session["user_id"],
            challenge["id"]
        )
    ).fetchone()

    conn.close()

    return render_template(
        "challenge.html",
        challenge=challenge,
        solved=bool(solved)
    )

@app.route("/challenges")
@login_required
def challenges():

    conn = get_db()

    categories = conn.execute(
        """
        SELECT

            category,

            COUNT(*) AS challenge_count,

            SUM(points) AS points

        FROM challenges

        WHERE active = 1

        GROUP BY category

        ORDER BY MIN(id)
        """
    ).fetchall()

    conn.close()

    descriptions = {

        "Web Exploitation":
            "Find vulnerabilities in web applications and exploit weak access controls.",

        "Cryptography":
            "Break ciphers, analyze encryption weaknesses, and recover hidden secrets.",

        "Digital Forensics":
            "Investigate files, network captures, artifacts, and digital evidence.",

        "OSINT":
            "Gather intelligence from publicly available information and digital traces.",

        "Reverse Engineering":
            "Analyze binaries and understand how hidden validation logic works.",

        "Pwn / Binary":
            "Exploit memory corruption vulnerabilities in vulnerable programs.",

        "Steganography":
            "Discover information hidden inside ordinary-looking media files.",

        "Mobile Security":
            "Reverse engineer Android applications and uncover hidden functionality.",

        "Blockchain / Web3":
            "Analyze smart contracts and discover vulnerabilities in decentralized applications.",

        "Miscellaneous":
            "Solve unusual puzzles involving encoding, scripting, logic, and unexpected techniques."
    }

    category_data = []

    for row in categories:

        category_data.append({

            "category":
                row["category"],

            "challenge_count":
                row["challenge_count"],

            "points":
                row["points"],

            "description":
                descriptions.get(
                    row["category"],
                    "Investigate the challenge and find the hidden flag."
                )
        })

    return render_template(
        "challenges.html",
        categories=category_data
    )


# =========================================================
# CATEGORY PAGE
# =========================================================

def category_slug(category):
    return re.sub(r"[^a-z0-9]+", "-", category.lower()).strip("-")

@app.route("/challenge/<slug>")
@login_required
def challenge_by_slug(slug):

    conn = get_db()

    challenge = conn.execute("""
        SELECT
            id,
            title,
            category,
            difficulty,
            description,
            points,
            lab_url
        FROM challenges
        WHERE active = 1
          AND lower(replace(category, ' ', '-')) = ?
        LIMIT 1
    """, (slug.lower(),)).fetchone()

    if challenge is None:
        conn.close()
        flash("Challenge not found.", "error")
        return redirect(url_for("challenges"))

    solved = conn.execute("""
        SELECT id
        FROM submissions
        WHERE user_id = ?
          AND challenge_id = ?
          AND correct = 1
        LIMIT 1
    """, (
        session["user_id"],
        challenge["id"]
    )).fetchone()

    conn.close()

    return render_template(
        "challenge.html",
        challenge=challenge,
        solved=bool(solved)
    )

# =========================================================
# CHALLENGE DETAILS
# =========================================================

@app.route(
    "/challenge/<int:challenge_id>"
)
@login_required
def challenge_details(challenge_id):

    conn = get_db()

    challenge = conn.execute(
        """
        SELECT

            id,

            title,

            category,

            difficulty,

            description,

            points,

            lab_url

        FROM challenges

        WHERE id = ?

        AND active = 1
        """,
        (challenge_id,)
    ).fetchone()

    # -----------------------------------------------------
    # CHECK WHETHER CURRENT USER SOLVED IT
    # -----------------------------------------------------

    solved = conn.execute(
        """
        SELECT id

        FROM submissions

        WHERE user_id = ?

        AND challenge_id = ?

        AND correct = 1

        LIMIT 1
        """,
        (
            session["user_id"],
            challenge_id
        )
    ).fetchone()

    conn.close()

    if not challenge:

        flash(
            "Challenge not found.",
            "error"
        )

        return redirect(
            url_for("challenges")
        )

    return render_template(
        "challenge.html",
        challenge=challenge,
        solved=bool(solved)
    )


# =========================================================
# FLAG SUBMISSION
# =========================================================

@app.route(
    "/challenge/<int:challenge_id>/submit",
    methods=["POST"]
)
@login_required
def submit_flag(challenge_id):

    submitted_flag = request.form.get(
        "flag",
        ""
    ).strip()

    conn = get_db()

    # -----------------------------------------------------
    # GET CHALLENGE
    # -----------------------------------------------------

    challenge = conn.execute(
        """
        SELECT *

        FROM challenges

        WHERE id = ?

        AND active = 1
        """,
        (challenge_id,)
    ).fetchone()

    if not challenge:

        conn.close()

        flash(
            "Challenge not found.",
            "error"
        )

        return redirect(
            url_for("challenges")
        )

    # -----------------------------------------------------
    # CHECK FLAG
    # -----------------------------------------------------

    correct = (
        submitted_flag
        == challenge["flag"]
    )

    # -----------------------------------------------------
    # CHECK IF ALREADY SOLVED
    # -----------------------------------------------------

    already_solved = conn.execute(
        """
        SELECT id

        FROM submissions

        WHERE user_id = ?

        AND challenge_id = ?

        AND correct = 1

        LIMIT 1
        """,
        (
            session["user_id"],
            challenge_id
        )
    ).fetchone()

    # -----------------------------------------------------
    # SAVE SUBMISSION
    # -----------------------------------------------------

    if not already_solved:

        try:

            conn.execute(
                """
                INSERT INTO submissions
                (
                    user_id,
                    challenge_id,
                    submitted_flag,
                    correct
                )

                VALUES (?, ?, ?, ?)
                """,
                (
                    session["user_id"],
                    challenge_id,
                    submitted_flag,
                    1 if correct else 0
                )
            )

        except sqlite3.IntegrityError:

            pass

    # -----------------------------------------------------
    # AWARD POINTS
    # -----------------------------------------------------

    if correct and not already_solved:

        conn.execute(
            """
            UPDATE users

            SET points = points + ?

            WHERE id = ?
            """,
            (
                challenge["points"],
                session["user_id"]
            )
        )

        flash(
            f"Correct flag! +{challenge['points']} points.",
            "success"
        )

    elif correct and already_solved:

        flash(
            "Correct flag! Challenge already solved.",
            "success"
        )

    else:

        flash(
            "Incorrect flag. Keep trying!",
            "error"
        )

    conn.commit()

    conn.close()

    return redirect(
        url_for(
            "challenge_details",
            challenge_id=challenge_id
        )
    )


# =========================================================
# LEADERBOARD
# =========================================================

@app.route("/leaderboard")
@login_required
def leaderboard():

    conn = get_db()

    users = conn.execute(
        """
        SELECT

            username,

            points

        FROM users

        ORDER BY

            points DESC,

            username ASC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "leaderboard.html",
        users=users
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("index")
    )


# =========================================================
# DIGITAL FORENSICS - PCAP DOWNLOAD
# =========================================================

@app.route(
    "/challenge/forensics/download"
)
@login_required
def download_forensics():

    evidence_dir = os.path.join(

        app.root_path,

        "CTF Challenges",

        "Digital Forensics"
    )

    file_path = os.path.join(
        evidence_dir,
        "evidence.pcap"
    )

    if not os.path.exists(file_path):

        flash(
            "Forensics PCAP not found.",
            "error"
        )

        return redirect(
            url_for("challenges")
        )

    return send_from_directory(

        evidence_dir,

        "evidence.pcap",

        as_attachment=True
    )


# =========================================================
# REVERSE ENGINEERING - BLACKBOX DOWNLOAD
# =========================================================

@app.route(
    "/challenge/blackbox/download"
)
@login_required
def download_blackbox():

    challenge_path = os.path.join(

        app.root_path,

        "CTF Challenges",

        "Reverse Engineering",

        "BLACKBOX"
    )

    file_path = os.path.join(

        challenge_path,

        "blackbox.exe"
    )

    if not os.path.exists(file_path):

        flash(
            "Challenge file not found.",
            "error"
        )

        return redirect(
            url_for("challenges")
        )

    return send_from_directory(

        challenge_path,

        "blackbox.exe",

        as_attachment=True
    )

# =========================================================
# STEGANOGRAPHY - WAV DOWNLOAD
# =========================================================

@app.route("/challenge/stego/download")
@login_required
def download_stego():

    challenge_path = os.path.join(
        app.root_path,
        "CTF Challenges",
        "Steganography"
    )

    file_path = os.path.join(
        challenge_path,
        "hidden_audio.wav"
    )

    if not os.path.exists(file_path):

        flash(
            "Steganography WAV file not found.",
            "error"
        )

        return redirect(
            url_for("challenges")
        )

    return send_from_directory(
        challenge_path,
        "hidden_audio.wav",
        as_attachment=True
    )
@app.route("/challenge/osint/download")
@login_required
def download_osint():

    challenge_path = os.path.join(
        app.root_path,
        "CTF Challenges",
        "OSINT"
    )

    file_path = os.path.join(
        challenge_path,
        "location_evidence.jpg"
    )

    if not os.path.exists(file_path):
        flash("OSINT evidence file not found.", "error")
        return redirect(url_for("challenges"))

    return send_from_directory(
        challenge_path,
        "location_evidence.jpg",
        as_attachment=True
    )
@app.route("/challenge/crypto/download")
@login_required
def download_crypto():
    return send_from_directory(
        os.path.join(app.root_path, "CTF Challenges", "Cryptography"),
        "evidence.txt",
        as_attachment=True
    )


@app.route("/challenge/pwn/download")
@login_required
def download_pwn():
    return send_from_directory(
        os.path.join(app.root_path, "CTF Challenges", "Pwn"),
        "stack_attack.exe",
        as_attachment=True
    )


@app.route("/challenge/mobile/download")
@login_required
def download_mobile():
    apk_path = os.path.join(
        app.root_path,
        "CTF Challenges",
        "Mobile Security",
        "lost_apk.apk"
    )

    if not os.path.exists(apk_path):
        return "Mobile challenge APK is not available yet.", 404

    return send_from_directory(
        os.path.dirname(apk_path),
        "lost_apk.apk",
        as_attachment=True
    )


@app.route("/challenge/blockchain/download")
@login_required
def download_blockchain():
    return send_from_directory(
        os.path.join(app.root_path, "CTF Challenges", "Blockchain"),
        "VulnerableVault.sol",
        as_attachment=True
    )


@app.route("/challenge/misc")
@login_required
def misc_challenge():
    return redirect(url_for("challenge", challenge_id=10))
# =========================================================
# OPTIONAL - USER SOLVED CHALLENGES
# =========================================================

@app.route("/my-solves")
@login_required
def my_solves():

    conn = get_db()

    solved = conn.execute(
        """
        SELECT

            challenges.title,

            challenges.category,

            challenges.points,

            submissions.submitted_at

        FROM submissions

        JOIN challenges

        ON submissions.challenge_id = challenges.id

        WHERE submissions.user_id = ?

        AND submissions.correct = 1

        ORDER BY submissions.submitted_at DESC
        """,
        (
            session["user_id"],
        )
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        solved=solved
    )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
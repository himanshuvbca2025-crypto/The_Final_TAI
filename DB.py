import os
import mysql.connector
import bcrypt

from dotenv import load_dotenv

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

DB_HOST = os.getenv("MYSQLHOST", "localhost")
DB_USER = os.getenv("MYSQLUSER", "root")
DB_PASSWORD = os.getenv("MYSQLPASSWORD", "")
DB_NAME = os.getenv("MYSQLDATABASE")
DB_PORT = int(os.getenv("MYSQLPORT", 3306))

print("HOST =", DB_HOST,repr(DB_HOST))
print("USER =", DB_USER,repr(DB_USER))
print("DB =", DB_NAME,repr(DB_NAME))


# ==========================================
# DATABASE CONNECTION
# ==========================================

def connect():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database= DB_NAME,
        port=DB_PORT
    )


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    con = connect()

    cursor = con.cursor()

    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
    )

    con.commit()

    cursor.close()

    con.close()


# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():

    con = get_connection()

    cursor = con.cursor()

    # ======================================
    # USERS TABLE
    # ======================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INT AUTO_INCREMENT PRIMARY KEY,

        full_name VARCHAR(150) NOT NULL,

        email VARCHAR(150) UNIQUE NOT NULL,

        mobile VARCHAR(15) UNIQUE NOT NULL,

        password VARCHAR(255) NOT NULL,

        state VARCHAR(100),

        district VARCHAR(100),

        village VARCHAR(150),

        language VARCHAR(50) DEFAULT 'English',

        role ENUM(
            'Farmer',
            'Student',
            'Researcher',
            'Admin'
        ) DEFAULT 'Farmer',

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # ======================================
    # FILE UPLOADS
    # ======================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS uploads(

        id INT AUTO_INCREMENT PRIMARY KEY,

        user_id INT NOT NULL,

        file_name VARCHAR(255),

        file_path TEXT,

        upload_time TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE

    )

    """)

    # ======================================
    # CHAT HISTORY
    # ======================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS chatbot_history(

        id INT AUTO_INCREMENT PRIMARY KEY,

        user_id INT NOT NULL,

        question TEXT,

        answer LONGTEXT,

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE

    )

    """)

    con.commit()

    cursor.close()

    con.close()


# ==========================================
# REGISTER USER
# ==========================================

def insert_user(

    full_name,

    email,

    mobile,

    password,

    state,

    district,

    village,

    language

):

    con = get_connection()

    cursor = con.cursor()

    hashed_password = bcrypt.hashpw(

        password.encode(),

        bcrypt.gensalt()

    ).decode()

    sql = """

    INSERT INTO users(

        full_name,

        email,

        mobile,

        password,

        state,

        district,

        village,

        language

    )

    VALUES(

        %s,

        %s,

        %s,

        %s,

        %s,

        %s,

        %s,

        %s

    )

    """

    cursor.execute(

        sql,

        (

            full_name,

            email,

            mobile,

            hashed_password,

            state,

            district,

            village,

            language

        )

    )

    con.commit()
    
    user_id = cursor.lastrowid

    cursor.close()
    con.close()

    return {
      "id": user_id,
      "full_name": full_name
}
    

# ==========================================
# LOGIN USER
# ==========================================

def login_user(email, password):

    con = get_connection()

    cursor = con.cursor(dictionary=True)

    cursor.execute(

        "SELECT * FROM users WHERE email=%s",

        (email,)

    )

    user = cursor.fetchone()

    cursor.close()

    con.close()

    if user:

        if bcrypt.checkpw(

            password.encode(),

            user["password"].encode()

        ):

            return user

    return None


# ==========================================
# SAVE FILE UPLOAD
# ==========================================

def save_upload(

    user_id,

    file_name,

    file_path

):

    con = get_connection()

    cursor = con.cursor()

    cursor.execute(

        """

        INSERT INTO uploads(

            user_id,

            file_name,

            file_path

        )

        VALUES(

            %s,

            %s,

            %s

        )

        """,

        (

            user_id,

            file_name,

            file_path

        )

    )

    con.commit()

    cursor.close()

    con.close()


# ==========================================
# SAVE CHAT HISTORY
# ==========================================

def save_chat(

    user_id,

    question,

    answer

):

    con = get_connection()

    cursor = con.cursor()

    cursor.execute(

        """

        INSERT INTO chatbot_history(

            user_id,

            question,

            answer

        )

        VALUES(

            %s,

            %s,

            %s

        )

        """,

        (

            user_id,

            question,

            answer

        )

    )

    con.commit()

    cursor.close()

    con.close()


# ==========================================
# INITIALIZE DATABASE
# ==========================================

if __name__ == "__main__":

    create_database()

    create_tables()

    print("✅ TRINETRA AI Database Initialized Successfully.")
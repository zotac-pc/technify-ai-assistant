import os, re, csv, jwt, random, string
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, render_template, request, redirect, make_response, jsonify

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from deep_translator import GoogleTranslator

# -------------------- Config --------------------
JWTSECRET = "mysecret"
CHROMADBDIR = "data/vector_store"
COLLECTIONNAME = "technify_policies"
USERS_CSV = "users.csv"
LOGINS_CSV = "logins.csv"

app = Flask(__name__)

# -------------------- CSV helpers --------------------
def init_csv():
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["username","email","password","userid","role"])
            writer.writerow(["student","student@technify.edu","12345678","STU0001","student"])
            writer.writerow(["faculty","faculty@technify.edu","faculty123","FAC001","faculty"])
            writer.writerow(["admin","admin@technify.edu","admin123","ADM001","admin"])
    if not os.path.exists(LOGINS_CSV):
        with open(LOGINS_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp","username","userid","role"])

def read_users():
    users = {}
    if os.path.exists(USERS_CSV):
        with open(USERS_CSV, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users[row["username"]] = {
                    "email": row.get("email",""),
                    "password": row["password"],
                    "userid": row["userid"],
                    "role": row["role"]
                }
                if row.get("email"):
                    users[row["email"]] = users[row["username"]]
    return users

def add_user(username, email, password, userid, role="student"):
    with open(USERS_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([username, email, password, userid, role])

def log_login(username, userid, role):
    with open(LOGINS_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.utcnow().isoformat(), username, userid, role])

# -------------------- LangChain setup --------------------
def get_chain():
    try:
        embedder = OllamaEmbeddings(model="llama3.2:1b")
        vectorstore = Chroma(
            persist_directory=CHROMADBDIR,
            embedding_function=embedder,
            collection_name=COLLECTIONNAME
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k":3})
        llm = ChatOllama(model="llama3.2:1b", temperature=0)
        memory = ConversationBufferMemory(memory_key="chat history", return_messages=True, output_key="answer")
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm, retriever=retriever, memory=memory, return_source_documents=True
        )
        return chain
    except Exception as e:
        print(f"Chain fallback: {e}")
        llm = ChatOllama(model="llama3.2:1b", temperature=0)
        memory = ConversationBufferMemory(memory_key="chat history", return_messages=True, output_key="answer")
        from langchain.chains import ConversationChain
        return ConversationChain(llm=llm, memory=memory)

chain = None

# -------------------- State & helpers --------------------
auditLog = []
DEFAULT_ATTENDANCE = {
    "Software Engineering": {"total": 18, "attended": 18},
    "Artificial Intelligence": {"total": 20, "attended": 20},
    "Operating System": {"total": 20, "attended": 20},
    "Advanced Database": {"total": 18, "attended": 18},
    "Python Programming": {"total": 20, "attended": 20},
    "Data Science": {"total": 20, "attended": 20},
    "Cyber Security": {"total": 18, "attended": 18},
    "Project Management": {"total": 16, "attended": 16},
    "Web Engineering": {"total": 18, "attended": 18}
}
lastCourseContext = {}
lastAttendanceData = {}
user_states = {}

def decodeToken(token: str):
    try:
        return jwt.decode(token, JWTSECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def cleanText(text: str):
    return re.sub(r'[^\w\s]', '', text).lower().strip()

def detectIntent(query: str, role: str):
    q = cleanText(query)
    if any(w in q for w in ["modify","change","update","delete","approve"]):
        return "outofscope", {}
    if q in ["hello","hi","hey","good morning","good afternoon","good evening","yo"]:
        return "greeting", {}
    if any(w in q for w in ["leave","escape","absent","day off","skip"]):
        return "leave", {}
    if any(w in q for w in ["miss"]) and any(w in q for w in ["day","class","lecture"]):
        return "missdays", {}
    if any(w in q for w in ["eligible","eligibility","can i sit","appear for exam","give exam"]):
        return "eligibility", {}
    if "cgpa" in q:
        return "cgpa", {}
    if "gpa" in q:
        return "gpa", {}
    if role == "student":
        if any(w in q for w in ["attendance","present"]): return "attendance", {}
        if any(w in q for w in ["assignment","pending"]): return "assignments", {}
        if any(w in q for w in ["exam","schedule"]): return "exams", {}
        if any(w in q for w in ["fee","payment","dues"]): return "fees", {}
        if any(w in q for w in ["course","registered"]): return "courses", {}
        if any(w in q for w in ["timetable","schedule"]): return "timetable", {}
        if any(w in q for w in ["study plan","recommend"]): return "studyplan", {}
    if role == "faculty":
        if "low attendance" in q: return "lowattendance", {}
        if "ungraded" in q: return "ungraded", {}
        if "risk" in q: return "atrisk", {}
        if "performance" in q: return "courseperf", {}
    if role == "admin":
        if "total students" in q: return "totalstudents", {}
        if "admission" in q: return "admissionstats", {}
        if "fee collection" in q: return "feecollection", {}
        if "department performance" in q: return "deptperf", {}
    if any(w in q for w in ["policy","rule","degree","calendar"]): return "policy", {}
    return "general", {}

def translateText(text, source, target):
    if target == "en" or source == target:
        return text
    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except:
        return None

def getCourseDataFromQuery(query: str):
    for course, data in lastAttendanceData.items():
        if course.lower() in query.lower():
            return course, data.copy()
    return None, None

# -------------------- GPA / CGPA State Machine --------------------
def handle_gpa_cgpa_intent(userid, query, intent_type):
    state = user_states.get(userid)
    if not state or state.get("intent") not in ("gpa","cgpa"):
        user_states[userid] = {"intent": intent_type, "step": "ask_presence"}
        return "Were you present in all mids and finals? (yes/no)"

    step = state["step"]
    if step == "ask_presence":
        if query.lower() in ["yes","y"]:
            state["present"] = True
            if intent_type == "cgpa":
                state["step"] = "ask_semesters_completed"
                return "How many semesters have you completed?"
            else:
                state["step"] = "ask_year"
                return "Which year do you want to calculate GPA for? (1st, 2nd, 3rd, 4th)"
        elif query.lower() in ["no","n"]:
            user_states.pop(userid, None)
            return "Sorry, you are absent and cannot calculate GPA."
        else:
            return "Please answer 'yes' or 'no'."

    elif step == "ask_year":
        yr = query.lower().strip()
        if yr in ["1st","first","1"]: state["year"] = 1
        elif yr in ["2nd","second","2"]: state["year"] = 2
        elif yr in ["3rd","third","3"]: state["year"] = 3
        elif yr in ["4th","fourth","4"]: state["year"] = 4
        else: return "Please specify 1st, 2nd, 3rd, or 4th year."
        state["step"] = "ask_semester"
        return "Which semester? (1st or 2nd)"

    elif step == "ask_semester":
        sem = query.lower().strip()
        if sem in ["1st","first","1","fall"]: state["semester"] = 1
        elif sem in ["2nd","second","2","spring"]: state["semester"] = 2
        else: return "Please specify 1st or 2nd semester."
        year = state["year"]
        state["subjects_count"] = 9 if year <= 3 else 4
        state["subjects_data"] = []
        state["current_subject"] = 1
        state["step"] = "ask_subject_name"
        return f"Semester {state['semester']}, Year {state['year']}. It has {state['subjects_count']} subjects. What is the name of subject 1?"

    elif step == "ask_subject_name":
        state["temp_subject"] = {"name": query}
        state["step"] = "ask_subject_credits"
        return f"How many credit hours for {query}?"

    elif step == "ask_subject_credits":
        if not query.replace('.','',1).isdigit(): return "Please enter a valid number for credit hours."
        state["temp_subject"]["credits"] = float(query)
        state["step"] = "ask_subject_marks"
        return f"What marks did you obtain in {state['temp_subject']['name']}? (out of 100)"

    elif step == "ask_subject_marks":
        if not query.replace('.','',1).isdigit(): return "Please enter valid marks."
        marks = float(query)
        subj = state["temp_subject"]
        if marks >= 85: gp = 4.0
        elif marks >= 70: gp = 3.0
        elif marks >= 60: gp = 2.0
        elif marks >= 50: gp = 1.0
        else: gp = 0.0
        subj["grade_points"] = gp
        state["subjects_data"].append(subj)
        state["current_subject"] += 1
        if state["current_subject"] > state["subjects_count"]:
            total_gp = sum(s["credits"] * s["grade_points"] for s in state["subjects_data"])
            total_credits = sum(s["credits"] for s in state["subjects_data"])
            gpa = total_gp / total_credits if total_credits else 0
            user_states.pop(userid, None)
            return f"Your GPA for Year {state['year']} Semester {state['semester']} is {gpa:.2f}."
        else:
            state["step"] = "ask_subject_name"
            return f"Subject {state['current_subject']}: Name?"

    elif step == "ask_semesters_completed":
        if not query.isdigit(): return "Please enter a valid number (e.g., 2)."
        state["semesters_completed"] = int(query)
        state["gpa_list"] = []
        state["current_sem"] = 1
        state["step"] = "ask_sem_gpa"
        return f"Please enter GPA for Semester 1:"

    elif step == "ask_sem_gpa":
        if not query.replace('.','',1).isdigit(): return "Please enter a valid GPA number (e.g., 3.5)."
        state["gpa_list"].append(float(query))
        if state["current_sem"] < state["semesters_completed"]:
            state["current_sem"] += 1
            return f"GPA for Semester {state['current_sem']}:"
        else:
            cgpa = sum(state["gpa_list"]) / len(state["gpa_list"])
            user_states.pop(userid, None)
            return f"Your CGPA across {state['semesters_completed']} semesters is {cgpa:.2f}."
    return "Something went wrong. Please start over."

# -------------------- Leave / Escape State Machine --------------------
def handle_leave_intent(userid, query):
    state = user_states.get(userid)
    if not state or state.get("intent") != "leave":
        user_states[userid] = {"intent": "leave", "step": "ask_reason"}
        return "What is the reason for your leave? (e.g., medical, personal, emergency)"

    step = state["step"]
    if step == "ask_reason":
        reason = query.lower()
        if any(w in reason for w in ["death", "accident", "hospitalised", "emergency", "life threat"]):
            user_states.pop(userid, None)
            return "This sounds very serious. Please contact the admin or your faculty members directly. Do not wait for the application."
        elif any(w in reason for w in ["medical", "sick", "family emergency", "personal emergency", "urgent"]):
            user_states.pop(userid, None)
            return "You should submit a leave application through the ERP portal. Your application will be reviewed by the concerned authorities."
        else:
            user_states.pop(userid, None)
            return "If it is not a critical issue, you may still submit a leave application. But for now, please attend your classes if possible."
    return "Something went wrong in leave process."

# -------------------- Core chat processor --------------------
def process_chat(userid, role, token, message, lang="en"):
    global chain, lastAttendanceData, lastCourseContext
    if chain is None:
        chain = get_chain()
    if not lastAttendanceData:
        lastAttendanceData = {k: v.copy() for k, v in DEFAULT_ATTENDANCE.items()}

    try:
        payload = decodeToken(token)
    except ValueError as e:
        return str(e)

    if payload.get("role") != role:
        return "Role mismatch."

    if lang != "en":
        queryEn = translateText(message, lang, "en") or message
    else:
        queryEn = message

    state = user_states.get(userid)
    if state:
        if state.get("intent") == "leave":
            return handle_leave_intent(userid, queryEn)
        if state.get("intent") in ("gpa","cgpa"):
            return handle_gpa_cgpa_intent(userid, queryEn, state["intent"])

    intent, _ = detectIntent(queryEn, role)

    auditLog.append({
        "userid": userid, "role": role, "query": queryEn,
        "intent": intent, "timestamp": datetime.utcnow().isoformat()
    })

    # -------------------- All intents --------------------
    if intent == "outofscope":
        return "I cannot modify or approve records. Please contact the relevant department."
    if intent == "greeting":
        return "Hello! How can I assist you with your academic queries today?"
    if intent == "leave":
        return handle_leave_intent(userid, queryEn)
    if intent in ("gpa","cgpa"):
        return handle_gpa_cgpa_intent(userid, queryEn, intent)

    if intent == "attendance":
        lastAttendanceData = {k: v.copy() for k, v in DEFAULT_ATTENDANCE.items()}
        course, data = getCourseDataFromQuery(queryEn)
        if course:
            lastCourseContext = {"course": course, "data": data}
            percent = data["attended"] / data["total"] * 100
            answer = f"{course} attendance: {data['attended']}/{data['total']} ({percent:.1f}%)"
            if percent < 75:
                answer += " ⚠️ You are below 75% and are not eligible for the final examination."
            return answer
        lines = []
        for c, d in lastAttendanceData.items():
            pct = d["attended"] / d["total"] * 100
            lines.append(f"• {c}: {d['attended']}/{d['total']} ({pct:.1f}%)")
        return "Your attendance:\n" + "\n".join(lines)

    if intent == "missdays":
        numbers = re.findall(r'\d+', queryEn)
        days = int(numbers[0]) if numbers else 1
        if any(w in cleanText(queryEn) for w in ["overall","all subject","all course","total","whole"]):
            total_attended = sum(d["attended"] for d in lastAttendanceData.values())
            total_classes = sum(d["total"] for d in lastAttendanceData.values())
            new_total = total_classes + days
            new_percent = total_attended / new_total * 100 if new_total else 0
            answer = f"If you miss {days} day(s) overall, your combined attendance would be {total_attended}/{new_total} ({new_percent:.1f}%)."
            if new_percent < 75:
                answer += " ⚠️ Overall attendance below 75% – you may become ineligible for examinations."
            return answer
        course, data = getCourseDataFromQuery(queryEn)
        if not course:
            if lastCourseContext:
                course = lastCourseContext["course"]
                data = lastCourseContext["data"]
            else:
                return "Which course are you asking about? (e.g., Web Engineering)"
        data["total"] += days
        new_percent = data["attended"] / data["total"] * 100
        answer = f"After missing {days} more day(s) in {course}, your attendance is now {data['attended']}/{data['total']} ({new_percent:.1f}%)."
        if new_percent < 75:
            answer += " ⚠️ You are below 75% and are not eligible for the final examination."
        lastCourseContext = {"course": course, "data": data}
        return answer

    if intent == "eligibility":
        total_attended = sum(d["attended"] for d in lastAttendanceData.values())
        total_classes = sum(d["total"] for d in lastAttendanceData.values())
        percent = total_attended / total_classes * 100 if total_classes else 0
        answer = f"Your overall attendance is {percent:.1f}%."
        if percent >= 75:
            answer += " You are eligible for the final examinations."
        else:
            answer += " You are NOT eligible for the final examinations (below 75%)."
        return answer

    if intent == "assignments":
        return "Pending: CS301 Lab 4 (due 10 June), EE202 Project (due 15 June)"
    if intent == "exams":
        q = queryEn.lower()
        if "mid" in q: return "Midterm exams start on 5 July 2026."
        elif "final" in q: return "Final exams start on 20 July 2026."
        else: return "Midterm exams start on 5 July 2026. Final exams start on 20 July 2026."
    if intent == "fees":
        return "Fee status: Paid. Next instalment due: August 2026"
    if intent == "courses":
        return "Your registered courses are:\n" + "\n".join([f"• {c}" for c in DEFAULT_ATTENDANCE.keys()])
    if intent == "timetable":
        return "Monday: CS301 09:00-10:30, EE202 11:00-12:30; Tuesday: MTH401 10:00-11:30"
    if intent == "studyplan":
        prompt = "You are an academic advisor. The student is taking CS301, EE202, MTH401. Create a balanced 7-day study plan with 3-4 hours per day."
        try:
            result = chain.invoke({"question": prompt})
            return result.get("answer", "Unable to generate study plan.")
        except:
            return "Study plan feature is temporarily unavailable."

    if intent == "lowattendance":
        return "Students below 75%: STU0012 (72%), STU0045 (68%), STU0078 (70%)"
    if intent == "ungraded":
        return "Ungraded assignments: CS301 Lab 4 (12 students), EE202 Project (8 students)"
    if intent == "atrisk":
        return "At risk of failure (attendance <60%): STU0012 (58%), STU0089 (55%)"
    if intent == "courseperf":
        return "CS301: avg 72%, EE202: avg 68%, MTH401: avg 75%"

    if intent == "totalstudents":
        return "Total enrolled students: 1,000"
    if intent == "admissionstats":
        return "Admissions 2026: 300 new students (150 CS, 100 BBA, 50 EE)"
    if intent == "feecollection":
        return "Fee collection this semester: 85% (PKR 4.25M of 5M)"
    if intent == "deptperf":
        return "Department average GPA: CS 3.2, EE 3.0, BBA 3.5"

    if intent in ("policy","general"):
        try:
            result = chain.invoke({"question": f"User role: {role}. {queryEn}"})
            return result.get("answer", "I'm not sure how to answer that.") or "I'm not sure how to answer that."
        except:
            return "I'm having trouble processing your request right now."

    return "I didn't understand that. Please try again."

# -------------------- Routes --------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return redirect("/")
        try:
            payload = decodeToken(token)
            request.user = payload
        except ValueError:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        users = read_users()
        user = users.get(username)
        if not user:
            for u in users.values():
                if u["email"] == username:
                    user = u
                    break
        if not user or user["password"] != password:
            error = "Invalid credentials"
        elif user["role"] != role:
            error = f"This account is not a {role}."
        else:
            token = jwt.encode(
                {"userid": user["userid"], "role": user["role"], "exp": datetime.utcnow() + timedelta(hours=1)},
                JWTSECRET, algorithm="HS256"
            )
            log_login(username, user["userid"], user["role"])
            resp = make_response(redirect("/chat"))
            resp.set_cookie("token", token, httponly=True, max_age=3600)
            return resp
    return render_template("login.html", error=error)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        if not role or role not in ("student","faculty","admin"):
            error = "Please select a valid role."
        else:
            users = read_users()
            if username in users or email in users:
                error = "User/email already exists"
            else:
                prefix = {"student":"STU","faculty":"FAC","admin":"ADM"}[role]
                existing = [u for u in users.values() if u["userid"].startswith(prefix)]
                userid = f"{prefix}{len(existing)+1:04d}"
                add_user(username, email, password, userid, role)
                return redirect("/")
    return render_template("signup.html", error=error)

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.delete_cookie("token")
    return resp

@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html")

@app.route("/chat/api", methods=["POST"])
@login_required
def chat_api():
    data = request.get_json()
    message = data.get("message", "")
    language = data.get("language", "en")
    answer = process_chat(request.user["userid"], request.user["role"], request.cookies.get("token"), message, language)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    os.makedirs(CHROMADBDIR, exist_ok=True)
    init_csv()
    chain = get_chain()
    app.run(host="127.0.0.1", port=5000, debug=True)
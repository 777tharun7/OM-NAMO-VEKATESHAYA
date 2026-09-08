from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import sqlite3
import hashlib
import urllib.parse

ROOT = Path(__file__).resolve().parent
INDEX_PATH = ROOT / 'index.html'
DB_PATH = ROOT / 'introvert.db'
API_KEY = os.environ.get('INTROVERT_API_KEY', 'introvert-demo-key')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_states_data_from_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    states_data = {}

    c.execute("SELECT * FROM states")
    states = c.fetchall()

    for state in states:
        state_id = state['id']
        states_data[state_id] = {
            'name': state['name'],
            'tagline': state['tagline'],
            'heroText': state['heroText'],
            'focus': state['focus'],
            'stats': json.loads(state['stats']),
            'communities': [],
            'campaigns': [],
            'events': [],
            'stories': []
        }

        c.execute("SELECT * FROM communities WHERE state_id = ?", (state_id,))
        communities = c.fetchall()
        for community in communities:
            states_data[state_id]['communities'].append({
                'id': community['id'],
                'title': community['title'],
                'city': community['city'],
                'topic': community['topic'],
                'mainDomain': community['mainDomain'],
                'subdomain': community['subdomain'],
                'category': community['category'],
                'pillar': community['pillar'],
                'communityType': community['communityType'],
                'channels': json.loads(community['channels']),
                'members': community['members'],
                'description': community['description']
            })

        c.execute("SELECT * FROM campaigns WHERE state_id = ?", (state_id,))
        campaigns = c.fetchall()
        for campaign in campaigns:
            states_data[state_id]['campaigns'].append({
                'id': campaign['id'],
                'title': campaign['title'],
                'category': campaign['category'],
                'description': campaign['description']
            })

        c.execute("SELECT * FROM events WHERE state_id = ?", (state_id,))
        events = c.fetchall()
        for event in events:
            states_data[state_id]['events'].append({
                'id': event['id'],
                'title': event['title'],
                'date': event['date'],
                'location': event['location'],
                'description': event['description']
            })

        c.execute("SELECT * FROM stories WHERE state_id = ?", (state_id,))
        stories = c.fetchall()
        for story in stories:
            states_data[state_id]['stories'].append({
                'id': story['id'],
                'title': story['title'],
                'text': story['text']
            })

    conn.close()
    return states_data

def get_posts_from_db(state_id=None, pillar=None, scope=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = "SELECT * FROM posts WHERE 1=1"
    params = []

    if state_id and state_id != 'all':
        query += " AND (state_id = ? OR state_id = 'all_india')"
        params.append(state_id)
    if pillar and pillar != 'all':
        query += " AND (pillar = ? OR pillar = 'general')"
        params.append(pillar)
    if scope and scope != 'all':
        query += " AND scope = ?"
        params.append(scope)

    query += " ORDER BY id DESC LIMIT 50"
    c.execute(query, params)
    posts = [dict(row) for row in c.fetchall()]
    conn.close()
    return posts

def get_projects_from_db(pillar=None, state_id=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    query = "SELECT * FROM projects WHERE 1=1"
    params = []
    if pillar and pillar != 'all':
        query += " AND pillar = ?"
        params.append(pillar)
    if state_id and state_id != 'all':
        query += " AND (state_id = ? OR state_id = 'all_india')"
        params.append(state_id)
    query += " ORDER BY id DESC"
    c.execute(query, params)
    projects = [dict(row) for row in c.fetchall()]
    conn.close()
    return projects


def get_user_by_email_and_password(email, password):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    password_hash = hash_password(password)
    c.execute("SELECT * FROM users WHERE email = ? AND password_hash = ?", (email, password_hash))
    user = c.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None


class IntrovertHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code, payload):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, x-api-key, Authorization')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, x-api-key, Authorization')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            body = json.loads(post_data.decode('utf-8'))
        except Exception:
            body = {}

        if path == '/api/auth/register':
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            try:
                c.execute("""
                    INSERT INTO users (name, email, password_hash, role, mobile, emailVerified, mobileVerified, profession, branch, communityDomains, domain, subdomain, rollNo, specialty, verificationId, address, city, state, docName, note, premium, xp, trustScore, badge)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    body.get('name', 'Anonymous Citizen'),
                    body['email'],
                    hash_password(body.get('password', '123456')),
                    body.get('role', 'student'),
                    body.get('mobile', ''),
                    body.get('emailVerified', True),
                    body.get('mobileVerified', True),
                    body.get('profession', body.get('role', 'student')),
                    body.get('branch', 'CSE / AI-ML'),
                    json.dumps(body.get('communityDomains', ['Technology & IT', 'Students & Education'])),
                    body.get('domain', 'Technology & IT'),
                    body.get('subdomain', body.get('specialization', 'AI/ML & State Apps')),
                    body.get('rollNo', 'DEMO-ID-2026'),
                    body.get('specialty', 'AI/ML Engineering'),
                    body.get('verificationId', 'VERIFIED-ID-GOVT'),
                    body.get('address', 'Innovation Hub'),
                    body.get('city', body.get('city', 'Hyderabad')),
                    body.get('state', body.get('state', 'tg')),
                    body.get('docName', 'Verified_Proof.pdf'),
                    body.get('note', 'Onboarded via Verified Eligibility Portal'),
                    body.get('premium', False),
                    body.get('xp', 300),
                    body.get('trustScore', 98),
                    body.get('badge', 'Verified Innovator')
                ))
                user_id = c.lastrowid
                conn.commit()

                user_record = {
                    'id': user_id,
                    'name': body.get('name', 'Anonymous Citizen'),
                    'email': body['email'],
                    'role': body.get('role', 'student'),
                    'profession': body.get('profession', body.get('role', 'student')),
                    'branch': body.get('branch', 'CSE / AI-ML'),
                    'state': body.get('state', 'tg'),
                    'city': body.get('city', 'Hyderabad'),
                    'domain': body.get('domain', 'Technology & IT'),
                    'subdomain': body.get('specialization', 'AI/ML & State Apps'),
                    'xp': 300,
                    'trustScore': 98,
                    'badge': 'Verified Innovator',
                    'premium': False
                }
                self.send_json(201, {'message': 'User verified & registered successfully', 'token': str(user_id), 'user': user_record})
            except sqlite3.IntegrityError:
                self.send_json(409, {'error': 'User with this email already exists'})
            finally:
                conn.close()

        elif path == '/api/auth/login':
            email = body.get('email')
            password = body.get('password')
            user = get_user_by_email_and_password(email, password)
            if user:
                # In a real app, generate a proper JWT token
                token = str(user['id'])
                self.send_json(200, {'message': 'Login successful', 'token': token, 'user': user})
            else:
                self.send_json(401, {'error': 'Invalid credentials'})

        elif path == '/api/posts':
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
                INSERT INTO posts (user_id, author_name, author_role, state_id, scope, pillar, domain, title, content, likes, comments_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                body.get('user_id', 1),
                body.get('author_name', 'Verified Member'),
                body.get('author_role', 'Innovator'),
                body.get('state_id', 'tg'),
                body.get('scope', 'state'),
                body.get('pillar', 'general'),
                body.get('domain', 'Technology & IT'),
                body.get('title', 'Community Update'),
                body.get('content', ''),
                0, 0
            ))
            post_id = c.lastrowid
            conn.commit()
            conn.close()
            self.send_json(201, {'message': 'Post created successfully', 'post_id': post_id})

        elif path == '/api/projects':
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
                INSERT INTO projects (author_name, author_role, pillar, state_id, title, description, roles_needed, members_joined)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                body.get('author_name', 'Verified Lead'),
                body.get('author_role', 'Research Lead'),
                body.get('pillar', 'tech'),
                body.get('state_id', 'tg'),
                body.get('title', 'Research Project Idea'),
                body.get('description', ''),
                body.get('roles_needed', 'Collaborators'),
                1
            ))
            prj_id = c.lastrowid
            conn.commit()
            conn.close()
            self.send_json(201, {'message': 'Project collaboration request posted successfully', 'project_id': prj_id})

        elif path == '/api/memberships':
            community_title = body.get('community')
            user_id = body.get('user_id', 1)
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id FROM communities WHERE title = ?", (community_title,))
            community = c.fetchone()

            if not community:
                self.send_json(404, {'error': 'Community not found'})
                conn.close()
                return

            try:
                c.execute("INSERT INTO memberships (user_id, community_id, status) VALUES (?, ?, ?)", (user_id, community[0], 'Approved'))
                conn.commit()
                self.send_json(201, {'message': 'Joined community successfully', 'community': community_title})
            except sqlite3.IntegrityError:
                self.send_json(200, {'message': 'Already a member', 'community': community_title})
            finally:
                conn.close()

        elif path == '/api/ai/ask':
            query = body.get('query', '').lower()
            role = body.get('role', 'student')
            state = body.get('state', 'all_india')

            ai_response = "Namaste! Bharat AI Assistant at your service. "
            if 'student' in query or role == 'student' or 'project' in query:
                ai_response += f"For students in {state.upper()}: Your home portal automatically unlocks your State & Nearby Campus Hub. Submit your project request in the Research Collaboration Board or join the #state-issue-apps channel to collaborate with professors and peer devs!"
            elif 'police' in query or 'safety' in query:
                ai_response += "For verified law enforcement: Use the Verified Command Channel for inter-commissionerate advisories and instant 1930 Helpline fraud recovery nodes."
            elif 'court' in query or 'legal' in query or 'law' in query:
                ai_response += "For verified legal practitioners: Access the High Court Legal Council for fast-track judgment indexes, arbitration precedents, and citizen legal aid clinics."
            elif 'clean' in query or 'swachh' in query or 'media' in query:
                ai_response += "For Clean India & Media Missions: Post your local ward drive on the Swachh Bharat tracker, mobilize youth creators via the PR channel, and share real progress videos across states!"
            elif 'builder' in query or 'architecture' in query:
                ai_response += "For Builders & Architects: Explore the Smart Infrastructure channel for European green construction guidelines, modular joinery suppliers, and government tender consortiums."
            elif 'game' in query or 'esports' in query:
                ai_response += "For Gaming & Esports: Register your collegiate team in the Bharat Esports Cup and collaborate with Unreal/Unity developers in the Game Dev Lounge!"
            else:
                ai_response += f"Connecting across India's 28 States & 8 UTs: Explore Public Visitor Mode to preview all 25 domains and 8 pillars, or Verify Your ID to enter your custom professional dashboard."

            self.send_json(200, {'answer': ai_response, 'status': 'success'})
        else:
            self.send_json(404, {'error': 'Endpoint not found'})

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        if path in ('/', '/index.html'):
            self.serve_file(INDEX_PATH, 'text/html; charset=utf-8')
            return

        if path == '/api/app-data':
            states_data = get_states_data_from_db()
            posts = get_posts_from_db()
            projects = get_projects_from_db()
            payload = {
                'statesData': states_data,
                'posts': posts,
                'projects': projects,
                'analytics': {'status': 'live', 'ecosystem': 'Bharat Unified Community Platform', 'statesCount': len(states_data)}
            }
            self.send_json(200, payload)
            return

        if path == '/api/posts':
            state_id = query_params.get('state', [None])[0]
            pillar = query_params.get('pillar', [None])[0]
            scope = query_params.get('scope', [None])[0]
            posts = get_posts_from_db(state_id=state_id, pillar=pillar, scope=scope)
            self.send_json(200, {'posts': posts})
            return

        if path == '/api/projects':
            state_id = query_params.get('state', [None])[0]
            pillar = query_params.get('pillar', [None])[0]
            projects = get_projects_from_db(pillar=pillar, state_id=state_id)
            self.send_json(200, {'projects': projects})
            return

        relative_path = path.lstrip('/')
        if not relative_path:
            self.send_error(404, 'Not Found')
            return

        full_path = (ROOT / relative_path).resolve()
        if full_path.exists() and full_path.is_file() and ROOT in full_path.parents:
            content_type = self.get_content_type(full_path)
            self.serve_file(full_path, content_type)
            return

        self.send_error(404, 'Not Found')

    def get_content_type(self, path):
        suffix = path.suffix.lower()
        if suffix == '.css':
            return 'text/css; charset=utf-8'
        if suffix == '.js':
            return 'application/javascript; charset=utf-8'
        if suffix == '.json':
            return 'application/json; charset=utf-8'
        if suffix in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}:
            return 'image/' + ('svg+xml' if suffix == '.svg' else suffix.lstrip('.'))
        return 'application/octet-stream'

    def serve_file(self, path, content_type):
        if not path.exists():
            self.send_error(404, 'Not Found')
            return
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(path.read_bytes())


def run_server(port=8001):
    server = ThreadingHTTPServer(('0.0.0.0', port), IntrovertHandler)
    print(f'Serving Bharat Connect on http://127.0.0.1:{port}')
    server.serve_forever()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    run_server(port)

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX_PATH = ROOT / 'index.html'


def load_states_data():
    return {
        'ap': {
            'name': 'Andhra Pradesh',
            'tagline': 'State-level collaboration with professional, civic, education, media, and local-area communities.',
            'heroText': 'Andhra Pradesh can grow fast through connected students, teachers, government servants, police, lawyers, IT employees, creators, and local leaders.',
            'focus': 'Tech + Civic + Local Growth',
            'stats': {'communities': 6, 'events': 4, 'actions': 1420},
            'communities': [
                {'title': 'Tech Community AP', 'city': 'Visakhapatnam', 'topic': 'Technology', 'members': 214, 'description': 'IT employees, developers, and startups sharing updates and collaboration opportunities.'},
                {'title': 'Student & Teacher Network', 'city': 'Vijayawada', 'topic': 'Education', 'members': 186, 'description': 'Students and teachers connecting for better learning and curriculum growth.'},
                {'title': 'CSE/ECE/EEE Student Circle', 'city': 'Vijayawada', 'topic': 'Student Community', 'members': 245, 'description': 'Students from CSE, ECE, EEE, Civil, and Mechanical branches sharing notes, campus updates, and career guidance.', 'audience': 'student', 'branchTags': ['cse', 'ece', 'eee', 'civil', 'mechanical']},
                {'title': 'Police & Public Safety Circle', 'city': 'Guntur', 'topic': 'Public Service', 'members': 142, 'description': 'Police, officers, and civic leaders discussing safer and smarter public coordination.'},
                {'title': 'Law & Governance Forum', 'city': 'Tirupati', 'topic': 'Law & Governance', 'members': 126, 'description': 'Lawyers, collectors, and government servants sharing legal and civic insights.'},
                {'title': 'Law & Courtroom Network', 'city': 'Tirupati', 'topic': 'Legal Community', 'members': 134, 'description': 'Lawyers, legal interns, and public servants sharing courtroom awareness, legal updates, and civic action.', 'audience': 'lawyer', 'branchTags': ['law']},
                {'title': 'Media & Creator Network', 'city': 'Rajahmundry', 'topic': 'News & Content', 'members': 158, 'description': 'PR professionals, reporters, TV channels, and content creators spreading awareness fast.'},
                {'title': 'Orthopedic & Dermatology Circle', 'city': 'Visakhapatnam', 'topic': 'Medical Specialty', 'members': 112, 'description': 'Doctors in orthopedics, dermatology, and related specialties coordinating outreach and shared medical learning.', 'audience': 'doctor', 'specialtyTags': ['orthopedic', 'dermatology', 'medicine']},
                {'title': 'Nearby Area Connect', 'city': 'Kurnool', 'topic': 'Local Community', 'members': 98, 'description': 'Sub-community spaces for nearby locality coordination, events, and local action.'}
            ],
            'campaigns': [
                {'title': 'Clean Village & City Drive', 'category': 'Civic', 'description': 'A state campaign focused on local cleanliness, awareness, and public participation.'},
                {'title': 'Digital Skill Growth Week', 'category': 'Technology', 'description': 'Connect students, IT employees, and educators around practical digital skill-building.'}
            ],
            'events': [
                {'title': 'AP Community Connect Meetup', 'date': 'Aug 4, 2026', 'location': 'Visakhapatnam', 'description': 'Bring together educators, tech professionals, and community leaders.'},
                {'title': 'Public Awareness Walk', 'date': 'Aug 8, 2026', 'location': 'Vijayawada', 'description': 'A civic event focused on cleanliness and local responsibility.'},
                {'title': 'Media & Creator Forum', 'date': 'Aug 12, 2026', 'location': 'Rajahmundry', 'description': 'PR, news, and creators discuss fast awareness and impact.'},
                {'title': 'Nearby Area Volunteer Day', 'date': 'Aug 16, 2026', 'location': 'Kurnool', 'description': 'Local-area collaboration for neighborhood growth and support.'}
            ],
            'stories': [
                {'title': 'From professional circles to public impact', 'text': 'IT employees, teachers, and public servants are now collaborating on local growth.'},
                {'title': 'Strong sub-communities for nearby areas', 'text': 'Local-area groups make it easier to act fast and stay connected.'}
            ]
        },
        'tg': {
            'name': 'Telangana',
            'tagline': 'Fast-growing state communities for education, governance, technology, media, and local action.',
            'heroText': 'Telangana can grow quickly by connecting students, teachers, police, government servants, lawyers, IT employees, creators, and local leaders in one platform.',
            'focus': 'Public Service + Tech + Awareness',
            'stats': {'communities': 6, 'events': 4, 'actions': 1360},
            'communities': [
                {'title': 'Tech Community TG', 'city': 'Hyderabad', 'topic': 'Technology', 'members': 238, 'description': 'Developers, IT employees, and startups building innovation together.'},
                {'title': 'Edu Leaders Circle', 'city': 'Warangal', 'topic': 'Education', 'members': 174, 'description': 'Students, teachers, and academic leaders sharing updates and support.'},
                {'title': 'CSE/ECE/EEE Student Circle', 'city': 'Warangal', 'topic': 'Student Community', 'members': 252, 'description': 'Students from CSE, ECE, EEE, Civil, and Mechanical branches sharing campus updates, clearer learning, and career support.', 'audience': 'student', 'branchTags': ['cse', 'ece', 'eee', 'civil', 'mechanical']},
                {'title': 'Police & Civic Coordination', 'city': 'Karimnagar', 'topic': 'Public Service', 'members': 132, 'description': 'A platform for coordination, planning, and safer communities.'},
                {'title': 'Law & Administration Forum', 'city': 'Nizamabad', 'topic': 'Law & Governance', 'members': 118, 'description': 'Lawyers, collectors, and government servants sharing governance insight.'},
                {'title': 'Medical & Public Health Circle', 'city': 'Hyderabad', 'topic': 'Medical Community', 'members': 142, 'description': 'Doctors, public health workers, and specialists sharing outreach plans, health awareness, and cross-specialty collaboration.', 'audience': 'doctor', 'specialtyTags': ['medical', 'health', 'public health']},
                {'title': 'News & Creator Hub', 'city': 'Khammam', 'topic': 'News & Content', 'members': 152, 'description': 'PR professionals, reporters, and content creators spreading awareness and updates.'},
                {'title': 'Nearby Area Community', 'city': 'Suryapet', 'topic': 'Local Community', 'members': 104, 'description': 'Sub-community spaces for local area events, support, and neighborhood action.'}
            ],
            'campaigns': [
                {'title': 'Smart City Awareness Week', 'category': 'Civic', 'description': 'A campaign focused on cleanliness, awareness, and local improvement.'},
                {'title': 'Future Skills Telangana', 'category': 'Technology', 'description': 'Connect students and professionals around digital growth and opportunity.'}
            ],
            'events': [
                {'title': 'Telangana Community Growth Meetup', 'date': 'Aug 5, 2026', 'location': 'Hyderabad', 'description': 'A meeting for educators, professionals, and local leaders.'},
                {'title': 'Clean Surface Drive', 'date': 'Aug 9, 2026', 'location': 'Warangal', 'description': 'A public drive for cleanliness and awareness.'},
                {'title': 'Media Awareness Forum', 'date': 'Aug 13, 2026', 'location': 'Khammam', 'description': 'News, PR, and creators sharing community stories and campaigns.'},
                {'title': 'Local Area Volunteer Day', 'date': 'Aug 17, 2026', 'location': 'Suryapet', 'description': 'A neighborhood event for support, coordination, and local growth.'}
            ],
            'stories': [
                {'title': 'Fast state-level collaboration', 'text': 'Multiple sectors are now connected through a single shared platform.'},
                {'title': 'Local action scales quickly', 'text': 'Nearby-area communities make it easier to turn ideas into real impact.'}
            ]
        }
    }


class IntrovertHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path == '/':
            self.serve_file(INDEX_PATH, 'text/html; charset=utf-8')
            return

        if path == '/api/app-data':
            self.handle_app_data()
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

    def do_OPTIONS(self):
        if self.path == '/api/app-data':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, x-api-key')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.end_headers()
            return
        self.send_error(404)

    def handle_app_data(self):
        api_key = self.headers.get('x-api-key')
        if not api_key or api_key != 'introvert-demo-key':
            self.send_response(401)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid API key'}).encode())
            return

        payload = {
            'statesData': load_states_data(),
            'analytics': {'status': 'live', 'source': 'python-backend'}
        }
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def get_content_type(self, path):
        suffix = path.suffix.lower()
        if suffix == '.css':
            return 'text/css; charset=utf-8'
        if suffix == '.js':
            return 'application/javascript; charset=utf-8'
        if suffix == '.json':
            return 'application/json; charset=utf-8'
        if suffix in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
            return 'image/' + suffix.lstrip('.')
        return 'application/octet-stream'

    def serve_file(self, path, content_type):
        if not path.exists():
            self.send_error(404, 'Not Found')
            return
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(path.read_bytes())


def run_server(port=8001):
    server = ThreadingHTTPServer(('127.0.0.1', port), IntrovertHandler)
    print(f'Serving Introvert app on http://127.0.0.1:{port}')
    server.serve_forever()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    run_server(port)

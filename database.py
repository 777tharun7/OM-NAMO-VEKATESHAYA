import sqlite3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / 'introvert.db'

def load_states_data():
    return {
        'all_india': {
            'name': '🇮🇳 All-India National Hub',
            'tagline': 'Unified National Community Ecosystem connecting 1.4 Billion citizens, professionals & creators.',
            'heroText': 'Empowering India’s transformation into a developed nation through cross-sector collaboration across tech, education, law, governance, civic infrastructure, and youth innovation.',
            'focus': 'National Integration + Tech Sovereignty + Civic Progress',
            'stats': {'communities': 148, 'events': 34, 'actions': 85400, 'members': 1250000},
            'communities': [
                {
                    'title': 'Bharat Cyber & AI Guild',
                    'city': 'Pan-India',
                    'topic': 'Technology & IT',
                    'mainDomain': 'Technology & IT',
                    'subdomain': 'AI & Cyber Defense',
                    'category': 'National Tech Sovereignty',
                    'pillar': 'tech',
                    'communityType': 'Verified',
                    'channels': ['General', 'AI-Research', 'Cyber-Defense', 'Open-Source', 'Jobs-Referrals', 'Voice-Stage'],
                    'members': 42800,
                    'description': 'Pan-India network of IT professionals, AI researchers, and cybersecurity experts building open sovereign technologies for India.'
                },
                {
                    'title': 'National Student Curriculum & Innovation Hub',
                    'city': 'Pan-India',
                    'topic': 'Students & Education',
                    'mainDomain': 'Students & Education',
                    'subdomain': 'Engineering & Higher Ed',
                    'category': 'Education Reform & Projects',
                    'pillar': 'education',
                    'communityType': 'College',
                    'channels': ['General', 'Syllabus-Upgrades', 'Hackathons', 'AI-ML-Specialization', 'Mentorship', 'Showcase'],
                    'members': 68500,
                    'description': 'Students and professors collaborating on cutting-edge curriculum, real-world state problem solvers, and AI/ML project specialization.'
                },
                {
                    'title': 'Fast-Track Justice & Legal Reform Council',
                    'city': 'New Delhi',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'Judiciary & Fast-Track Courts',
                    'category': 'Legal Excellence',
                    'pillar': 'legal',
                    'communityType': 'Verified',
                    'channels': ['General', 'Fast-Track-Judgments', 'Case-Precedents', 'Legal-Aid-Clinics', 'Law-Students'],
                    'members': 18900,
                    'description': 'Senior advocates, judicial clerks, law students, and legal scholars advancing fast-track court efficiency and citizen legal awareness.'
                },
                {
                    'title': 'All-India Police & Civil Administration Alliance',
                    'city': 'Pan-India',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'Police & Civil Services',
                    'category': 'Public Safety & Rapid Governance',
                    'pillar': 'police',
                    'communityType': 'Verified',
                    'channels': ['General', 'Inter-State-Advisory', 'Cyber-Crime-Alerts', 'Disaster-Response', 'Community-Policing'],
                    'members': 24300,
                    'description': 'DGP, SP, CI, SI officers, HAS, and administrative officials sharing rapid advisories, crime-prevention tactics, and local area justice.'
                },
                {
                    'title': 'Swachh Bharat & National Media Mission',
                    'city': 'Pan-India',
                    'topic': 'Entertainment',
                    'mainDomain': 'Entertainment',
                    'subdomain': 'PR, Media & Civic Awareness',
                    'category': 'Clean India & Verified News',
                    'pillar': 'media',
                    'communityType': 'Verified',
                    'channels': ['General', 'Clean-City-Drives', 'Verified-News-Stream', 'Viral-Awareness-Creatives', 'Volunteer-Ops'],
                    'members': 35400,
                    'description': 'Journalists, PR marketers, ad makers, content creators, and volunteers organizing nationwide cleanliness drives and factual progress reporting.'
                },
                {
                    'title': 'Indian Builders & Smart Architecture Guild',
                    'city': 'Pan-India',
                    'topic': 'Real Estate',
                    'mainDomain': 'Real Estate',
                    'subdomain': 'Architecture & Smart Housing',
                    'category': 'World-Class Infrastructure',
                    'pillar': 'builders',
                    'communityType': 'Verified',
                    'channels': ['General', 'Modern-Apartments', 'Sustainable-Interiors', 'Premium-Furniture-Design', 'Govt-Tenders'],
                    'members': 29600,
                    'description': 'Civil contractors, visionary architects, interior designers, and furniture creators elevating Indian urban living to global standards.'
                },
                {
                    'title': 'Rashtriya Citizen Voice & Grassroots Ideation',
                    'city': 'Pan-India',
                    'topic': 'NGOs & Social Impact',
                    'mainDomain': 'NGOs & Social Impact',
                    'subdomain': 'Grassroots Democracy',
                    'category': 'Citizen Ideation',
                    'pillar': 'citizen',
                    'communityType': 'Public',
                    'channels': ['General', 'Policy-Proposals', 'State-Problem-Solvers', 'Youth-Voices', 'Polls-Debates'],
                    'members': 89200,
                    'description': 'Direct voice for every Indian citizen to submit national improvement ideas, vote on policy proposals, and mobilize local change.'
                },
                {
                    'title': 'Bharat Gaming & Esports Arena',
                    'city': 'Pan-India',
                    'topic': 'Gaming',
                    'mainDomain': 'Gaming',
                    'subdomain': 'Esports & Game Development',
                    'category': 'Gaming League & Indie Devs',
                    'pillar': 'gaming',
                    'communityType': 'Public',
                    'channels': ['General', 'Esports-Tournaments', 'Game-Dev-Unreal-Unity', 'Streaming-Hub', 'Team-Recruit'],
                    'members': 52100,
                    'description': 'Esports athletes, mobile gamers, indie Indian game developers, and streamers building India’s gaming championship ecosystem.'
                }
            ],
            'campaigns': [
                {'title': 'Mission Viksit Bharat 2047', 'category': 'National Mission', 'description': 'Transforming India into a high-income developed powerhouse through technology, civic hygiene, and inter-state knowledge sharing.'},
                {'title': 'National Clean Cities & Waterways Drive', 'category': 'Civic & Environment', 'description': 'Unifying 500+ cities in coordinated weekly volunteer cleanliness blitzes led by creators and local youth.'},
                {'title': 'AI for Bharat: 1 Million Developers', 'category': 'Technology', 'description': 'Upskilling engineering students across tier-2 and tier-3 colleges in generative AI and sovereign LLM tooling.'}
            ],
            'events': [
                {'title': 'India National Tech & Innovation Summit', 'date': 'Aug 25, 2026', 'location': 'New Delhi / Hybrid', 'description': 'Keynote from leading IT chiefs, startup founders, and government secretaries on India tech expansion.'},
                {'title': 'All-India Cleanliness Hackathon', 'date': 'Sep 2, 2026', 'location': 'Pan-India Virtual', 'description': 'Engineering students and municipal leaders building smart waste-tracking and civic reporting tools.'},
                {'title': 'Bharat Esports National Cup', 'date': 'Sep 10, 2026', 'location': 'Bengaluru & Online', 'description': 'State champions clash in national gaming championships with prizes and developer showcases.'}
            ],
            'stories': [
                {'title': 'Unifying 28 States Through Real-Time Collaboration', 'text': 'How seamless digital cross-pollination is accelerating problem-solving in governance and engineering.'},
                {'title': 'From Local Wards to National Recognition', 'text': 'Neighborhood volunteer teams in Andhra and Telangana are setting benchmarks for nationwide replication.'}
            ]
        },
        'tg': {
            'name': 'Telangana',
            'tagline': 'Fast-growing innovation state for AI, IT, Governance, Education & Smart Urban Living.',
            'heroText': 'Telangana is surging ahead as India’s premier innovation engine by connecting students, IT specialists, police, lawyers, creators, and civic builders in one unified hub.',
            'focus': 'Hyderabad AI Hub + Public Safety + Smart Urban Living',
            'stats': {'communities': 28, 'events': 14, 'actions': 28400, 'members': 340000},
            'communities': [
                {
                    'title': 'Hyderabad Tech & Cyber Collective',
                    'city': 'Hyderabad',
                    'topic': 'Technology & IT',
                    'mainDomain': 'Technology & IT',
                    'subdomain': 'Cloud & AI/ML',
                    'category': 'IT Guild',
                    'pillar': 'tech',
                    'communityType': 'Verified',
                    'channels': ['General', 'Cloud-Native', 'Cyber-Security', 'Startup-Demos', 'Jobs-Referrals'],
                    'members': 14200,
                    'description': 'HITEC City & Financial District engineers sharing tech upgrades, cybersecurity protocols, and open-source contributions.'
                },
                {
                    'title': 'Telangana State Student & Faculty Network',
                    'city': 'Hyderabad',
                    'topic': 'Students & Education',
                    'mainDomain': 'Students & Education',
                    'subdomain': 'Engineering & Research',
                    'category': 'Campus Collaboration',
                    'pillar': 'education',
                    'communityType': 'College',
                    'channels': ['General', 'State-Issue-Apps', 'AIML-Specialization', 'JNTU-OU-Curriculum', 'Placements'],
                    'members': 21400,
                    'description': 'Students from JNTU, Osmania, IIIT Hyderabad, and Kakatiya building state apps and mastering modern AI/ML curriculum.'
                },
                {
                    'title': 'Telangana High Court & Fast-Track Legal Forum',
                    'city': 'Hyderabad',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'High Court & Fast-Track Courts',
                    'category': 'Legal Advisory',
                    'pillar': 'legal',
                    'communityType': 'Verified',
                    'channels': ['General', 'Fast-Track-Benches', 'Commercial-Disputes', 'Free-Legal-Aid', 'Bar-Council-Updates'],
                    'members': 5400,
                    'description': 'Advocates, legal aid volunteers, and law graduates discussing fast-track case dispatch and judicial tech integration.'
                },
                {
                    'title': 'Telangana Police & Civil Safety Coordination',
                    'city': 'Hyderabad',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'Police & Civil Services',
                    'category': 'Smart Policing',
                    'pillar': 'police',
                    'communityType': 'Verified',
                    'channels': ['General', 'Commissionerates-Advisory', 'Traffic-Safety', 'Cyber-Fraud-War-Room', 'She-Teams'],
                    'members': 7800,
                    'description': 'Hyderabad, Cyberabad, Rachakonda, and district police units coordinating with civil employees for rapid emergency action.'
                },
                {
                    'title': 'Swachh Telangana & Digital Creators Hub',
                    'city': 'Warangal',
                    'topic': 'Entertainment',
                    'mainDomain': 'Entertainment',
                    'subdomain': 'PR & Content Creators',
                    'category': 'Clean City & Public Awareness',
                    'pillar': 'media',
                    'communityType': 'Verified',
                    'channels': ['General', 'Clean-Hyderabad-Drive', 'Telugu-Content-Creators', 'Civic-Awareness-Vlogs', 'Broadcasts'],
                    'members': 9600,
                    'description': 'Creators, TV reporters, and influencers spearheading clean city campaigns across Musi rejuvenation, Warangal, and Nizamabad.'
                },
                {
                    'title': 'Hyderabad Builders & Luxury Architecture Guild',
                    'city': 'Hyderabad',
                    'topic': 'Real Estate',
                    'mainDomain': 'Real Estate',
                    'subdomain': 'Smart Infrastructure & Interior',
                    'category': 'Foreign-Grade Construction',
                    'pillar': 'builders',
                    'communityType': 'Verified',
                    'channels': ['General', 'Skyscrapers-West-Hyd', 'Green-Architecture', 'Premium-Interiors', 'Smart-Material-Procure'],
                    'members': 8100,
                    'description': 'Architects, contractors, and interior designers building world-class gated communities, foreign-standard villas, and modular spaces.'
                },
                {
                    'title': 'Telangana Esports & Game Guild',
                    'city': 'Hyderabad',
                    'topic': 'Gaming',
                    'mainDomain': 'Gaming',
                    'subdomain': 'Mobile & PC Esports',
                    'category': 'Competitive Gaming',
                    'pillar': 'gaming',
                    'communityType': 'Public',
                    'channels': ['General', 'BGMI-TG-Tournaments', 'Valorant-Lobbies', 'Game-Designers', 'Streams'],
                    'members': 12300,
                    'description': 'Competitive gamers and indie studios in Hyderabad creating Telugu and Indian localized game worlds.'
                },
                {
                    'title': 'AgriTech Telangana Farmers Forum',
                    'city': 'Karimnagar',
                    'topic': 'Agriculture',
                    'mainDomain': 'Agriculture',
                    'subdomain': 'AgriTech & Irrigation',
                    'category': 'Smart Farming',
                    'pillar': 'tech',
                    'communityType': 'Local',
                    'channels': ['General', 'Crop-Yield-AI', 'Drip-Irrigation', 'Market-Prices', 'Subsidies'],
                    'members': 6700,
                    'description': 'Cotton, paddy, and chilli farmers utilizing digital sensors, precision drone spraying, and government scheme updates.'
                }
            ],
            'campaigns': [
                {'title': 'Clean Musi & Green Hyderabad Drive', 'category': 'Civic & Environment', 'description': 'Multi-ward cleanliness, waste segregation, and green canopy plantation across Hyderabad & Secunderabad.'},
                {'title': 'Telangana AI Academy: 50,000 Engineers', 'category': 'Technology', 'description': 'Upskilling tier-2 engineering graduates in Nizamabad, Khammam, and Warangal with high-paying tech skills.'},
                {'title': 'Zero-Cyber-Fraud Awareness Mission', 'category': 'Public Safety', 'description': 'Statewide public education campaign on digital payment safety and rapid reporting mechanisms.'}
            ],
            'events': [
                {'title': 'T-Hub Mega Founder & Student Mixer', 'date': 'Aug 26, 2026', 'location': 'T-Hub, Hyderabad', 'description': 'Connecting 500 student innovators with venture capital and state incubators.'},
                {'title': 'Warangal Smart Heritage Cleanliness Drive', 'date': 'Aug 30, 2026', 'location': 'Warangal Fort & City', 'description': 'Civic volunteers and creators restoring historical monuments and public sanitation.'},
                {'title': 'Telangana Bar Council Fast-Track Seminar', 'date': 'Sep 4, 2026', 'location': 'Hyderabad High Court Annexe', 'description': 'Interactive workshop on AI-driven legal search and fast disposal of consumer disputes.'}
            ],
            'stories': [
                {'title': 'How Warangal Students Created a City Grievance App', 'text': 'Connected students and municipal commissioners built a 24-hour pothole and drainage resolution system.'},
                {'title': 'Smart Policing in Cyberabad Reaches Zero Response Delay', 'text': 'Inter-departmental messaging enabled rapid incident mitigation in IT corridor traffic hubs.'}
            ]
        },
        'ap': {
            'name': 'Andhra Pradesh',
            'tagline': 'State-level collaboration across Sunrise Coastline, AI Tech, Agri, Law & Port Infrastructure.',
            'heroText': 'Andhra Pradesh is unleashing its immense coastal, agricultural, educational, and tech potential by connecting students, teachers, builders, police, and advocates.',
            'focus': 'Vizag Tech Port + AgriTech + Amaravati Capital Build',
            'stats': {'communities': 26, 'events': 12, 'actions': 24900, 'members': 310000},
            'communities': [
                {
                    'title': 'Vizag AI & Coastal Tech Guild',
                    'city': 'Visakhapatnam',
                    'topic': 'Technology & IT',
                    'mainDomain': 'Technology & IT',
                    'subdomain': 'AI, Web & Cloud',
                    'category': 'Coastal Tech Hub',
                    'pillar': 'tech',
                    'communityType': 'Verified',
                    'channels': ['General', 'AI-Builders', 'Port-Logistics-Software', 'Cyber-Security', 'Jobs'],
                    'members': 11800,
                    'description': 'Visakhapatnam tech corridor engineers and tech founders developing smart logistics, AI, and enterprise software.'
                },
                {
                    'title': 'AP Student & Teacher Academic Network',
                    'city': 'Vijayawada',
                    'topic': 'Students & Education',
                    'mainDomain': 'Students & Education',
                    'subdomain': 'Engineering, Medical & Diploma',
                    'category': 'Academic Excellence',
                    'pillar': 'education',
                    'communityType': 'College',
                    'channels': ['General', 'Curriculum-Upgrades', 'State-Issue-Solvers', 'AIML-Specialization', 'Campus-Drives'],
                    'members': 19500,
                    'description': 'AU, JNTUK, JNTUA, and SRM-AP students collaborating with teachers to build local state solutions and crack global placements.'
                },
                {
                    'title': 'AP High Court & Fast-Track Legal Circle',
                    'city': 'Amaravati',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'High Court & Fast-Track Courts',
                    'category': 'Judicial Dispatch',
                    'pillar': 'legal',
                    'communityType': 'Verified',
                    'channels': ['General', 'Fast-Track-Cases', 'Coastal-Land-Laws', 'Pro-Bono-Clinic', 'Judicial-Updates'],
                    'members': 4800,
                    'description': 'Legal practitioners and law faculty in Amaravati and Visakhapatnam streamlining speedy dispute resolution.'
                },
                {
                    'title': 'AP Police & Law Enforcement Network',
                    'city': 'Vijayawada',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'Police & Civil Services',
                    'category': 'Law & Order Coordination',
                    'pillar': 'police',
                    'communityType': 'Verified',
                    'channels': ['General', 'Coastal-Security', 'Highway-Patrol', 'Cyber-Crime-War-Room', 'Citizen-Help'],
                    'members': 6900,
                    'description': 'Statewide IPS, SP, CI, and SI officers coordinating emergency responses, highway safety, and district law enforcement.'
                },
                {
                    'title': 'Swachh Andhra & Coastal Media Alliance',
                    'city': 'Rajahmundry',
                    'topic': 'Entertainment',
                    'mainDomain': 'Entertainment',
                    'subdomain': 'PR, Media & Cleanliness',
                    'category': 'Clean Andhra Mission',
                    'pillar': 'media',
                    'communityType': 'Verified',
                    'channels': ['General', 'Clean-Godavari-Drive', 'Beach-Sanitation', 'Verified-News', 'Creator-Workshops'],
                    'members': 8400,
                    'description': 'Content creators, reporters, and volunteer squads organizing Clean Beach drives in Vizag and Godavari river conservation.'
                },
                {
                    'title': 'Amaravati & Coastal Builders Guild',
                    'city': 'Amaravati',
                    'topic': 'Real Estate',
                    'mainDomain': 'Real Estate',
                    'subdomain': 'Capital City Infrastructure & Architecture',
                    'category': 'World-Class Urban Architecture',
                    'pillar': 'builders',
                    'communityType': 'Verified',
                    'channels': ['General', 'Amaravati-Master-Plan', 'Foreign-Standard-Villas', 'Smart-Interiors', 'Port-Infra'],
                    'members': 7300,
                    'description': 'Contractors, civil engineers, and master architects building sustainable smart cities, luxury apartments, and modern commercial hubs.'
                },
                {
                    'title': 'Andhra Esports & Gaming League',
                    'city': 'Visakhapatnam',
                    'topic': 'Gaming',
                    'mainDomain': 'Gaming',
                    'subdomain': 'Mobile Esports & Streaming',
                    'category': 'Esports League',
                    'pillar': 'gaming',
                    'communityType': 'Public',
                    'channels': ['General', 'AP-Esports-Championship', 'Valorant-Squads', 'Game-Dev-Vizag', 'Streams'],
                    'members': 10500,
                    'description': 'Passionate gamers and young developers competing in state leagues and building regional gaming assets.'
                },
                {
                    'title': 'AgriTech Coastal & Rayalaseema Circle',
                    'city': 'Guntur',
                    'topic': 'Agriculture',
                    'mainDomain': 'Agriculture',
                    'subdomain': 'Aqua Farming & Chilli AgriTech',
                    'category': 'Agri Export & Farming',
                    'pillar': 'tech',
                    'communityType': 'Local',
                    'channels': ['General', 'Aqua-Tech-Sensors', 'Chilli-Tobacco-Trading', 'Drip-Rayalaseema', 'Market-Live'],
                    'members': 9100,
                    'description': 'Aquaculture farmers, chilli growers, and agri-entrepreneurs adopting smart IoT water testing and export logistics.'
                }
            ],
            'campaigns': [
                {'title': 'Clean Beaches of Vizag & Coastal Rejuvenation', 'category': 'Civic & Environment', 'description': 'Cleaning 974 km of Andhra coastline with youth volunteers, fishermen communities, and local authorities.'},
                {'title': 'Amaravati Green Capital Initiative', 'category': 'Architecture & Urban', 'description': 'Adopting European and Singapore standard green building codes for commercial and residential developments.'},
                {'title': 'Digital Rayalaseema Tech Upskilling', 'category': 'Education & Tech', 'description': 'Bringing high-tech AI, data science, and cloud bootcamps to Tirupati, Kurnool, and Anantapur students.'}
            ],
            'events': [
                {'title': 'Vizag International Tech Expo', 'date': 'Aug 28, 2026', 'location': 'Visakhapatnam Convention Centre', 'description': 'Showcasing coastal AI startups, port automation, and enterprise engineering solutions.'},
                {'title': 'Vijayawada Clean Riverfront Action Day', 'date': 'Sep 1, 2026', 'location': 'Krishna Riverfront, Vijayawada', 'description': 'Civic leaders, media, and citizens uniting for riverside sanitation and tree planting.'},
                {'title': 'Amaravati Legal & Judicial Tech Conclave', 'date': 'Sep 6, 2026', 'location': 'High Court Complex, Amaravati', 'description': 'Speedy justice through modern case tracking and automated e-filing masterclasses.'}
            ],
            'stories': [
                {'title': 'From Fishermen Villages to Smart IoT Monitoring', 'text': 'How connected coastal youth deployed solar salinity monitors to protect shrimp yields.'},
                {'title': 'Vijayawada High-Speed Placement Revolution', 'text': 'Connected alumni and teachers from Tier-2 colleges helped 4,000 students secure top tech positions.'}
            ]
        },
        'ka': {
            'name': 'Karnataka',
            'tagline': 'India’s Silicon Silicon Hub leading DeepTech, Aerospace, Biotech & Smart Governance.',
            'heroText': 'Connecting Bengaluru’s world-renowned tech power with Mysuru, Hubballi, and Mangaluru to build a developed, clean, and technologically unmatched state.',
            'focus': 'Silicon Valley of India + DeepTech + Clean Bengaluru',
            'stats': {'communities': 32, 'events': 18, 'actions': 39200, 'members': 480000},
            'communities': [
                {
                    'title': 'Bengaluru DeepTech & AI Architects',
                    'city': 'Bengaluru',
                    'topic': 'Technology & IT',
                    'mainDomain': 'Technology & IT',
                    'subdomain': 'AI, Quantum & Chips',
                    'category': 'DeepTech Leadership',
                    'pillar': 'tech',
                    'communityType': 'Verified',
                    'channels': ['General', 'GenAI-LLMs', 'Semiconductor-Design', 'SaaS-Founders', 'Hiring-Board'],
                    'members': 28500,
                    'description': 'Silicon City software engineers, chip architects, and startup founders driving next-generation global software from India.'
                },
                {
                    'title': 'Karnataka Higher Education & University Circle',
                    'city': 'Bengaluru',
                    'topic': 'Students & Education',
                    'mainDomain': 'Students & Education',
                    'subdomain': 'IISc, VTU & Research',
                    'category': 'Research & Skills',
                    'pillar': 'education',
                    'communityType': 'College',
                    'channels': ['General', 'Curriculum-Evolution', 'DeepTech-Projects', 'AI-ML-Tracks', 'Hackathons'],
                    'members': 24000,
                    'description': 'Students and professors across VTU, IISc, IIIT-B, and PES University building deep engineering solutions.'
                },
                {
                    'title': 'Karnataka High Court & Fast-Track Commercial Bench',
                    'city': 'Bengaluru',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'High Court & Commercial Courts',
                    'category': 'Speedy Commercial Justice',
                    'pillar': 'legal',
                    'communityType': 'Verified',
                    'channels': ['General', 'Commercial-Disputes', 'IP-Patents-Law', 'Fast-Track-Tribunals', 'Legal-Tech'],
                    'members': 6200,
                    'description': 'Advocates, patent attorneys, and arbitration experts solving commercial and civic cases with rapid turnaround.'
                },
                {
                    'title': 'Bengaluru City Police & KSP Administration',
                    'city': 'Bengaluru',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'Police & Civil Safety',
                    'category': 'Tech-Enabled Policing',
                    'pillar': 'police',
                    'communityType': 'Verified',
                    'channels': ['General', 'Traffic-Management-AI', 'Cyber-Crime-Bureau', 'Women-Safety-Nirbhaya', 'Local-Station-Alerts'],
                    'members': 9100,
                    'description': 'Bengaluru City Police, Karnataka State Police, and civic administrative officers coordinating AI-driven urban safety.'
                },
                {
                    'title': 'Clean Bengaluru & Karnataka Media Guild',
                    'city': 'Bengaluru',
                    'topic': 'Entertainment',
                    'mainDomain': 'Entertainment',
                    'subdomain': 'Civic PR & Creator Hub',
                    'category': 'Swachh Bengaluru & Truth Media',
                    'pillar': 'media',
                    'communityType': 'Verified',
                    'channels': ['General', 'Clean-Lakes-Campaign', 'Waste-Segregation-Drive', 'Kannada-Creators', 'Impact-News'],
                    'members': 11400,
                    'description': 'Media professionals, lake conservationists, and content creators mobilizing neighborhood cleanup drives across Bengaluru and Mysuru.'
                },
                {
                    'title': 'Karnataka Master Builders & Luxury Architecture Guild',
                    'city': 'Bengaluru',
                    'topic': 'Real Estate',
                    'mainDomain': 'Real Estate',
                    'subdomain': 'Sustainable Urban Architecture',
                    'category': 'Global Standard Real Estate',
                    'pillar': 'builders',
                    'communityType': 'Verified',
                    'channels': ['General', 'Biophilic-Apartments', 'Italian-Interiors-Furniture', 'Smart-City-Infra', 'Green-Certification'],
                    'members': 9800,
                    'description': 'Elite architects, interior artists, and master builders bringing international Scandinavian and Japanese designs to Indian homes.'
                },
                {
                    'title': 'Bengaluru Esports & Game Developers Hub',
                    'city': 'Bengaluru',
                    'topic': 'Gaming',
                    'mainDomain': 'Gaming',
                    'subdomain': 'AAA Game Dev & Esports',
                    'category': 'Game Dev Capital',
                    'pillar': 'gaming',
                    'communityType': 'Public',
                    'channels': ['General', 'Unreal-Engine-India', 'Esports-Pro-Scrims', 'Unity-Devs', 'Console-Gaming'],
                    'members': 16800,
                    'description': 'India’s largest hub of game developers, 3D artists, sound designers, and pro esports athletes.'
                }
            ],
            'campaigns': [
                {'title': 'Save Bengaluru Lakes & Zero Waste City', 'category': 'Civic & Environment', 'description': 'Restoring Bellandur, Varthur, and 40+ neighborhood lakes with AI water monitoring and community action.'},
                {'title': 'Beyond Bengaluru: Tech Hubballi & Mysuru', 'category': 'Economy & IT', 'description': 'Expanding IT infrastructure, tech parks, and engineering hiring across tier-2 Karnataka cities.'},
                {'title': 'Sovereign AI Hackathon Karnataka', 'category': 'Technology', 'description': '5,000 developers creating Indic LLMs and localized government service automated agents.'}
            ],
            'events': [
                {'title': 'Bengaluru Tech Summit Global Stage', 'date': 'Aug 29, 2026', 'location': 'Bangalore Palace & Hybrid', 'description': 'Asia’s premier technology conclave uniting founders, ministers, and investors.'},
                {'title': 'Mysuru Heritage Green Walk', 'date': 'Sep 3, 2026', 'location': 'Mysuru Palace Environs', 'description': 'Civic cleanliness and heritage preservation drive with over 3,000 participants.'},
                {'title': 'Karnataka Game Developers Conference', 'date': 'Sep 8, 2026', 'location': 'Whitefield, Bengaluru', 'description': 'Showcasing 100+ new made-in-India games for PC, console, and mobile.'}
            ],
            'stories': [
                {'title': 'How 5,000 Residents Restored a Dead Lake in 30 Days', 'text': 'Connected citizens and municipal engineers funded and completed eco-filtration on Saul Kere.'},
                {'title': 'From Tier-3 College to Global Semiconductor Lead', 'text': 'A student mentorship community in Hubballi led to a breakthrough in open-source RISC-V chip designs.'}
            ]
        },
        'mh': {
            'name': 'Maharashtra',
            'tagline': 'Financial Capital & Industrial Powerhouse connecting Finance, Cinema, Tech, Law & Police.',
            'heroText': 'Uniting Mumbai, Pune, Nagpur, and Nashik into a synchronized powerhouse for economic growth, swift legal resolution, smart policing, and foreign-standard architecture.',
            'focus': 'Financial Capital + Smart Infrastructure + Safe Cities',
            'stats': {'communities': 35, 'events': 20, 'actions': 44100, 'members': 520000},
            'communities': [
                {
                    'title': 'Mumbai & Pune FinTech & Software Guild',
                    'city': 'Mumbai',
                    'topic': 'Technology & IT',
                    'mainDomain': 'Technology & IT',
                    'subdomain': 'FinTech, Banking & AI',
                    'category': 'Financial Tech Core',
                    'pillar': 'tech',
                    'communityType': 'Verified',
                    'channels': ['General', 'FinTech-Innovations', 'Algorithmic-Trading', 'Cloud-Security', 'Careers'],
                    'members': 24300,
                    'description': 'BFSI tech leaders, payment gateway architects, and Pune software engineers driving India’s digital economy.'
                },
                {
                    'title': 'Maharashtra Student & University Innovation Hub',
                    'city': 'Pune',
                    'topic': 'Students & Education',
                    'mainDomain': 'Students & Education',
                    'subdomain': 'Engineering & Automotive',
                    'category': 'Oxford of the East',
                    'pillar': 'education',
                    'communityType': 'College',
                    'channels': ['General', 'EV-Automotive-Projects', 'AIML-Tracks', 'SPPU-Curriculum', 'Internships'],
                    'members': 27800,
                    'description': 'Students from Pune, Mumbai, and Nagpur universities building smart mobility, EV prototypes, and deep tech algorithms.'
                },
                {
                    'title': 'Bombay High Court & Fast-Track Corporate Bench',
                    'city': 'Mumbai',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'High Court & Fast-Track Courts',
                    'category': 'Fast-Track Corporate & Civil Law',
                    'pillar': 'legal',
                    'communityType': 'Verified',
                    'channels': ['General', 'Fast-Track-Hearings', 'NCLT-Insolvency', 'Maritime-RealEstate-Law', 'Pro-Bono'],
                    'members': 7600,
                    'description': 'Senior counsel, solicitors, and law students expediting commercial arbitrations, NCLT cases, and public interest matters.'
                },
                {
                    'title': 'Maharashtra Police & Mumbai Safety Network',
                    'city': 'Mumbai',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'Police & Civil Services',
                    'category': 'Rapid Law & Order',
                    'pillar': 'police',
                    'communityType': 'Verified',
                    'channels': ['General', 'Mumbai-Local-Safety', 'Cyber-Crime-Cell', 'Coastal-Vigilance', 'Disaster-Response'],
                    'members': 10200,
                    'description': 'Mumbai Police, Pune Police, and Maharashtra State Police officers coordinating transit safety, cyber security, and disaster response.'
                },
                {
                    'title': 'Clean Mumbai & Bollywood Media Creators',
                    'city': 'Mumbai',
                    'topic': 'Entertainment',
                    'mainDomain': 'Entertainment',
                    'subdomain': 'Cinema, PR & Civic Campaigns',
                    'category': 'Clean City & Mass Reach',
                    'pillar': 'media',
                    'communityType': 'Verified',
                    'channels': ['General', 'Beach-Cleanup-Versova-Juhu', 'Creators-For-Civic-Duty', 'Verified-News', 'Short-Films'],
                    'members': 14800,
                    'description': 'Film creators, journalists, PR agencies, and youth volunteers running high-impact beach cleanups and civic pride campaigns.'
                },
                {
                    'title': 'Mumbai-Pune Luxury Architecture & Skyscraper Guild',
                    'city': 'Mumbai',
                    'topic': 'Real Estate',
                    'mainDomain': 'Real Estate',
                    'subdomain': 'High-Rise & Luxury Interiors',
                    'category': 'Skyline Standards',
                    'pillar': 'builders',
                    'communityType': 'Verified',
                    'channels': ['General', 'High-Rise-Engineering', 'European-Luxury-Furniture', 'Modular-Interior-Craft', 'Smart-Tenders'],
                    'members': 11200,
                    'description': 'Structural engineers, luxury interior designers, and real estate developers building world-class sea-facing residences and commercial towers.'
                },
                {
                    'title': 'Maharashtra Esports & Gaming Arena',
                    'city': 'Pune',
                    'topic': 'Gaming',
                    'mainDomain': 'Gaming',
                    'subdomain': 'Esports & Gaming Leagues',
                    'category': 'Pro Esports',
                    'pillar': 'gaming',
                    'communityType': 'Public',
                    'channels': ['General', 'Maha-Esports-Championship', 'Valorant-Mumbai-Lobby', 'Streamers-Circle', 'LAN-Events'],
                    'members': 18400,
                    'description': 'Top-tier esports teams, collegiate tournament organizers, and gaming cafes hosting major regional championships.'
                }
            ],
            'campaigns': [
                {'title': 'Clean Coastlines: Versova to Marine Drive', 'category': 'Civic & Environment', 'description': 'Mobilizing 50,000 citizens weekly for ocean plastic recovery and mangrove ecosystem preservation.'},
                {'title': 'Navi Mumbai & Pune Smart Corridor Development', 'category': 'Urban & Architecture', 'description': 'Adopting smart transit-oriented design and international construction safety standards.'},
                {'title': 'Maharashtra FinTech Inclusion Drive', 'category': 'Finance & Tech', 'description': 'Bringing digital banking literacy and micro-enterprise payment tools to 10,000 rural villages.'}
            ],
            'events': [
                {'title': 'Mumbai Financial & Tech Leadership Conclave', 'date': 'Aug 31, 2026', 'location': 'BKC, Mumbai', 'description': 'The premier gathering of banking executives, tech titans, and policy makers.'},
                {'title': 'Pune Smart Automotive Hackathon', 'date': 'Sep 5, 2026', 'location': 'COEP Tech University, Pune', 'description': 'Engineering students developing AI autonomous driving algorithms for Indian road conditions.'},
                {'title': 'Versova Mega Cleanliness Celebration', 'date': 'Sep 9, 2026', 'location': 'Versova Beach, Mumbai', 'description': 'Public civic celebration of community-driven environmental restoration.'}
            ],
            'stories': [
                {'title': 'How Mumbai Citizen Volunteers Removed 10 Million KG of Plastic', 'text': 'A unified digital community brought together Bollywood actors, fishermen, and college students.'},
                {'title': 'Fast-Track Commercial Arbitration Saves 500 MSME Jobs', 'text': 'Digitized dispute forums resolved contractor payments in 14 days instead of 3 years.'}
            ]
        },
        'tn': {
            'name': 'Tamil Nadu',
            'tagline': 'Industrial, Automotive & SaaS Heartland with deep cultural strength and engineering excellence.',
            'heroText': 'Chennai SaaS capital, Coimbatore manufacturing, and Madurai education uniting across IT, legal dispatch, clean living, and world-class architectural design.',
            'focus': 'SaaS Capital + Clean Cities + Modern Engineering',
            'stats': {'communities': 27, 'events': 13, 'actions': 26700, 'members': 330000},
            'communities': [
                {
                    'title': 'Chennai SaaS & Product Engineering Guild',
                    'city': 'Chennai',
                    'topic': 'Technology & IT',
                    'mainDomain': 'Technology & IT',
                    'subdomain': 'B2B SaaS & AI',
                    'category': 'SaaS Capital of India',
                    'pillar': 'tech',
                    'communityType': 'Verified',
                    'channels': ['General', 'SaaS-Playbooks', 'Cloud-Architecture', 'AI-Agents', 'Hiring'],
                    'members': 15900,
                    'description': 'Product engineers, SaaS founders, and UI/UX designers building world-leading enterprise products from Chennai.'
                },
                {
                    'title': 'Tamil Nadu Engineering & Anna University Circle',
                    'city': 'Chennai',
                    'topic': 'Students & Education',
                    'mainDomain': 'Students & Education',
                    'subdomain': 'Engineering & Polytechnic',
                    'category': 'Core Engineering',
                    'pillar': 'education',
                    'communityType': 'College',
                    'channels': ['General', 'Curriculum-Evolution', 'State-Issue-Solvers', 'AI-ML-Specialization', 'Placements'],
                    'members': 22100,
                    'description': 'Students and faculty across Anna University, IIT Madras, and PSG Tech collaborating on robotics, AI, and automotive software.'
                },
                {
                    'title': 'Madras High Court & Fast-Track Legal Forum',
                    'city': 'Chennai',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'High Court & Fast-Track Courts',
                    'category': 'Legal Excellence',
                    'pillar': 'legal',
                    'communityType': 'Verified',
                    'channels': ['General', 'Fast-Track-Hearings', 'Industrial-Disputes', 'Pro-Bono-Aid', 'Legal-Updates'],
                    'members': 5200,
                    'description': 'Advocates and legal minds expediting industrial labor cases, property documentation, and citizen legal rights.'
                },
                {
                    'title': 'Tamil Nadu Police & City Safety Command',
                    'city': 'Chennai',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'Police & Civil Services',
                    'category': 'Citizen Safety',
                    'pillar': 'police',
                    'communityType': 'Verified',
                    'channels': ['General', 'Kavalan-Safety-App', 'Traffic-Management', 'Coastal-Patrol', 'District-Alerts'],
                    'members': 7400,
                    'description': 'Greater Chennai Police, Coimbatore City Police, and state IPS officers collaborating on rapid crime deterrence and road safety.'
                },
                {
                    'title': 'Clean Marina & Tamil Creators Alliance',
                    'city': 'Chennai',
                    'topic': 'Entertainment',
                    'mainDomain': 'Entertainment',
                    'subdomain': 'Media, PR & Civic Drives',
                    'category': 'Clean City & Creative Media',
                    'pillar': 'media',
                    'communityType': 'Verified',
                    'channels': ['General', 'Marina-Sanitation-Drive', 'Tamil-Creators-Network', 'Verified-Civic-News', 'Vlogs'],
                    'members': 9200,
                    'description': 'Tamil YouTube creators, cinema technicians, and civic volunteers running massive cleanliness awareness and water conservation campaigns.'
                },
                {
                    'title': 'Tamil Nadu Master Builders & Smart Architecture',
                    'city': 'Coimbatore',
                    'topic': 'Real Estate',
                    'mainDomain': 'Real Estate',
                    'subdomain': 'Contemporary Dravidian & Modern Housing',
                    'category': 'World-Class Housing',
                    'pillar': 'builders',
                    'communityType': 'Verified',
                    'channels': ['General', 'Contemporary-Architecture', 'Teak-Rosewood-Furniture', 'Smart-Gated-Communities', 'Tenders'],
                    'members': 7900,
                    'description': 'Blending timeless South Indian architectural wisdom with modern European structural aesthetics and sustainable climate design.'
                },
                {
                    'title': 'Tamil Nadu Esports & Gaming Arena',
                    'city': 'Chennai',
                    'topic': 'Gaming',
                    'mainDomain': 'Gaming',
                    'subdomain': 'Esports & Mobile Gaming',
                    'category': 'Competitive Esports',
                    'pillar': 'gaming',
                    'communityType': 'Public',
                    'channels': ['General', 'TN-Esports-League', 'FreeFire-BGMI-Tournaments', 'Game-Devs-Chennai', 'Streams'],
                    'members': 11800,
                    'description': 'Mobile and PC gaming enthusiasts competing in state championships and developing localized Tamil games.'
                }
            ],
            'campaigns': [
                {'title': 'Clean Marina Beach & Adyar River Rebirth', 'category': 'Civic & Environment', 'description': 'Restoring Chennai’s iconic beachfront and water channels through community waste trapping.'},
                {'title': 'SaaS for Bharat: Tier-2 Tech Boom', 'category': 'Technology & Jobs', 'description': 'Setting up remote SaaS engineering pods in Madurai, Trichy, and Salem.'},
                {'title': 'Zero-Accident Tamil Nadu Highways', 'category': 'Public Safety', 'description': 'Integrated police and driver awareness campaign targeting highway safety.'}
            ],
            'events': [
                {'title': 'SaaSBoomi Chennai Founders Festival', 'date': 'Sep 1, 2026', 'location': 'Chennai Trade Centre', 'description': 'The definitive gathering of Indian B2B product builders and global scale leaders.'},
                {'title': 'Marina Sunrise Civic Cleanliness Drive', 'date': 'Sep 6, 2026', 'location': 'Marina Beach, Chennai', 'description': 'Uniting 4,000 student volunteers and civic workers.'},
                {'title': 'Anna University Innovation Showcase', 'date': 'Sep 11, 2026', 'location': 'Guindy Campus, Chennai', 'description': '500+ student prototypes addressing urban mobility and flood prevention.'}
            ],
            'stories': [
                {'title': 'How Coimbatore Engineers Built Solar Desalination for Coastal Wards', 'text': 'Student innovators connected with local manufacturing units to deliver low-cost drinking water.'},
                {'title': 'Chennai SaaS Guild Helps 1,000 Freshers Land Remote Global Roles', 'text': 'Peer code reviews and mentor mock interviews opened doors to tier-1 salaries.'}
            ]
        },
        'dl': {
            'name': 'Delhi NCR',
            'tagline': 'National Capital Region driving Governance, Supreme Court Justice, Startups & Clean Air Action.',
            'heroText': 'Connecting New Delhi, Gurugram, and Noida across governance, supreme judiciary, IT headquarters, civic cleanliness, and modern urban infrastructure.',
            'focus': 'National Governance + Supreme Legal Dispatch + Clean Air Action',
            'stats': {'communities': 30, 'events': 16, 'actions': 36500, 'members': 410000},
            'communities': [
                {
                    'title': 'Delhi-NCR Tech & Startup Guild',
                    'city': 'Gurugram',
                    'topic': 'Technology & IT',
                    'mainDomain': 'Technology & IT',
                    'subdomain': 'AI, E-Commerce & Web3',
                    'category': 'NCR Startup Powerhouse',
                    'pillar': 'tech',
                    'communityType': 'Verified',
                    'channels': ['General', 'AI-Startups', 'Cyber-Security', 'Scale-Engineering', 'Hiring'],
                    'members': 21200,
                    'description': 'Cyber City & Noida tech leads, AI researchers, and startup founders driving consumer tech at national scale.'
                },
                {
                    'title': 'Delhi University & IIT-D Student Innovation Hub',
                    'city': 'New Delhi',
                    'topic': 'Students & Education',
                    'mainDomain': 'Students & Education',
                    'subdomain': 'IIT, DU, DTU & Higher Ed',
                    'category': 'National Student Forum',
                    'pillar': 'education',
                    'communityType': 'College',
                    'channels': ['General', 'National-Issue-Apps', 'UPSC-Knowledge', 'AIML-Tracks', 'Hackathons'],
                    'members': 26400,
                    'description': 'Students from IIT Delhi, DTU, NSUT, and DU colleges building national problem-solving apps and policy prototypes.'
                },
                {
                    'title': 'Supreme Court & Delhi High Court Legal Forum',
                    'city': 'New Delhi',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'Supreme Court & Fast-Track Benches',
                    'category': 'Apex Legal Standards',
                    'pillar': 'legal',
                    'communityType': 'Verified',
                    'channels': ['General', 'Constitutional-Law', 'Fast-Track-Tribunals', 'PIL-Discussion', 'Bar-Council-Updates'],
                    'members': 8900,
                    'description': 'Supreme Court advocates, high court practitioners, and constitutional scholars sharing fast-track procedural reforms.'
                },
                {
                    'title': 'Delhi Police & Central Administration Alliance',
                    'city': 'New Delhi',
                    'topic': 'Local Communities',
                    'mainDomain': 'Local Communities',
                    'subdomain': 'Police & Civil Services',
                    'category': 'Capital Safety & Governance',
                    'pillar': 'police',
                    'communityType': 'Verified',
                    'channels': ['General', 'Capital-Security-Advisory', 'Cyber-Crime-War-Room', 'Traffic-Management', 'Citizen-Vigilance'],
                    'members': 9800,
                    'description': 'Delhi Police, CISF, and central administrative officers coordinating traffic management, cybercrime prevention, and rapid crisis management.'
                },
                {
                    'title': 'Swachh NCR & National Media Alliance',
                    'city': 'Noida',
                    'topic': 'Entertainment',
                    'mainDomain': 'Entertainment',
                    'subdomain': 'National News, PR & Civic Drives',
                    'category': 'Clean Capital & Fact-Checking',
                    'pillar': 'media',
                    'communityType': 'Verified',
                    'channels': ['General', 'Clean-Yamuna-Mission', 'Anti-Pollution-Drive', 'Verified-National-News', 'Creators-Desk'],
                    'members': 13600,
                    'description': 'National television reporters, digital journalists, and environmental creators organizing Clean Yamuna drives and anti-smog awareness.'
                },
                {
                    'title': 'NCR Master Architects & Infrastructure Guild',
                    'city': 'Gurugram',
                    'topic': 'Real Estate',
                    'mainDomain': 'Real Estate',
                    'subdomain': 'World-Class Urban Architecture',
                    'category': 'Modern Capital Infrastructure',
                    'pillar': 'builders',
                    'communityType': 'Verified',
                    'channels': ['General', 'Golf-Course-Ext-Skylines', 'Green-Sustainable-Homes', 'Luxury-Furnishing', 'Infra-Tenders'],
                    'members': 8900,
                    'description': 'Architects and structural engineers transforming Gurugram, Noida Expressway, and Delhi NCR into modern, sustainable smart cities.'
                },
                {
                    'title': 'Delhi NCR Esports & Gaming Guild',
                    'city': 'New Delhi',
                    'topic': 'Gaming',
                    'mainDomain': 'Gaming',
                    'subdomain': 'Esports & Gaming Leagues',
                    'category': 'North India Esports',
                    'pillar': 'gaming',
                    'communityType': 'Public',
                    'channels': ['General', 'NCR-Gaming-Championship', 'Valorant-Lobbies', 'BGMI-Squads', 'Game-Designers'],
                    'members': 14900,
                    'description': 'Esports athletes, streamer syndicates, and game developers building North India’s gaming championship circuit.'
                }
            ],
            'campaigns': [
                {'title': 'Clean Yamuna & Green Delhi Action Blitz', 'category': 'Civic & Environment', 'description': 'Multi-stakeholder riverfront revitalization and community tree plantation drive across 250 wards.'},
                {'title': 'Clean Air Mission NCR', 'category': 'Public Health & Environment', 'description': 'Grassroots anti-dust mitigation, industrial emission reporting, and electric mobility adoption.'},
                {'title': 'National Fast-Track Judicial Tech Workshop', 'category': 'Legal & Governance', 'description': 'Training 10,000 legal practitioners on digital evidence validation and automated dispute resolution.'}
            ],
            'events': [
                {'title': 'National Governance & Startup Conclave', 'date': 'Sep 2, 2026', 'location': 'Bharat Mandapam, New Delhi', 'description': 'Union ministers, startup unicorns, and researchers mapping India’s 2047 economic roadmap.'},
                {'title': 'Clean Yamuna Youth Action Day', 'date': 'Sep 7, 2026', 'location': 'Yamuna Ghats, New Delhi', 'description': 'Volunteer cleanup drive with 6,000 students and environmental activists.'},
                {'title': 'Supreme Court National Legal Tech Summit', 'date': 'Sep 12, 2026', 'location': 'Vigyan Bhawan, New Delhi', 'description': 'Keynotes on digitizing fast-track dispute courts across all Indian districts.'}
            ],
            'stories': [
                {'title': 'How DTU Students Built an AI Yamuna Pollution Tracker', 'text': 'Low-cost sensor buoys deployed by engineering students alerted municipal bodies to chemical dumps within minutes.'},
                {'title': 'Cyber Crime War Room Saves ₹40 Crore in Senior Citizen Scams', 'text': 'Rapid police-bank inter-departmental channel blocked fraudulent transfers across 12 states.'}
            ]
        }
    }

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS states')
    c.execute('DROP TABLE IF EXISTS communities')
    c.execute('DROP TABLE IF EXISTS campaigns')
    c.execute('DROP TABLE IF EXISTS events')
    c.execute('DROP TABLE IF EXISTS stories')
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('DROP TABLE IF EXISTS memberships')
    c.execute('DROP TABLE IF EXISTS posts')
    c.execute('DROP TABLE IF EXISTS chat_messages')
    c.execute('DROP TABLE IF EXISTS projects')

    c.execute('''
        CREATE TABLE states (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            tagline TEXT,
            heroText TEXT,
            focus TEXT,
            stats TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE communities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state_id TEXT,
            title TEXT,
            city TEXT,
            topic TEXT,
            mainDomain TEXT,
            subdomain TEXT,
            category TEXT,
            pillar TEXT DEFAULT 'general',
            communityType TEXT,
            channels TEXT,
            members INTEGER,
            description TEXT,
            FOREIGN KEY (state_id) REFERENCES states (id)
        )
    ''')

    c.execute('''
        CREATE TABLE campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state_id TEXT,
            title TEXT,
            category TEXT,
            description TEXT,
            FOREIGN KEY (state_id) REFERENCES states (id)
        )
    ''')

    c.execute('''
        CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state_id TEXT,
            title TEXT,
            date TEXT,
            location TEXT,
            description TEXT,
            FOREIGN KEY (state_id) REFERENCES states (id)
        )
    ''')

    c.execute('''
        CREATE TABLE stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state_id TEXT,
            title TEXT,
            text TEXT,
            FOREIGN KEY (state_id) REFERENCES states (id)
        )
    ''')

    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT,
            mobile TEXT,
            emailVerified BOOLEAN DEFAULT FALSE,
            mobileVerified BOOLEAN DEFAULT FALSE,
            profession TEXT,
            branch TEXT,
            communityDomains TEXT,
            domain TEXT,
            subdomain TEXT,
            rollNo TEXT,
            specialty TEXT,
            verificationId TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            docName TEXT,
            note TEXT,
            premium BOOLEAN DEFAULT FALSE,
            xp INTEGER DEFAULT 150,
            trustScore INTEGER DEFAULT 85,
            badge TEXT DEFAULT 'Citizen Pioneer'
        )
    ''')

    c.execute('''
        CREATE TABLE memberships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            community_id INTEGER,
            status TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (community_id) REFERENCES communities (id)
        )
    ''')

    c.execute('''
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            author_name TEXT,
            author_role TEXT,
            state_id TEXT,
            scope TEXT DEFAULT 'state',
            pillar TEXT DEFAULT 'general',
            domain TEXT,
            title TEXT,
            content TEXT,
            likes INTEGER DEFAULT 0,
            comments_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            community_id INTEGER,
            channel_name TEXT,
            user_name TEXT,
            user_role TEXT,
            text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_name TEXT,
            author_role TEXT,
            pillar TEXT,
            state_id TEXT,
            title TEXT,
            description TEXT,
            roles_needed TEXT,
            members_joined INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Open for Research & Team'
        )
    ''')

    states_data = load_states_data()

    for state_id, state_data in states_data.items():
        c.execute("INSERT INTO states (id, name, tagline, heroText, focus, stats) VALUES (?, ?, ?, ?, ?, ?)",
                  (state_id, state_data['name'], state_data['tagline'], state_data['heroText'], state_data['focus'], json.dumps(state_data['stats'])))

        for community in state_data['communities']:
            c.execute("""INSERT INTO communities (state_id, title, city, topic, mainDomain, subdomain, category, pillar, communityType, channels, members, description)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (state_id, community['title'], community['city'], community['topic'], community['mainDomain'],
                       community['subdomain'], community['category'], community.get('pillar', 'general'),
                       community['communityType'], json.dumps(community['channels']), community['members'], community['description']))

        for campaign in state_data['campaigns']:
            c.execute("INSERT INTO campaigns (state_id, title, category, description) VALUES (?, ?, ?, ?)",
                      (state_id, campaign['title'], campaign['category'], campaign['description']))

        for event in state_data['events']:
            c.execute("INSERT INTO events (state_id, title, date, location, description) VALUES (?, ?, ?, ?, ?)",
                      (state_id, event['title'], event['date'], event['location'], event['description']))

        for story in state_data['stories']:
            c.execute("INSERT INTO stories (state_id, title, text) VALUES (?, ?, ?)",
                      (state_id, story['title'], story['text']))

    sample_posts = [
        ('Aditi Sharma', 'Student Innovator (JNTU Hyderabad)', 'tg', 'state', 'education', 'Students & Education', 'State Drainage Problem Solver App Built by JNTU & OU Students!', 'We developed an open-source mobile app where citizens report water logging and potholes with GPS accuracy. Looking for 3 more flutter/backend devs to help scale state-wide!', 48, 12),
        ('Rahul Varma', 'Senior Cyber Architect', 'all_india', 'nation', 'tech', 'Technology & IT', 'Open Source Security Framework for Indian MSMEs Released', 'We just open-sourced a lightweight sovereign compliance audit tool designed specifically for Indian FinTech and MSMEs. Check out the github link in our channel!', 92, 24),
        ('SP Vikram Rathore, IPS', 'Police Superintendent', 'ap', 'state', 'police', 'Local Communities', 'Cyber Fraud Alert: Immediate 1930 Helpline Golden Hour Protocol', 'If you or someone in your ward encounters an unauthorized UPI withdrawal, call 1930 within the first 60 minutes to freeze the receiving bank node immediately.', 134, 18),
        ('Adv. Meera Swaminathan', 'High Court Advocate', 'ka', 'state', 'legal', 'Local Communities', 'Fast-Track Court Precedent on Builder Delay Compensation', 'New ruling clarifies that homebuyers are entitled to immediate interest payouts if project completion exceeds 6 months past RERA agreed timeline without force majeure.', 76, 15),
        ('Rohan Kapoor', 'Civic Media Producer', 'mh', 'state', 'media', 'Entertainment', 'Versova Beach Clean Drive Reaches 500 Tons Milestone!', 'Over 1,200 volunteers, creators, and local BMC workers joined us this Sunday. Next Sunday we target Juhu and Bandra waterfronts. Join the volunteer channel!', 115, 31),
        ('Arjun Singhania', 'Chief Architect', 'dl', 'state', 'builders', 'Real Estate', 'Modular Sustainable Apartment Standards for Modern Indian Cities', 'Adopting Japanese earthquake-resistant joinery and solar-passive cross ventilation saves 30% AC energy in northern summers while matching luxury penthouse aesthetics.', 64, 9),
        ('Karan Deshmukh', 'Esports Lead', 'all_india', 'nation', 'gaming', 'Gaming', 'Bharat Esports Collegiate Cup Registrations Now Open!', '32 colleges qualified from Hyderabad, Bangalore, Mumbai and Delhi. ₹10 Lakhs prize pool with live streaming on our platform arena channel!', 158, 42)
    ]

    for p in sample_posts:
        c.execute("""INSERT INTO posts (author_name, author_role, state_id, scope, pillar, domain, title, content, likes, comments_count)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", p)

    sample_projects = [
        ('Aditi Sharma', 'Student Lead', 'education', 'tg', 'Telangana Municipal Issue Solver App & AI Routing', 'Building a low-latency geo-tagging tool for municipal ward commissioners. Need 2 Flutter devs and 1 FastAPI data engineer.', 'Flutter, Python, GeoJSON', 4),
        ('Rahul Varma', 'Cyber Architect', 'tech', 'ka', 'Open Source Sovereign Cloud Audit Tool', 'Developing lightweight security scanner for Indian FinTech startups to comply with RBI data localization standards.', 'Python, Golang, Docker', 6),
        ('SP Vikram IPS', 'Police Command', 'police', 'ap', '1930 Cyber Fraud Instant Freeze API', 'Inter-departmental research to connect district bank nodes with police dispatch for <15 min fraud recovery.', 'Bank API Integration, Security', 8),
        ('Adv. Meera Swaminathan', 'Senior Advocate', 'legal', 'ka', 'Fast-Track Court Automated Precedent Indexer', 'Creating an AI-assisted search database for rapid retrieval of Karnataka and Supreme Court consumer dispute judgments.', 'Legal Research, Natural Language Processing', 5),
        ('Arjun Singhania', 'Chief Architect', 'builders', 'dl', 'Zero-Carbon Modular Housing Joined Frame Design', 'Structural research team building lightweight earthquake-resistant prefabricated housing units for urban re-development.', 'Structural Civil Eng, CAD, Sustainability', 7)
    ]

    for prj in sample_projects:
        c.execute("""INSERT INTO projects (author_name, author_role, pillar, state_id, title, description, roles_needed, members_joined)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", prj)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print(f"Database initialized at {DB_PATH} with projects and eligibility schema successfully.")

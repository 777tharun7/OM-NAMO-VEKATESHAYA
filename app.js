/**
 * Project Introvert — Bharat Community Ecosystem (app.js) - v1.1
 * Master logic for:
 * 1. Pre-Login Public Discovery View (What platform does for life in India)
 * 2. Role & Profession Eligibility Verification & Login Engine
 * 3. Verified Customized Home Feed (Filtered strictly to user profession & location)
 * 4. Research & Project Collaboration Board ("Request to Join Team", "Share Work")
 * 5. Nearby Activity Radar & Local Meetings
 * 6. Multilingual AI Bharat Assistant
 */

// Global App State
let isLoggedIn = false; // Start in logged-out public view by default
let currentLevel = 'state'; // 'nation', 'state', 'local'
let currentState = 'tg'; // 'all_india', 'tg', 'ap', 'ka', 'mh', 'tn', 'dl'
let currentPillar = 'all'; // 'all', 'tech', 'education', 'legal', 'police', 'media', 'builders', 'citizen', 'gaming'
let activeTab = 'feedTab';
let activeChannel = 'general';
let isAudioConnected = false;
let isMicMuted = false;
let activeRoleFilterOnly = true;
let memberSearchQuery = '';

// 25 Core Domains Taxonomy
const platformDomains = [
  { id: 'tech', name: '1. Technology & IT', icon: '💻', subdomains: ['AI & GenAI', 'Machine Learning', 'Cybersecurity', 'Cloud & DevOps', 'Web & Mobile', 'Open-Source Bharat', 'Semiconductors', 'Robotics'] },
  { id: 'education', name: '2. Students & Education', icon: '🎓', subdomains: ['Engineering', 'Medical', 'Diploma', 'UPSC & Civil Services', 'State Problem Solvers', 'Placements', 'Hackathons', 'Alumni Circles'] },
  { id: 'agriculture', name: '3. Agriculture', icon: '🌾', subdomains: ['AgriTech', 'Organic Farming', 'Aquaculture', 'Drip Irrigation', 'Farm Equipment', 'Government Subsidies', 'Export Markets'] },
  { id: 'jobs', name: '4. Jobs & Careers', icon: '💼', subdomains: ['Freshers Hub', 'Internships', 'Remote Tech Roles', 'Resume Review', 'Mock Interviews', 'Company Referrals'] },
  { id: 'business', name: '5. Business & Trade', icon: '🏢', subdomains: ['MSME Growth', 'B2B Procurement', 'Supply Chain', 'Sales & Distribution', 'Retail Innovation'] },
  { id: 'startups', name: '6. Startups & Incubation', icon: '🚀', subdomains: ['Founders Hub', 'Seed & VC Funding', 'Product Market Fit', 'T-Hub & Incubators', 'Govt Grants'] },
  { id: 'finance', name: '7. Finance & Banking', icon: '💰', subdomains: ['FinTech', 'Personal Finance', 'UPI Innovations', 'Taxation & GST', 'Stock Market', 'Micro Lending'] },
  { id: 'health', name: '8. Health & Medicine', icon: '🏥', subdomains: ['Public Health', 'Tele-Medicine', 'Ayush & Wellness', 'Hospital Network', 'Mental Health Support'] },
  { id: 'fitness', name: '9. Fitness & Yoga', icon: '🏋️', subdomains: ['Yoga & Pranayama', 'Running Clubs', 'Nutrition & Diet', 'CrossFit & Gyms', 'Sports Conditioning'] },
  { id: 'gaming', name: '10. Gaming & Esports', icon: '🎮', subdomains: ['Bharat Esports Cup', 'BGMI & Valorant Squads', 'Unreal Engine Devs', 'Unity 3D', 'Streaming Syndicate'] },
  { id: 'arts', name: '11. Arts & Design', icon: '🎨', subdomains: ['UI/UX Design', 'Traditional Indian Art', 'Graphic Design', '3D Animation', 'Fashion Design'] },
  { id: 'music', name: '12. Music & Audio', icon: '🎵', subdomains: ['Classical & Carnatic', 'Playback Production', 'Indie Artists', 'Sound Engineering', 'Podcasts'] },
  { id: 'entertainment', name: '13. Entertainment & Media', icon: '🎬', subdomains: ['Cinema & VFX', 'Digital Creators', 'Broadcast News', 'Short Films', 'Theatre'] },
  { id: 'sports', name: '14. Sports & Athletics', icon: '🏏', subdomains: ['Cricket Leagues', 'Kabaddi', 'Badminton', 'Football', 'Olympic Pathways', 'Local Sports Clubs'] },
  { id: 'travel', name: '15. Travel & Tourism', icon: '✈️', subdomains: ['Heritage Tourism', 'Eco-Tourism', 'Spiritual Circuits', 'Backpacking', 'Local Tour Guides'] },
  { id: 'food', name: '16. Food & Culinary', icon: '🍲', subdomains: ['Regional Cuisines', 'Food Startups', 'Cloud Kitchens', 'Organic Food', 'Restaurant Owners'] },
  { id: 'realestate', name: '17. Real Estate & Architecture', icon: '🏗️', subdomains: ['Smart Cities', 'Luxury Apartments', 'Sustainable Interiors', 'Modular Furniture', 'Contractors'] },
  { id: 'pets', name: '18. Pets & Animals', icon: '🐾', subdomains: ['Pet Care', 'Veterinary Tele-Clinic', 'Adoption Drives', 'Animal Rescue', 'Livestock Welfare'] },
  { id: 'environment', name: '19. Environment & Sustainability', icon: '🌱', subdomains: ['Swachh Bharat Clean Drives', 'Lake Restoration', 'Solar & Renewables', 'Waste Recycling', 'Afforestation'] },
  { id: 'ngos', name: '20. NGOs & Social Impact', icon: '🤝', subdomains: ['Youth Volunteering', 'Disaster Relief', 'Rural Education', 'Women Empowerment', 'CSR Partnerships'] },
  { id: 'family', name: '21. Family & Parenting', icon: '👨‍👩‍👧', subdomains: ['Early Childhood Care', 'Parent Support Circles', 'Elderly Care', 'Family Nutrition'] },
  { id: 'relationships', name: '22. Relationships & Community', icon: '💬', subdomains: ['Peer Support', 'Community Bonding', 'Mentorship Circles', 'Senior Citizen Care'] },
  { id: 'spirituality', name: '23. Spirituality & Mindfulness', icon: '🕉️', subdomains: ['Meditation & Dhyana', 'Ancient Indian Wisdom', 'Mindful Living', 'Philosophical Debates'] },
  { id: 'automobiles', name: '24. Automobiles & Mobility', icon: '🚗', subdomains: ['Electric Vehicles (EV)', 'Autonomous Driving', 'Two-Wheeler Innovation', 'Road Safety Patrol'] },
  { id: 'localgov', name: '25. Local Communities & Governance', icon: '🛡️', subdomains: ['Police Advisories', 'Fast-Track Court Aid', 'Municipal Ward Forums', 'Grievance Solvers'] }
];

// Personas with Detailed Verification Parameters
const personas = {
  student: {
    name: 'Aditi Sharma',
    role: 'Student Innovator',
    title: 'Student Innovator • JNTU Hyderabad',
    pillar: 'education',
    state: 'tg',
    city: 'Kukatpally, Hyderabad',
    branch: 'CSE / AI-ML Specialization',
    proofId: 'JNTUH-2026-CS-408',
    avatar: 'A',
    xp: 300,
    trust: 98,
    badge: 'Verified Student Innovator'
  },
  tech: {
    name: 'Rahul Varma',
    role: 'Senior Cyber Architect',
    title: 'Lead Architect • Bengaluru DeepTech Circle',
    pillar: 'tech',
    state: 'ka',
    city: 'Whitefield, Bengaluru',
    branch: 'Cloud Infrastructure & AI',
    proofId: 'EMP-77402-KA',
    avatar: 'R',
    xp: 680,
    trust: 99,
    badge: 'Verified Cyber Architect'
  },
  police: {
    name: 'SP Vikram Rathore, IPS',
    role: 'Police Superintendent',
    title: 'Law Enforcement Command • AP Police',
    pillar: 'police',
    state: 'ap',
    city: 'Vijayawada, AP',
    branch: 'Cyber Defense & Rapid Safety',
    proofId: 'IPS-AP-2014-99',
    avatar: 'V',
    xp: 920,
    trust: 99,
    badge: 'Verified Police Command'
  },
  lawyer: {
    name: 'Adv. Meera Swaminathan',
    role: 'High Court Advocate',
    title: 'Senior Advocate • Fast-Track Commercial Bench',
    pillar: 'legal',
    state: 'ka',
    city: 'High Court Complex, Bengaluru',
    branch: 'Fast-Track Corporate & Constitutional Law',
    proofId: 'BAR-KA-2018-441',
    avatar: 'M',
    xp: 540,
    trust: 97,
    badge: 'Verified Advocate'
  },
  builder: {
    name: 'Arjun Singhania',
    role: 'Chief Architect & Builder',
    title: 'Smart City Infrastructure Guild • Delhi NCR',
    pillar: 'builders',
    state: 'dl',
    city: 'Gurugram, NCR',
    branch: 'Sustainable High-Rise Architecture',
    proofId: 'COA-DL-8821',
    avatar: 'A',
    xp: 490,
    trust: 96,
    badge: 'Verified Master Architect'
  },
  media: {
    name: 'Rohan Kapoor',
    role: 'Civic Media Producer',
    title: 'PR & Swachh Bharat Campaigner • Mumbai',
    pillar: 'media',
    state: 'mh',
    city: 'Bandra, Mumbai',
    branch: 'Broadcast News & Viral Civic Campaigns',
    proofId: 'PRESS-MH-990',
    avatar: 'R',
    xp: 510,
    trust: 95,
    badge: 'Verified Press Producer'
  },
  gamer: {
    name: 'Karan Deshmukh',
    role: 'Esports Champion & Dev',
    title: 'Esports League Lead • All-India Arena',
    pillar: 'gaming',
    state: 'all_india',
    city: 'Pan-India Hub',
    branch: 'Unreal Game Design & Pro Esports',
    proofId: 'ESPORTS-IN-401',
    avatar: 'K',
    xp: 430,
    trust: 94,
    badge: 'Verified Esports Lead'
  }
};

// Create a searchable array of all verified users from the personas object
const verifiedUsers = Object.values(personas);

let currentUser = personas.student;

// Active State Database
let statesDatabase = {
  tg: {
    name: 'Telangana',
    tagline: 'Fast-growing innovation state for AI, IT, Governance, Education & Smart Urban Living.',
    focus: 'Hyderabad AI Hub + Public Safety + Smart Urban Living',
    stats: { communities: 28, members: '340k', events: 14, actions: '28.4k' },
    campaigns: [
      { title: 'Clean Musi & Green Hyderabad Drive', category: 'Civic & Cleanliness', desc: 'Multi-ward cleanliness, waste segregation, and green canopy plantation across Hyderabad & Secunderabad.' },
      { title: 'Telangana AI Academy: 50,000 Engineers', category: 'Education & Tech', desc: 'Upskilling tier-2 engineering graduates in Nizamabad, Khammam, and Warangal with high-paying tech skills.' },
      { title: 'Zero-Cyber-Fraud Awareness Mission', category: 'Public Safety & Police', desc: 'Statewide public education campaign on 1930 digital payment safety and rapid freeze protocol.' }
    ]
  },
  ap: {
    name: 'Andhra Pradesh',
    tagline: 'State-level collaboration across Sunrise Coastline, AI Tech, Agri, Law & Port Infrastructure.',
    focus: 'Vizag Tech Port + AgriTech + Amaravati Capital Build',
    stats: { communities: 26, members: '310k', events: 12, actions: '24.9k' },
    campaigns: [
      { title: 'Clean Beaches of Vizag & Coastal Rejuvenation', category: 'Civic & Cleanliness', desc: 'Cleaning 974 km of Andhra coastline with youth volunteers, fishermen communities, and local authorities.' },
      { title: 'Amaravati Green Capital Initiative', category: 'Smart Architecture', desc: 'Adopting European and Singapore standard green building codes for commercial and residential developments.' },
      { title: 'Digital Rayalaseema Tech Upskilling', category: 'Education & AI', desc: 'Bringing high-tech AI, data science, and cloud bootcamps to Tirupati, Kurnool, and Anantapur students.' }
    ]
  },
  ka: {
    name: 'Karnataka',
    tagline: 'India’s Silicon Silicon Hub leading DeepTech, Aerospace, Biotech & Smart Governance.',
    focus: 'Silicon Valley of India + DeepTech + Clean Bengaluru',
    stats: { communities: 32, members: '480k', events: 18, actions: '39.2k' },
    campaigns: [
      { title: 'Save Bengaluru Lakes & Zero Waste City', category: 'Civic & Cleanliness', desc: 'Restoring Bellandur, Varthur, and 40+ neighborhood lakes with AI water monitoring and community action.' },
      { title: 'Beyond Bengaluru: Tech Hubballi & Mysuru', category: 'Economy & IT', desc: 'Expanding IT infrastructure, tech parks, and engineering hiring across tier-2 Karnataka cities.' },
      { title: 'Sovereign AI Hackathon Karnataka', category: 'Technology & AI', desc: '5,000 developers creating Indic LLMs and localized government service automated agents.' }
    ]
  },
  mh: {
    name: 'Maharashtra',
    tagline: 'Financial Capital & Industrial Powerhouse connecting Finance, Cinema, Tech, Law & Police.',
    focus: 'Financial Capital + Smart Infrastructure + Safe Cities',
    stats: { communities: 35, members: '520k', events: 20, actions: '44.1k' },
    campaigns: [
      { title: 'Clean Coastlines: Versova to Marine Drive', category: 'Civic & Cleanliness', desc: 'Mobilizing 50,000 citizens weekly for ocean plastic recovery and mangrove ecosystem preservation.' },
      { title: 'Navi Mumbai & Pune Smart Corridor Development', category: 'Architecture & Urban', desc: 'Adopting smart transit-oriented design and international construction safety standards.' },
      { title: 'Maharashtra FinTech Inclusion Drive', category: 'Finance & MSME', desc: 'Bringing digital banking literacy and micro-enterprise payment tools to 10,000 rural villages.' }
    ]
  },
  tn: {
    name: 'Tamil Nadu',
    tagline: 'Industrial, Automotive & SaaS Heartland with deep cultural strength and engineering excellence.',
    focus: 'SaaS Capital + Clean Cities + Modern Engineering',
    stats: { communities: 27, members: '330k', events: 13, actions: '26.7k' },
    campaigns: [
      { title: 'Clean Marina Beach & Adyar River Rebirth', category: 'Civic & Cleanliness', desc: 'Restoring Chennai’s iconic beachfront and water channels through community waste trapping.' },
      { title: 'SaaS for Bharat: Tier-2 Tech Boom', category: 'Technology & Jobs', desc: 'Setting up remote SaaS engineering pods in Madurai, Trichy, and Salem.' },
      { title: 'Zero-Accident Tamil Nadu Highways', category: 'Public Safety & Police', desc: 'Integrated police and driver awareness campaign targeting highway safety.' }
    ]
  },
  dl: {
    name: 'Delhi NCR',
    tagline: 'National Capital Region driving Governance, Supreme Court Justice, Startups & Clean Air Action.',
    focus: 'National Governance + Supreme Legal Dispatch + Clean Air Action',
    stats: { communities: 30, members: '410k', events: 16, actions: '36.5k' },
    campaigns: [
      { title: 'Clean Yamuna & Green Delhi Action Blitz', category: 'Civic & Cleanliness', desc: 'Multi-stakeholder riverfront revitalization and community tree plantation drive across 250 wards.' },
      { title: 'Clean Air Mission NCR', category: 'Environment & Health', desc: 'Grassroots anti-dust mitigation, industrial emission reporting, and electric mobility adoption.' },
      { title: 'National Fast-Track Judicial Tech Workshop', category: 'Legal & Judiciary', desc: 'Training 10,000 legal practitioners on digital evidence validation and automated dispute resolution.' }
    ]
  },
  all_india: {
    name: 'All-India National Hub',
    tagline: 'Unified National Community Ecosystem connecting 1.4 Billion citizens, professionals & creators.',
    focus: 'National Integration + Tech Sovereignty + Civic Progress',
    stats: { communities: 148, members: '1.25M', events: 34, actions: '85.4k' },
    campaigns: [
      { title: 'Mission Viksit Bharat 2047', category: 'National Mission', desc: 'Transforming India into a high-income developed powerhouse through technology, civic hygiene, and inter-state knowledge sharing.' },
      { title: 'National Clean Cities & Waterways Drive', category: 'Civic & Cleanliness', desc: 'Unifying 500+ cities in coordinated weekly volunteer cleanliness blitzes led by creators and local youth.' },
      { title: 'AI for Bharat: 1 Million Developers', category: 'Technology & Education', desc: 'Upskilling engineering students across tier-2 and tier-3 colleges in generative AI and sovereign LLM tooling.' }
    ]
  }
};

// Initial Sample Posts for Feeds
let livePosts = [
  {
    id: 1,
    author: 'Aditi Sharma',
    role: 'Student Innovator (JNTU Hyderabad)',
    pillar: 'education',
    state: 'tg',
    scope: 'state',
    domain: 'Students & Education',
    title: 'State Drainage & Pothole Problem Solver App Built by JNTU & OU Students!',
    content: 'We developed an open-source mobile app where citizens report water logging and potholes with GPS accuracy directly to ward engineers. Looking for 3 more Flutter/FastAPI devs to help scale state-wide!',
    likes: 54,
    comments: 14,
    time: '15 mins ago'
  },
  {
    id: 2,
    author: 'Rahul Varma',
    role: 'Senior Cyber Architect',
    pillar: 'tech',
    state: 'ka',
    scope: 'nation',
    domain: 'Technology & IT',
    title: 'Open Source Security Audit Framework for Indian MSMEs Released 🇮🇳',
    content: 'We just open-sourced a lightweight sovereign compliance audit tool designed specifically for Indian FinTechs and MSMEs to protect against ransomware and data breaches. Check out our #Projects channel for the repo!',
    likes: 112,
    comments: 29,
    time: '1 hour ago'
  },
  {
    id: 3,
    author: 'SP Vikram Rathore, IPS',
    role: 'Police Superintendent',
    pillar: 'police',
    state: 'ap',
    scope: 'state',
    domain: 'Local Communities',
    title: 'Cyber Fraud Golden Hour Alert: Immediate 1930 Helpline Protocol',
    content: 'If you or someone in your neighborhood encounters an unauthorized UPI/Banking withdrawal, call 1930 within the first 60 minutes. Our joint cyber team freezes the destination beneficiary nodes immediately.',
    likes: 186,
    comments: 24,
    time: '2 hours ago'
  },
  {
    id: 4,
    author: 'Adv. Meera Swaminathan',
    role: 'High Court Advocate',
    pillar: 'legal',
    state: 'ka',
    scope: 'state',
    domain: 'Local Communities',
    title: 'Fast-Track Court Precedent on Homebuyer Delay Compensation',
    content: 'A recent division bench ruling reinforces that homebuyers are entitled to monthly delayed possession interest payouts if project handover exceeds agreed RERA timeline by over 6 months without genuine force majeure.',
    likes: 89,
    comments: 18,
    time: '3 hours ago'
  },
  {
    id: 5,
    author: 'Rohan Kapoor',
    role: 'Civic Media Producer',
    pillar: 'media',
    state: 'mh',
    scope: 'state',
    domain: 'Entertainment',
    title: 'Versova Beach Clean Drive Crosses 500 Tons Recovered Milestone!',
    content: 'Over 1,400 youth volunteers, Bollywood creators, and BMC workers joined us this Sunday. Next weekend we launch the Bandra & Juhu coastal restoration wave. Volunteer registration open in the Swachh Bharat tab!',
    likes: 142,
    comments: 38,
    time: '4 hours ago'
  },
  {
    id: 6,
    author: 'Arjun Singhania',
    role: 'Chief Architect & Builder',
    pillar: 'builders',
    state: 'dl',
    scope: 'state',
    domain: 'Real Estate',
    title: 'Modular Sustainable Apartment Standards for Modern Indian Metros',
    content: 'By integrating Japanese joinery principles, biophilic indoor balconies, and passive solar cross-ventilation, we can cut residential summer cooling electricity loads by 35% while creating world-class luxury finishes.',
    likes: 78,
    comments: 12,
    time: '5 hours ago'
  }
];

// Initial Research & Project Collaboration Board
let researchProjects = [
  {
    id: 101,
    author_name: 'Aditi Sharma',
    author_role: 'Student Lead • JNTU Hyderabad',
    pillar: 'education',
    state_id: 'tg',
    title: 'Telangana Municipal Issue Solver App & AI Routing Engine',
    description: 'Building a low-latency geo-tagging tool for municipal ward commissioners to automatically prioritize pothole and drainage repairs. Seeking 2 Flutter developers and 1 FastAPI data engineer.',
    roles_needed: '2 Flutter Devs, 1 Data Engineer',
    members_joined: 4,
    status: 'Open for Research & Team'
  },
  {
    id: 102,
    author_name: 'Rahul Varma',
    author_role: 'Cyber Architect • Whitefield',
    pillar: 'tech',
    state_id: 'ka',
    title: 'Open Source Sovereign Cloud Security Audit Tool for MSMEs',
    description: 'Developing lightweight security scanner for Indian FinTech startups to comply with RBI data localization and CERT-In reporting standards automatically.',
    roles_needed: 'Python, Golang, Docker',
    members_joined: 6,
    status: 'Open for Research & Team'
  },
  {
    id: 103,
    author_name: 'SP Vikram IPS',
    author_role: 'Police Command • Vijayawada',
    pillar: 'police',
    state_id: 'ap',
    title: '1930 Cyber Fraud Instant Freeze Bank API Integration',
    description: 'Inter-departmental research initiative connecting district bank nodes with police dispatch for <15 min fraud recovery. Inviting security researchers and banking system engineers.',
    roles_needed: 'Banking API Integration, Security Researcher',
    members_joined: 8,
    status: 'Open for Research & Team'
  },
  {
    id: 104,
    author_name: 'Adv. Meera Swaminathan',
    author_role: 'Senior Advocate • Bengaluru',
    pillar: 'legal',
    state_id: 'ka',
    title: 'Fast-Track Court Automated Precedent Indexer for Consumer Courts',
    description: 'Creating an AI-assisted search database for rapid retrieval of Karnataka High Court and Supreme Court consumer dispute judgments to speed up trial resolutions.',
    roles_needed: 'Legal Research, NLP Specialist',
    members_joined: 5,
    status: 'Open for Research & Team'
  },
  {
    id: 105,
    author_name: 'Arjun Singhania',
    author_role: 'Chief Architect • Gurugram',
    pillar: 'builders',
    state_id: 'dl',
    title: 'Zero-Carbon Modular Housing Joined Frame Design',
    description: 'Structural research team building lightweight earthquake-resistant prefabricated housing units for urban re-development in Delhi NCR.',
    roles_needed: 'Structural Civil Eng, CAD Designer, Sustainability Specialist',
    members_joined: 7,
    status: 'Open for Research & Team'
  }
];

// Nearby Activity Radar & Meetings Data
const nearbyMeetings = [
  {
    title: 'State Student & Professor Tech Roundtable',
    time: 'Tomorrow, 5:00 PM',
    location: 'JNTUH Campus Auditorium & Hybrid',
    pillar: 'education',
    organizer: 'Prof. K. Reddy',
    attendees: 48
  },
  {
    title: 'HITEC City Cyber Defense & AI Dev Meetup',
    time: 'Saturday, 11:00 AM',
    location: 'T-Hub 2.0, Hyderabad',
    pillar: 'tech',
    organizer: 'Rahul Varma',
    attendees: 120
  },
  {
    title: 'Ward Cleanliness & Musi River Action Meeting',
    time: 'Sunday, 7:00 AM',
    location: 'Chaderghat Ward Office',
    pillar: 'media',
    organizer: 'Rohan Kapoor',
    attendees: 210
  },
  {
    title: 'Fast-Track Court Legal Aid Workshop',
    time: 'Next Tuesday, 4:00 PM',
    location: 'High Court Annexe, Room 4',
    pillar: 'legal',
    organizer: 'Adv. Meera S.',
    attendees: 35
  }
];

// Chat Messages Memory per Channel
const channelChats = {
  general: [
    { sender: 'Prof. K. Reddy (JNTU)', role: 'Faculty Mentor', text: 'Welcome verified peers! Share your research work and project idea requests.' },
    { sender: 'Aditi Sharma', role: 'Student Innovator', text: 'Thank you Professor! Our Municipal Issue Solver App project request is live in the Research Collaboration Board!' },
    { sender: 'Rahul Varma', role: 'Lead Dev', text: 'Excellent! I have submitted a team join request to assist with backend API optimization.' }
  ],
  'state-issue-apps': [
    { sender: 'Aditi Sharma', role: 'Student Innovator', text: 'We just updated the Redis caching repo for the state drainage app. Let us test with 500 concurrent ward submissions.' }
  ],
  'aiml-specialization': [
    { sender: 'Prof. K. Reddy (JNTU)', role: 'Faculty Mentor', text: 'Indic-LLM fine-tuning session scheduled for Thursday 6 PM.' }
  ]
};

// ==========================================================================
// Initialization & Data Loading
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  initDOMListeners();
  loadDataFromBackend();
  applyViewMode();
  applyUserToUI();
  renderHeroAndStats();
  renderPosts();
  renderProjectsBoard();
  renderNearbyRadar();
  renderDomains();
  renderMembersList();
  renderChatMessages();
});

function loadDataFromBackend() {
  fetch('/api/app-data')
    .then(res => res.json())
    .then(data => {
      if (data && data.statesData) {
        statesDatabase = Object.assign(statesDatabase, data.statesData);
        if (data.posts && data.posts.length > 0) livePosts = data.posts.concat(livePosts);
        if (data.projects && data.projects.length > 0) researchProjects = data.projects.concat(researchProjects);
        renderHeroAndStats();
        renderPosts();
        renderProjectsBoard();
      }
    })
    .catch(err => {
      console.log('Loaded client-side database cache:', err);
    });
}

// ==========================================================================
// View Mode Switcher (Public Discovery vs Verified Custom Hub)
// ==========================================================================

function applyViewMode() {
  const publicViewBtn = document.getElementById('publicViewBtn');
  const verifiedDashboardBtn = document.getElementById('verifiedDashboardBtn');
  const publicLandingView = document.getElementById('publicLandingView');
  const verifiedDashboardView = document.getElementById('verifiedDashboardView');
  const userProfileBtn = document.getElementById('userProfileBtn');

  if (isLoggedIn) {
    if (publicLandingView) publicLandingView.style.display = 'none';
    if (verifiedDashboardView) verifiedDashboardView.style.display = 'block';
    if (publicViewBtn) publicViewBtn.classList.remove('active');
    if (verifiedDashboardBtn) verifiedDashboardBtn.classList.add('active');
    if (userProfileBtn) userProfileBtn.style.display = 'flex';
  } else {
    if (publicLandingView) publicLandingView.style.display = 'block';
    if (verifiedDashboardView) verifiedDashboardView.style.display = 'none';
    if (publicViewBtn) publicViewBtn.classList.add('active');
    if (verifiedDashboardBtn) verifiedDashboardBtn.classList.remove('active');
    if (userProfileBtn) userProfileBtn.style.display = 'none';
  }
}

// ==========================================================================
// DOM Listeners & Handlers
// ==========================================================================

function initDOMListeners() {
  // Public vs Verified Toggle
  const publicViewBtn = document.getElementById('publicViewBtn');
  const verifiedDashboardBtn = document.getElementById('verifiedDashboardBtn');

  if (publicViewBtn) {
    publicViewBtn.addEventListener('click', () => {
      isLoggedIn = false;
      applyViewMode();
    });
  }
  if (verifiedDashboardBtn) {
    verifiedDashboardBtn.addEventListener('click', () => {
      isLoggedIn = true;
      applyViewMode();
      applyUserToUI();
      renderPosts();
    });
  }

  // 3-Tier Level Switcher
  const levelBtns = document.querySelectorAll('.level-btn[data-level]');
  levelBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      levelBtns.forEach(b => b.classList.remove('active'));
      const target = e.currentTarget;
      target.classList.add('active');
      currentLevel = target.dataset.level;
      handleLevelChange(currentLevel);
    });
  });

  // State Selector
  const stateSelect = document.getElementById('stateSelect');
  if (stateSelect) {
    stateSelect.addEventListener('change', (e) => {
      currentState = e.target.value;
      renderHeroAndStats();
      renderPosts();
      renderProjectsBoard();
      renderMembersList();
    });
  }

  // Persona Quick Switcher Chips
  const personaChips = document.querySelectorAll('.persona-chip');
  personaChips.forEach(chip => {
    chip.addEventListener('click', (e) => {
      personaChips.forEach(c => c.classList.remove('active'));
      const target = e.currentTarget;
      target.classList.add('active');
      const personaKey = target.dataset.persona;
      switchPersona(personaKey);
    });
  });

  // Main Tabs Navigation
  const tabBtns = document.querySelectorAll('.tab-btn, .mobile-dock-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const tabKey = e.currentTarget.dataset.tab;
      switchTab(tabKey);
    });
  });

  // Post Composer & Clear Role Filter
  const submitPostBtn = document.getElementById('submitPostBtn');
  if (submitPostBtn) submitPostBtn.addEventListener('click', handleCreatePost);

  const clearRoleFilterBtn = document.getElementById('clearRoleFilterBtn');
  if (clearRoleFilterBtn) {
    clearRoleFilterBtn.addEventListener('click', () => {
      activeRoleFilterOnly = !activeRoleFilterOnly;
      // The text now reflects the action to be taken, which is more intuitive.
      clearRoleFilterBtn.textContent = activeRoleFilterOnly ? 'Show All Professions' : 'Filter to My Profession Only';
      renderPosts();
    });
  }

  // Workspace Channel Switching
  const channelItems = document.querySelectorAll('.channel-item');
  channelItems.forEach(item => {
    item.addEventListener('click', (e) => {
      channelItems.forEach(i => i.classList.remove('active'));
      const target = e.currentTarget;
      target.classList.add('active');
      activeChannel = target.dataset.channel;
      document.getElementById('activeChannelName').textContent = target.textContent;
      renderChatMessages();
    });
  });

  // Workspace Send Chat
  const sendWorkspaceMsgBtn = document.getElementById('sendWorkspaceMsgBtn');
  const workspaceChatInput = document.getElementById('workspaceChatInput');
  if (sendWorkspaceMsgBtn && workspaceChatInput) {
    sendWorkspaceMsgBtn.addEventListener('click', () => {
      sendWorkspaceMessage(workspaceChatInput.value);
    });
    workspaceChatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendWorkspaceMessage(workspaceChatInput.value);
    });
  }

  // AI Assistant Controls
  const aiFabBtn = document.getElementById('aiFabBtn');
  const openAiAssistantBtn = document.getElementById('openAiAssistantBtn');
  const publicAskAiBtn = document.getElementById('publicAskAiBtn');
  const aiChatWindow = document.getElementById('aiChatWindow');
  const closeAiChatBtn = document.getElementById('closeAiChatBtn');
  const sendAiChatBtn = document.getElementById('sendAiChatBtn');
  const aiChatInput = document.getElementById('aiChatInput');

  function toggleAiWindow() {
    aiChatWindow.classList.toggle('open');
    if (aiChatWindow.classList.contains('open')) aiChatInput.focus();
  }

  if (aiFabBtn) aiFabBtn.addEventListener('click', toggleAiWindow);
  if (openAiAssistantBtn) openAiAssistantBtn.addEventListener('click', toggleAiWindow);
  if (publicAskAiBtn) publicAskAiBtn.addEventListener('click', toggleAiWindow);
  if (closeAiChatBtn) closeAiChatBtn.addEventListener('click', toggleAiWindow);

  if (sendAiChatBtn && aiChatInput) {
    sendAiChatBtn.addEventListener('click', handleAiQuery);
    aiChatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') handleAiQuery();
    });
  }

  // Member Search Input
  const memberSearchInput = document.getElementById('memberSearchInput');
  if (memberSearchInput) {
    memberSearchInput.addEventListener('input', (e) => {
      memberSearchQuery = e.target.value.toLowerCase();
      renderMembersList();
    });
  }

  // Verification & Onboarding Modals
  const loginModalBtn = document.getElementById('loginModalBtn');
  const signupModalBtn = document.getElementById('signupModalBtn');
  const publicVerifyBtn = document.getElementById('publicVerifyBtn');
  const bannerVerifyBtn = document.getElementById('bannerVerifyBtn');
  const wizardCloseBtn = document.getElementById('wizardCloseBtn');
  const wizardNextBtn = document.getElementById('wizardNextBtn');
  const wizardBackBtn = document.getElementById('wizardBackBtn');
  const wizardRole = document.getElementById('wizardRole');

  // Modal Tab Switching (Login vs Verify)
  const modalTabVerify = document.getElementById('modalTabVerify');
  const modalTabLogin = document.getElementById('modalTabLogin');
  const loginFormBody = document.getElementById('loginFormBody');
  const verifyFormBody = document.getElementById('verifyFormBody');
  const submitLoginBtn = document.getElementById('submitLoginBtn');

  function showModalLoginView() {
    if (loginFormBody) loginFormBody.style.display = 'block';
    if (verifyFormBody) verifyFormBody.style.display = 'none';
    if (modalTabLogin) { modalTabLogin.className = 'btn-primary'; }
    if (modalTabVerify) { modalTabVerify.className = 'btn-secondary'; }
  }

  function showModalVerifyView() {
    if (loginFormBody) loginFormBody.style.display = 'none';
    if (verifyFormBody) verifyFormBody.style.display = 'block';
    if (modalTabLogin) { modalTabLogin.className = 'btn-secondary'; }
    if (modalTabVerify) { modalTabVerify.className = 'btn-primary'; }
  }

  if (modalTabLogin) modalTabLogin.addEventListener('click', showModalLoginView);
  if (modalTabVerify) modalTabVerify.addEventListener('click', showModalVerifyView);

  if (loginModalBtn) {
    loginModalBtn.addEventListener('click', () => {
      openOnboardingModal();
      showModalLoginView();
    });
  }

  if (signupModalBtn) {
    signupModalBtn.addEventListener('click', () => {
      openOnboardingModal();
      showModalVerifyView();
    });
  }

  if (publicVerifyBtn) publicVerifyBtn.addEventListener('click', openOnboardingModal);
  if (bannerVerifyBtn) bannerVerifyBtn.addEventListener('click', openOnboardingModal);
  if (wizardCloseBtn) wizardCloseBtn.addEventListener('click', closeOnboardingModal);

  // Submit Login Handler
  if (submitLoginBtn) {
    submitLoginBtn.addEventListener('click', () => {
      const email = document.getElementById('loginEmailInput').value || 'user@domain.com';
      const roleKey = document.getElementById('loginRoleSelect').value || 'student';
      
      switchPersona(roleKey);
      closeOnboardingModal();
      alert(`Welcome back! Logged in as ${currentUser.name} (${currentUser.role}). Your custom dashboard is live!`);
    });
  }

  if (wizardRole) {
    wizardRole.addEventListener('change', (e) => {
      updateProofLabelText(e.target.value);
    });
  }

  // Project Creation Modal
  const openCreateProjectModalBtn = document.getElementById('openCreateProjectModalBtn');
  const createProjectBoardBtn = document.getElementById('createProjectBoardBtn');
  const createProjectModal = document.getElementById('createProjectModal');
  const closeProjectModalBtn = document.getElementById('closeProjectModalBtn');
  const submitProjectModalBtn = document.getElementById('submitProjectModalBtn');

  function openProjectModal() {
    if (createProjectModal) createProjectModal.style.display = 'flex';
  }
  function closeProjectModal() {
    if (createProjectModal) createProjectModal.style.display = 'none';
  }

  if (openCreateProjectModalBtn) openCreateProjectModalBtn.addEventListener('click', openProjectModal);
  if (createProjectBoardBtn) createProjectBoardBtn.addEventListener('click', openProjectModal);
  if (closeProjectModalBtn) closeProjectModalBtn.addEventListener('click', closeProjectModal);
  if (submitProjectModalBtn) submitProjectModalBtn.addEventListener('click', handleCreateProjectSubmission);

  // Theme Toggle
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('light-theme');
      themeToggleBtn.textContent = document.body.classList.contains('light-theme') ? '☀️' : '🌓';
    });
  }

  // Wizard Navigation
  let currentWizardStep = 1;
  if (wizardNextBtn) {
    wizardNextBtn.addEventListener('click', () => {
      if (currentWizardStep < 4) {
        currentWizardStep++;
        updateWizardView(currentWizardStep);
      } else {
        const name = document.getElementById('wizardName').value || 'Aditi Sharma';
        const roleVal = document.getElementById('wizardRole').value || 'student';
        const state = document.getElementById('wizardState').value || 'tg';
        const org = document.getElementById('wizardOrg').value || 'JNTU Hyderabad';
        const proofId = document.getElementById('wizardProofId').value || 'VERIFIED-ID-2026';

        let matchedPillar = 'education';
        let matchedRoleTitle = 'Student Innovator';

        if (roleVal === 'tech') { matchedPillar = 'tech'; matchedRoleTitle = 'Cyber Architect'; }
        else if (roleVal === 'police') { matchedPillar = 'police'; matchedRoleTitle = 'Police Officer'; }
        else if (roleVal === 'lawyer') { matchedPillar = 'legal'; matchedRoleTitle = 'High Court Advocate'; }
        else if (roleVal === 'builder') { matchedPillar = 'builders'; matchedRoleTitle = 'Master Architect'; }
        else if (roleVal === 'media') { matchedPillar = 'media'; matchedRoleTitle = 'Civic Press Producer'; }

        currentUser = {
          name: name,
          role: matchedRoleTitle,
          title: `${matchedRoleTitle} • ${org}`,
          pillar: matchedPillar,
          state: state,
          city: 'State Hub Chapter',
          branch: 'Specialization Track',
          proofId: proofId,
          avatar: name.charAt(0).toUpperCase(),
          xp: 350,
          trust: 98,
          badge: `Verified ${matchedRoleTitle}`
        };

        isLoggedIn = true;
        currentState = state;
        const stateSelect = document.getElementById('stateSelect');
        if (stateSelect) stateSelect.value = state;

        applyViewMode();
        applyUserToUI();
        renderHeroAndStats();
        renderPosts();
        renderProjectsBoard();
        closeOnboardingModal();
        switchTab('feedTab');
        alert(`Congratulations ${name}! Your ${matchedRoleTitle} ID (${proofId}) is verified. Welcome to your customized home dashboard!`);
      }
    });
  }

  if (wizardBackBtn) {
    wizardBackBtn.addEventListener('click', () => {
      if (currentWizardStep > 1) {
        currentWizardStep--;
        updateWizardView(currentWizardStep);
      }
    });
  }
}

function updateProofLabelText(role) {
  const proofLabelText = document.getElementById('proofLabelText');
  const wizardProofId = document.getElementById('wizardProofId');
  if (!proofLabelText || !wizardProofId) return;

  if (role === 'student') {
    proofLabelText.textContent = 'College Roll No / Student ID Number';
    wizardProofId.placeholder = 'e.g. JNTUH-2026-CS-408';
  } else if (role === 'tech') {
    proofLabelText.textContent = 'Company Employee ID / Developer Handle';
    wizardProofId.placeholder = 'e.g. EMP-77402-KA';
  } else if (role === 'police') {
    proofLabelText.textContent = 'Police Badge ID / Station Code';
    wizardProofId.placeholder = 'e.g. IPS-AP-2014-99';
  } else if (role === 'lawyer') {
    proofLabelText.textContent = 'Bar Council Enrollment Number';
    wizardProofId.placeholder = 'e.g. BAR-KA-2018-441';
  } else if (role === 'builder') {
    proofLabelText.textContent = 'Council of Architecture (COA) / License No';
    wizardProofId.placeholder = 'e.g. COA-DL-8821';
  } else if (role === 'media') {
    proofLabelText.textContent = 'Press Accreditation / Channel Handle';
    wizardProofId.placeholder = 'e.g. PRESS-MH-990';
  } else {
    proofLabelText.textContent = 'Government ID / Verification Proof Number';
    wizardProofId.placeholder = 'e.g. GOVT-VERIFIED-2026';
  }
}

// ==========================================================================
// Tab & Level Switcher Handlers
// ==========================================================================

function switchTab(tabId) {
  activeTab = tabId;
  const tabBtns = document.querySelectorAll('.tab-btn');
  const dockBtns = document.querySelectorAll('.mobile-dock-btn');
  const viewContents = document.querySelectorAll('.tab-view-content');

  tabBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tabId));
  dockBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tabId));
  viewContents.forEach(view => view.style.display = view.id === tabId ? 'block' : 'none');

  window.scrollTo({ top: 380, behavior: 'smooth' });
}

function handleLevelChange(level) {
  const stateSelect = document.getElementById('stateSelect');
  if (level === 'nation') {
    currentState = 'all_india';
    if (stateSelect) stateSelect.value = 'all_india';
  } else {
    if (currentState === 'all_india') currentState = 'tg';
    if (stateSelect) stateSelect.value = currentState;
  }

  renderHeroAndStats();
  renderPosts();
  renderProjectsBoard();
  renderMembersList();
}

function switchPersona(personaKey) {
  if (personas[personaKey]) {
    currentUser = personas[personaKey];
    currentState = currentUser.state;
    isLoggedIn = true;

    const stateSelect = document.getElementById('stateSelect');
    if (stateSelect) stateSelect.value = currentState;

    applyViewMode();
    applyUserToUI();
    renderHeroAndStats();
    renderPosts();
    renderProjectsBoard();
    renderMembersList();
  }
}

function applyUserToUI() {
  document.getElementById('topbarUserName').textContent = currentUser.name;
  document.getElementById('topbarUserRole').textContent = currentUser.role;
  document.getElementById('userAvatarChar').textContent = currentUser.avatar;
  
  const composerAvatar = document.getElementById('composerAvatar');
  const composerName = document.getElementById('composerName');
  const composerRole = document.getElementById('composerRole');
  if (composerAvatar) composerAvatar.textContent = currentUser.avatar;
  if (composerName) composerName.textContent = currentUser.name;
  if (composerRole) composerRole.textContent = currentUser.title;

  const dashUserName = document.getElementById('dashUserName');
  const dashBadge = document.getElementById('dashBadge');
  const dashUserTitle = document.getElementById('dashUserTitle');
  const dashUserGeo = document.getElementById('dashUserGeo');
  const dashAvatar = document.getElementById('dashAvatar');
  const dashXp = document.getElementById('dashXp');
  const filterRoleText = document.getElementById('filterRoleText');
  const filterStateText = document.getElementById('filterStateText');

  if (dashUserName) dashUserName.textContent = currentUser.name;
  if (dashBadge) dashBadge.textContent = `✓ ${currentUser.badge}`;
  if (dashUserTitle) dashUserTitle.textContent = currentUser.title;
  if (dashUserGeo) dashUserGeo.textContent = `📍 Nearby Radar: ${currentUser.city}`;
  if (dashAvatar) dashAvatar.textContent = currentUser.avatar;
  if (dashXp) dashXp.textContent = `${currentUser.xp} XP`;
  if (filterRoleText) filterRoleText.textContent = currentUser.role;
  if (filterStateText) filterStateText.textContent = currentState.toUpperCase();

  const profileNameBig = document.getElementById('profileNameBig');
  const profileRoleBig = document.getElementById('profileRoleBig');
  const profileGeoBig = document.getElementById('profileGeoBig');
  const profileAvatarBig = document.getElementById('profileAvatarBig');
  const profileXp = document.getElementById('profileXp');
  const profileTrust = document.getElementById('profileTrust');
  const profileBadgeName = document.getElementById('profileBadgeName');
  const proofRollNoText = document.getElementById('proofRollNoText');

  if (profileNameBig) profileNameBig.textContent = currentUser.name;
  if (profileRoleBig) profileRoleBig.textContent = currentUser.title;
  if (profileGeoBig) profileGeoBig.textContent = `${currentUser.city}, India • Verified Member`;
  if (profileAvatarBig) profileAvatarBig.textContent = currentUser.avatar;
  if (profileXp) profileXp.textContent = `${currentUser.xp} XP`;
  if (profileTrust) profileTrust.textContent = `${currentUser.trust}/100`;
  if (profileBadgeName) profileBadgeName.textContent = currentUser.badge;
  if (proofRollNoText) proofRollNoText.textContent = `✓ Verified (${currentUser.proofId})`;
}

// ==========================================================================
// Rendering Engine: Posts, Projects Board & Nearby Radar
// ==========================================================================

function renderHeroAndStats() {
  const currentData = statesDatabase[currentState] || statesDatabase.tg;
  const activeWorkspaceTitle = document.getElementById('activeWorkspaceTitle');
  const activeWorkspaceAvatar = document.getElementById('activeWorkspaceAvatar');
  if (activeWorkspaceTitle) activeWorkspaceTitle.textContent = `${currentData.name} Collaboration Hub`;
  if (activeWorkspaceAvatar) activeWorkspaceAvatar.textContent = currentState.toUpperCase().slice(0, 2);
}

function renderPosts() {
  const postsStream = document.getElementById('postsStream');
  if (!postsStream) return;

  // Enhanced filtering logic to strictly enforce profession-based content visibility for logged-in users.
  let filtered = livePosts.filter(post => {
    const matchState = (currentState === 'all_india') || (post.state === currentState) || (post.state === 'all_india');
    const matchRolePillar = !activeRoleFilterOnly || (post.pillar === currentUser.pillar) || (post.pillar === 'general') || (post.pillar === currentPillar);
    return matchState && matchRolePillar;
  });

  if (filtered.length === 0) {
    postsStream.innerHTML = `
      <div class="post-card" style="text-align: center; padding: 40px;">
        <div style="font-size: 2rem; margin-bottom: 8px;">🇮🇳</div>
        <h3 style="font-family: var(--font-display); font-size: 1.1rem; margin-bottom: 6px;">No posts matching your verified profession in this state yet.</h3>
        <p style="font-size: 0.85rem; color: var(--text-secondary);">Be the first pioneer in your field to publish a research update or local area alert!</p>
      </div>
    `;
    return;
  }

  postsStream.innerHTML = filtered.map(post => {
    const scopeClass = post.scope === 'nation' ? 'nation' : (post.scope === 'local' ? 'local' : 'state');
    const scopeLabel = post.scope === 'nation' ? '🇮🇳 Pan-India' : (post.scope === 'local' ? '📍 Nearby Area' : '🏛️ State Level');

    return `
      <article class="post-card">
        <div class="post-header">
          <div class="post-author-block">
            <div class="post-avatar">${post.author.charAt(0)}</div>
            <div>
              <div class="author-name">${post.author}</div>
              <div class="author-role-badge">${post.role} • <span style="color: var(--text-muted); font-weight: normal;">${post.time || 'Recently'}</span></div>
            </div>
          </div>
          <div class="post-badges-right">
            <span class="scope-badge ${scopeClass}">${scopeLabel}</span>
          </div>
        </div>
        <h3 class="post-title">${post.title}</h3>
        <p class="post-body">${post.content}</p>
        <div class="post-actions-bar">
          <button class="post-action-btn" onclick="handleLikePost(${post.id})">
            <span>❤️</span> <span>${post.likes} Upvotes</span>
          </button>
          <button class="post-action-btn" onclick="switchTab('workspaceTab')">
            <span>💬</span> <span>${post.comments} Discussions</span>
          </button>
          <button class="post-action-btn" onclick="handleSharePost('${post.title}')">
            <span>🔗</span> <span>Share Work</span>
          </button>
        </div>
      </article>
    `;
  }).join('');
}

function handleLikePost(postId) {
  const post = livePosts.find(p => p.id === postId);
  if (post) {
    post.likes += 1;
    renderPosts();
  }
}

function handleSharePost(title) {
  alert(`Work link for "${title}" copied to clipboard! Shared with verified peers in your state.`);
}

function handleCreatePost() {
  const titleInput = document.getElementById('postTitleInput');
  const contentInput = document.getElementById('postContentInput');
  const scopeSelect = document.getElementById('postScopeSelect');
  const pillarSelect = document.getElementById('postPillarSelect');

  if (!titleInput.value.trim() || !contentInput.value.trim()) {
    alert('Please enter both a title and description.');
    return;
  }

  const newPost = {
    id: Date.now(),
    author: currentUser.name,
    role: currentUser.title,
    state: currentState,
    scope: scopeSelect.value,
    pillar: pillarSelect.value,
    domain: 'General Collaboration',
    title: titleInput.value.trim(),
    content: contentInput.value.trim(),
    likes: 1,
    comments: 0,
    time: 'Just now'
  };

  livePosts.unshift(newPost);
  titleInput.value = '';
  contentInput.value = '';

  currentUser.xp += 25;
  applyUserToUI();
  renderPosts();
  alert('Your update has been published to your verified profession feed! +25 XP earned.');
}

// Research & Project Collaboration Board
function renderProjectsBoard() {
  const projectsGrid = document.getElementById('projectsGrid');
  const sideProjectsList = document.getElementById('sideProjectsList');

  const filteredProjects = researchProjects.filter(prj => (currentState === 'all_india' || prj.state_id === currentState || prj.state_id === 'all_india'));

  if (projectsGrid) {
    projectsGrid.innerHTML = filteredProjects.map(prj => `
      <div class="domain-card-item">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span style="font-size: 0.72rem; color: var(--saffron); font-weight: 700; text-transform: uppercase;">${prj.pillar.toUpperCase()} RESEARCH</span>
          <span style="font-size: 0.7rem; background: var(--emerald-glow); color: var(--emerald); padding: 2px 8px; border-radius: 999px; font-weight: 700;">${prj.status || 'Open'}</span>
        </div>
        <h3 style="font-family: var(--font-display); font-size: 1.15rem; margin-bottom: 6px;">${prj.title}</h3>
        <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">${prj.description}</p>
        <div style="font-size: 0.78rem; color: var(--cyan); font-weight: 600; margin-bottom: 14px;">
          🛠️ Roles Needed: ${prj.roles_needed}
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 10px;">
          <span style="font-size: 0.75rem; color: var(--text-muted);">${prj.members_joined} Peers Working</span>
          <button class="btn-primary" style="padding: 6px 12px; font-size: 0.78rem;" onclick="handleJoinResearchTeam('${prj.title}')">Request to Join Team</button>
        </div>
      </div>
    `).join('');
  }

  if (sideProjectsList) {
    sideProjectsList.innerHTML = filteredProjects.slice(0, 3).map(prj => `
      <div style="padding: 10px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 8px; margin-bottom: 8px;">
        <div style="font-size: 0.72rem; color: var(--saffron); font-weight: 700;">${prj.pillar.toUpperCase()} RESEARCH</div>
        <div style="font-weight: 700; font-size: 0.85rem; margin: 2px 0;">${prj.title}</div>
        <div style="font-size: 0.75rem; color: var(--cyan);">Roles: ${prj.roles_needed}</div>
        <button class="btn-secondary" style="width: 100%; margin-top: 6px; padding: 4px; font-size: 0.72rem;" onclick="handleJoinResearchTeam('${prj.title}')">Request to Join Team</button>
      </div>
    `).join('');
  }
}

function handleJoinResearchTeam(title) {
  currentUser.xp += 35;
  applyUserToUI();
  alert(`Request to join "${title}" team submitted! The research lead has been notified. +35 XP earned.`);
}

function handleCreateProjectSubmission() {
  const titleInput = document.getElementById('projectTitleInput');
  const pillarSelect = document.getElementById('projectPillarSelect');
  const descInput = document.getElementById('projectDescInput');
  const rolesInput = document.getElementById('projectRolesInput');

  if (!titleInput.value.trim() || !descInput.value.trim()) {
    alert('Please enter a research title and description.');
    return;
  }

  const newPrj = {
    id: Date.now(),
    author_name: currentUser.name,
    author_role: currentUser.title,
    pillar: pillarSelect.value,
    state_id: currentState,
    title: titleInput.value.trim(),
    description: descInput.value.trim(),
    roles_needed: rolesInput.value.trim() || 'Peer Collaborators',
    members_joined: 1,
    status: 'Open for Research & Team'
  };

  researchProjects.unshift(newPrj);
  titleInput.value = '';
  descInput.value = '';
  rolesInput.value = '';

  const createProjectModal = document.getElementById('createProjectModal');
  if (createProjectModal) createProjectModal.style.display = 'none';

  currentUser.xp += 50;
  applyUserToUI();
  renderProjectsBoard();
  alert('Your Research & Project Idea Request has been posted to verified peers across India! +50 XP earned.');
}

// Nearby Activity Radar
function renderNearbyRadar() {
  const nearbyRadarList = document.getElementById('nearbyRadarList');
  if (!nearbyRadarList) return;

  // Filter nearby meetings to only show those relevant to the user's professional pillar.
  const filteredMeetings = nearbyMeetings.filter(mt => mt.pillar === currentUser.pillar);

  nearbyRadarList.innerHTML = filteredMeetings.map((mt, idx) => `
    <div class="clean-drive-card">
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <div style="font-size: 0.75rem; color: var(--saffron); font-weight: 700; text-transform: uppercase;">📅 ${mt.time} • ${mt.location}</div>
          <h3 style="font-family: var(--font-display); font-size: 1.1rem; color: var(--text-primary); margin: 4px 0;">${mt.title}</h3>
          <p style="font-size: 0.82rem; color: var(--text-secondary);">Organized by ${mt.organizer} • ${mt.attendees} Peers Attending</p>
        </div>
        <button class="btn-primary" style="padding: 6px 14px; font-size: 0.8rem;" onclick="handleRsvpMeeting(${idx})">RSVP Meeting</button>
      </div>
    </div>
  `).join('');
}

function handleRsvpMeeting(idx) {
  const meeting = nearbyMeetings.find((m, i) => i === idx);
  meeting.attendees += 1;
  currentUser.xp += 30;
  applyUserToUI();
  renderNearbyRadar();
  alert(`RSVP confirmed for "${meeting.title}"! Calendar invite sent to your verified email. +30 XP earned.`);
}

// Members Directory Tab
function renderMembersList() {
  const membersContainer = document.getElementById('membersListContainer');
  if (!membersContainer) return;

  // 1. Primary filter for state, pillar, and self-exclusion
  let filteredMembers = verifiedUsers.filter(user => {
    const isSameState = user.state === currentState || user.state === 'all_india';
    const isSamePillar = user.pillar === currentUser.pillar;
    const isNotCurrentUser = user.name !== currentUser.name;
    return isSameState && isSamePillar && isNotCurrentUser;
  });

  // 2. Secondary filter based on the search query
  if (memberSearchQuery) {
    filteredMembers = filteredMembers.filter(member =>
      member.name.toLowerCase().includes(memberSearchQuery) ||
      member.city.toLowerCase().includes(memberSearchQuery)
    );
  }

  // 3. Render the final list
  if (filteredMembers.length === 0) {
    membersContainer.innerHTML = `<div class="post-card" style="text-align: center; padding: 40px;">
      <div style="font-size: 2rem; margin-bottom: 8px;">🧑‍🤝‍🧑</div>
      <h3 style="font-family: var(--font-display); font-size: 1.1rem; margin-bottom: 6px;">No other verified peers found in your profession for this state yet.</h3>
      <p style="font-size: 0.85rem; color: var(--text-secondary);">Be a pioneer and invite colleagues to join the platform!</p>
    </div>`;
    return;
  }

  const highlightMatch = (text, query) => {
    if (!query) return text;
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, `<mark class="search-highlight">$1</mark>`);
  };

  membersContainer.innerHTML = filteredMembers.map(member => {
    const highlightedName = highlightMatch(member.name, memberSearchQuery);
    const highlightedCity = highlightMatch(member.city, memberSearchQuery);

    return `
      <div class="member-card">
        <div class="post-avatar">${member.avatar}</div>
        <div class="member-details">
          <div class="member-name">${highlightedName}</div>
          <div class="member-title">${member.title}</div>
          <div class="member-location">📍 ${highlightedCity}</div>
      </div>
      <button class="btn-secondary" style="padding: 6px 12px; font-size: 0.78rem;" onclick="alert('Connection request sent to ${member.name}!')">Connect</button>
    </div>
  `}).join('');
}

// 25 Domains Directory Render
function renderDomains(query = '') {
  const container = document.getElementById('domainsExplorerGrid');
  if (!container) return;

  let filtered = platformDomains;
  if (query) {
    filtered = platformDomains.filter(d => 
      d.name.toLowerCase().includes(query) || 
      d.subdomains.some(s => s.toLowerCase().includes(query))
    );
  }

  container.innerHTML = filtered.map(domain => `
    <div class="domain-card-item">
      <div class="domain-title-wrap">
        <div class="domain-name">${domain.icon} ${domain.name}</div>
        <span class="domain-count-badge">${domain.subdomains.length} Subdomains</span>
      </div>
      <div class="subdomain-chips">
        ${domain.subdomains.map(sub => `<span class="sub-chip" onclick="handleSubdomainClick('${sub}', '${domain.name}')">${sub}</span>`).join('')}
      </div>
    </div>
  `).join('');
}

function handleSubdomainClick(subdomain, domainName) {
  alert(`Connecting to ${domainName} -> [${subdomain}] active room.`);
  switchTab('workspaceTab');
}

// Workspace Live Chat & Channels
function renderChatMessages() {
  const chatStream = document.getElementById('chatStream');
  if (!chatStream) return;

  const msgs = channelChats[activeChannel] || channelChats.general;
  chatStream.innerHTML = msgs.map(msg => `
    <div class="chat-msg-card">
      <div class="post-avatar" style="width: 36px; height: 36px; font-size: 0.8rem;">${msg.sender.charAt(0)}</div>
      <div class="chat-msg-content">
        <div class="chat-msg-header">
          <span class="chat-sender-name">${msg.sender}</span>
          <span style="font-size: 0.7rem; color: var(--emerald); font-weight: 600;">${msg.role}</span>
          <span class="chat-timestamp">Just now</span>
        </div>
        <div class="chat-text">${msg.text}</div>
      </div>
    </div>
  `).join('');

  chatStream.scrollTop = chatStream.scrollHeight;
}

function sendWorkspaceMessage(text) {
  if (!text || !text.trim()) return;

  if (!channelChats[activeChannel]) channelChats[activeChannel] = [];

  channelChats[activeChannel].push({
    sender: currentUser.name,
    role: currentUser.role,
    text: text.trim()
  });

  const workspaceChatInput = document.getElementById('workspaceChatInput');
  if (workspaceChatInput) workspaceChatInput.value = '';
  renderChatMessages();

  setTimeout(() => {
    if (!channelChats[activeChannel]) return;
    channelChats[activeChannel].push({
      sender: 'Prof. K. Reddy (Mentor)',
      role: 'Faculty Mentor',
      text: `Acknowledged @${currentUser.name}! Added to our state collaboration action list.`
    });
    renderChatMessages();
  }, 1200);
}

// AI Assistant Handler
function handleAiQuery() {
  const input = document.getElementById('aiChatInput');
  const stream = document.getElementById('aiMsgStream');
  const query = input.value.trim();
  if (!query) return;

  const userBubble = document.createElement('div');
  userBubble.className = 'ai-bubble user';
  userBubble.textContent = query;
  stream.appendChild(userBubble);
  input.value = '';
  stream.scrollTop = stream.scrollHeight;

  const botBubble = document.createElement('div');
  botBubble.className = 'ai-bubble';
  botBubble.innerHTML = '<em>Consulting Bharat Knowledge Base & State Councils...</em>';
  stream.appendChild(botBubble);
  stream.scrollTop = stream.scrollHeight;

  fetch('/api/ai/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: query, role: currentUser.role, state: currentState })
  })
  .then(res => res.json())
  .then(data => {
    botBubble.innerHTML = data.answer || 'Namaste! Ask me how to join research projects, find nearby meetings, or report civic issues.';
    stream.scrollTop = stream.scrollHeight;
  })
  .catch(() => {
    let answer = 'Namaste! Bharat AI Assistant at your service. ';
    answer += `You are currently logged in as a verified ${currentUser.role} in ${currentState.toUpperCase()}. Check the Research & Project Collaboration board to post work or request team members!`;
    botBubble.innerHTML = answer;
    stream.scrollTop = stream.scrollHeight;
  });
}

// Onboarding Wizard Logic
function openOnboardingModal() {
  const modal = document.getElementById('onboardingModal');
  if (modal) {
    modal.style.display = 'flex';
    updateWizardView(1);
  }
}

function closeOnboardingModal() {
  const modal = document.getElementById('onboardingModal');
  if (modal) modal.style.display = 'none';
}

function updateWizardView(step) {
  for (let i = 1; i <= 4; i++) {
    const stepEl = document.getElementById(`wizardStep${i}`);
    const indicatorEl = document.getElementById(`stepIndicator${i}`);
    if (stepEl) stepEl.style.display = i === step ? 'block' : 'none';
    if (indicatorEl) {
      indicatorEl.classList.toggle('active', i === step);
      indicatorEl.classList.toggle('completed', i < step);
    }
  }

  const backBtn = document.getElementById('wizardBackBtn');
  const nextBtn = document.getElementById('wizardNextBtn');
  const title = document.getElementById('modalStepTitle');
  const desc = document.getElementById('modalStepDesc');

  if (backBtn) backBtn.style.display = step > 1 ? 'block' : 'none';

  if (step === 1) {
    if (title) title.textContent = 'Step 1: Select Your Profession / Guild';
    if (desc) desc.textContent = 'Select whether you are a Student, Educator, IT/Cyber Lead, Police Officer, Lawyer, or Builder.';
    if (nextBtn) nextBtn.textContent = 'Submit Proof ID →';
  } else if (step === 2) {
    if (title) title.textContent = 'Step 2: Verification Proof & ID Details';
    if (desc) desc.textContent = 'Submit your Roll No, Bar Council Reg, Police Badge, COA License, or Employee ID for verification.';
    if (nextBtn) nextBtn.textContent = 'Select Location →';
  } else if (step === 3) {
    if (title) title.textContent = 'Step 3: State & City Location (Nearby Radar)';
    if (desc) desc.textContent = 'Set your location to unlock nearby activity radar and local area meetings.';
    if (nextBtn) nextBtn.textContent = 'Verify & Unlock Hub →';
  } else if (step === 4) {
    if (title) title.textContent = 'Step 4: Custom Home Dashboard Unlocked!';
    if (desc) desc.textContent = 'Your home feed is now customized to show ONLY updates matching your verified profession!';
    if (nextBtn) nextBtn.textContent = 'Enter Custom Hub 🚀';
  }
}

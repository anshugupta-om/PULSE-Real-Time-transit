## Title
**🚆 PULSE: Live Mumbai Transit Navigator**

## Tagline
**The Smart, Safe, and Proactive Transit Ecosystem for Mumbaikars. 🌆**

## Description
**PULSE is not just another map application; it is a complete B2C + B2G (Business-to-Government) transit ecosystem. Designed specifically for the chaos of Mumbai Locals, PULSE provides real-time proactive alerts, AI-driven crowd predictions, and robust safety features for commuters, while simultaneously generating actionable data logs for Transit Authorities.**

## Badges
**🚆 PULSE: Live Mumbai Transit Navigator**

![Python]
![Streamlit]
![SQLite3]
![Status]
![Safety](
![License](

> **The Smart, Safe, and Proactive Transit Ecosystem for Mumbaikars.** 🌆

##  Key Features & Capabilities

**🛡️ Advanced Safety & Accident Prevention**

*🚨 Guardian Mode (Women's Safety):** A 1-click SOS button that generates a secure live-tracking link and instantly triggers a "Red Alert" on the Admin Dashboard.*
* ⚠️ Station Hazard Warnings:** Pre-alerts users about station-specific risks (e.g., *Stampede risk at Dadar, Platform gap at Kurla*).*
* 🛑 Anti-Door Rushing Alert:** Sends a strict "Do Not De-board" warning when the train is exactly 3 minutes away to prevent moving-train accidents.*

**🧠 Smart Transit & AI**

* 🤖 AI Crowd Predictor:** Dynamically calculates crowd density percentages based on peak hours, station popularity, and weather conditions.*
* 🌧️ Monsoon Mode:** Automatically adjusts ETAs and routing logic to account for Mumbai's unpredictable heavy rains.*
* 📲 Proactive ETA Notifications:** Sends live Toast Alerts to the user's screen if a train is delayed or arriving early, eliminating the need to manually refresh.*

**🗺️ Core Navigation & Ticketing**
* 📍 Live Route Mapping:** Interactive Folium map integration showing the live transit path from source to destination.*

* 🌍 Multi-Language Support:** Accessible interface available in English, Hindi, and Marathi for all Mumbaikars.*

**🛠️ B2G (Business-to-Government) Admin Panel**
* 🗄️ Relational SQL Logging:** Every journey is assigned a unique `Journey ID`. All ETA updates, routes, and SOS triggers are systematically logged in a local SQLite database.*
* 👀 Active SOS Monitoring:** A dedicated sidebar panel for Transit Authorities to monitor live emergencies with exact user details and timestamps.*
* 📥 1-Click Data Management:** Admins can easily export the entire transit log as a CSV for crowd analysis or clear the database with a single click.*

**🎨 Premium UI/UX**
* ✨ Glassmorphism Design:** Modern, floating 3D dashboard metrics with interactive hover effects.*
* 🎬 Lottie Animations:** High-quality, engaging JSON animations integrated directly into the login interface.*

## RoadMap & MindMap
**PULSE_Transit_Ecosystem/**
│
├── 🖥️ 1. FRONTEND_UI_LAYER (Streamlit)
│   ├── 🎨 Custom_CSS/
│   │   ├── Glassmorphism_Cards
│   │   └── Gradient_Hover_Buttons
│   ├── 🎬 Lottie_Animations/
│   │   └── Login_Screen_Train_JSON
│   ├── 🗺️ Folium_Live_Maps/
│   │   └── Interactive_Route_Plotting
│   └── 🌍 Localization/
│       └── Multi_Language (EN, HI, MR)
│
├── ⚙️ 2. BACKEND_&_DATABASE (SQLite3)
│   ├── 🗄️ pulse_database.db
│   │   └── transit_logs_table
│   ├── 🔄 Operations/
│   │   ├── generate_journey_id()
│   │   ├── log_eta_updates()
│   │   └── log_sos_emergencies()
│   └── 🛠️ Admin_Controls/
│       ├── Active_SOS_Monitor
│       └── CSV_Data_Export
│
├── 🧩 3. MICROSERVICES (Python Modules)
│   ├── 🐍 app.py                  -> (Main Application & Logic Routing)
│   ├── 🐍 db_manager.py           -> (SQL Queries & Admin Panel Logic)
│   ├── 🐍 ai_predictor.py         -> (Crowd Density & Monsoon Logic)
│   ├── 🐍 womens_safety.py        -> (Guardian Mode & Tracking Links)
│   ├── 🐍 accident_prevention.py  -> (Hazards & De-boarding Alerts)
│   └── 🐍 ticket_generator.py     -> (Fare Calculation & QR Ticket)
│
├── 👥 4. USER_ROLES_&_FEATURES
│   ├── 🚇 Commuter (B2C)
│   │   ├── Enter Source/Destination
│   │   ├── Pay Fare & Get QR Ticket
│   │   ├── View AI Crowd Predictor
│   │   ├── Get Proactive ETA Push Alerts
│   │   └── Trigger SOS in Emergency
│   │
│   └── 👮 Transit_Admin (B2G)
│       ├── Secure Login Panel
│       ├── Monitor Red-Alert SOS Triggers
│       └── Download Commuter Data for Analytics
│
└── 🚀 5. FUTURE_ROADMAP (Post-Hackathon)
    ├── Phase_1: ☁️ Cloud Deployment (Render/AWS)
    ├── Phase_2: 📡 Real-time GPS API Integration
    ├── Phase_3: 💳 UPI Payment Gateway for Tickets
    └── Phase_4: 📱 React Native Mobile App Conversion

## Explaination of Flowchart
**🚶‍♀️ 1. The Commuter Flow (Normal User Journey)**
This section of the flowchart represents the experience of an everyday commuter navigating the app:

*Start:* The user opens the application, enters their name, and logs in using the "Commuter" portal.

*Input:* The user selects their transit Route (Line, Source, Destination) and toggles the Weather setting (Monsoon mode).

ai_predictor.py evaluates the selected route and weather conditions to calculate a real-time "Crowd Percentage."

*Action (Live Tracking):* The user clicks "Start Journey."

The system generates a unique Journey ID and uses db_manager.py to save the initial journey status as "Started" within the SQL database.

*End:* When the commuter checks the "Reached" box, the SQL database updates the journey status to "Completed," effectively ending the active tracking session.

**🚨 2. The Safety & Emergency Flow (Guardian Ecosystem)**
This is the most critical and high-impact component of the flowchart:

*Trigger:* During an active journey, the user presses the "🔴 TRIGGER SOS ALERT" button.

*Action 1 (User Side):* The womens_safety.py module immediately generates a secure live-location tracking link and displays it on the screen for the user to share with family or friends.

*Action 2 (Database Side):* Simultaneously, the system updates the SQL database in the background, changing the status of that specific Journey ID to "🚨 SOS EMERGENCY."

*Action 3 (Accident Prevention):* In parallel, the accident_prevention.py module continuously monitors the live ETA. The moment the ETA drops to exactly 3 minutes, it automatically triggers a strict "Do not jump off!" de-boarding warning to prevent moving-train accidents.

**👮‍♂️ 3. The Admin/B2G Flow (Backend Monitoring)**
This flowchart details the backend operations designed for Transit Authorities:

*Start:* The Admin logs into the portal using secure credentials.

*Processing:* The application calls db_manager.py to fetch all recorded transit logs directly from the SQLite database (pulse_database.db).

*Filtering (The Alert System):* * The system scans the active data: Are there any logs with the "🚨 SOS EMERGENCY" status?

*If YES:* A prominent Red Alert box instantly pops up in the Admin's sidebar, displaying the distressed user's exact location route and timestamp.

*End Action:* The Admin has full control to either download the entire transit log as a CSV file for analytical purposes or click the "Clear All Data" button to instantly reset the database for the next demo presentation. 

## Tech Stack
**PULSE_Tech_Stack/**
│
├── 🖥️ Frontend (UI & UX)
│   ├── ⚛️ Framework: Streamlit
│   ├── 🎨 Styling: Custom CSS3 (Glassmorphism, Hover Gradients)
│   ├── 🎬 Animations: Lottie JSON (streamlit-lottie)
│   └── 🗺️ Mapping Engine: Folium & streamlit-folium
│
├── ⚙️ Backend (Core Logic)
│   ├── 🐍 Language: Python 3.x
│   ├── 🐼 Data Processing: Pandas
│   └── 📦 Core Libraries: datetime, random, hashlib, requests, time
│
├── 🗄️ Database (Storage)
│   ├── 🗃️ Type: Relational SQL
│   ├── 🛢️ Engine: SQLite3
│   └── 🏗️ Schema: Dynamic Journey ID & SOS Logging
│
└── 🧠 Key Algorithms (Microservices)
    ├── 🎟️ Ticketing: Custom Cryptographic Hashing
    ├── 🤖 Crowd Prediction: Rule-based AI Weightage System
    └── 🚨 Safety Alerts: Real-time ETA Monitor Engine

## SetUp & Instructions
**Step 1: Check Python**
Make sure Python is installed on your computer.

**Step 2: Open the Project Folder**
Download the project files and keep them all in one folder (make sure app.py, db_manager.py, and all other files are together). Open your Command Prompt or Terminal and go to that folder.

**Step 3: Install the Required Tools**
Type this exact command in your terminal and press Enter. This will download all the necessary tools the app needs to run:
*pip install streamlit pandas folium streamlit-folium requests streamlit-lottie*

**Step 4: Start the App**
Once the installation is completely done, type this command and press Enter:
*streamlit run app.py*

**Step 5: View the App**
The app should automatically open in your web browser. If it does not open, just open Chrome or any browser and type this address:
*http://localhost:8501*   
And also the project is deployed using Streamlit, so you can use it for live demo *https://pulse-real-time-transit.streamlit.app/*

## ScreenShots

## Frequently Asked Questions (FAQs)

**Ques 1:** *🚇 What exactly is PULSE?*
**Ans:** *PULSE is a complete live transit ecosystem for Mumbai locals. It doesn’t just show routes; it predicts crowd density, warns about station hazards, generates dynamic QR tickets, and provides proactive safety alerts for commuters*.

**Ques 2:** *🚨 How does the Guardian Mode (SOS) protect commuters?*
**Ans:** *When a user feels unsafe and clicks the "🔴 TRIGGER SOS ALERT" button, two things happen instantly:*

*It generates a live-tracking link for the user to share with their family.*

*It sends a "Red Alert" directly to the Admin/Railway Authority dashboard with the user's exact location and timestamp.*

**Ques 3:** *🛑 How does PULSE prevent moving-train accidents?*
**Ans:** *Most local train accidents happen at the doors or platform gaps. PULSE monitors your live ETA. When the train is exactly 3 minutes away from your destination, it flashes a strict "Do not de-board / Anti-Door Rushing" warning to prevent commuters from jumping off early.*

**Ques 4:** *🧠 How does the AI Crowd Predictor work?
Ans: The built-in AI predictor calculates an estimated crowd percentage based on multiple real-world factors: the specific source/destination, peak travel hours, and whether the "Monsoon Mode" (heavy rains) is active.*

**Ques 5:** *🛠️ Who is the Admin Portal designed for?*
**Ans:** *The Admin Portal is a B2G (Business-to-Government) feature designed for Transit Authorities, Police, or Railway Admins. It allows them to monitor active SOS emergencies in real-time and export commuter travel logs (CSV) for crowd management and analysis.*

## Contribution & Acknowledgments
**🏆 Special Thanks to HackIndia Hackathon!** 
*A huge shoutout and heartfelt thanks to the organizers of the HackIndia Hackathon! This project, PULSE, was proudly conceptualized and built during this incredible event. Thank you for providing such an amazing platform for developers to innovate, solve real-world problems, and push the boundaries of technology. It has been an absolute honor and a massive learning experience to build this here! 🚀*

**💡 How to Contribute**
*We strongly believe in community-driven development! If you are a developer and have ideas to make Mumbai transit even safer and smarter, we welcome your contributions:*

1- *Fork the Project*

2- *Create your Feature Branch (git checkout -b feature/AmazingFeature)*

3- *Commit your Changes (git commit -m 'Added an AmazingFeature')*

4- *Push to the Branch (git push origin feature/AmazingFeature)*

**Open a Pull Request**

## Feedback & Support
**Got feedback, found a bug, or have a brilliant suggestion for PULSE? We'd love to hear from you!**

*Please open an Issue in this GitHub repository.*

**Drop a star ⭐ on the repo if you liked our approach to Women's Safety and Transit Management!**

## Future Enhancements
**Future Enhancements:** The Transit-Sustainability Ecosystem
Our vision for PULSE goes beyond just smart navigation.In the upcoming phases, we are evolving PULSE into a complete, unified Transit-Sustainability Ecosystem to bridge the gap between smart commuting and environmental responsibility.

*Here are the advanced components slated for our next major update:*

**🌱 Carbon Shield Tracking:** Integrating an advanced calculation logic to track, measure, and log the exact amount of CO2 saved per public transit journey directly into our SQL transit database. Commuters will be able to see their personal "Green Impact."

**🔔 Eco-Alert System:** Implementing a robust ntfy-based push notification setup to send commuters proactive "Low-Carbon Departure Alerts" and green journey completion updates directly to their devices.

**♻️ Smart E-Waste Reporting Portal:** Adding a dedicated community-driven section in the app where commuters can report broken or defunct station electronics (like display boards or ticket machines). This data will feed directly into an AI-driven waste classification engine for rapid authority response.

**🔐 Secure Unified Authentication:** Upgrading the current login system with a highly secure, custom-built authentication and signup architecture to support the expanded unified commuter portal.

**🌍 Unified Green Branding:** Merging smart transit features with eco-conscious tracking under a single, powerful identity, encouraging Mumbaikars to travel not just faster, but greener.

## Authors
Anshu Gupta and Mili Srivastava with Team



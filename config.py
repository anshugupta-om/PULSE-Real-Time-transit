# config.py - Centralized Configuration & Constants

MUMBAI_LOCATIONS = [
    "Andheri East", "Andheri West", "Bandra Kurla Complex (BKC)", 
    "Bandra West", "Borivali", "Churchgate", "CSMT", "Dadar", 
    "Goregaon", "Kurla", "Lower Parel", "Marine Drive", "Thane"
]

KNOWN_COORDS = {
    "Andheri East": [19.1136, 72.8697], 
    "Bandra Kurla Complex (BKC)": [19.0653, 72.8656], 
    "Borivali": [19.2307, 72.8567], 
    "Churchgate": [18.9322, 72.8264], 
    "Dadar": [19.0178, 72.8478], 
    "Kurla": [19.0732, 72.8798], 
    "CSMT": [18.9400, 72.8353], 
    "Thane": [19.2183, 72.9781]
}

LANGUAGES = {
    "English": {
        "title": "🚆 PULSE: Real-Time Transit Navigator",
        "subtitle": "Search locations, track live routes, check crowd density, and get smart alerts.",
        "line": "Select Line",
        "from": "📍 From",
        "to": "🏁 To",
        "monsoon": "🌧️ Is it Raining? (Monsoon Mode)",
        "start": "Start Live Tracking 🚀",
        "same_loc": "Source and Destination cannot be the same!",
        "tracking_msg": "🟢 Tracking:",
        "dashboard": "### 📡 Live Status Dashboard",
        "map_title": "### 🗺️ Live Route Map",
        "orig_eta": "Original ETA",
        "live_eta": "Live ETA",
        "sync": "Last Data Sync",
        "insights": "#### 🚉 Transit Insights",
        "crowd": "AI Crowd Predictor",
        "next_train": "Next Train In",
        "weather": "Monsoon Impact",
        "completed": "🎉 Journey Completed!"
    },
    "Hindi": {
        "title": "🚆 पल्स (PULSE): लाइव ट्रांज़िट नेविगेटर",
        "subtitle": "लोकेशन खोजें, लाइव रूट ट्रैक करें, भीड़ की जानकारी लें और स्मार्ट अलर्ट पाएं।",
        "line": "रूट लाइन चुनें",
        "from": "📍 कहाँ से",
        "to": "🏁 कहाँ तक",
        "monsoon": "🌧️ क्या बारिश हो रही है? (मानसून मोड)",
        "start": "लाइव ट्रैकिंग शुरू करें 🚀",
        "same_loc": "शुरुआती और आखिरी लोकेशन एक नहीं हो सकती!",
        "tracking_msg": "🟢 ट्रैकिंग जारी:",
        "dashboard": "### 📡 लाइव स्टेटस डैशबोर्ड",
        "map_title": "### 🗺️ लाइव रूट मैप",
        "orig_eta": "मूल अनुमानित समय",
        "live_eta": "वर्तमान लाइव ETA",
        "sync": "आखिरी डेटा सिंक",
        "insights": "#### 🚉 ट्रांज़िट इनसाइट्स",
        "crowd": "AI भीड़ का अनुमान",
        "next_train": "अगली ट्रेन",
        "weather": "मौसम का असर",
        "completed": "🎉 यात्रा पूरी हुई!"
    },
    "Marathi": {
        "title": "🚆 पल्स (PULSE): थेट ट्रान्झिट नेव्हिगेटर",
        "subtitle": "लोकेशन शोधा, थेट मार्ग ट्रॅक करा, गर्दी तपासा आणि स्मार्ट अलर्ट मिळवा.",
        "line": "मार्ग लाइन निवडा",
        "from": "📍 कुठून",
        "to": "🏁 कुठे",
        "monsoon": "🌧️ पाऊस पडत आहे का? (पावसाळा मोड)",
        "start": "थेट ट्रॅकिंग सुरू करा 🚀",
        "same_loc": "सुरुवातीचे आणि अंतिम लोकेशन एकच असू शकत नाही!",
        "tracking_msg": "🟢 ट्रॅकिंग चालू:",
        "dashboard": "### 📡 थेट स्थिती डॅशबोर्ड",
        "map_title": "### 🗺️ थेट मार्ग नकाशा",
        "orig_eta": "मूळ अंदाजित वेळ",
        "live_eta": "सध्याची थेट ETA",
        "sync": "शेवटचा डेटा सिंक",
        "insights": "#### 🚉 ट्रान्झिट इनसाइट्स",
        "crowd": "AI गर्दीची घनता",
        "next_train": "पुढची ट्रेन",
        "weather": "हवामानाचा प्रभाव",
        "completed": "🎉 प्रवास पूर्ण झाला!"
    }
}
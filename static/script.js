// 🌐 LANGUAGE DATA
const langData = {
    en: {
        title: "Welcome to Karmakand",
        subtitle: "Smart Vedic Platform powered by Karma AI",
        card1: "🧘 Brahmin Services",
        card1p: "Join as verified Brahmin",
        card2: "🤖 Karma AI",
        card2p: "Ask astrology & rituals",
        card3: "📿 Book Pooja",
        card3p: "Book rituals easily"
    },
    gu: {
        title: "કર્મકાંડમાં આપનું સ્વાગત છે",
        subtitle: "કર્મ AI દ્વારા સંચાલિત વૈદિક પ્લેટફોર્મ",
        card1: "🧘 બ્રાહ્મણ સેવા",
        card1p: "વેરિફાઈડ બ્રાહ્મણ તરીકે જોડાઓ",
        card2: "🤖 કર્મ AI",
        card2p: "જ્યોતિષ અને વિધિ વિશે પૂછો",
        card3: "📿 પૂજા બુક કરો",
        card3p: "સરળ રીતે પૂજા બુક કરો"
    },
    hi: {
        title: "कर्मकांड में स्वागत है",
        subtitle: "कर्म AI द्वारा संचालित वैदिक प्लेटफॉर्म",
        card1: "🧘 ब्राह्मण सेवा",
        card1p: "सत्यापित ब्राह्मण बनें",
        card2: "🤖 कर्म AI",
        card2p: "ज्योतिष और पूजा पूछें",
        card3: "📿 पूजा बुक करें",
        card3p: "आसानी से पूजा बुक करें"
    }
};

// 🔥 SET LANGUAGE
function setLang(lang) {
    localStorage.setItem("lang", lang);

    const updateElementText = (id, key) => {
        const element = document.getElementById(id);
        if (element && langData[lang][key]) {
            element.innerText = langData[lang][key];
        }
    };

    // Update Home Page Elements
    updateElementText("title", "title");
    updateElementText("subtitle", "subtitle");
    updateElementText("card1", "card1");
    updateElementText("card1p", "card1p");
    updateElementText("card2", "card2");
    updateElementText("card2p", "card2p");
    updateElementText("card3", "card3");
    updateElementText("card3p", "card3p");

    // Hide Popup
    const popup = document.getElementById("langPopup");
    if (popup) {
        popup.style.display = "none";
    }
}

// 🔥 AUTO LOAD LANGUAGE ON WINDOW LOAD
window.onload = function () {
    const savedLang = localStorage.getItem("Lang");
    const popup = document.getElementById("langPopup");

    if (savedLang) {
        setLang(savedLang);
        if (popup) popup.style.display = "none";
    } else {
        if (popup) popup.style.display = "flex";
    }
};

// 🔥 NAVIGATION FUNCTIONS
function goBrahmin() {
    window.location.href = "/brahmin";
}

function goYajman() {
    window.location.href = "/yajman";
}

function openAI() {
    alert("Karma AI Coming Soon 🔥");
}

// 🔥 BRAHMIN FORM VALIDATION
function validateBrahminForm() {
    const inputs = document.querySelectorAll("input[required]");
    
    for (let i = 0; i < inputs.length; i++) {
        if (!inputs[i].value) {
            alert("All fields are mandatory ❌");
            return false;
        }
    }

    alert("Verification Data Submitted ✅");
    return true; // Set to true to allow form submission to Flask
}

// 🔥 BRAHMIN DASHBOARD DATA
function loadBrahminDashboard() {

    let data = JSON.parse(localStorage.getItem("brahminData"));

    if (!data) {
        data = {
            name: "Brahmin",
            wallet: 0,
            rating: 0,
            reviews: 0,
            team: 0
        };
    }

    if (document.getElementById("bname")) {

        document.getElementById("wallet").innerText =
            "₹" + data.wallet.toLocaleString('en-IN');

        document.getElementById("rating").innerText =
            data.rating + " / 5 (" + data.reviews + " reviews)";

        document.getElementById("team").innerText =
            data.team + " Members";
    }
}

// 🔥 UPDATE DATA FUNCTION (IMPORTANT)
function updateBrahminData(newData) {

    let oldData = JSON.parse(localStorage.getItem("brahminData")) || {};

    let updated = { ...oldData, ...newData };

    localStorage.setItem("brahminData", JSON.stringify(updated));

    loadBrahminDashboard();
}

// AUTO LOAD
window.addEventListener("load", loadBrahminDashboard);


// ==============================
// 📱 DEMO OTP SYSTEM
// ==============================

let generatedOTP = "";

// SEND OTP
function sendOTP() {

    const mobile = document.getElementById("mobile").value;

    if (!mobile || mobile.length < 10) {
        alert("Enter valid mobile ❌");
        return;
    }

    generatedOTP = Math.floor(1000 + Math.random() * 9000);

    alert("Your OTP: " + generatedOTP); // DEMO

    document.getElementById("otpBox").style.display = "block";
}

// VERIFY OTP
function verifyOTP() {

    const userOTP = document.getElementById("otp").value;

    if (userOTP == generatedOTP) {

        document.getElementById("loginBox").style.display = "none";
        document.getElementById("yajmanDashboard").style.display = "block";

        setYajmanName("Guest User");

    } else {
        alert("Wrong OTP ❌");
    }
}

// ==============================
// 👤 YAJMAN NAME
// ==============================

function setYajmanName(name) {

    document.getElementById("yname").innerText =
        name + " (Yajman)";
}

// ==============================
// 🔍 SEARCH BRAHMIN
// ==============================

function searchBrahmin() {

    let input = document.getElementById("search").value.toLowerCase();
    let cards = document.querySelectorAll("#brahminList .card");

    cards.forEach(card => {

        let text = card.innerText.toLowerCase();

        if (text.includes(input)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }

    });
}

// ==============================
// ⭐ RATE BRAHMIN (FORM BASED)
// ==============================

function rateBrahmin(name) {

    document.getElementById("rname").value = name;

    let rating = prompt("Give rating (1 to 5)");

    if (!rating) return; 

    if (rating < 1 || rating > 5) {
        alert("Invalid rating ❌");
        return;
    }

    document.querySelector("select[name='rating']").value = rating;

    alert("Ready to submit ✅");
}
  
// ==============================
// 📿 BOOKING SYSTEM
// ==============================

let selectedBrahmin = "";

// OPEN BOOKING FORM
function openBooking(name) {

    selectedBrahmin = name;

    document.getElementById("bookingForm").style.display = "block";
    document.getElementById("bname").value = name;
}

// CONFIRM BOOKING
function confirmBooking() {

    let date = document.getElementById("bdate").value;
    let location = document.getElementById("blocation").value;

    if (!date || !location) {
        alert("Fill all details ❌");
        return;
    }

    let booking = {
        brahmin: selectedBrahmin,
        date: date,
        location: location
    };

    localStorage.setItem("bookingData", JSON.stringify(booking));

    alert("Booking Confirmed ✅");

    document.getElementById("bookingForm").style.display = "none";
}

// ==============================
// 📥 LOAD BOOKING INTO DASHBOARD
// ==============================

function loadBooking() {

    let data = JSON.parse(localStorage.getItem("bookingData"));

    if (data && document.getElementById("bookingInfo")) {

        document.getElementById("bookingInfo").innerText =
            data.brahmin + " | " + data.date + " | " + data.location;
    }
}

window.addEventListener("load", loadBooking);

function goToPayment() {
    window.location.href = "/payment";
}

// ==============================
// 📊 LOAD BRAHMIN FROM DATABASE
// ==============================
function loadBrahminFromDB(name) {  
  
    fetch("/get_brahmin/" + name)  
    .then(res => res.json())  
    .then(data => {  
  
        document.getElementById("wallet").innerText =  
            "₹" + data.wallet;  
  
        document.getElementById("rating").innerText =  
            data.rating + " ⭐";  
  
        document.getElementById("team").innerText =  
            data.team + " Members";  
  
        document.getElementById("status").innerText =  
            "Status: " + data.status;  
  
    });  
}
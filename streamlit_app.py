import streamlit as st

pg_bg = """
<style>
div.stButton > button:first-child {
background-color: #005F73;
color: #F5F5F5;
}
[data-testid="stBaseButton-secondary"] {
background-color: #005F73;
}
[data-testid="stAppViewContainer"] {
background-color: #0A9396;
color: #F5F5F5;
}
</style>
"""
st.markdown(pg_bg, unsafe_allow_html=True)
st.title("Let's get rid of diesel gensets!")
st.write("#### At NEBITH, we have developed a solar microgrid that can reduce diesel fuel consumption by up to 85%.")
st.write("#### Have you rented a diesel genset recently for your operations? Give us a couple of details about it and we'll tell you how much money NEBITH could save you.")

st.write("##### 1. What business are you in?")

industry = ["Construction", "Mining", "Data Centers", "Agriculture", "Other"]
industry_input = st.selectbox(label="Industry", options=industry, index=None, placeholder="Select an industry...")

st.write("##### 2. Where is your project located?")
city_input = st.text_input(label="City")
country = ["Afghanistan",    "Albania",    "Algeria",    "Andorra",    "Angola",    "Antigua and Barbuda",    "Argentina",    "Armenia",    "Australia",    "Austria",    "Azerbaijan",    "Bahamas",    "Bahrain",    "Bangladesh",
    "Barbados",    "Belarus",    "Belgium",    "Belize",    "Benin",    "Bhutan",    "Bolivia",    "Bosnia and Herzegovina",    "Botswana",    "Brazil",    "Brunei",    "Bulgaria",    "Burkina Faso",    "Burundi",
    "Cambodia",    "Cameroon",    "Canada",    "Cape Verde",    "Central African Republic",   "Chad",    "Chile",    "China",    "Colombia",    "Comoros",    "Congo",    "Costa Rica",    "Croatia",    "Cuba",
    "Cyprus",    "Czech Republic",    "Denmark",    "Djibouti",    "Dominica",    "Dominican Republic",    "East Timor",    "Ecuador",    "Egypt",    "El Salvador",    "Equatorial Guinea",    "Eritrea",    "Estonia",
    "Eswatini",    "Ethiopia",    "Fiji",    "Finland",    "France",    "Gabon",    "Gambia",    "Georgia",    "Germany",    "Ghana",    "Greece",    "Grenada",    "Guatemala",    "Guinea",    "Guinea-Bissau",
    "Guyana",    "Haiti",    "Honduras",    "Hungary",    "Iceland",    "India",    "Indonesia",    "Iran",    "Iraq",    "Ireland",    "Israel",    "Italy",    "Jamaica",    "Japan",    "Jordan",    "Kazakhstan",
    "Kenya",    "Kiribati",    "Kuwait",    "Kyrgyzstan",    "Laos",    "Latvia",    "Lebanon",    "Lesotho",    "Liberia",    "Libya",    "Liechtenstein",    "Lithuania",    "Luxembourg",    "Madagascar",
    "Malawi",    "Malaysia",    "Maldives",    "Mali",    "Malta",    "Marshall Islands",    "Mauritania",    "Mauritius",    "Mexico",    "Micronesia",    "Moldova",    "Monaco",    "Mongolia",    "Montenegro",
    "Morocco",    "Mozambique",    "Myanmar",    "Namibia",    "Nauru",    "Nepal",    "Netherlands",    "New Zealand",    "Nicaragua",    "Niger",    "Nigeria",    "North Korea",    "North Macedonia",    "Norway",
    "Oman",    "Pakistan",    "Palau",    "Panama",    "Papua New Guinea",    "Paraguay",    "Peru",    "Philippines",    "Poland",    "Portugal",    "Qatar",    "Romania",    "Russia",    "Rwanda",    "Saint Kitts and Nevis",
    "Saint Lucia",    "Saint Vincent and the Grenadines",    "Samoa",    "San Marino",    "Sao Tome and Principe",    "Saudi Arabia",    "Senegal",    "Serbia",    "Seychelles",    "Sierra Leone",    "Singapore",
    "Slovakia",    "Slovenia",    "Solomon Islands",    "Somalia",    "South Africa",    "South Sudan",    "Spain",    "Sri Lanka",    "Sudan",    "Suriname",    "Sweden",    "Switzerland",    "Syria",    "Taiwan",
    "Tajikistan",    "Tanzania",    "Thailand",    "Togo",    "Tonga",    "Trinidad and Tobago",    "Tunisia",    "Turkey",    "Turkmenistan",    "Tuvalu",    "Uganda",    "Ukraine",    "United Arab Emirates",    "United Kingdom",    "United States",
    "Uruguay",    "Uzbekistan",    "Vanuatu",    "Vatican City",    "Venezuela",    "Vietnam",    "Yemen",    "Zambia",    "Zimbabwe"]
country_input = st.selectbox(label="Country", options=country, index=None, placeholder="Select a country...")

st.write("##### 3. How much did you spend last year on your diesel genset?")
tco_choice = st.number_input(label="Total expenditure (fuel + rental + O&M)",
                step=100)
currency_input = st.selectbox(label="Currency", options= ["USD", "GBP", "EUR"])

# st.write("##### 3. Upload a yearly power profile for your project, if you have one. If not, please select our sample power profile.")
# st.file_uploader(label="Upload a .csv file (8760 rows, hourly power in kW)", type=".csv")
# st.button(label="Use our own sample data")

st.write("#### We're almost there, now give us your name and e-mail address, so we can send you the current report as a PDF file.")

st.write("##### 4. Full name")
name_input = st.text_input(label="First name, Last name")

st.write("##### 5. E-mail address")
email_input = st.text_input(label="", label_visibility="collapsed", placeholder="jane@doe.com")

st.button(label="Generate report")

# Simulate microgrid data
# Plot map with location centered
# Show diesel costs
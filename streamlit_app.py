import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import microgrids as mgs
import pandas as pd
import geopandas as gpd
import pvlib
import seaborn as sns

pg_bg = """
<style>
div.stButton > button:first-child {
background-color: #005F73;
color: #F5F5F5;
}
[data-testid="stBaseButton-secondaryFormSubmit"] {
background-color: #005F73;
}
[data-testid="stBaseButton-segmented_control"] {
color: #2E2E2E;
}
[data-testid="stBaseButton-segmented_controlActive"] {
color: #F5F5F5;
}
[data-testid="stBaseButton-pills"] {
color: #2E2E2E;
}
[data-testid="stBaseButton-pillsActive"] {
color: #F5F5F5;
}
[data-testid="stAlertContentSuccess"] {
color: #F5F5F5;
}
[data-testid="stAppViewContainer"] {
background-color: #0A9396;
color: #F5F5F5;
}
[data-testid="stMetric"] {
background-color: #F5F5F5;
}
[data-testid="stExpander"] {
background-color: #005F73;
}
</style>
"""
st.markdown(pg_bg, unsafe_allow_html=True)
st.title("Let's get rid of diesel gensets!")
st.write("#### At NEBITH, we have developed a solar microgrid that can reduce diesel fuel consumption by up to 85%.")
st.write("#### Have you rented a diesel genset for your operations? Give us a couple of details about it and we'll tell you how much money NEBITH could save you.")

with st.form("nebith_form"):

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

    st.write("##### 3. How big is your diesel genset?")
    genset_opts = [5, 10, 25, 50, 100, 200, 300, 400, 500, 1000, 1500, 2000]
    genset_size = st.segmented_control(label="Genset rated power (kW)", options=genset_opts, default=500)
    st.write("#####    How much did you spend on fuel last year?")
    money_input = st.pills(label="Amount spent", options=["< 10K", "10K - 50K", "50K - 100K", "100K - 500K", "> 500K"], default="10K - 50K")
    currency_input = st.segmented_control(label="Currency", options= ["USD", "GBP", "EUR"], default="USD")

    st.divider()

    st.write("#### We're almost there, now share your name and e-mail address with us to receive the current report as a PDF file.")

    st.write("##### 4. Full name")
    name_input = st.text_input(label="First name, Last name", placeholder="Jane Doe")

    st.write("##### 5. E-mail address")
    email_input = st.text_input(label="", label_visibility="collapsed", placeholder="jane@doe.com")

    generate = st.form_submit_button(label="Generate report")

if generate:
    st.success("Thank you! Your report is being generated and will be sent to your e-mail address shortly. Please find below a preview of the results.")

    # Locate city

    # Location = "Monza, Italy"
    Location = f"{city_input}, {country_input}"
    loc = gpd.tools.geocode(Location)["geometry"]

    pvgis_data = pvlib.iotools.get_pvgis_hourly(latitude=float(loc.y[0]), 
                                                longitude=float(loc.x[0]), 
                                                start=2023, end=2023, 
                                                components=False, 
                                                optimalangles=True)
    df = pd.DataFrame(pvgis_data[0])
    irradiance = (df["poa_global"].values / 1000)
    Pload = np.loadtxt("Construction site load.csv", skiprows=1)

    # Simulate microgrid data

    lifetime = 25 # yr
    discount_rate = 0.05
    timestep = 1 # h
    investment_price_pv = 600 # initial investiment price ($/kW)
    energy_rated_sto = 1000 # rated energy capacity (kWh)
    investment_price_sto = 250 # initial investiment price ($/kWh)
    fuel_price = 2 # fuel price ($/l)

    project = mgs.Project(lifetime, discount_rate, timestep)

    power_rated_gen = 500.  # /2 to see some load shedding
    fuel_intercept = 0.0 # fuel curve intercept (l/h/kW_max)
    fuel_slope = 0.240 # fuel curve slope (l/h/kW)
    investment_price_gen = 400. # initial investiment price ($/kW)
    om_price_gen = 0.02 # operation & maintenance price ($/kW/h of operation)
    lifetime_gen = 15000. # generator lifetime (h)

    generator = mgs.DispatchableGenerator(power_rated_gen,
        fuel_intercept, fuel_slope, fuel_price,
        investment_price_gen, om_price_gen,
        lifetime_gen
    )

    om_price_sto = 10. # operation and maintenance price ($/kWh/y)
    lifetime_sto = 15. # calendar lifetime (y)
    lifetime_cycles = 6000 # maximum number of cycles over life (1)
    # Parameters with default values
    charge_rate_max = 1.0 # max charge power for 1 kWh (kW/kWh = h^-1)
    discharge_rate_max = 1.0 # max discharge power for 1 kWh (kW/kWh = h^-1)
    loss_factor_sto = 0.05 # linear loss factor α (round-trip efficiency is about 1 − 2α) ∈ [0,1]

    battery = mgs.Battery(energy_rated_sto,
        investment_price_sto, om_price_sto,
        lifetime_sto, lifetime_cycles,
        charge_rate_max, discharge_rate_max,
        loss_factor_sto,SoC_ini=1)

    power_rated_pv = 350. # rated power (kW)
    om_price_pv = 20.# operation and maintenance price ($/kW)
    lifetime_pv = 25. # lifetime (y)
    # Parameters with default values
    derating_factor_pv = 1.0 # derating factor (or performance ratio) ∈ [0,1]"

    photovoltaic = mgs.Photovoltaic(power_rated_pv, irradiance,
        investment_price_pv, om_price_pv,
        lifetime_pv, derating_factor_pv)

    microgrid = mgs.Microgrid(project, Pload,
        generator, battery,
        {'Solar PV': photovoltaic}
    )

    oper_traj = mgs.TrajRecorder()
    oper_stats = mgs.sim_operation(microgrid, oper_traj)

    mg_costs = mgs.sim_economics(microgrid, oper_stats)

    df_lcoe = pd.DataFrame()
    df_lcoe["City"] = Location
    df_lcoe["Max Irradiance (W/m2)"] = [irradiance.max()]
    df_lcoe["Mean Irradiance (W/m2)"] = [irradiance.mean()]
    df_lcoe["PV Price (USD/kW)"] = [investment_price_pv]
    df_lcoe["BESS Price (USD/kWh)"] = [investment_price_sto]
    df_lcoe["BESS Size (kWh)"] = [energy_rated_sto]
    df_lcoe["Fuel Price"] = [fuel_price]
    df_lcoe["Load Shedding (%)"] = [float(oper_stats.shed_rate)]
    df_lcoe["Renewable Rate (%)"] = [float(oper_stats.renew_rate)]
    df_lcoe["LCOE (USD/kWh)"] = [round(float(mg_costs.lcoe),4)]
    df_lcoe["LAT"] = loc.y[0]
    df_lcoe["LON"] = loc.x[0]

# Plot map with location centered
    with st.spinner('Generating map...'):
        st.map(df_lcoe, zoom=4, 
            latitude=df_lcoe["LAT"], 
            longitude=df_lcoe["LON"], 
            color="#FFD60A", size=70000)
        
    st.write(f"### Location: {Location}")

    st.write("#### Your diesel genset performance:")
    col1, col2, col3 = st.columns(3, gap="small")
    col1.metric("CO2 emissions", "500 ton", delta="ESG", delta_arrow="down", delta_color="red", border=True)
    col2.metric("Noise pollution", "85 dB", delta="noisy", delta_color="red", border=True)
    col3.metric("VOC compounds", "12,000 ppm", delta="HSE costs", delta_color="red", border=True)
    

    st.write("#### Your costs:")
    col4, col5, col6 = st.columns(3, gap="small")    
    col4.metric("Yearly expenditure", f"{genset_size} * 500 {currency_input}", delta=None, border=True)
    col5.metric("Yearly fuel costs", f"60% of total", delta=None, border=True)
    col6.metric("Yearly maintenance costs", f"21% of total", delta=None, border=True)
        
    st.divider()

    with st.expander("### If you switch to NEBITH's solar microgrid, you could:"):
        st.write(f"#### 1. Reduce your diesel fuel consumption by up to {100 - round(float(oper_stats.renew_rate),2)}%")
        st.write(f"#### 2. Save up to {round(genset_size * (100 - float(oper_stats.renew_rate)) / 100, 2)} {currency_input} every year!")
        st.write("#### 3. Electrify your operations with clean, reliable energy.")

    st.divider()

    download = st.download_button("Download full report (PDF)", data="dummy_pdf_content", file_name="nebith_report.pdf", mime="application/pdf")

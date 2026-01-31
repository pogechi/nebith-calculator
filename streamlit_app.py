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
div.stDownloadButton > button:first-child {
background-color: #005F73;
color: #F5F5F5;
}
</style>
"""
st.markdown(pg_bg, unsafe_allow_html=True)
st.title("Let's get rid of diesel gensets!")
st.write("#### At NEBITH, we have developed a solar microgrid that can reduce diesel fuel consumption by up to 85%.")
st.write("#### Have you rented a diesel genset for your operations? Share your story and we'll tell you how much money NEBITH could save you.")

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

    st.write("#### We're almost there, now share your name and e-mail address to receive our report as a PDF file.")

    st.write("##### 4. Full name")
    name_input = st.text_input(label="First name, Last name", placeholder="Jane Doe")

    st.write("##### 5. E-mail address")
    email_input = st.text_input(label="", label_visibility="collapsed", placeholder="jane@doe.com")

    generate = st.form_submit_button(label="Generate report")

if generate:
    st.success(f"Thank you {name_input}! Your report is being generated and will be sent to your e-mail address shortly. Please find below a preview of the results.")

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

    # Diesel genset

    power_rated_gen = 500.  # /2 to see some load shedding
    fuel_intercept = 0.0 # fuel curve intercept (l/h/kW_max)
    fuel_slope = 0.240 # fuel curve slope (l/h/kW)
    investment_price_gen = 400. # initial investiment price ($/kW)
    om_price_gen = 0.02 # operation & maintenance price ($/kW/h of operation)
    lifetime_gen = 15000. # generator lifetime (h)

    generator = mgs.DispatchableGenerator(power_rated_gen,
        fuel_intercept, fuel_slope, fuel_price,
        investment_price_gen, om_price_gen,
        lifetime_gen)

    # Battery energy storage system

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

    # Photovoltaic system

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
        {'Solar PV': photovoltaic})

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

# Calculate diesel data

    d_investment_price_pv = 600 # initial investiment price ($/kW)
    d_energy_rated_sto = 1000 # rated energy capacity (kWh)
    d_investment_price_sto = 250 # initial investiment price ($/kWh)
    d_fuel_price = 2 # fuel price ($/l)
    d_power_rated_pv = 0 # rated power (kW)

    d_generator = mgs.DispatchableGenerator(power_rated_gen,
        fuel_intercept, fuel_slope, d_fuel_price,
        investment_price_gen, om_price_gen,
        lifetime_gen)
    
    d_battery = mgs.Battery(d_energy_rated_sto,
        d_investment_price_sto, om_price_sto,
        lifetime_sto, lifetime_cycles,
        charge_rate_max, discharge_rate_max,
        loss_factor_sto,SoC_ini=1)
    
    d_photovoltaic = mgs.Photovoltaic(d_power_rated_pv, irradiance,
        d_investment_price_pv, om_price_pv,
        lifetime_pv, derating_factor_pv)
    
    d_microgrid = mgs.Microgrid(project, Pload,
        d_generator, d_battery,
        {'Solar PV': d_photovoltaic})

    d_oper_traj = mgs.TrajRecorder()
    d_oper_stats = mgs.sim_operation(d_microgrid, d_oper_traj)
    d_mg_costs = mgs.sim_economics(d_microgrid, d_oper_stats)    

    d_df_lcoe = pd.DataFrame()
    d_df_lcoe["City"] = Location
    d_df_lcoe["Fuel Price"] = [d_fuel_price]
    d_df_lcoe["Renewable Rate (%)"] = [float(d_oper_stats.renew_rate)]
    d_df_lcoe["LCOE (USD/kWh)"] = [round(float(d_mg_costs.lcoe),4)]

    ratio = genset_size / power_rated_gen

    yearly_load = ratio * Pload.sum() # kWh
    yearly_fuel_consumption = ratio * (d_oper_stats.gen_fuel) # l
    yearly_fuel_costs = yearly_fuel_consumption * d_fuel_price
    yearly_om_costs = ratio * d_mg_costs.system.om / lifetime
    yearly_total_costs = ratio * (d_mg_costs.generator.investment + d_mg_costs.generator.replacement) / lifetime
    yearly_co2_emissions = yearly_fuel_consumption * 2.68 / 1000 # ton
    yearly_voc_compounds = yearly_fuel_consumption * 24 / 1000 # ppm
    diesel_genset_noise = 75 + 10 * np.log10(ratio * power_rated_gen)  # dB

# Currency exchange

    exch_rates = {"USD": 1, "GBP": 0.81, "EUR": 0.91}
    currency_symbols = {"USD": "$", "GBP": "£", "EUR": "€"} 

# Plot map with location centered
    with st.spinner('Generating map...'):
        st.map(df_lcoe, zoom=4, 
            latitude=df_lcoe["LAT"], 
            longitude=df_lcoe["LON"], 
            color="#FFD60A", size=70000)
        
    st.write(f"### Location: {Location} ({round(loc.y[0],5)}, {round(loc.x[0],5)})")

    st.write("#### Your diesel genset performance:")
    col1, col2, col3 = st.columns(3, gap="small")
    col1.metric("CO2 emissions", f"{yearly_co2_emissions:.0f} ton", delta="ESG", delta_arrow="down", delta_color="red", border=True)
    col2.metric("Noise pollution", f"{diesel_genset_noise:.0f} dB", delta="noisy", delta_color="red", border=True)
    col3.metric("VOC compounds", f"{yearly_voc_compounds:.0f} ppm", delta="HSE costs", delta_color="red", border=True)
    

    st.write("#### Your yearly costs:")
    col4, col5, col6 = st.columns(3, gap="small")    
    col4.metric(f"Genset rental", f"{currency_symbols[currency_input]} {exch_rates[currency_input] * yearly_total_costs:,.0f}", delta=None, border=True)
    col5.metric(f"Fuel", f"{currency_symbols[currency_input]} {exch_rates[currency_input] * yearly_fuel_costs:,.0f}", delta=None, border=True)
    col6.metric(f"Maintenance costs", f"{currency_symbols[currency_input]} {exch_rates[currency_input] * yearly_om_costs:,.0f}", delta=None, border=True)
        
    st.divider()

    with st.expander("### If you switch to NEBITH's solar microgrid, you could:"):
        
        load = microgrid.load
        arr = oper_traj.Prep - oper_traj.Pspill
        yearly_df = pd.DataFrame()
        yearly_df["Load (kWh)"] = np.bincount(np.arange(len(load))//730, load)
        yearly_df["Solar Production (kWh)"] = np.bincount(np.arange(len(arr))//730, arr)
        yearly_df["Month"] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        st.bar_chart(yearly_df, x="Month", y=["Load (kWh)", "Solar Production (kWh)"], 
                     height=400, stack="layered", color=["#0A9496FF", "#FFD60AFF"],
                     sort=False)
        st.write(f"#### 1. Reduce your diesel fuel consumption by up to {round(float(oper_stats.renew_rate), 2):.0%}!")
        st.write(f"#### 2. Save up to {currency_symbols[currency_input]} {abs(exch_rates[currency_input] * (yearly_fuel_costs - d_df_lcoe['LCOE (USD/kWh)'].iloc[0] * yearly_load)):,.0f} every year!")
        st.write("#### 3. Electrify your operations with clean, reliable energy.")

    st.divider()

    download = st.download_button("Download full report (PDF)", data="dummy_pdf_content", file_name="nebith_report.pdf", mime="application/pdf")

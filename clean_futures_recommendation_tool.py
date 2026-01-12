"""
Clean Futures Solution Recommendation Tool
Permian Basin Soil Remediation Decision Support System

Compares three remediation approaches:
1. Dig & Haul to Landfill
2. Clean Futures Onsite Remediation
3. Clean Futures Surface Facility Treatment
"""

import streamlit as st
import pandas as pd
import json
import math
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Clean Futures Solution Recommendation",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - DISTINCTIVE DESIGN
# ============================================================================

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=Work+Sans:wght@300;400;500;600&display=swap');
    
    /* Main styling */
    .main {
        background: linear-gradient(135deg, #f8faf9 0%, #e8f4f0 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Crimson Pro', serif;
        color: #1a4d2e;
    }
    
    h1 {
        font-size: 3.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Body text */
    p, li, label, .stMarkdown {
        font-family: 'Work Sans', sans-serif;
        color: #2d5f3f;
    }
    
    /* Welcome section */
    .welcome-box {
        background: linear-gradient(135deg, #1a4d2e 0%, #2d7a4f 100%);
        color: white;
        padding: 3rem;
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(26, 77, 46, 0.3);
    }
    
    .welcome-title {
        font-family: 'Crimson Pro', serif;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: white;
    }
    
    .welcome-subtitle {
        font-family: 'Work Sans', sans-serif;
        font-size: 1.3rem;
        font-weight: 300;
        color: #d4f1e3;
        margin-bottom: 1.5rem;
    }
    
    .mission-statement {
        font-family: 'Work Sans', sans-serif;
        font-size: 1.1rem;
        line-height: 1.8;
        color: white;
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #81c995;
    }
    
    /* Mode selector cards */
    .mode-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .mode-card:hover {
        border-color: #2d7a4f;
        box-shadow: 0 8px 24px rgba(45, 122, 79, 0.15);
        transform: translateY(-4px);
    }
    
    .mode-card-title {
        font-family: 'Crimson Pro', serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #1a4d2e;
        margin-bottom: 1rem;
    }
    
    /* Results cards */
    .solution-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 6px solid #2d7a4f;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }
    
    .recommended-badge {
        display: inline-block;
        background: linear-gradient(135deg, #81c995 0%, #2d7a4f 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 24px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    /* Metrics */
    .metric-box {
        background: linear-gradient(135deg, #f0f7f4 0%, #e1f0e8 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #c8e6d4;
    }
    
    .metric-value {
        font-family: 'Crimson Pro', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a4d2e;
        margin: 0;
    }
    
    .metric-label {
        font-family: 'Work Sans', sans-serif;
        font-size: 0.95rem;
        color: #5a8a6f;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2d7a4f 0%, #1a4d2e 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-family: 'Work Sans', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(45, 122, 79, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(45, 122, 79, 0.4);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8faf9;
    }
    
    /* Tables */
    .dataframe {
        font-family: 'Work Sans', sans-serif;
    }
    
    /* Pro/Con lists */
    .pros-list {
        background: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
    }
    
    .cons-list {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Work Sans', sans-serif;
        font-weight: 600;
        color: #1a4d2e;
    }
    
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS - DISTANCE AND GEOSPATIAL
# ============================================================================

# ============================================================================
# HELPER FUNCTIONS - DISTANCE AND GEOSPATIAL
# ============================================================================

def determine_state_county(lat, lon, db):
    """Determine state and county from GPS coordinates"""
    # Texas/New Mexico boundary is roughly at -103° longitude
    state = "Texas" if lon > -103.0 else "New Mexico"
    
    # Find nearest county from the landfill database (use county centroids)
    county_distances = {}
    counties_seen = set()
    
    for lf in db['landfills']:
        county = lf['county']
        if county not in counties_seen:
            # Use first landfill in each county as representative
            distance = haversine_distance(lat, lon, lf['latitude'], lf['longitude'])
            county_distances[county] = distance
            counties_seen.add(county)
    
    nearest_county = min(county_distances, key=county_distances.get) if county_distances else "Unknown"
    
    return state, nearest_county

def get_soil_type(lat, lon, state):
    """Estimate soil type based on location in Permian Basin"""
    # Simplified soil classification for Permian Basin
    # In production, this would query USDA Web Soil Survey or similar database
    
    # Eastern Permian (more clay-rich)
    if lon > -102.0:
        return "Clay Loam / Silty Clay"
    # Central Permian (mixed)
    elif lon > -103.5:
        return "Sandy Clay Loam / Caliche"
    # Western Permian (more sandy)
    else:
        return "Sandy Loam / Desert Soils"

def get_regulatory_thresholds(state):
    """Get soil regulatory thresholds for TPH and Chlorides"""
    # Texas TCEQ Protective Concentration Levels (PCLs)
    # New Mexico NMED Soil Screening Levels (SSLs)
    
    if state == "Texas":
        return {
            'tph_residential_mgkg': 100,
            'tph_industrial_mgkg': 500,
            'chloride_soil_mgkg': 'Not directly regulated in soil; groundwater standard: 300 mg/L',
            'regulatory_agency': 'TCEQ (Texas Commission on Environmental Quality)',
            'notes': 'Risk-based, site-specific cleanup levels may vary'
        }
    else:  # New Mexico
        return {
            'tph_residential_mgkg': 100,
            'tph_industrial_mgkg': 1000,
            'chloride_soil_mgkg': 'Not directly regulated in soil; groundwater standard: 250 mg/L',
            'regulatory_agency': 'NMED (New Mexico Environment Department)',
            'notes': 'Risk-based corrective action (RBCA) standards apply'
        }

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates in miles"""
    R = 3959  # Earth's radius in miles
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def load_facilities_database():
    """Load the facilities database from JSON"""
    db_path = Path('/home/claude/permian_facilities_db.json')
    if db_path.exists():
        with open(db_path, 'r') as f:
            return json.load(f)
    return {"landfills": [], "clean_futures_facilities": []}

def find_nearest_qualified_landfill(lat, lon, tph_level, chloride_level, needs_backfill, db):
    """Find the nearest landfill that accepts the contamination levels"""
    qualified = []
    
    for lf in db['landfills']:
        # Check if landfill accepts the contamination levels
        accepts_tph = tph_level <= lf['tph_max_mgkg'] if tph_level > 0 else True
        accepts_chloride = chloride_level <= lf['chloride_max_mgkg'] if chloride_level > 0 else True
        
        if accepts_tph and accepts_chloride:
            # If backfill is needed, prefer landfills with backfill
            if needs_backfill and not lf['backfill_available']:
                continue  # Skip landfills without backfill if it's needed
            
            distance = haversine_distance(lat, lon, lf['latitude'], lf['longitude'])
            qualified.append({
                'landfill': lf,
                'distance_miles': distance
            })
    
    # Sort by distance
    qualified.sort(key=lambda x: x['distance_miles'])
    
    return qualified[0] if qualified else None

def find_nearest_cf_facility(lat, lon, db):
    """Find the nearest Clean Futures facility"""
    facilities = []
    
    for cf in db['clean_futures_facilities']:
        distance = haversine_distance(lat, lon, cf['latitude'], cf['longitude'])
        facilities.append({
            'facility': cf,
            'distance_miles': distance
        })
    
    facilities.sort(key=lambda x: x['distance_miles'])
    
    return facilities[0] if facilities else None

# ============================================================================
# CALCULATION FUNCTIONS
# ============================================================================

def calculate_volume_cy(surface_area_sqft, depth_ft):
    """Calculate volume in cubic yards from surface area and depth"""
    cubic_feet = surface_area_sqft * depth_ft
    cubic_yards = cubic_feet / 27
    return cubic_yards

def calculate_co2_emissions(fuel_gallons):
    """Calculate CO2 emissions from fuel consumption"""
    # Diesel produces approximately 22.38 lbs CO2 per gallon
    co2_lbs = fuel_gallons * 22.38
    co2_tons = co2_lbs / 2000
    return co2_lbs, co2_tons

def calculate_dig_and_haul(volume_cy, site_lat, site_lon, needs_backfill, 
                          tph_level, chloride_level, db, advanced_params=None):
    """Calculate costs and metrics for Dig & Haul option"""
    
    # Find nearest qualified landfill
    nearest_lf = find_nearest_qualified_landfill(site_lat, site_lon, tph_level, 
                                                  chloride_level, needs_backfill, db)
    
    if not nearest_lf:
        return None
    
    landfill = nearest_lf['landfill']
    distance_miles = nearest_lf['distance_miles']
    
    # Use advanced parameters or defaults
    if advanced_params:
        truck_capacity = advanced_params.get('truck_capacity_cy', 18)
        num_trucks = advanced_params.get('num_trucks', 3)
        truck_hourly_rate = advanced_params.get('truck_hourly_rate', 85)
        excavator_rate = advanced_params.get('excavator_rate', 150)
        loader_rate = advanced_params.get('loader_rate', 125)
        work_hours_per_day = advanced_params.get('work_hours_per_day', 10)
        disposal_cost = advanced_params.get('disposal_cost_cy', landfill['disposal_cost_cy'])
        backfill_cost = advanced_params.get('backfill_cost_cy', landfill['backfill_cost_cy'])
    else:
        # Default parameters
        truck_capacity = 18
        num_trucks = 3
        truck_hourly_rate = 85
        excavator_rate = 150
        loader_rate = 125
        work_hours_per_day = 10
        disposal_cost = landfill['disposal_cost_cy']
        backfill_cost = landfill['backfill_cost_cy'] if needs_backfill else 0
    
    # Trip time calculation (simplified)
    avg_speed_mph = 45
    travel_time_hours = distance_miles / avg_speed_mph
    loading_time = 0.25
    unloading_time = 0.5
    trip_time = loading_time + travel_time_hours + unloading_time + travel_time_hours + loading_time
    
    # Calculate number of trips and duration
    num_trips = math.ceil(volume_cy / truck_capacity)
    trips_per_truck_per_day = work_hours_per_day / trip_time
    total_trips_per_day = trips_per_truck_per_day * num_trucks
    project_days = math.ceil(num_trips / total_trips_per_day)
    project_hours = project_days * work_hours_per_day
    
    # Equipment capacity (simplified - assume balanced)
    excavation_capacity = 40  # CY/hr
    loading_capacity = 35  # CY/hr
    equipment_capacity = min(excavation_capacity, loading_capacity)
    
    # Costs
    total_equipment_hours = project_hours
    equipment_cost = (excavator_rate + loader_rate) * total_equipment_hours
    
    total_truck_hours = num_trips * trip_time
    trucking_cost = total_truck_hours * truck_hourly_rate
    
    disposal_total = volume_cy * disposal_cost
    backfill_total = volume_cy * backfill_cost if needs_backfill else 0
    
    total_cost = equipment_cost + trucking_cost + disposal_total + backfill_total
    cost_per_cy = total_cost / volume_cy
    
    # CO2 calculations (simplified)
    excavator_fuel_gph = 6
    loader_fuel_gph = 5
    truck_fuel_gph = 4
    
    total_fuel = (excavator_fuel_gph * total_equipment_hours + 
                  loader_fuel_gph * total_equipment_hours +
                  truck_fuel_gph * total_truck_hours)
    
    co2_lbs, co2_tons = calculate_co2_emissions(total_fuel)
    
    return {
        'option_name': 'Dig & Haul to Landfill',
        'total_cost': total_cost,
        'cost_per_cy': cost_per_cy,
        'project_days': project_days,
        'landfill_name': f"{landfill['company']} - {landfill['site_name']}",
        'distance_miles': distance_miles,
        'co2_tons': co2_tons,
        'equipment_cost': equipment_cost,
        'trucking_cost': trucking_cost,
        'disposal_cost': disposal_total,
        'backfill_cost': backfill_total,
        'includes_backfill': needs_backfill,
        'backfill_available_at_landfill': landfill['backfill_available']
    }

def calculate_onsite_remediation(volume_cy, site_lat, site_lon, soil_permeability='medium',
                                tph_level=0, chloride_level=0, advanced_params=None):
    """Calculate costs and metrics for Onsite Remediation option"""
    
    # Processing cost
    if advanced_params:
        processing_cost_cy = advanced_params.get('onsite_processing_cost_cy', 25)
    else:
        processing_cost_cy = 25
    
    # Treatment duration estimation based on soil permeability
    base_treatment_days = 45
    if soil_permeability == 'high':
        treatment_days = base_treatment_days * 0.7  # Faster treatment
    elif soil_permeability == 'low':
        treatment_days = base_treatment_days * 1.5  # Slower treatment
    else:
        treatment_days = base_treatment_days
    
    # Adjust for contamination levels
    if tph_level > 3000:
        treatment_days *= 1.2
    if chloride_level > 7000:
        treatment_days *= 1.2
    
    treatment_days = int(treatment_days)
    
    # Costs
    total_processing_cost = volume_cy * processing_cost_cy
    
    # Mobilization cost (estimated)
    mobilization_cost = 5000 if volume_cy < 1000 else 10000
    
    # Amendment costs (estimated based on permeability)
    if soil_permeability == 'low':
        amendment_cost = volume_cy * 3  # Need more amendments for poor permeability
    else:
        amendment_cost = volume_cy * 1
    
    total_cost = total_processing_cost + mobilization_cost + amendment_cost
    cost_per_cy = total_cost / volume_cy
    
    # CO2 estimation (much lower than dig & haul)
    # Onsite equipment and limited trucking
    estimated_fuel_gallons = volume_cy * 0.1  # Much less fuel than hauling
    co2_lbs, co2_tons = calculate_co2_emissions(estimated_fuel_gallons)
    
    return {
        'option_name': 'Clean Futures Onsite Remediation',
        'total_cost': total_cost,
        'cost_per_cy': cost_per_cy,
        'project_days': treatment_days,
        'processing_cost': total_processing_cost,
        'mobilization_cost': mobilization_cost,
        'amendment_cost': amendment_cost,
        'co2_tons': co2_tons,
        'includes_backfill': True,
        'soil_returned_clean': True,
        'permeability_factor': soil_permeability
    }

def calculate_surface_facility(volume_cy, site_lat, site_lon, needs_backfill,
                               tph_level, chloride_level, db, advanced_params=None):
    """Calculate costs and metrics for Surface Facility option"""
    
    # Find nearest CF facility
    nearest_cf = find_nearest_cf_facility(site_lat, site_lon, db)
    
    if not nearest_cf:
        return None
    
    facility = nearest_cf['facility']
    distance_miles = nearest_cf['distance_miles']
    
    # Transportation parameters
    if advanced_params:
        truck_capacity = advanced_params.get('truck_capacity_cy', 18)
        num_trucks = advanced_params.get('num_trucks', 3)
        truck_hourly_rate = advanced_params.get('truck_hourly_rate', 85)
        processing_cost_cy = advanced_params.get('surface_processing_cost_cy', 25)
    else:
        truck_capacity = 18
        num_trucks = 3
        truck_hourly_rate = 85
        processing_cost_cy = facility['processing_cost_cy']
    
    # Trip calculations
    avg_speed_mph = 45
    travel_time_hours = distance_miles / avg_speed_mph
    loading_time = 0.25
    unloading_time = 0.5
    
    # Round trip (haul contaminated + return clean)
    trip_time = loading_time + travel_time_hours + unloading_time + travel_time_hours + loading_time
    
    num_trips = math.ceil(volume_cy / truck_capacity)
    total_truck_hours = num_trips * trip_time
    
    # Costs
    trucking_cost = total_truck_hours * truck_hourly_rate
    processing_cost = volume_cy * processing_cost_cy
    
    total_cost = trucking_cost + processing_cost
    cost_per_cy = total_cost / volume_cy
    
    # Timeline
    turnaround_days = facility['typical_turnaround_days']
    
    # CO2 (trucking both ways but treatment is efficient)
    truck_fuel_gph = 4
    total_fuel = truck_fuel_gph * total_truck_hours
    co2_lbs, co2_tons = calculate_co2_emissions(total_fuel)
    
    return {
        'option_name': 'Clean Futures Surface Facility',
        'total_cost': total_cost,
        'cost_per_cy': cost_per_cy,
        'project_days': turnaround_days,
        'facility_name': facility['facility_name'],
        'distance_miles': distance_miles,
        'trucking_cost': trucking_cost,
        'processing_cost': processing_cost,
        'co2_tons': co2_tons,
        'includes_backfill': True,
        'soil_returned_clean': True
    }

def generate_recommendation(dig_haul, onsite, surface_facility, user_priorities):
    """Generate recommendation based on calculations and user priorities"""
    
    options = []
    if dig_haul:
        options.append(('dig_haul', dig_haul))
    if onsite:
        options.append(('onsite', onsite))
    if surface_facility:
        options.append(('surface', surface_facility))
    
    if not options:
        return None
    
    # Score each option based on priorities
    scores = {}
    for opt_type, opt in options:
        score = 0
        
        # Cost priority
        if user_priorities.get('cost', 'medium') == 'high':
            # Lower cost = higher score
            min_cost = min([o[1]['cost_per_cy'] for o in options])
            score += 40 * (1 - (opt['cost_per_cy'] - min_cost) / min_cost) if min_cost > 0 else 20
        elif user_priorities.get('cost', 'medium') == 'medium':
            min_cost = min([o[1]['cost_per_cy'] for o in options])
            score += 20 * (1 - (opt['cost_per_cy'] - min_cost) / min_cost) if min_cost > 0 else 10
        
        # Timeline priority
        if user_priorities.get('speed', 'medium') == 'high':
            min_days = min([o[1]['project_days'] for o in options])
            score += 30 * (1 - (opt['project_days'] - min_days) / min_days) if min_days > 0 else 15
        elif user_priorities.get('speed', 'medium') == 'medium':
            min_days = min([o[1]['project_days'] for o in options])
            score += 15 * (1 - (opt['project_days'] - min_days) / min_days) if min_days > 0 else 7
        
        # ESG priority
        if user_priorities.get('esg', 'medium') == 'high':
            min_co2 = min([o[1]['co2_tons'] for o in options])
            score += 30 * (1 - (opt['co2_tons'] - min_co2) / min_co2) if min_co2 > 0 else 15
            # Bonus for treatment vs disposal
            if opt_type in ['onsite', 'surface']:
                score += 10
        elif user_priorities.get('esg', 'medium') == 'medium':
            min_co2 = min([o[1]['co2_tons'] for o in options])
            score += 15 * (1 - (opt['co2_tons'] - min_co2) / min_co2) if min_co2 > 0 else 7
        
        scores[opt_type] = score
    
    # Find recommendation
    recommended = max(scores, key=scores.get)
    
    return recommended, scores

# ============================================================================
# WELCOME PAGE
# ============================================================================

def show_welcome_page():
    """Display the welcome page"""
    
    st.markdown("""
        <div class="welcome-box">
            <div class="welcome-title">Clean Futures Solution Recommendation Tool</div>
            <div class="welcome-subtitle">Intelligent Decision Support for Soil Remediation in the Permian Basin</div>
            <div class="mission-statement">
                At Clean Futures, we're committed to providing innovative solutions that make our world 
                better and cleaner. Our approach combines cutting-edge remediation technology with 
                environmental stewardship, helping you make informed decisions that balance cost, 
                timeline, and sustainability. Whether you need rapid dig-and-haul services, onsite 
                treatment, or surface facility processing, we're here to guide you to the best solution 
                for your unique situation.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🎯 How Can We Help You Today?")
    st.write("Choose your path to get started:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="mode-card">
                <div class="mode-card-title">⚡ Simple Mode</div>
                <p><strong>Quick estimates with minimal input</strong></p>
                <ul>
                    <li>Basic site information</li>
                    <li>Standard assumptions</li>
                    <li>Fast preliminary recommendations</li>
                    <li>Perfect for initial planning</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Simple Mode", key="simple", use_container_width=True):
            st.session_state.mode = 'simple'
            st.rerun()
    
    with col2:
        st.markdown("""
            <div class="mode-card">
                <div class="mode-card-title">🎛️ Advanced Mode</div>
                <p><strong>Detailed analysis with custom parameters</strong></p>
                <ul>
                    <li>Comprehensive site data</li>
                    <li>Custom equipment & costs</li>
                    <li>Precise recommendations</li>
                    <li>Ideal for final decision-making</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Advanced Mode", key="advanced", use_container_width=True):
            st.session_state.mode = 'advanced'
            st.rerun()
    
    st.markdown("---")
    
    # Additional info
    with st.expander("📚 About This Tool"):
        st.markdown("""
            ### What This Tool Does
            
            This recommendation engine analyzes your contaminated soil situation and compares three 
            remediation approaches:
            
            1. **Dig & Haul to Landfill** - Excavate, transport to qualified landfill, replace with clean fill
            2. **Clean Futures Onsite Remediation** - Treat soil in place using our proven methods
            3. **Clean Futures Surface Facility** - Transport to our facility for treatment, return clean soil
            
            ### What You'll Get
            
            - **Cost Analysis** - Detailed breakdown of all costs for each option
            - **Timeline Estimates** - Project duration from start to completion
            - **Environmental Impact** - CO2 emissions and sustainability metrics
            - **Pros & Cons** - Clear comparison of advantages and limitations
            - **Smart Recommendation** - AI-powered suggestion based on your priorities
            
            ### Coverage Area
            
            Currently optimized for the **Permian Basin** region (West Texas & SE New Mexico), with:
            - 14 qualified landfills in the database
            - 4 Clean Futures surface facilities
            - Regional cost and regulatory data
        """)

# ============================================================================
# QUESTIONNAIRE - SIMPLE MODE
# ============================================================================

def show_simple_questionnaire():
    """Display simple mode questionnaire"""
    
    st.title("📝 Simple Mode Questionnaire")
    st.markdown("### Tell us about your contaminated soil site")
    st.write("Provide basic details and we'll recommend the best remediation solution.")
    
    # Back button
    if st.button("← Back to Welcome", key="back_simple"):
        st.session_state.mode = None
        st.rerun()
    
    with st.form("simple_form"):
        st.markdown("### 📍 Site Location")
        col1, col2 = st.columns(2)
        with col1:
            site_lat = st.number_input("Latitude", value=31.9, min_value=30.0, max_value=35.0, format="%.4f")
        with col2:
            site_lon = st.number_input("Longitude", value=-102.0, min_value=-105.0, max_value=-100.0, format="%.4f")
        
        st.markdown("### 🧪 Contamination Details")
        contam_type = st.selectbox("Contamination Type", 
                                   ["TPH Only", "Chloride Only", "Both TPH and Chloride"])
        
        col1, col2 = st.columns(2)
        with col1:
            if contam_type in ["TPH Only", "Both TPH and Chloride"]:
                tph_level = st.number_input("TPH Level (mg/kg)", value=1000, min_value=0, max_value=10000)
            else:
                tph_level = 0
        with col2:
            if contam_type in ["Chloride Only", "Both TPH and Chloride"]:
                chloride_level = st.number_input("Chloride Level (mg/kg)", value=5000, min_value=0, max_value=20000)
            else:
                chloride_level = 0
        
        st.markdown("### 📏 Site Dimensions")
        col1, col2 = st.columns(2)
        with col1:
            surface_area = st.number_input("Surface Area (square feet)", value=5000, min_value=100)
        with col2:
            depth = st.number_input("Depth of Contamination (feet)", value=5.0, min_value=0.5, max_value=30.0, step=0.5)
        
        volume_cy = calculate_volume_cy(surface_area, depth)
        st.info(f"📦 **Estimated Volume:** {volume_cy:,.0f} cubic yards")
        
        st.markdown("### 🎯 Project Priorities")
        col1, col2, col3 = st.columns(3)
        with col1:
            cost_priority = st.select_slider("Cost Importance", 
                                            options=['low', 'medium', 'high'],
                                            value='medium')
        with col2:
            speed_priority = st.select_slider("Speed Importance",
                                             options=['low', 'medium', 'high'],
                                             value='medium')
        with col3:
            esg_priority = st.select_slider("ESG/Sustainability",
                                           options=['low', 'medium', 'high'],
                                           value='medium')
        
        needs_backfill = st.checkbox("Clean backfill required", value=True)
        
        submitted = st.form_submit_button("🔍 Analyze Solutions", type="primary", use_container_width=True)
        
        if submitted:
            # Store in session state
            st.session_state.analysis = {
                'site_lat': site_lat,
                'site_lon': site_lon,
                'tph_level': tph_level,
                'chloride_level': chloride_level,
                'volume_cy': volume_cy,
                'needs_backfill': needs_backfill,
                'priorities': {
                    'cost': cost_priority,
                    'speed': speed_priority,
                    'esg': esg_priority
                },
                'advanced_params': None,
                'soil_permeability': 'medium'
            }
            st.session_state.show_results = True
            st.rerun()

# ============================================================================
# QUESTIONNAIRE - ADVANCED MODE
# ============================================================================

def show_advanced_questionnaire():
    """Display advanced mode questionnaire"""
    
    st.title("🎛️ Advanced Mode Questionnaire")
    st.markdown("### Detailed Project Specifications")
    st.write("Provide comprehensive information for precise analysis and recommendations.")
    
    # Back button
    if st.button("← Back to Welcome", key="back_advanced"):
        st.session_state.mode = None
        st.rerun()
    
    with st.form("advanced_form"):
        st.markdown("### 📍 Site Location")
        col1, col2 = st.columns(2)
        with col1:
            site_lat = st.number_input("Latitude", value=31.9, min_value=30.0, max_value=35.0, format="%.4f")
        with col2:
            site_lon = st.number_input("Longitude", value=-102.0, min_value=-105.0, max_value=-100.0, format="%.4f")
        
        st.markdown("### 🧪 Contamination Details")
        contam_type = st.selectbox("Contamination Type", 
                                   ["TPH Only", "Chloride Only", "Both TPH and Chloride"])
        
        col1, col2 = st.columns(2)
        with col1:
            if contam_type in ["TPH Only", "Both TPH and Chloride"]:
                tph_level = st.number_input("TPH Level (mg/kg)", value=1000, min_value=0, max_value=10000)
            else:
                tph_level = 0
        with col2:
            if contam_type in ["Chloride Only", "Both TPH and Chloride"]:
                chloride_level = st.number_input("Chloride Level (mg/kg)", value=5000, min_value=0, max_value=20000)
            else:
                chloride_level = 0
        
        st.markdown("### 📏 Site Dimensions")
        col1, col2 = st.columns(2)
        with col1:
            surface_area = st.number_input("Surface Area (square feet)", value=5000, min_value=100)
        with col2:
            depth = st.number_input("Depth of Contamination (feet)", value=5.0, min_value=0.5, max_value=30.0, step=0.5)
        
        volume_cy = calculate_volume_cy(surface_area, depth)
        st.info(f"📦 **Estimated Volume:** {volume_cy:,.0f} cubic yards")
        
        st.markdown("### 🌍 Soil Characteristics")
        soil_permeability = st.selectbox("Soil Permeability", 
                                        ["high", "medium", "low"],
                                        help="Affects onsite treatment duration")
        
        st.markdown("### 🚜 Equipment & Operations")
        col1, col2, col3 = st.columns(3)
        with col1:
            num_trucks = st.number_input("Number of Trucks", value=3, min_value=1, max_value=10)
            truck_capacity = st.number_input("Truck Capacity (CY)", value=18, min_value=10, max_value=30)
        with col2:
            truck_hourly_rate = st.number_input("Truck Hourly Rate ($)", value=85, min_value=50, max_value=200)
            excavator_rate = st.number_input("Excavator Rate ($/hr)", value=150, min_value=75, max_value=300)
        with col3:
            loader_rate = st.number_input("Loader Rate ($/hr)", value=125, min_value=75, max_value=250)
            work_hours_per_day = st.number_input("Work Hours/Day", value=10, min_value=6, max_value=16)
        
        st.markdown("### 💰 Custom Pricing (Optional)")
        use_custom_pricing = st.checkbox("Override default pricing")
        
        if use_custom_pricing:
            col1, col2, col3 = st.columns(3)
            with col1:
                disposal_cost = st.number_input("Landfill Disposal ($/CY)", value=25, min_value=10, max_value=100)
                backfill_cost = st.number_input("Backfill Cost ($/CY)", value=10, min_value=5, max_value=50)
            with col2:
                onsite_cost = st.number_input("Onsite Processing ($/CY)", value=25, min_value=15, max_value=75)
            with col3:
                surface_cost = st.number_input("Surface Facility ($/CY)", value=25, min_value=15, max_value=75)
        else:
            disposal_cost = 25
            backfill_cost = 10
            onsite_cost = 25
            surface_cost = 25
        
        st.markdown("### 🎯 Project Priorities")
        col1, col2, col3 = st.columns(3)
        with col1:
            cost_priority = st.select_slider("Cost Importance", 
                                            options=['low', 'medium', 'high'],
                                            value='medium')
        with col2:
            speed_priority = st.select_slider("Speed Importance",
                                             options=['low', 'medium', 'high'],
                                             value='medium')
        with col3:
            esg_priority = st.select_slider("ESG/Sustainability",
                                           options=['low', 'medium', 'high'],
                                           value='medium')
        
        needs_backfill = st.checkbox("Clean backfill required", value=True)
        
        submitted = st.form_submit_button("🔍 Analyze Solutions", type="primary", use_container_width=True)
        
        if submitted:
            advanced_params = {
                'truck_capacity_cy': truck_capacity,
                'num_trucks': num_trucks,
                'truck_hourly_rate': truck_hourly_rate,
                'excavator_rate': excavator_rate,
                'loader_rate': loader_rate,
                'work_hours_per_day': work_hours_per_day,
                'disposal_cost_cy': disposal_cost,
                'backfill_cost_cy': backfill_cost,
                'onsite_processing_cost_cy': onsite_cost,
                'surface_processing_cost_cy': surface_cost
            }
            
            st.session_state.analysis = {
                'site_lat': site_lat,
                'site_lon': site_lon,
                'tph_level': tph_level,
                'chloride_level': chloride_level,
                'volume_cy': volume_cy,
                'needs_backfill': needs_backfill,
                'priorities': {
                    'cost': cost_priority,
                    'speed': speed_priority,
                    'esg': esg_priority
                },
                'advanced_params': advanced_params if use_custom_pricing or True else None,
                'soil_permeability': soil_permeability
            }
            st.session_state.show_results = True
            st.rerun()

# ============================================================================
# RESULTS DISPLAY
# ============================================================================

def show_results():
    """Display analysis results and recommendations"""
    
    analysis = st.session_state.analysis
    db = load_facilities_database()
    
    st.markdown("## 🎯 Solution Analysis & Recommendations")
    
    # ========================================================================
    # LOCATION SUMMARY
    # ========================================================================
    
    st.markdown("### 📍 Location Summary")
    
    # Get location details
    state, county = determine_state_county(analysis['site_lat'], analysis['site_lon'], db)
    soil_type = get_soil_type(analysis['site_lat'], analysis['site_lon'], state)
    reg_thresholds = get_regulatory_thresholds(state)
    
    # Find nearest qualified landfill for distance
    nearest_lf = find_nearest_qualified_landfill(
        analysis['site_lat'], 
        analysis['site_lon'],
        analysis['tph_level'],
        analysis['chloride_level'],
        analysis['needs_backfill'],
        db
    )
    
    distance_to_landfill = nearest_lf['distance_miles'] if nearest_lf else "N/A"
    nearest_landfill_name = f"{nearest_lf['landfill']['company']} - {nearest_lf['landfill']['site_name']}" if nearest_lf else "None found"
    
    # Display location info in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <p class="metric-label">Location</p>
            <p class="metric-value" style="font-size: 1.5rem;">{state}</p>
            <p style="color: #5a8a6f; margin: 0.5rem 0 0 0;">
                <strong>County:</strong> {county}<br>
                <strong>Coordinates:</strong> {analysis['site_lat']:.4f}, {analysis['site_lon']:.4f}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <p class="metric-label">Soil Characteristics</p>
            <p class="metric-value" style="font-size: 1.3rem;">{soil_type}</p>
            <p style="color: #5a8a6f; margin: 0.5rem 0 0 0;">
                <strong>Volume:</strong> {analysis['volume_cy']:,.0f} CY
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <p class="metric-label">Nearest Landfill</p>
            <p class="metric-value" style="font-size: 1.3rem;">{distance_to_landfill:.1f} mi</p>
            <p style="color: #5a8a6f; margin: 0.5rem 0 0 0; font-size: 0.85rem;">
                {nearest_landfill_name}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Regulatory information
    with st.expander("📋 Regulatory Thresholds & Standards", expanded=False):
        st.markdown(f"""
        **Regulatory Agency:** {reg_thresholds['regulatory_agency']}
        
        **TPH (Total Petroleum Hydrocarbons) - Soil Cleanup Standards:**
        - Residential Use: {reg_thresholds['tph_residential_mgkg']} mg/kg
        - Industrial/Commercial Use: {reg_thresholds['tph_industrial_mgkg']} mg/kg
        
        **Chlorides:**
        - {reg_thresholds['chloride_soil_mgkg']}
        
        **Your Site:**
        - TPH Level: {analysis['tph_level']} mg/kg {'✅ Below industrial threshold' if analysis['tph_level'] < reg_thresholds['tph_industrial_mgkg'] else '⚠️ Exceeds industrial threshold'}
        - Chloride Level: {analysis['chloride_level']} mg/kg
        
        *Note: {reg_thresholds['notes']}*
        """)
    
    st.markdown("---")
    
    # ========================================================================
    # PERFORM CALCULATIONS
    # ========================================================================
    
    with st.spinner("Analyzing remediation options..."):
        dig_haul = calculate_dig_and_haul(
            analysis['volume_cy'],
            analysis['site_lat'],
            analysis['site_lon'],
            analysis['needs_backfill'],
            analysis['tph_level'],
            analysis['chloride_level'],
            db,
            analysis['advanced_params']
        )
        
        onsite = calculate_onsite_remediation(
            analysis['volume_cy'],
            analysis['site_lat'],
            analysis['site_lon'],
            analysis.get('soil_permeability', 'medium'),
            analysis['tph_level'],
            analysis['chloride_level'],
            analysis['advanced_params']
        )
        
        surface = calculate_surface_facility(
            analysis['volume_cy'],
            analysis['site_lat'],
            analysis['site_lon'],
            analysis['needs_backfill'],
            analysis['tph_level'],
            analysis['chloride_level'],
            db,
            analysis['advanced_params']
        )
    
    # Generate recommendation
    recommended, scores = generate_recommendation(dig_haul, onsite, surface, analysis['priorities'])
    
    # ========================================================================
    # COMPARISON TABLE
    # ========================================================================
    
    st.markdown("### 📊 Solution Comparison")
    
    # Build options list
    options_list = []
    if dig_haul:
        options_list.append(('dig_haul', dig_haul))
    if onsite:
        options_list.append(('onsite', onsite))
    if surface:
        options_list.append(('surface', surface))
    
    # Create comprehensive comparison dataframe
    comparison_data = []
    for opt_type, opt in options_list:
        is_recommended = (opt_type == recommended)
        
        row = {
            '': '⭐ RECOMMENDED' if is_recommended else '',
            'Solution': opt['option_name'],
            'Total Cost': f"${opt['total_cost']:,.0f}",
            'Cost per CY': f"${opt['cost_per_cy']:.2f}",
            'Timeline': f"{opt['project_days']} days",
            'CO₂ Emissions': f"{opt['co2_tons']:.2f} tons",
            'Backfill Included': '✅ Yes' if opt.get('includes_backfill', False) else '❌ No',
        }
        
        # Add specific details
        if opt_type == 'dig_haul':
            row['Key Details'] = f"{opt['distance_miles']:.0f} mi to landfill"
            if not opt.get('backfill_available_at_landfill'):
                row['Key Details'] += " ⚠️ Separate backfill needed"
        elif opt_type == 'onsite':
            row['Key Details'] = "Soil treated in place"
        else:  # surface
            row['Key Details'] = f"{opt['distance_miles']:.0f} mi to facility"
        
        comparison_data.append(row)
    
    df_comparison = pd.DataFrame(comparison_data)
    
    # Display table with custom styling
    st.dataframe(
        df_comparison,
        hide_index=True,
        use_container_width=True,
        column_config={
            '': st.column_config.TextColumn(width="small"),
            'Solution': st.column_config.TextColumn(width="medium"),
            'Total Cost': st.column_config.TextColumn(width="medium"),
            'Cost per CY': st.column_config.TextColumn(width="small"),
            'Timeline': st.column_config.TextColumn(width="small"),
            'CO₂ Emissions': st.column_config.TextColumn(width="small"),
            'Backfill Included': st.column_config.TextColumn(width="small"),
            'Key Details': st.column_config.TextColumn(width="medium"),
        }
    )
    
    st.markdown("---")
    
    # ========================================================================
    # DETAILED BREAKDOWNS
    # ========================================================================
    
    st.markdown("### 💰 Detailed Cost Breakdowns")
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (opt_type, opt) in enumerate(options_list):
        col = [col1, col2, col3][idx]
        is_recommended = (opt_type == recommended)
        
        with col:
            if is_recommended:
                st.markdown('<div class="recommended-badge">⭐ RECOMMENDED</div>', unsafe_allow_html=True)
            
            st.markdown(f"**{opt['option_name']}**")
            
            if opt_type == 'dig_haul':
                breakdown = {
                    'Equipment': f"${opt['equipment_cost']:,.0f}",
                    'Trucking': f"${opt['trucking_cost']:,.0f}",
                    'Disposal': f"${opt['disposal_cost']:,.0f}",
                    'Backfill': f"${opt['backfill_cost']:,.0f}",
                }
            elif opt_type == 'onsite':
                breakdown = {
                    'Processing': f"${opt['processing_cost']:,.0f}",
                    'Mobilization': f"${opt['mobilization_cost']:,.0f}",
                    'Amendments': f"${opt['amendment_cost']:,.0f}",
                }
            else:  # surface
                breakdown = {
                    'Trucking': f"${opt['trucking_cost']:,.0f}",
                    'Processing': f"${opt['processing_cost']:,.0f}",
                }
            
            for category, cost in breakdown.items():
                st.write(f"• {category}: {cost}")
            
            st.markdown(f"**Total: ${opt['total_cost']:,.0f}**")
    
    st.markdown("---")
    
    # ========================================================================
    # PROS & CONS
    # ========================================================================
    
    st.markdown("### ✅ ⚠️ Advantages & Considerations")
    
    col1, col2, col3 = st.columns(3)
    
    pros_cons = {
        'dig_haul': {
            'pros': [
                'Fast execution',
                'Immediate removal',
                'No onsite disruption',
                'Predictable timeline'
            ],
            'cons': [
                'Highest carbon footprint',
                'Permanent disposal liability',
                'Backfill coordination needed',
                'Distance-dependent costs'
            ]
        },
        'onsite': {
            'pros': [
                'Lowest carbon footprint',
                'Original soil retained',
                'No disposal liability',
                'Cost-effective for large volumes',
                'Sustainable solution'
            ],
            'cons': [
                'Longer timeline',
                'Weather dependent',
                'Space requirements',
                'Ongoing site presence'
            ]
        },
        'surface': {
            'pros': [
                'Clean soil returned',
                'Controlled environment',
                'No disposal liability',
                'Single vendor solution',
                'Good for complex contamination'
            ],
            'cons': [
                'Transportation both ways',
                'Facility scheduling',
                'Moderate timeline'
            ]
        }
    }
    
    for idx, (opt_type, opt) in enumerate(options_list):
        col = [col1, col2, col3][idx]
        
        with col:
            st.markdown(f"**{opt['option_name']}**")
            
            st.markdown('<div class="pros-list">', unsafe_allow_html=True)
            st.markdown("**✅ Advantages**")
            for pro in pros_cons[opt_type]['pros']:
                st.markdown(f"• {pro}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("")
            
            st.markdown('<div class="cons-list">', unsafe_allow_html=True)
            st.markdown("**⚠️ Considerations**")
            for con in pros_cons[opt_type]['cons']:
                st.markdown(f"• {con}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # RECOMMENDATION EXPLANATION
    # ========================================================================
    
    st.markdown("### 💡 Why This Recommendation?")
    
    if recommended == 'dig_haul':
        st.info("""
            **Dig & Haul** is recommended for your project because:
            - Fast execution meets your timeline needs
            - Volume and distance make trucking economical
            - Immediate site remediation is prioritized
            - Landfill proximity makes this cost-effective
        """)
    elif recommended == 'onsite':
        st.success("""
            **Onsite Remediation** is recommended for your project because:
            - Excellent cost-effectiveness for your volume
            - Lowest environmental impact (CO₂ emissions)
            - Original soil retained, reducing waste
            - No long-term disposal liability
            - Sustainable approach aligns with ESG goals
            - Treatment duration is acceptable for your timeline priorities
        """)
    else:  # surface
        st.success("""
            **Surface Facility Treatment** is recommended for your project because:
            - Balanced cost and timeline
            - Clean soil returned to site (no backfill sourcing needed)
            - Professional treatment in controlled environment
            - No disposal liability
            - Facility proximity makes transportation economical
            - Excellent for sites requiring backfill
        """)
    
    # ========================================================================
    # DOWNLOAD & RESTART
    # ========================================================================
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create downloadable report
        report_data = []
        for opt_type, opt in options_list:
            report_data.append({
                'Solution': opt['option_name'],
                'Recommended': 'Yes' if opt_type == recommended else 'No',
                'Total_Cost': opt['total_cost'],
                'Cost_Per_CY': opt['cost_per_cy'],
                'Project_Days': opt['project_days'],
                'CO2_Tons': opt['co2_tons'],
                'Includes_Backfill': 'Yes' if opt.get('includes_backfill', False) else 'No'
            })
        
        df_report = pd.DataFrame(report_data)
        csv = df_report.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Report (CSV)",
            data=csv,
            file_name=f"clean_futures_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application"""
    
    # Initialize session state
    if 'mode' not in st.session_state:
        st.session_state.mode = None
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    
    # Show appropriate page
    if st.session_state.show_results:
        show_results()
    elif st.session_state.mode == 'simple':
        show_simple_questionnaire()
    elif st.session_state.mode == 'advanced':
        show_advanced_questionnaire()
    else:
        show_welcome_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #5a8a6f; padding: 2rem 0;'>
            <p style='margin: 0; font-family: "Crimson Pro", serif; font-size: 1.2rem;'>
                <strong>Clean Futures</strong> | Making Our World Better and Cleaner
            </p>
            <p style='margin: 0.5rem 0 0 0; font-family: "Work Sans", sans-serif; font-size: 0.9rem;'>
                Permian Basin Solution Recommendation Tool | v1.0
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

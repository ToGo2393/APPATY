
def convert_power(value, conversion_type):
    """
    Convert power between kW and HP.
    conversion_type: 'kW to HP' or 'HP to kW'
    """
    if conversion_type == 'kW to HP':
        return value * 1.34102
    elif conversion_type == 'HP to kW':
        return value / 1.34102
    return None

def convert_length(value, from_unit, to_unit):
    """Convert length between metric and imperial units."""
    # Base unit: meters
    to_meters = {
        "m": 1.0, "cm": 0.01, "mm": 0.001, 
        "in": 0.0254, "ft": 0.3048, "km": 1000.0, "mi": 1609.344
    }
    if from_unit not in to_meters or to_unit not in to_meters: return None
    meters = value * to_meters[from_unit]
    return meters / to_meters[to_unit]

def convert_area(value, from_unit, to_unit):
    """Convert area (m^2, ft^2, etc). Base: m^2"""
    to_sq_m = {
        "m²": 1.0, "mm²": 0.000001, 
        "ft²": 0.09290304,
        "cm²": 0.0001,
        "in²": 0.00064516,
        "acre": 4046.856
    }
    if from_unit not in to_sq_m or to_unit not in to_sq_m: return None
    sq_m = value * to_sq_m[from_unit]
    return sq_m / to_sq_m[to_unit]

def convert_volume(value, from_unit, to_unit):
    """Convert volume (m^3, L, Gal). Base: m^3"""
    to_cu_m = {
        "m³": 1.0,
        "L": 0.001,
        "Gal": 0.00378541,
        "ft³": 0.0283168,
        "in³": 0.000016387
    }
    if from_unit not in to_cu_m or to_unit not in to_cu_m: return None
    cu_m = value * to_cu_m[from_unit]
    return cu_m / to_cu_m[to_unit]

def convert_mass(value, from_unit, to_unit):
    """Convert mass between kg and lbs."""
    if from_unit == "kg" and to_unit == "lbs": return value * 2.20462
    elif from_unit == "lbs" and to_unit == "kg": return value / 2.20462
    return value if from_unit == to_unit else None

def convert_force(value, from_unit, to_unit):
    """Convert Force (N, kN, lbf)"""
    to_newton = { "N": 1.0, "kN": 1000.0, "lbf": 4.44822 }
    if from_unit not in to_newton or to_unit not in to_newton: return None
    n_val = value * to_newton[from_unit]
    return n_val / to_newton[to_unit]

def convert_pressure(value, from_unit, to_unit):
    """Convert Pressure (Pa, Bar, Psi)"""
    to_pa = { "Pa": 1.0, "Bar": 100000.0, "Psi": 6894.76 }
    if from_unit not in to_pa or to_unit not in to_pa: return None
    p_val = value * to_pa[from_unit]
    return p_val / to_pa[to_unit]

def convert_temperature(value, from_unit, to_unit):
    """
    Convert temperature (C, K, F).
    """
    if from_unit == to_unit: return value
    
    # Normalize inputs for partial matches (e.g. "Celsius (°C)")
    if "C" in from_unit and "K" not in from_unit: from_unit = "°C"
    elif "K" in from_unit: from_unit = "K"
    elif "F" in from_unit: from_unit = "°F"

    if "C" in to_unit and "K" not in to_unit: to_unit = "°C"
    elif "K" in to_unit: to_unit = "K"
    elif "F" in to_unit: to_unit = "°F"
    
    # Convert to Celsius first
    c_val = 0.0
    if from_unit == "°C": c_val = value
    elif from_unit == "K": c_val = value - 273.15
    elif from_unit == "°F": c_val = (value - 32) * 5/9
    
    # Convert from Celsius to target
    if to_unit == "°C": return c_val
    elif to_unit == "K": return c_val + 273.15
    elif to_unit == "°F": return (c_val * 9/5) + 32
    return None

def calculate_appliance_cost(watts, hours_per_day, unit_price):
    """
    Calculate energy cost.
    watts: Power rating
    hours_per_day: Usage
    unit_price: Cost per kWh
    """
    try:
        daily_kwh = (watts * hours_per_day) / 1000.0
        daily_cost = daily_kwh * unit_price
        monthly_cost = daily_cost * 30
        return daily_kwh, daily_cost, monthly_cost
    except:
        return None, None, None

def calculate_heat_transfer(m, c, dt):
    """
    Calculate heat transfer Q = m * c * dt.
    """
    return m * c * dt

def calculate_thermo_general(target, Q=None, m=None, c=None, dt=None):
    """
    Solve for target variable in Q = m * c * dt.
    target: 'Q', 'm', 'c', or 'dt'
    """
    try:
        if target == 'Q':
            return m * c * dt
        elif target == 'm':
            return Q / (c * dt)
        elif target == 'c':
            return Q / (m * dt)
        elif target == 'dt':
            return Q / (m * c)
    except (TypeError, ZeroDivisionError):
        return None
    return None

def calculate_1st_law_thermo(target, dU=None, Q=None, W=None):
    """
    Solve for variable in First Law: dU = Q - W
    target: 'dU', 'Q', 'W'
    """
    try:
        if target == 'dU':
            return Q - W
        elif target == 'Q':
            return dU + W
        elif target == 'W':
            return Q - dU
    except (TypeError):
        return None
    return None

def calculate_carnot_efficiency(target, eff=None, Tc=None, Th=None):
    """
    Solve for variable in Carnot Efficiency: eff = 1 - Tc/Th
    Temps in Kelvin.
    target: 'eff', 'Tc', 'Th'
    """
    try:
        if target == 'eff':
            return 1 - (Tc / Th)
        elif target == 'Tc':
            return Th * (1 - eff)
        elif target == 'Th':
            return Tc / (1 - eff)
    except (TypeError, ZeroDivisionError):
        return None
    return None

def calculate_ideal_gas(target, P=None, V=None, n=None, R=0.0821, T=None):
    """
    Solve for variable in PV = nRT
    Default R = 0.0821 L*atm/(mol*K)
    target: 'P', 'V', 'n', 'T'
    """
    try:
        if target == 'P':
            return (n * R * T) / V
        elif target == 'V':
            return (n * R * T) / P
        elif target == 'n':
            return (P * V) / (R * T)
        elif target == 'T':
            return (P * V) / (n * R)
    except (TypeError, ZeroDivisionError):
        return None
    return None

def calculate_boyles_law(target, P1=None, V1=None, P2=None, V2=None):
    """
    Solve for variable in P1*V1 = P2*V2
    """
    try:
        if target == 'P1':
            return (P2 * V2) / V1
        elif target == 'V1':
            return (P2 * V2) / P1
        elif target == 'P2':
            return (P1 * V1) / V2
        elif target == 'V2':
            return (P1 * V1) / P2
    except (TypeError, ZeroDivisionError):
        return None
    return None

def calculate_charles_law(target, V1=None, T1=None, V2=None, T2=None):
    """
    Solve for variable in V1/T1 = V2/T2
    """
    try:
        if target == 'V1':
            return (V2 * T1) / T2
        elif target == 'T1':
            return (V1 * T2) / V2
        elif target == 'V2':
            return (V1 * T2) / T1
        elif target == 'T2':
            return (V2 * T1) / V1
    except (TypeError, ZeroDivisionError):
        return None
    return None

def calculate_ohm_general(target, V=None, I=None, R=None):
    """
    Solve for target variable in V = I * R
    """
    try:
        if target == 'V':
            return I * R
        elif target == 'I':
            return V / R
        elif target == 'R':
            return V / I
    except (TypeError, ZeroDivisionError):
        return None
    return None

def calculate_fluid_pressure(target, P=None, F=None, A=None):
    """
    Solve for target variable in P = F / A
    """
    try:
        if target == 'P':
            return F / A
        elif target == 'F':
            return P * A
        elif target == 'A':
            return F / P
    except (TypeError, ZeroDivisionError):
        return None
    return None

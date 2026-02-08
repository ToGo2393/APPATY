import streamlit as st
import pandas as pd
import utils.calculators as calc
import utils.formulas as forms
import utils.auth as auth
import utils.db as db
import utils.algebra_solver as algebra
import time
# Note: Lazy imports for sympy/scipy are used inside functions to prevent white screen lag.

# Page Configuration
st.set_page_config(
    page_title="APPATY Engineering Toolkit",
    page_icon="⚙️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize Database
db.init_db()

# Initialize Session
auth.init_session()

# PWA & Mobile UX Injection
# PWA & Mobile UX Injection
try:
    import utils.ux as ux
    ux.inject_custom_css()
    ux.inject_pwa_meta()
    ux.inject_haptics()
    ux.inject_auto_select_js()
except ImportError:
    pass # Fallback if ux module issues

# Helper to save history if logged in
def save_log(calc_name, result):
    if st.session_state.user:
        db.add_history_item(st.session_state.user['id'], calc_name, result)
    else:
        st.toast("🔐 Login to Save History")

def render_ad_slot(position='top'):
    """Renders a consistent advertisement slot."""
    is_premium = False
    if st.session_state.user and st.session_state.user.get('is_premium'):
        is_premium = True
    
    if not is_premium:
        if position == 'top':
            height = "60px"
            content = "<strong>📢 ADVERTISEMENT</strong> - Support APPATY"
        else: # bottom
            height = "100px"
            content = "<strong>🚀 Upgrade to Premium</strong><br><span style='font-size:0.8em'>for an Ad-Free Experience and Advanced Tools!</span>"

        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; background-color: #f9f9f9; padding: 10px; 
                        text-align: center; margin: 20px 0; border-radius: 5px; height: {height}; 
                        display: flex; align-items: center; justify-content: center; color: #555;">
                <div>
                    {content}
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

# --- Sidebar ---
with st.sidebar:
    st.title("APPATY 🛠️")
    st.markdown("### Engineering Cloud")
    st.markdown("---")
    
    # Auth System
    auth.render_auth_sidebar()
    
    st.markdown("---")
    
    # Advertisement System
    is_premium = False
    if st.session_state.user and st.session_state.user['is_premium']:
        is_premium = True
        
    if not is_premium:
        st.markdown('<div class="ad-box">📢 ADVERTISEMENT<br><span style="font-size:0.8em">Upgrade to Premium to remove ads</span></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2026 APPATY v2.0")

# --- Main Interface ---
# Top-Right Navigation Layout
col_header, col_nav = st.columns([3, 2])

with col_header:
    st.title("Engineering Suite")

with col_nav:
    # Navigation Selector (Top-Right)
    selected_module = st.selectbox(
        "🛠️ Select Module",
        [
            "📐 Dimensions", 
            "⚡ Power", 
            "🌡️ Temperature", 
            "🎈 Pressure",
            "💡 Electricity", 
            "💰 Energy Cost",
            "🔥 Thermodynamics",
            "🧮 Equation Solver",
            "🌌 Universal Solver"
        ]
    )

# Helper for smart formatting
smart_fmt = lambda x: f"{x:.8f}".rstrip('0').rstrip('.')

# 1. 📐 Dimensions
if selected_module == "📐 Dimensions":
    render_ad_slot()
    st.header("Unit Conversions")
    subtabs = st.tabs(["Length", "Area", "Volume"])

    with subtabs[0]:
        c1, c2, c3 = st.columns(3)
        val = c1.number_input("Value", 0.0, key="len_val", format="%.4f")
        u1 = c2.selectbox("From", ["m", "cm", "mm", "in", "ft", "km", "mi"], key="len_from")
        u2 = c3.selectbox("To", ["m", "cm", "mm", "in", "ft", "km", "mi"], key="len_to")
        if st.button("Calculate", key="len_btn", use_container_width=True):
            res = calc.convert_length(val, u1, u2)
            res_str = smart_fmt(res)
            st.markdown(f"### Result: {res_str} {u2}")
            save_log(f"Length: {val}{u1} -> {u2}", f"{res_str} {u2}")

    with subtabs[1]:
        c1, c2, c3 = st.columns(3)
        val = c1.number_input("Value", 0.0, key="area_val", format="%.4f")
        u1 = c2.selectbox("From", ["m²", "ft²", "cm²", "in²", "acre"], key="area_from")
        u2 = c3.selectbox("To", ["m²", "ft²", "cm²", "in²", "acre"], key="area_to")
        if st.button("Calculate", key="area_btn", use_container_width=True):
            res = calc.convert_area(val, u1, u2)
            res_str = smart_fmt(res)
            st.markdown(f"### Result: {res_str} {u2}")
            save_log(f"Area: {val}{u1} -> {u2}", f"{res_str} {u2}")

    with subtabs[2]:
        c1, c2, c3 = st.columns(3)
        val = c1.number_input("Value", 0.0, key="vol_val", format="%.4f")
        u1 = c2.selectbox("From", ["m³", "L", "Gal", "ft³", "in³"], key="vol_from")
        u2 = c3.selectbox("To", ["m³", "L", "Gal", "ft³", "in³"], key="vol_to")
        if st.button("Calculate", key="vol_btn", use_container_width=True):
            res = calc.convert_volume(val, u1, u2)
            res_str = smart_fmt(res)
            st.markdown(f"### Result: {res_str} {u2}")
            save_log(f"Volume: {val}{u1} -> {u2}", f"{res_str} {u2}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_ad_slot(position='bottom')

# 2. ⚡ Power
elif selected_module == "⚡ Power":
    render_ad_slot()
    st.header("Power Converter")
    st.latex(r"P_{HP} \approx P_{kW} \times 1.341")
    
    col1, col2 = st.columns(2)
    val = col1.number_input("Power Value", 0.0, key="power_val", format="%.4f")
    direct = col2.selectbox("Direction", ["kW to HP", "HP to kW"], key="power_dir")
    
    if st.button("Calculate Power", key="power_btn", use_container_width=True):
        res = calc.convert_power(val, direct)
        unit = "HP" if "kW to HP" == direct else "kW"
        res_str = smart_fmt(res)
        st.markdown(f"### Result: {res_str} {unit}")
        save_log(f"Power {direct}", f"{res_str} {unit}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_ad_slot(position='bottom')

# 3. 🌡️ Temperature
elif selected_module == "🌡️ Temperature":
    render_ad_slot()
    st.header("🌡️ Temperature Converter")
    c1, c2, c3 = st.columns(3)
    t_val = c1.number_input("Value", value=0.0, format="%.4f", key="temp_val")
    t_from = c2.selectbox("From", ["Celsius (°C)", "Kelvin (K)", "Fahrenheit (°F)"], key="temp_from")
    t_to = c3.selectbox("To", ["Celsius (°C)", "Kelvin (K)", "Fahrenheit (°F)"], key="temp_to")
    
    if st.button("Convert Temperature", key="temp_btn", use_container_width=True):
        # Conversion Logic
        import utils.calculators as calc
        res = calc.convert_temperature(t_val, t_from, t_to)
        
        # Display Formula (LaTeX)
        if "Celsius" in t_from and "Kelvin" in t_to:
            st.latex(r"T_K = T_C + 273.15")
        elif "Kelvin" in t_from and "Celsius" in t_to:
            st.latex(r"T_C = T_K - 273.15")
        elif "Celsius" in t_from and "Fahrenheit" in t_to:
            st.latex(r"T_F = (T_C \cdot 9/5) + 32")
        elif "Fahrenheit" in t_from and "Celsius" in t_to:
            st.latex(r"T_C = (T_F - 32) \cdot 5/9")
        elif "Kelvin" in t_from and "Fahrenheit" in t_to:
            st.latex(r"T_F = (T_K - 273.15) \cdot 9/5 + 32")
        
        # Smart formatting for result
        res_str = f"{res:g}" if res is not None else "Error"
        
        st.markdown(f"### Result: {res_str} {t_to}")
        save_log(f"Temp: {t_val}{t_from} to {t_to}", f"{res_str}")

    st.markdown("<br>", unsafe_allow_html=True)
    render_ad_slot(position='bottom')

# 4. 🎈 Pressure (Overhauled)
elif selected_module == "🎈 Pressure":
    render_ad_slot()
    st.header("💨 Pressure Suite")

    # Tab 1: Physics Calculation
    tab1, tab2 = st.tabs(["🔢 Pressure Solver (P=F/A)", "🔄 Unit Converter"])

    with tab1:
        st.latex(r"P = \frac{F}{A}")
        col1, col2 = st.columns(2)
        with col1:
            f = st.number_input("Force", value=0.0, format="%.4f", key="p_f")
            f_unit = st.selectbox("Unit", ["N", "kN", "lbf"], key="p_f_u")
        with col2:
            a = st.number_input("Area", value=0.0, format="%.4f", key="p_a")
            a_unit = st.selectbox("Unit", ["m²", "mm²", "in²"], key="p_a_u")
        
        if st.button("Calculate Pressure", use_container_width=True):
            # Normalization logic
            try:
                # Normalize Force to N
                f_norm = calc.convert_force(f, f_unit, "N")
                # Normalize Area to m²
                a_norm = calc.convert_area(a, a_unit, "m²")
                
                if a == 0 or a_norm == 0:
                     st.error("Mathematical limit reached: Divisor cannot be zero.")
                elif a_norm > 0:
                    p_pa = f_norm / a_norm
                    st.success(f"Calculated Pressure: {p_pa:.4f} Pa")
                    save_log(f"Pressure P=F/A", f"{p_pa:.4f} Pa")
                else:
                    st.error("Area must be positive")
            except Exception as e:
                st.error(f"Error: {e}")

    with tab2:
        st.subheader("Pressure Unit Converter")
        # Layout for converter
        c_col1, c_col2, c_col3 = st.columns([2, 1, 1])
        with c_col1:
            p_val = st.number_input("Enter Value", value=0.0, format="%.4f")
        with c_col2:
            p_from = st.selectbox("From", ["Bar", "PSI", "kPa", "MPa", "atm"], key="p_from")
        with c_col3:
            p_to = st.selectbox("To", ["Bar", "PSI", "kPa", "MPa", "atm"], key="p_to")
        
        # Immediate calculation
        rates = {"Bar": 1.0, "PSI": 14.5038, "kPa": 100.0, "MPa": 0.1, "atm": 0.9869}
        if p_from in rates and p_to in rates:
            # Convert to Bar first
            val_in_bar = p_val / rates[p_from]
            # Convert to target
            res = val_in_bar * rates[p_to]
            
            st.markdown(f"**Result:** {res:.4f} {p_to}")
            st.success(f"{p_val} {p_from} = {res:.4f} {p_to}")
            save_log(f"Pressure Conv {p_from}->{p_to}", f"{res:.4f}")

    st.markdown("<br>", unsafe_allow_html=True)
    render_ad_slot(position='bottom')

# 5. 💡 Electricity
elif selected_module == "💡 Electricity":
    render_ad_slot()
    st.header("Electrical Engineering")
    st.subheader("Ohm's Law")
    st.latex(r'V = I \cdot R')
    
    col1, col2 = st.columns(2)
    target = col1.selectbox("Target", ["V", "I", "R"], key="ohm_target")
    
    inputs = {}
    if target != 'V': inputs['V'] = col2.number_input("Voltage (V)", value=0.0, key="ohm_v", format="%.4f")
    if target != 'I': inputs['I'] = col2.number_input("Current (I)", value=0.0, key="ohm_i", format="%.4f")
    if target != 'R': inputs['R'] = col2.number_input("Resistance (Ω)", value=0.0, key="ohm_r", format="%.4f")
    
    if st.button("Calculate Ohm", key="ohm_btn", use_container_width=True):
        res = calc.calculate_ohm_general(target, **inputs)
        unit_map = {'V': 'V', 'I': 'A', 'R': 'Ω'}
        if res is not None:
            res_str = smart_fmt(res)
            st.markdown(f"### Result: {res_str} {unit_map[target]}")
            save_log(f"Ohm {target}", f"{res_str} {unit_map[target]}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_ad_slot(position='bottom')

# 6. 💰 Energy Cost
elif selected_module == "💰 Energy Cost":
    render_ad_slot()
    st.header("Appliance Energy Cost")
    st.caption("Calculate monthly cost based on usage.")
    
    # Currency Selection
    curr_map = {"TL": "₺", "USD": "$", "EUR": "€", "GBP": "£"}
    col1, col2 = st.columns(2)
    currency = col1.selectbox("Currency", list(curr_map.keys()), key="cost_curr")
    sym = curr_map[currency]
    
    watts = col2.number_input("Power Rating (Watts)", 0.0, key="cost_watts", format="%.4f")
    hours = col1.number_input("Hours used per day", 0.0, key="cost_hours", format="%.4f")
    price = col2.number_input(f"Unit Price ({currency}/kWh)", 0.0, format="%.4f", key="cost_price")
    
    if st.button("Calculate Cost", key="cost_btn", use_container_width=True):
        dkwh, dcost, mcost = calc.calculate_appliance_cost(watts, hours, price)
        if dkwh:
            dkwh_str = smart_fmt(dkwh)
            dcost_str = smart_fmt(dcost)
            mcost_str = smart_fmt(mcost)
            
            st.success(f"Daily Usage: {dkwh_str} kWh")
            st.info(f"Daily Cost: {dcost_str} {sym}")
            st.markdown(f"### Total Monthly Cost: {mcost_str} {sym}")
            save_log("Appliance Cost", f"{mcost_str} {sym}/mo")
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_ad_slot(position='bottom')

# 7. 🔥 Thermodynamics
elif selected_module == "🔥 Thermodynamics":
    render_ad_slot()
    st.header("Thermodynamics")
    st.subheader("Heat Transfer")
    st.latex(r'Q = m \cdot c \cdot \Delta T')
    
    presets = {
        "Aluminium": 0.887, "Asphalt": 0.915, "Bone": 0.44, "Boron": 1.106, 
        "Brass": 0.92, "Brick": 0.841, "Cast Iron": 0.554, "Clay": 0.878, 
        "Coal": 1.262, "Cobalt": 0.42, "Concrete": 0.879, "Copper": 0.385, 
        "Glass": 0.792, "Gold": 0.13, "Granite": 0.774, "Gypsum": 1.09, 
        "Helium": 5.192, "Hydrogen": 14.3, "Ice": 2.09, "Iron": 0.462, 
        "Lead": 0.13, "Limestone": 0.806, "Lithium": 3.58, "Magnesium": 1.024, 
        "Marble": 0.832, "Mercury": 0.126, "Nitrogen": 1.04, "Oak Wood": 2.38, 
        "Oxygen": 0.919, "Platinum": 0.15, "Plutonium": 0.14, "Quartzite": 1.1, 
        "Rubber": 2.005, "Salt": 0.881, "Sand": 0.78, "Sandstone": 0.74, 
        "Silicon": 0.71, "Silver": 0.236, "Soil": 1.81, "Stainless Steel 316": 0.468, 
        "Steam": 2.094, "Sulfur": 0.706, "Thorium": 0.118, "Tin": 0.226, 
        "Titanium": 0.521, "Tungsten": 0.133, "Uranium": 0.115, "Vanadium": 0.49, 
        "Water": 4.187, "Zinc": 0.389
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mat = st.selectbox("Material Preset", ["Manual"] + sorted(list(presets.keys())))
        c_val = 1.0
        if mat != "Manual":
            c_val = presets[mat]
            st.info(f"Specific Heat: {c_val}")
        
    with col1:
        c_input = st.number_input("Specific Heat c (kJ/kg·K)", value=0.0 if mat == "Manual" else c_val, disabled=(mat != "Manual"), format="%.4f", step=0.0001)
        
    with col2:
        # High precision mass input
        m = st.number_input("Mass (kg)", min_value=0.001, value=0.0, step=0.01, format="%.4f")
        
    with col3:
        t1 = st.number_input("Initial Temp T1 (K)", 0.0, format="%.4f")
        t2 = st.number_input("Final Temp T2 (K)", 0.0, format="%.4f")
        
    if st.button("Calculate", key="thermo_btn", use_container_width=True):
        if m <= 0:
            st.warning("⚠️ Mass must be a positive value.")
        else:
            dt = t2 - t1
            res = calc.calculate_heat_transfer(m, c_input, dt)
            res_str = smart_fmt(res)
            st.markdown(f"### Result: {res_str} kJ")
            save_log("Thermo Q", f"{res_str} kJ")
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_ad_slot(position='bottom')

# 8. 🧮 Equation Solver
elif selected_module == "🧮 Equation Solver":
    render_ad_slot()
    st.header("Algebraic Solver (Coefficient Method)")
    
    eq_type = st.selectbox("Equation Type", [
        "1st Degree (1 Variable)",
        "1st Degree (System of 2)",
        "2nd Degree (1 Variable)",
        "Quadratic System (Intersection)"
    ])
    
    st.markdown("---")
    
    def format_res(val):
        import sympy as sp
        """Helper to format symbolic value with decimal approx."""
        try:
            # Calculate decimal
            dec = val.evalf(3)
            
            # Check if complex
            if dec.is_complex and not dec.is_real:
                 # Format complex: a +/- bi
                 re = float(sp.re(dec))
                 im = float(sp.im(dec))
                 sign = "+" if im >= 0 else "-"
                 im_abs = abs(im)
                 dec_str = f"{re:.3f} {sign} {im_abs:.3f}i"
            else:
                 dec_str = f"{float(dec):.3f}"
            
            return f"{sp.latex(val)} \\approx {dec_str}"
        except:
            return str(val)

    if eq_type == "1st Degree (1 Variable)":
        st.latex("ax + b = 0")
        c1, c2 = st.columns(2)
        a = c1.text_input("Coefficient a", "1")
        b = c2.text_input("Coefficient b", "0")
        
        if st.button("Solve 1st Deg", key="solve_1d", use_container_width=True):
            res = algebra.solve_linear_1var(a, b)
            st.success("Solution Found:")
            st.latex(f"x = {format_res(res)}")
            save_log(f"1st Deg: {a}x + {b} = 0", f"x={res}")

    elif eq_type == "1st Degree (System of 2)":
        st.markdown("System:")
        st.latex(r"\\begin{cases} a_1x + b_1y = c_1 \\\\ a_2x + b_2y = c_2 \\end{cases}")
        
        c1, c2, c3 = st.columns(3)
        a1 = c1.text_input("a1", "1")
        b1 = c2.text_input("b1", "1")
        c1_val = c3.text_input("c1", "10")
        
        c4, c5, c6 = st.columns(3)
        a2 = c4.text_input("a2", "1")
        b2 = c5.text_input("b2", "-1")
        c2_val = c6.text_input("c2", "2")
        
        if st.button("Solve System", key="solve_sys_1d", use_container_width=True):
            import sympy as sp
            res = algebra.solve_linear_2vars([a1, b1, c1_val], [a2, b2, c2_val])
            if isinstance(res, dict):
                st.success("Solution Found:")
                for k, v in res.items():
                    st.latex(f"{sp.latex(k)} = {format_res(v)}")
            else:
                st.error(res)
            save_log("Linear System", str(res))

    elif eq_type == "2nd Degree (1 Variable)":
        st.latex("ax^2 + bx + c = 0")
        c1, c2, c3 = st.columns(3)
        a = c1.text_input("a", "1")
        b = c2.text_input("b", "0")
        c = c3.text_input("c", "-4")
        
        if st.button("Solve Quadratic", key="solve_quad", use_container_width=True):
            res = algebra.solve_quadratic_1var(a, b, c)
            if isinstance(res, list):
                st.success("Solution Found:")
                for i, r in enumerate(res):
                    st.latex(f"x_{{{i+1}}} = {format_res(r)}")
            else:
                st.error(res)
            save_log(f"Quad: {a}x^2+{b}x+{c}=0", str(res))

    elif eq_type == "Quadratic System (Intersection)":
        st.info("Find intersection of two curves.")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Equation 1")
            t1 = st.selectbox("Type 1", ["Quadratic (y = ax^2 + bx + c)", "Linear (ax + by = c)"])
            coeffs1 = []
            if "Quadratic" in t1:
                coeffs1 = [st.text_input("a (Eq1)", "1"), st.text_input("b (Eq1)", "0"), st.text_input("c (Eq1)", "0")]
            else:
                coeffs1 = [st.text_input("a (Eq1)", "1", key="l1a"), st.text_input("b (Eq1)", "-1", key="l1b"), st.text_input("c (Eq1)", "0", key="l1c")]
        
        with col2:
            st.subheader("Equation 2")
            t2 = st.selectbox("Type 2", ["Linear (ax + by = c)", "Quadratic (y = ax^2 + bx + c)"])
            coeffs2 = []
            if "Quadratic" in t2:
                coeffs2 = [st.text_input("a (Eq2)", "1", key="q2a"), st.text_input("b (Eq2)", "0", key="q2b"), st.text_input("c (Eq2)", "1", key="q2c")]
            else:
                coeffs2 = [st.text_input("a (Eq2)", "0", key="l2a"), st.text_input("b (Eq2)", "1", key="l2b"), st.text_input("c (Eq2)", "2", key="l2c")]

        if st.button("Find Intersection", key="solve_inter", use_container_width=True):
            import sympy as sp
            res = algebra.solve_quadratic_system(t1, coeffs1, t2, coeffs2)
            
            if isinstance(res, list) and len(res) > 0:
                 st.success(f"Solutions Found ({len(res)}):")
                 x_sym, y_sym = sp.symbols('x y')
                 
                 for i, sol in enumerate(res):
                     x_val, y_val = None, None
                     
                     if isinstance(sol, dict):
                         x_val = sol.get(x_sym)
                         y_val = sol.get(y_sym)
                     elif isinstance(sol, tuple) and len(sol) == 2:
                         x_val, y_val = sol
                     
                     if x_val is not None and y_val is not None:
                         # Format
                         st.latex(f"P_{{{i+1}}}: x = {format_res(x_val)}, \\quad y = {format_res(y_val)}")
                     else:
                         st.warning(f"Could not parse solution {i+1}: {sol}")
            elif isinstance(res, list) and len(res) == 0:
                st.info("No Real Intersection Points Found.")
            else:
                st.error(f"Error: {res}")
                
            save_log("Curve Intersection", str(res))
            
    # Advanced Higher-Degree Solver
    st.markdown("### Advanced Options")
    with st.expander("Solve Higher Degrees (3rd - 10th)"):
        st.caption("Solves equations of form: $c_n x^n + \dots + c_1 x + c_0 = 0$")
        
        # Degree Selection
        degree = st.number_input("Equation Degree", min_value=3, max_value=10, value=3)
        
        # Generic Equation Display
        latex_eq = ""
        for d in range(degree, -1, -1):
            sign = "+" if d != degree else ""
            if d > 1: latex_eq += f"{sign} c_{{{d}}} x^{{{d}}} "
            elif d == 1: latex_eq += f"{sign} c_1 x "
            else: latex_eq += f"{sign} c_0 "
        latex_eq += "= 0"
        st.latex(latex_eq)
        
        # Responsive Coefficient Inputs
        coeffs_dict = {}
        cols = st.columns(2)  # Pairs for better mobile layout
        
        for i in range(degree, -1, -1):
            col_idx = (degree - i) % 2
            with cols[col_idx]:
                 coeffs_dict[i] = st.number_input(f"c_{i} (x^{i})", value=0.0, key=f"high_deg_c_{i}", format="%.4f")

        if st.button("Calculate", key="solve_high_deg", use_container_width=True):
            res = algebra.solve_poly_high_deg(coeffs_dict)
            
            if isinstance(res, list):
                if not res:
                    st.warning("No solutions found.")
                else:
                    st.success(f"Solutions Found ({len(res)}):")
                    # Scrollable container for many results
                    with st.container(height=200):
                        for i, r in enumerate(res):
                            st.latex(f"x_{{{i+1}}} = {format_res(r)}")
            else:
                 st.error(res)
            save_log(f"Poly Deg {degree}", str(res))
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_ad_slot(position='bottom')

# 9. 🌌 Universal Solver
elif selected_module == "🌌 Universal Solver":
    render_ad_slot()
    st.header("Universal Equation Solver")
    st.info("Dynamically generate and solve systems of equations.")
    
    # Dynamic Settings
    c1, c2 = st.columns(2)
    num_vars = c1.slider("Number of Unknowns", 2, 5, 2)
    degree = c2.slider("Max Degree", 1, 10, 1)
    
    # Generate Variables
    import sympy as sp
    vars_str = ["x", "y", "z", "w", "v"][:num_vars]
    sym_vars = sp.symbols(' '.join(vars_str))
    if not isinstance(sym_vars, (list, tuple)):
        sym_vars = [sym_vars]
        
    st.write(f"Variables: {', '.join(vars_str)}")
    
    # Form to prevent re-runs
    with st.form("univ_solver_form"):
        # Dynamic Input Fields
        st.subheader("System Definitions")
        equations = []
        
        for i in range(num_vars):
            with st.expander(f"Equation {i+1}", expanded=(i==0)): # Collapse others by default for mobile
                st.caption("Enter coefficients:")
                eq_expr = 0
                
                # Stacked Layout (Simpler than grid for mobile speed)
                for j, var_sym in enumerate(sym_vars):
                    st.markdown(f"**{vars_str[j]} Terms**")
                    # Reduce columns -> Faster rendering
                    cols = st.columns(2) 
                    
                    for d in range(degree, 0, -1):
                        with cols[(degree - d) % 2]:
                            coeff = st.number_input(f"Coeff ${vars_str[j]}^{d}$", value=0.0, key=f"univ_c_{i}_{j}_{d}", format="%.4f")
                            if coeff != 0:
                                eq_expr += coeff * (var_sym**d)
                
                # Constant
                st.markdown("---")
                const = st.number_input(f"Constant (Eq {i+1})", value=0.0, key=f"univ_const_{i}", format="%.4f")
                eq_expr += const
                equations.append(eq_expr)
                
        # Submit Button
        submitted = st.form_submit_button("Calculate System", use_container_width=True)

    if submitted:
        # Show Equations Preview (Post-Submit to avoid re-run lag)
        with st.expander("Review Equations"):
            for i, eq in enumerate(equations):
                if eq != 0: st.latex(f"{sp.latex(eq)} = 0")
                else: st.caption(f"Eq {i+1}: 0 = 0")

        with st.spinner("Solving high-degree system... This may take a minute."):
            start_time = time.time()
            
            # Pure Symbolic Call (Cached)
            results = algebra.solve_general_system(equations, sym_vars)
            
            if isinstance(results, list) and results:
                st.success(f"Solutions Found ({len(results)}):")
                
                # Mobile-Optimized Result List
                with st.container(height=400):
                    for idx, sol in enumerate(results):
                        # Shaded Box for each solution set
                        st.markdown(f"""
                        <div style='background-color: #f1f3f6; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 5px solid #00E5FF;'>
                            <strong>Solution #{idx+1}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        cols = st.columns(len(sol)) if len(sol) <= 3 else st.columns(3)
                        
                        i = 0
                        for v_sym in sym_vars:
                             if v_sym in sol:
                                 # Determine value
                                 val = sol[v_sym]
                                 
                                 # Format
                                 val_disp = format_res(val)
                                 
                                 # Display in grid
                                 with cols[i % 3]:
                                     st.markdown(f"${sp.latex(v_sym)} = {val_disp}$")
                                 i += 1
                                 
            elif isinstance(results, str):
                 if "System is too complex" in results:
                     st.warning(results)
                 else:
                     st.error(results)
            elif not results:
                 st.warning("No solution found or system is inconsistent.")
            
            st.caption(f"Calculation time: {time.time() - start_time:.3f}s")
            save_log("Universal (Symbolic)", str(results))
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_ad_slot(position='bottom')

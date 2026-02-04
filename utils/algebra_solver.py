import streamlit as st

# Note: Lazy imports used inside functions for performance
# import sympy as sp

def solve_linear_1var(a, b):
    import sympy as sp
    """ Solve ax + b = 0 """
    try:
        x = sp.symbols('x')
        a_val = sp.sympify(a)
        b_val = sp.sympify(b)
        if a_val == 0:
            return "Infinite solutions" if b_val == 0 else "No solution"
        return sp.simplify(-b_val / a_val)
    except Exception as e:
        return f"Error: {str(e)}"

def solve_linear_2vars(eq1_coeffs, eq2_coeffs):
    import sympy as sp
    """ Solve linear system of 2 vars """
    try:
        x, y = sp.symbols('x y')
        a1, b1, c1 = [sp.sympify(v) for v in eq1_coeffs]
        a2, b2, c2 = [sp.sympify(v) for v in eq2_coeffs]
        eq1 = sp.Eq(a1*x + b1*y, c1)
        eq2 = sp.Eq(a2*x + b2*y, c2)
        sol = sp.solve((eq1, eq2), (x, y))
        return sol if sol else "No unique solution"
    except Exception as e:
        return f"Error: {str(e)}"

def solve_quadratic_1var(a, b, c):
    import sympy as sp
    """ Solve ax^2 + bx + c = 0 """
    try:
        x = sp.symbols('x')
        a_val, b_val, c_val = [sp.sympify(v) for v in [a, b, c]]
        if a_val == 0:
            return [solve_linear_1var(b_val, c_val)]
        sols = sp.solve(a_val*x**2 + b_val*x + c_val, x)
        return [sp.simplify(s) for s in sols]
    except Exception as e:
        return f"Error: {str(e)}"

def solve_quadratic_system(eq1_type, eq1_coeffs, eq2_type, eq2_coeffs):
    import sympy as sp
    """ Curve intersection solver """
    try:
        x, y = sp.symbols('x y')
        def build_eq(etype, coeffs):
            if etype == 'Linear (ax + by = c)':
                a, b, c_const = [sp.sympify(v) for v in coeffs]
                return sp.Eq(a*x + b*y, c_const)
            elif etype == 'Quadratic (y = ax^2 + bx + c)':
                a, b, c_const = [sp.sympify(v) for v in coeffs]
                return sp.Eq(y, a*x**2 + b*x + c_const)
            elif etype == 'Circle (x^2 + y^2 = r^2)':
                 r = sp.sympify(coeffs[0])
                 return sp.Eq(x**2 + y**2, r**2)
            return None

        eq1 = build_eq(eq1_type, eq1_coeffs)
        eq2 = build_eq(eq2_type, eq2_coeffs)
        
        return sp.solve((eq1, eq2), (x, y))
    except Exception as e:
        return f"Error: {str(e)}"

def solve_poly_high_deg(coeffs_dict):
    import sympy as sp
    """ Solve general polynomial """
    try:
        x_sym = sp.symbols('x')
        poly_expr = 0
        for deg, val in coeffs_dict.items():
            poly_expr += sp.sympify(val) * (x_sym ** deg)
        if poly_expr == 0: return "Empty Equation"
        sols = sp.solve(poly_expr, x_sym)
        return [sp.simplify(s) for s in sols]
    except Exception as e:
        return f"Error: {str(e)}"

@st.cache_data(show_spinner=False)
def solve_general_system(equations, vars_list):
    import sympy as sp
    """ 
    Solve symbolic system using pure SymPy.
    equations: list of SymPy expressions (implied = 0)
    vars_list: list of SymPy symbols
    """
    try:
        # User requested specifically: sympy.solve(equations, variables, dict=True)
        # This is more robust for general consistency than nonlinsolve
        sols = sp.solve(equations, vars_list, dict=True)
        
        # Parse results to ensure they are JSON/UI friendly
        results = []
        if isinstance(sols, list):
            for s in sols:
                # s is already a dictionary {x: val, y: val}
                res_dict = {}
                for v, val in s.items():
                    res_dict[v] = sp.simplify(val)
                results.append(res_dict)
            return results
        elif isinstance(sols, dict):
            # Single solution case
            res_dict = {}
            for v, val in sols.items():
                res_dict[v] = sp.simplify(val)
            return [res_dict]
        
        return []

    except Exception as e:
        return f"System is too complex for symbolic solution. Please simplify terms. ({str(e)})"

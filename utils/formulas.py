
# Mechanical Engineering
MECHANICAL_FORMULAS = {
    "Heat Transfer": r"Q = m \cdot c \cdot \Delta T",
    "1st Law (Closed)": r"\Delta U = Q - W",
    "Carnot Efficiency": r"\eta = 1 - \frac{T_C}{T_H}",
    "Work (Isobaric)": r"W = P \cdot \Delta V",
    "Stress": r"\sigma = \frac{F}{A}",
    "Strain": r"\epsilon = \frac{\Delta L}{L_0}"
}

# Civil Engineering
CIVIL_FORMULAS = {
    "Pressure": r"P = \frac{F}{A}",
    "Bernoulli": r"P + \frac{1}{2}\rho v^2 + \rho gh = \text{constant}",
    "Manning's Eq": r"V = \frac{k}{n} R_h^{2/3} S^{1/2}",
    "Beam Deflection (Max)": r"\delta_{max} = \frac{5wL^4}{384EI}"
}

# Chemical Engineering
CHEMICAL_FORMULAS = {
    "Ideal Gas Law": r"PV = nRT",
    "Boyle's Law": r"P_1 V_1 = P_2 V_2",
    "Charles's Law": r"\frac{V_1}{T_1} = \frac{V_2}{T_2}",
    "Mass Balance": r"\text{Input} - \text{Output} + \text{Gen} - \text{Cons} = \text{Accumulation}",
    "Arrhenius Eq": r"k = A e^{-E_a/RT}"
}

# Electrical Engineering
ELECTRICAL_FORMULAS = {
    "Ohm's Law": r"V = I \cdot R",
    "Power (DC)": r"P = V \cdot I = I^2 R = \frac{V^2}{R}",
    "Capacitance": r"C = \frac{Q}{V}",
    "Inductance": r"V = L \frac{di}{dt}",
    "Kirchhoff's Current": r"\sum I_{in} = \sum I_{out}"
}

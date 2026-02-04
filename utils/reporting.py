
import pandas as pd
import io

def generate_csv_report(history):
    """
    Generate a CSV string from the session history.
    history: List of dictionaries [{'timestamp': ..., 'calculation': ..., 'result': ...}]
    """
    if not history:
        return ""
    
    df = pd.DataFrame(history)
    return df.to_csv(index=False)

def generate_txt_report(history):
    """
    Generate a TXT string from the session history.
    """
    if not history:
        return "No calculations performed."
        
    report = "APPATY Session Report\n=====================\n\n"
    for item in history:
        report += f"[{item['timestamp']}] {item['calculation']} = {item['result']}\n"
    return report

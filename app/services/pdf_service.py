import pdfplumber
import re
from typing import Dict, List, Any
from datetime import datetime

def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from PDF"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_tables_from_pdf(file_path: str) -> List[List]:
    """Extract tables from PDF"""
    tables = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
    return tables

def find_amounts(text: str) -> List[float]:
    """Find money amounts in text"""
    # Matches: 1,234.56 | 1234.56 | Rs 5000 | 5000.00
    patterns = [
        r'(?:Rs\.?|PKR|USD|\$)\s*([0-9,]+\.?\d*)',
        r'([0-9]{1,3}(?:,[0-9]{3})+(?:\.\d{2})?)',
        r'([0-9]+\.\d{2})'
    ]
    amounts = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            try:
                val = float(m.replace(",", ""))
                if 10 <= val <= 10000000:  # reasonable range
                    amounts.append(val)
            except:
                pass
    return list(set(amounts))

def find_account_numbers(text: str) -> List[str]:
    """Find possible account numbers"""
    patterns = [
        r'\bPK\d{10,14}\b',
        r'\b\d{10,16}\b',
        r'Account\s*(?:No|Number|#)?[:\s]*([A-Z0-9]{8,20})'
    ]
    accounts = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        accounts.extend(matches)
    return list(set(accounts))[:10]

def find_names(text: str) -> List[str]:
    """Find possible person names (simple heuristic)"""
    # Lines that look like names
    names = []
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        # Simple: 2-4 capitalized words
        if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}$', line):
            if len(line) > 5 and len(line) < 40:
                names.append(line)
    return list(set(names))[:8]

def find_dates(text: str) -> List[str]:
    """Find dates"""
    patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b'
    ]
    dates = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        dates.extend(matches)
    return list(set(dates))[:15]

def detect_suspicious_patterns(amounts: List[float], text: str) -> List[str]:
    """Detect possible fraud / suspicious signals from PDF"""
    alerts = []
    text_lower = text.lower()

    if amounts:
        max_amt = max(amounts)
        if max_amt >= 100000:
            alerts.append(f"High value amount found: Rs {max_amt:,.0f}")
        large = [a for a in amounts if a >= 50000]
        if len(large) >= 3:
            alerts.append(f"Multiple large transactions ({len(large)}) detected")

    keywords = ["fraud", "block", "blocked", "suspicious", "chargeback", "dispute", "unauthorized"]
    for kw in keywords:
        if kw in text_lower:
            alerts.append(f"Keyword found in document: '{kw}'")

    return alerts

def analyze_pdf(file_path: str) -> Dict[str, Any]:
    """Complete PDF analysis"""
    text = extract_text_from_pdf(file_path)
    tables = extract_tables_from_pdf(file_path)
    amounts = find_amounts(text)
    accounts = find_account_numbers(text)
    names = find_names(text)
    dates = find_dates(text)
    alerts = detect_suspicious_patterns(amounts, text)

    summary = {
        "total_characters": len(text),
        "total_pages_text_length": len(text.split("\n")),
        "tables_found": len(tables),
        "amounts_found": len(amounts),
        "max_amount": max(amounts) if amounts else 0,
        "total_amount_sum": round(sum(amounts), 2) if amounts else 0,
        "accounts_found": accounts,
        "possible_names": names,
        "dates_found": dates,
        "suspicious_alerts": alerts,
        "preview_text": text[:800] + ("..." if len(text) > 800 else ""),
        "full_text": text
    }
    return summary
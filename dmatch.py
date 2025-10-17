import pandas as pd
import random
from datetime import datetime, timedelta
import uuid

columns = [
    "PROVIDER_ID", "RFRNC_DLR_NB", "VIN_ID", "RPR_ORDR_NB", "RPR_ORDR_OPN_DT", "DBS_RO_CRTE_TS", "DBS_RO_UPDT_TS",
    "DBS_RPR_ORDR_KY", "DBS_RPR_ORDR_LN_KY", "ADAM_DMS_OPRTN_PYMNT_TYP_CD", "DBS_PAY_TYP_CD",
    "ADAM_DMS_OPRTN_PYMNT_TYP_CD_vs_DBS_PAY_TYP_CD", "ADAM_DLR_OPRTN_CD", "DBS_DLR_OPRTN_CD", "DBS_FLAT_RT_MNL_CD",
    "ADAM_DLR_OPRTN_CD_vs_DBS_DLR_OPRTN_CD", "ADAM_DLR_OPRTN_CD_vs_DBS_FLAT_RT_MNL_CD", "OPRTN_CD_MATCH_FIELD",
    "ADAM_RPR_ORDR_LN_NB", "DBS_RPR_ORDR_LN_NB", "DBS_DLR_OPRTN_CD", "ADAM_DLR_OPRTN_CD",
    "ADAM_DLR_OPRTN_CD_vs_DBS_DLR_OPRTN_CD", "similarity_score", "DBS_FLAT_RT_MNL_CD", "ADAM_DLR_OPRTN_CD",
    "ADAM_DLR_OPRTN_CD_vs_DBS_FLAT_RT_MNL_CD", "similarity_score", "DBS_DLR_OPRTN_DS", "ADAM_DLR_OPRTN_DS",
    "ADAM_DLR_OPRTN_DS_vs_DBS_DLR_OPRTN_DS", "similarity_score", "DBS_LBR_DS", "ADAM_DLR_OPRTN_DS",
    "ADAM_DLR_OPRTN_DS_vs_DBS_LBR_DS", "similarity_score", "DBS_JOB_LBR_PRC_AM", "ADAM_OPRTN_LBR_PRC_AM",
    "ADAM_OPRTN_LBR_PRC_AM_vs_DBS_JOB_LBR_PRC_AM", "DBS_LBR_PRC_AM", "ADAM_OPRTN_LBR_PRC_AM",
    "ADAM_OPRTN_LBR_PRC_AM_vs_DBS_LBR_PRC_AM", "DBS_JOB_MSCLNS_PRC_AM", "ADAM_OPRTN_MSCLNS_PRC_AM",
    "ADAM_OPRTN_MSCLNS_PRC_AM_vs_DBS_JOB_MSCLNS_PRC_AM", "DBS_MSCLNS_PRC_AM", "ADAM_OPRTN_MSCLNS_PRC_AM",
    "ADAM_OPRTN_MSCLNS_PRC_AM_vs_DBS_MSCLNS_PRC_AM", "DBS_JOB_PRT_PRC_AM", "ADAM_OPRTN_PRT_PRC_AM",
    "ADAM_OPRTN_PRT_PRC_AM_vs_DBS_JOB_PRT_PRC_AM", "DBS_OPRTN_PRTS_PRC_AM", "ADAM_OPRTN_PRT_PRC_AM",
    "ADAM_OPRTN_PRT_PRC_AM_vs_DBS_OPRTN_PRTS_PRC_AM", "DBS_JOB_HR_CN", "ADAM_OPRTN_ACTL_LBR_HR_NB",
    "ADAM_OPRTN_ACTL_LBR_HR_NB_vs_DBS_JOB_HR_CN", "DBS_RQSTD_LBR_FLAT_HR_NB", "ADAM_OPRTN_ACTL_LBR_HR_NB",
    "ADAM_OPRTN_ACTL_LBR_HR_NB_vs_DBS_RQSTD_LBR_FLAT_HR_NB"
]

def random_date(start_year=2020, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

def generate_row(index):
    vin = f"1HGCM82633A{random.randint(100000, 999999)}"
    dealer_code = f"D{random.randint(1000,9999)}"
    price = lambda: round(random.uniform(50, 1500), 2)
    hours = lambda: round(random.uniform(0.5, 10.0), 2)
    score = lambda: round(random.uniform(0.6, 1.0), 2)

    row = {
        "PROVIDER_ID": f"PROV{1000 + index}",
        "RFRNC_DLR_NB": dealer_code,
        "VIN_ID": vin,
        "RPR_ORDR_NB": f"RO{random.randint(100000,999999)}",
        "RPR_ORDR_OPN_DT": random_date(),
        "DBS_RO_CRTE_TS": random_date(),
        "DBS_RO_UPDT_TS": random_date(),
        "DBS_RPR_ORDR_KY": str(uuid.uuid4())[:8],
        "DBS_RPR_ORDR_LN_KY": str(uuid.uuid4())[:8],
        "ADAM_DMS_OPRTN_PYMNT_TYP_CD": "CC",
        "DBS_PAY_TYP_CD": "Credit",
        "ADAM_DMS_OPRTN_PYMNT_TYP_CD_vs_DBS_PAY_TYP_CD": "Match",
        "ADAM_DLR_OPRTN_CD": f"OP{random.randint(100, 999)}",
        "DBS_DLR_OPRTN_CD": f"OP{random.randint(100, 999)}",
        "DBS_FLAT_RT_MNL_CD": f"MNL{random.randint(1, 99)}",
        "ADAM_DLR_OPRTN_CD_vs_DBS_DLR_OPRTN_CD": "Partial Match",
        "ADAM_DLR_OPRTN_CD_vs_DBS_FLAT_RT_MNL_CD": "Mismatch",
        "OPRTN_CD_MATCH_FIELD": random.choice(["Yes", "No"]),
        "ADAM_RPR_ORDR_LN_NB": f"LN{random.randint(100, 999)}",
        "DBS_RPR_ORDR_LN_NB": f"LN{random.randint(100, 999)}",
        "DBS_DLR_OPRTN_CD": f"OP{random.randint(100, 999)}",
        "ADAM_DLR_OPRTN_CD": f"OP{random.randint(100, 999)}",
        "ADAM_DLR_OPRTN_CD_vs_DBS_DLR_OPRTN_CD": "Match",
        "similarity_score": score(),
        "DBS_FLAT_RT_MNL_CD": f"MNL{random.randint(1, 99)}",
        "ADAM_DLR_OPRTN_CD": f"OP{random.randint(100, 999)}",
        "ADAM_DLR_OPRTN_CD_vs_DBS_FLAT_RT_MNL_CD": "Mismatch",
        "similarity_score": score(),
        "DBS_DLR_OPRTN_DS": "Brake Replacement",
        "ADAM_DLR_OPRTN_DS": "Brake Rplcmnt",
        "ADAM_DLR_OPRTN_DS_vs_DBS_DLR_OPRTN_DS": "High Semantic Match",
        "similarity_score": score(),
        "DBS_LBR_DS": "Labor Description",
        "ADAM_DLR_OPRTN_DS": "Labor Desc",
        "ADAM_DLR_OPRTN_DS_vs_DBS_LBR_DS": "Partial Match",
        "similarity_score": score(),
        "DBS_JOB_LBR_PRC_AM": price(),
        "ADAM_OPRTN_LBR_PRC_AM": price(),
        "ADAM_OPRTN_LBR_PRC_AM_vs_DBS_JOB_LBR_PRC_AM": "Close",
        "DBS_LBR_PRC_AM": price(),
        "ADAM_OPRTN_LBR_PRC_AM": price(),
        "ADAM_OPRTN_LBR_PRC_AM_vs_DBS_LBR_PRC_AM": "Mismatch",
        "DBS_JOB_MSCLNS_PRC_AM": price(),
        "ADAM_OPRTN_MSCLNS_PRC_AM": price(),
        "ADAM_OPRTN_MSCLNS_PRC_AM_vs_DBS_JOB_MSCLNS_PRC_AM": "Match",
        "DBS_MSCLNS_PRC_AM": price(),
        "ADAM_OPRTN_MSCLNS_PRC_AM": price(),
        "ADAM_OPRTN_MSCLNS_PRC_AM_vs_DBS_MSCLNS_PRC_AM": "Partial",
        "DBS_JOB_PRT_PRC_AM": price(),
        "ADAM_OPRTN_PRT_PRC_AM": price(),
        "ADAM_OPRTN_PRT_PRC_AM_vs_DBS_JOB_PRT_PRC_AM": "Match",
        "DBS_OPRTN_PRTS_PRC_AM": price(),
        "ADAM_OPRTN_PRT_PRC_AM": price(),
        "ADAM_OPRTN_PRT_PRC_AM_vs_DBS_OPRTN_PRTS_PRC_AM": "Partial Match",
        "DBS_JOB_HR_CN": hours(),
        "ADAM_OPRTN_ACTL_LBR_HR_NB": hours(),
        "ADAM_OPRTN_ACTL_LBR_HR_NB_vs_DBS_JOB_HR_CN": "Close",
        "DBS_RQSTD_LBR_FLAT_HR_NB": hours(),
        "ADAM_OPRTN_ACTL_LBR_HR_NB": hours(),
        "ADAM_OPRTN_ACTL_LBR_HR_NB_vs_DBS_RQSTD_LBR_FLAT_HR_NB": "Match"
    }
    return row

df = pd.DataFrame([generate_row(i) for i in range(100)])

file_path = "car_repair_synthetic_data.csv"
df.to_csv(file_path, index=False)
file_path
 

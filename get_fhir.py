mport requests
import json
import time

# ====== 設定區 ======

# FHIR伺服器URL
FHIR_BASE_URL = "https://hapi.fhir.org/baseR4"

# 查詢的資源類型
RESOURCE_TYPE = "Patient"

# 假設你有一個病人ID清單
patient_ids = [
    "example",    # HAPI Server內建的example病人
    "1798670",    # 其他測試ID，可以換成你的ID
    "1798671"
]

# 是否需要認證 (如果要，加在headers)
headers = {
    "Accept": "application/fhir+json"
    # "Authorization": "Bearer <你的Token>"  # 如果FHIR伺服器有認證需求
}

# 設定每次請求間的延遲，避免伺服器被打爆（可選）
DELAY_BETWEEN_REQUESTS = 1  # 秒

# ====== 工具函式 ======

def fetch_patient_data(patient_id):
    """查詢單一病人資料"""
    url = f"{FHIR_BASE_URL}/{RESOURCE_TYPE}/{patient_id}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[警告] 查詢病人ID {patient_id} 失敗，狀態碼：{response.status_code}")
            return None
    except Exception as e:
        print(f"[錯誤] 查詢病人ID {patient_id} 時發生錯誤：{str(e)}")
        return None

def save_patient_data(patient_id, data):
    """將查到的病人資料儲存成JSON檔案"""
    filename = f"patient_{patient_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ 病人ID {patient_id} 資料已儲存為 {filename}")

# ====== 主程式 ======

def main():
    print("🚀 開始批量查詢FHIR病人資料...\n")
    for patient_id in patient_ids:
        print(f"🔍 查詢病人ID: {patient_id}")
        data = fetch_patient_data(patient_id)
        if data:
            save_patient_data(patient_id, data)
        time.sleep(DELAY_BETWEEN_REQUESTS)  # 小延遲，友善伺服器
    print("\n🎯 所有病人資料查詢完畢！")

if __name__ == "__main__":
    main()


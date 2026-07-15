import pandas as pd
import pulp
import random
import sys
import io
import itertools
import math

# Fix encoding cho tiếng Việt trên Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# =====================================================================
# 6. DATA PREPROCESSING (Đọc file thật & Sinh dữ liệu)
# =====================================================================
def preprocess_real_data(csv_file_path):
    print("Đang đọc dữ liệu từ file Baseline...")
    
    try:
        df = pd.read_excel(csv_file_path)
    except Exception as e:
        print(f"Lỗi đọc file: {e}")
        return None
    
    print("Các cột có trong file dữ liệu của bạn là:", df.columns.tolist())
    
    # ⚠️ BẠN CẦN SỬA CÁC TÊN CỘT NÀY SAU KHI XEM DÒNG PRINT Ở TRÊN ⚠️
    COL_STAFF = 'MS của CÁN BỘ COI THI'  # Mã cán bộ
    COL_SHIFT = 'MS Ca thi'               # Mã ca thi
    COL_CAMPUS = 'Cơ sở'                  # Cơ sở
    COL_DATE = 'Ngày'                     # Ngày thi
    COL_TIME = 'GIỜ'                      # Giờ thi

    # 1. Tập hợp I và J
    I = df[COL_STAFF].dropna().unique().tolist()
    J = df[COL_SHIFT].dropna().unique().tolist()
    
    print(f"Tổng số cán bộ (I): {len(I)}")
    print(f"Tổng số ca thi (J): {len(J)}")

    # 2. Tính Demand
    demand = df.groupby(COL_SHIFT)[COL_STAFF].count().to_dict()

    # 3. Tìm ca thi trùng lịch
    overlapping_shifts = []
    grouped_time = df.groupby([COL_DATE, COL_TIME])[COL_SHIFT].unique()
    for shifts in grouped_time:
        if len(shifts) > 1:
            overlapping_shifts.extend(list(itertools.combinations(shifts, 2)))

    # 4. Sinh Preferences và Penalty
    staff_groups = {}
    random.seed(42) 
    for i in I:
        staff_groups[i] = random.choice(['CS1_Pref', 'CS2_Pref', 'Balanced'])

    shift_campus = df.set_index(COL_SHIFT)[COL_CAMPUS].to_dict()

    penalty = {}
    for i in I:
        penalty[i] = {}
        for j in J:
            campus = str(shift_campus[j]).upper() 
            if staff_groups[i] == 'Balanced':
                penalty[i][j] = 1
            elif staff_groups[i] == 'CS1_Pref':
                penalty[i][j] = 0 if '1' in campus else 2
            elif staff_groups[i] == 'CS2_Pref':
                penalty[i][j] = 0 if '2' in campus else 2
            else:
                penalty[i][j] = 1 

    # 5. Availability và Max Load
    availability = {i: {j: 1 for j in J} for i in I}

    # Tự động tính max_load dựa trên tổng demand và số cán bộ
    total_demand = sum(demand.values())
    avg_load = total_demand / len(I)
    # Cộng thêm 30% dự phòng và làm tròn lên để đảm bảo feasible
    auto_max_load = math.ceil(avg_load * 1.3)
    max_load = {i: auto_max_load for i in I}

    print(f"\n--- Thông tin chẩn đoán ---")
    print(f"  Tổng demand (tổng lượt coi thi cần phân): {total_demand}")
    print(f"  Số cán bộ: {len(I)}, Số ca thi: {len(J)}")
    print(f"  Tải trung bình mỗi người: {avg_load:.1f} ca")
    print(f"  Max load tự động (avg * 1.3, làm tròn lên): {auto_max_load} ca/người")
    print(f"  Tổng capacity: {len(I)} × {auto_max_load} = {len(I) * auto_max_load}")
    print(f"  Số cặp ca trùng lịch: {len(overlapping_shifts)}")
    print("Tiền xử lý dữ liệu hoàn tất!\n" + "-"*40)
    return I, J, demand, overlapping_shifts, availability, max_load, penalty


# =====================================================================
# 7. SOLVER IMPLEMENTATION (Giải bằng PuLP)
# =====================================================================
def solve_iap_model(I, J, demand, overlapping_shifts, availability, max_load, penalty):
    prob = pulp.LpProblem("Invigilator_Assignment_Problem", pulp.LpMinimize)
    
    x = pulp.LpVariable.dicts("x", ((i, j) for i in I for j in J), cat='Binary')
    w_max = pulp.LpVariable("w_max", lowBound=0, cat='Integer')
    w_min = pulp.LpVariable("w_min", lowBound=0, cat='Integer')
    
    w = {i: pulp.lpSum(x[i, j] for j in J) for i in I}

    # Hàm mục tiêu
    alpha = 1.0  
    beta = 2.0   
    total_penalty = pulp.lpSum(penalty[i][j] * x[i, j] for i in I for j in J)
    fairness_penalty = w_max - w_min
    prob += (alpha * total_penalty + beta * fairness_penalty), "Total_Cost"
    
    # Ràng buộc
    for j in J:
        prob += pulp.lpSum(x[i, j] for i in I) == demand[j], f"Demand_{j}"
        
    for i in I:
        for j in J:
            prob += x[i, j] <= availability[i][j], f"Avail_{i}_{j}"
            
    for i in I:
        for (j1, j2) in overlapping_shifts:
            prob += x[i, j1] + x[i, j2] <= 1, f"Overlap_{i}_{j1}_{j2}"
            
    for i in I:
        prob += w[i] <= max_load[i], f"MaxLoad_{i}"
        
    for i in I:
        prob += w[i] <= w_max, f"W_Max_Bound_{i}"
        prob += w[i] >= w_min, f"W_Min_Bound_{i}"

    print("Bắt đầu giải bài toán với dữ liệu thực tế...")
    prob.solve(pulp.PULP_CBC_CMD(msg=0))  # msg=0 để tắt log CBC
    
    print(f"Trạng thái bộ giải: {pulp.LpStatus[prob.status]}")
    
    if pulp.LpStatus[prob.status] == 'Optimal':
        print(f"Giá trị hàm mục tiêu tối ưu: {pulp.value(prob.objective):.2f}")
        print(f"Max Workload: {int(pulp.value(w_max))}, Min Workload: {int(pulp.value(w_min))}")
        
        # In lịch phân công chi tiết
        print("\n" + "="*60)
        print("               LỊCH PHÂN CÔNG CHI TIẾT")
        print("="*60)
        for j in J:
            assigned = [i for i in I if pulp.value(x[i, j]) == 1]
            print(f"\nCa thi {j} (Cần {demand[j]}): {assigned}")
        
        # In khối lượng công việc mỗi người
        print("\n" + "="*60)
        print("            KHỐI LƯỢNG CÔNG VIỆC MỖI NGƯỜI")
        print("="*60)
        workloads = []
        for i in I:
            wi = int(pulp.value(w[i]))
            workloads.append((i, wi))
        workloads.sort(key=lambda x: x[1], reverse=True)
        for staff, wl in workloads:
            bar = '█' * wl
            print(f"  {staff}: {wl:2d} ca  {bar}")
    else:
        print("Không tìm thấy nghiệm (Infeasible). Hãy kiểm tra lại max_load hoặc nới lỏng ràng buộc!")


# =====================================================================
# CHẠY CHƯƠNG TRÌNH CHÍNH
# =====================================================================
if __name__ == "__main__":
    # ĐIỀN TÊN FILE CSV CỦA BẠN VÀO ĐÂY (nhớ để cùng thư mục với file Python)
    csv_path = "Dataset_Anonymized_Invigilator_Assignment_Problem.xlsx"
    
    # Bước 1: Xử lý dữ liệu
    data = preprocess_real_data(csv_path)
    
    # Bước 2: Bỏ dữ liệu vào bộ giải
    if data:
        I, J, demand, overlapping_shifts, availability, max_load, penalty = data
        solve_iap_model(I, J, demand, overlapping_shifts, availability, max_load, penalty)
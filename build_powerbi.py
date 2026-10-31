import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
# -*- coding: utf-8 -*-
# Build Power BI DataModel & Dashboard 2026
# Tự động quét và tổng hợp dữ liệu toàn bộ Folder:
# - Đã xóa toàn bộ tên công ty (BSV, Bông Sen Vàng -> Doanh nghiệp / Công ty / Nội bộ)
# - Đã ẩn danh danh tính nhân sự (Nhân sự A, B, C...)
# - Bộ lọc tương tác đa chiều đồng bộ biểu đồ + bảng + tự động chuyển tab hiển thị

import os
import re
import json
import base64
import webbrowser
import pandas as pd
import openpyxl

def clean_text(val):
    if val is None:
        return ""
    text = str(val).strip()
    text = re.sub(r'BÔNG\s*SEN\s*VÀNG|Bông\s*Sen\s*Vàng', 'Công ty', text, flags=re.IGNORECASE)
    text = re.sub(r'\bBSV\b', 'Công ty', text)
    text = re.sub(r'\[BSV\]\s*-?\s*', '', text)
    return text

SRC_FILE_STRATEGY = "260401_CL_MT_SDTC-MTCV-KPI - BP BIM_TK.xlsx"
SRC_FILE_TASKS = "Báo cáo công việc.xlsx"
if not os.path.exists(SRC_FILE_TASKS):
    SRC_FILE_TASKS = "[BSV] - Báo cáo công việc.xlsx"

OUT_XLSX = "BIM_TK_PowerBI_DataModel_2026.xlsx"
OUT_HTML = "index.html"
OUT_HTML_DASHBOARD = "BIM_TK_PowerBI_Dashboard_2026.html"

if not os.path.exists(SRC_FILE_STRATEGY):
    raise FileNotFoundError(f"Vui lòng đặt file '{SRC_FILE_STRATEGY}' cùng thư mục với script này!")

wb_src = openpyxl.load_workbook(SRC_FILE_STRATEGY, data_only=True)

# 1. Bảng Định biên Nhân sự (02_Fact_NhanSu)
nhan_su_nhom = [
    ("GRP_MGT", "Quản lý điều hành", "Trưởng bộ phận BIM - Thiết kế", "Trưởng bộ phận BIM - TK", "Quản lý", 1, 1, 0, "Đang làm việc"),
    ("GRP_TK_BIM_KC", "Thiết kế & BIM Kết cấu", "Lead Bộ môn Kết cấu", "Lead Bộ môn Kết cấu", "Lead Bộ Môn", 2, 2, 0, "Đang làm việc"),
    ("GRP_TK_BIM_KC", "Thiết kế & BIM Kết cấu", "Kỹ sư TK Kết cấu & Kỹ sư BIM KC", "2 KS Thiết kế & 3 KS BIM Kết cấu", "Nhân viên", 6, 5, 0, "Đã chia đều 3 KS BIM về bộ môn"),
    ("GRP_TK_BIM_KT", "Thiết kế & BIM Kiến trúc", "Lead Bộ môn Kiến trúc", "Lead Bộ môn Kiến trúc", "Lead Bộ Môn", 1, 1, 0, "Đang làm việc"),
    ("GRP_TK_BIM_KT", "Thiết kế & BIM Kiến trúc", "KTS Triển khai & Kỹ sư BIM Kiến trúc", "1 KTS Thiết kế & 3 KS BIM Kiến trúc", "Nhân viên", 5, 4, 1, "Đã chia đều 3 KS BIM về bộ môn"),
    ("GRP_TK_BIM_MEP", "Thiết kế & BIM Cơ điện (MEPF)", "Lead BIM MEPF", "Lead Bộ môn BIM MEPF", "Lead Bộ Môn", 2, 2, 0, "Đang làm việc"),
    ("GRP_TK_BIM_MEP", "Thiết kế & BIM Cơ điện (MEPF)", "Kỹ sư TK Cơ Điện & Kỹ sư BIM MEP", "1 KS TK + 1 KS MEP + 3 KS BIM MEP", "Nhân viên", 5, 5, 0, "Đã chia đều 3 KS BIM về bộ môn"),
    ("GRP_TK_BIM_HVAC", "Thiết kế & BIM HVAC", "Lead Bộ môn HVAC", "Lead Bộ môn HVAC", "Lead Bộ Môn", 1, 1, 0, "Đang làm việc"),
    ("GRP_TK_BIM_HVAC", "Thiết kế & BIM HVAC", "Kỹ sư TK HVAC & Triển khai", "1 KS Triển khai HVAC", "Nhân viên", 2, 1, 0, "Đang làm việc"),
    ("GRP_BIM_HT", "BIM Hạ tầng & CDE", "Lead BIM Hạ tầng & Quản trị CDE", "Lead Kỹ thuật Hạ tầng & CDE", "Lead Bộ Môn", 2, 1, 0, "Đang làm việc"),
    ("GRP_BIM_HT", "BIM Hạ tầng & CDE", "Kỹ sư BIM Hạ tầng & CDE", "2 KS BIM Hạ tầng & CDE", "Nhân viên", 3, 3, 1, "Đã chia đều 2 KS BIM về bộ môn")
]
df_hr = pd.DataFrame(nhan_su_nhom, columns=[
    "MaNhom", "TenNhom", "ViTri", "NhanSuChuChot", "CapBac",
    "DinhBienKeHoach", "NhanSuHienTai_T04_2026", "NghiViec_T04_2026", "GhiChuTrangThai"
])
df_hr["NhanSuConLai"] = df_hr["NhanSuHienTai_T04_2026"] - df_hr["NghiViec_T04_2026"]
df_hr["ThieuHutDinhBien"] = df_hr["DinhBienKeHoach"] - df_hr["NhanSuConLai"]
df_hr["TiLeLapDay"] = (df_hr["NhanSuConLai"] / df_hr["DinhBienKeHoach"]).round(4)

# 2. Bảng Ma trận RACI Unpivot (03_Fact_RACI)
ws_raci = wb_src['Ma Tran BP BIM']
people_cols = {
    4: ("Trưởng bộ phận BIM - TK", "Ban Quản lý", "Quản lý"),
    5: ("Lead BIM Kiến Trúc", "BIM Kiến Trúc", "Leader"),
    6: ("Kỹ sư BIM Kiến Trúc 1", "BIM Kiến Trúc", "Nhân viên"),
    7: ("Kỹ sư BIM Kiến Trúc 2", "BIM Kiến Trúc", "Nhân viên"),
    8: ("Kỹ sư BIM Kết Cấu 1", "BIM Kết Cấu", "Nhân viên"),
    9: ("Kỹ sư BIM Kết Cấu 2", "BIM Kết Cấu", "Nhân viên"),
    10: ("Lead BIM MEPF", "BIM MEPF", "Leader"),
    11: ("Kỹ sư BIM MEPF", "BIM MEPF", "Nhân viên"),
    12: ("Kỹ sư BIM Hạ Tầng & CDE", "BIM Hạ Tầng", "Nhân viên"),
}
raci_rows, current_cat_id, current_cat_name = [], "", ""
for r in range(4, 44):
    code, task = ws_raci.cell(r, 2).value, ws_raci.cell(r, 3).value
    if code is not None and task is not None:
        code_str, task_str = str(code).strip(), clean_text(task)
        if "." not in code_str:
            current_cat_id, current_cat_name = code_str, task_str
        else:
            for c_idx, (person, dept, level) in people_cols.items():
                role = ws_raci.cell(r, c_idx).value
                if role is not None and str(role).strip() != "":
                    role_str = str(role).strip()
                    role_desc = {
                        "R": "Responsible (Trực tiếp thực hiện)",
                        "A": "Accountable (Chịu trách nhiệm cuối)",
                        "C": "Consulted (Tham vấn)",
                        "I": "Informed (Được thông báo)",
                        "S": "Support (Hỗ trợ)"
                    }.get(role_str, role_str)
                    raci_rows.append((f"NV_{code_str}", current_cat_id, current_cat_name, code_str, task_str, person, dept, level, role_str, role_desc))

df_raci = pd.DataFrame(raci_rows, columns=[
    "MaGiaoDich", "MaNhomNhiemVu", "NhomNhiemVu", "MaNhiemVu", "TenNhiemVu",
    "HoTenNhanSu", "BoMon", "CapBac", "VaiTro_RACI", "MoTaVaiTro"
])

# 3. Bảng 115 Tài liệu Chuẩn hóa Thiết kế (05_Fact_TaiLieuTK)
ht_sheets = {
    "HT_ThietKe_KC": ("KC", "Thiết kế Kết cấu", "Lead Kết Cấu"),
    "HT_ThietKe_KT": ("KT", "Thiết kế Kiến trúc", "Lead Kiến Trúc"),
    "HT_ThietKe_Dien": ("DIEN", "Thiết kế Điện", "Lead Điện"),
    "HT_ThietKe_HVAC": ("HVAC", "Thiết kế HVAC", "Lead HVAC"),
    "HT_ThietKe_CTN": ("CTN", "Thiết kế Cấp thoát nước", "Lead Cấp Thoát Nước"),
    "HT_ThietKe_PCCC": ("PCCC", "Thiết kế PCCC", "Lead PCCC"),
}
doc_rows = []
for sh_name, (bm_code, bm_name, chu_tri) in ht_sheets.items():
    ws = wb_src[sh_name]
    for r in range(2, ws.max_row + 1):
        stt, doc_name, req, purpose = ws.cell(r, 1).value, ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 4).value
        if stt is not None and doc_name is not None:
            stt_int, doc_str = int(float(stt)), clean_text(doc_name)
            if bm_code == "KC" and "HVAC" in doc_str:
                doc_str = doc_str.replace("HVAC", "Kết cấu")
            audit_note = "Bình thường"
            req_str = clean_text(req) if req is not None else "Theo tiêu chuẩn chung nội bộ"
            req_str_clean = req_str.replace("Lam sẽ gửi", "Nhân sự A sẽ gửi").replace("Lam", "Nhân sự A")
            purp_str = clean_text(purpose) if purpose is not None else "Đồng bộ và tối ưu hóa hệ thống thiết kế - thi công"
            status, pct = ("Đã có dự thảo (Cần tinh chỉnh)", 0.70) if "Đã làm" in req_str else (
                          ("Giai đoạn 2 (Sau dự án mẫu)", 0.10) if ("Sẽ viết sau" in req_str or "làm sau" in req_str) else (
                          ("Đang tổng hợp tài liệu nguồn", 0.40) if ("Nhân sự A sẽ gửi" in req_str_clean or "tham khảo" in req_str.lower() or "Lam" in req_str) else
                          ("Giai đoạn 1 (Ưu tiên xây dựng)", 0.25)))
            doc_lower = doc_str.lower()
            doc_type, prio = ("Template (Revit / CAD / Tính toán)", "P1 - Tối ưu & Tự động hóa") if "template" in doc_lower else (
                             ("Quy chuẩn Mã hóa & Danh mục gốc", "P1 - Nền tảng dữ liệu") if any(k in doc_lower for k in ["quy định", "phân loại", "danh mục"]) else (
                             ("Quy trình (SOP) & Hướng dẫn", "P2 - Chuẩn hóa vận hành") if any(k in doc_lower for k in ["quy trình", "hướng dẫn"]) else (
                             ("Tự động hóa, BOQ & Module hóa", "P1 - Đòn bẩy hiệu suất 70%") if any(k in doc_lower for k in ["boq", "tự động hoá", "chuẩn hoá thiết kế"]) else
                             ("Biểu mẫu, Checklist & Thuyết minh", "P2 - Kiểm soát chất lượng"))))
            doc_rows.append((f"{bm_code}_{stt_int:02d}", bm_code, bm_name, chu_tri, stt_int, doc_str, doc_type, prio, status, pct, req_str_clean, purp_str, audit_note))

df_docs = pd.DataFrame(doc_rows, columns=[
    "MaTaiLieu", "MaBoMon", "TenBoMon", "LeadPhuTrach", "STT", "TenTaiLieu",
    "NhomTaiLieu", "MucDoUuTien", "TrangThaiTrienKhai", "TiLeHoanThanh_UocTinh",
    "MoTaYeuCau", "MucDichChienLuoc", "GhiChuRasoát"
])

# 4. Bảng Quy trình SLA (04_Fact_QuyTrinhSLA)
sla_rows = [
    ("QT_SHOP", "Quy trình BIM Shop Drawing", 1, "Chuẩn bị", "Tiếp nhận hồ sơ, đọc hiểu, chuẩn bị CSDL, đặt mục tiêu, lập biểu TCQ", "Leader Shop XD & MEPF", 0.5, 0.5, 0.5),
    ("QT_SHOP", "Quy trình BIM Shop Drawing", 2, "Hoạch định", "Lập danh mục hạng mục cần triển khai, phân bổ nguồn lực, giao deadline", "Leader Shop XD & MEPF", 0.5, 0.5, 0.5),
    ("QT_SHOP", "Quy trình BIM Shop Drawing", 3, "Kế hoạch chi tiết", "Lập danh mục bản vẽ chi tiết, deadline hoàn thành phù hợp hoạch định", "KS/KTS BIM Shop (HT, KC, KT, Cơ, Điện)", 0.5, 0.5, 0.5),
    ("QT_SHOP", "Quy trình BIM Shop Drawing", 4, "Thực thi", "Triển khai bản vẽ theo tài liệu hướng dẫn hoặc hướng dẫn của Leader", "KS/KTS BIM Shop (HT, KC, KT, Cơ, Điện)", 1.0, 5.0, 3.0),
    ("QT_SHOP", "Quy trình BIM Shop Drawing", 5, "Kiểm soát chất lượng", "Tự kiểm tra theo checklist, Spec; Leader & TBP kiểm tra", "KS BIM Shop & Leader", 0.5, 0.5, 0.5),
    ("QT_SHOP", "Quy trình BIM Shop Drawing", 6, "Phát hành", "Phát hành bản vẽ cho BCH trình CĐT/TVGS, nhận phản hồi, họp giải trình", "Leader Shop XD & MEPF", 1.0, 1.0, 1.0),
    ("QT_SHOP", "Quy trình BIM Shop Drawing", 7, "Kết thúc", "Lưu trữ hồ sơ, bổ sung lỗi hay gặp vào tài liệu nội bộ để đào tạo", "Leader Shop XD & MEPF", 0.1, 0.1, 0.1),
    ("QT_COMBINE", "Quy trình BIM Combine", 1, "Chuẩn bị", "Tiếp nhận hồ sơ, chuẩn bị mô hình combine đúng TMB & tọa độ VN2000", "Leader Combine", 0.5, 0.5, 0.5),
    ("QT_COMBINE", "Quy trình BIM Combine", 2, "Hoạch định", "Lập danh mục 3D, chốt tiến độ bộ môn, chiến lược tách file theo phần cứng", "Leader Combine", 0.5, 0.5, 0.5),
    ("QT_COMBINE", "Quy trình BIM Combine", 3, "Kế hoạch chi tiết", "Lập danh sách bản vẽ combine, danh mục mô hình 3D & IFC phối hợp", "Leader Combine", 0.5, 0.5, 0.5),
    ("QT_COMBINE", "Quy trình BIM Combine", 4, "Thực thi", "Liên kết 3D, lập báo cáo va chạm, đề xuất & chốt phương án xử lý với CĐT/TVTK/NTP", "Leader Combine", 3.0, 7.0, 5.0),
    ("QT_COMBINE", "Quy trình BIM Combine", 5, "Kiểm soát chất lượng", "Tự kiểm tra theo checklist, ma trận va chạm, kiểm tra trực quan mô hình online", "Leader Combine", 0.5, 0.5, 0.5),
    ("QT_COMBINE", "Quy trình BIM Combine", 6, "Phát hành", "Phát hành bản vẽ combine phần ngầm/nổi, họp giải trình, cấp IFC/Revit/Excel cho NTP", "Leader Combine", 3.0, 3.0, 3.0),
    ("QT_COMBINE", "Quy trình BIM Combine", 7, "Kết thúc", "Lưu trữ mô hình, báo cáo, bài học kinh nghiệm", "Leader Combine", 0.1, 0.1, 0.1),
    ("QT_QS", "Quy trình BIM QS (Khối lượng)", 1, "Chuẩn bị", "Tiếp nhận hồ sơ, chuẩn bị Template Revit, BOQ, VLHT, rà soát tham biến khối lượng", "Leader QS XD & MEPF", 0.5, 0.5, 0.5),
    ("QT_QS", "Quy trình BIM QS (Khối lượng)", 2, "Hoạch định", "Lập danh mục hạng mục cần bóc khối lượng, phân bổ nguồn lực, thiết lập BOQ", "Leader QS XD & MEPF", 0.5, 0.5, 0.5),
    ("QT_QS", "Quy trình BIM QS (Khối lượng)", 3, "Kế hoạch chi tiết", "Lập kế hoạch chi tiết theo đầu mục BOQ cho các bộ môn kèm deadline", "KS/KTS BIM QS (HT, KC, KT, Cơ, Điện)", 0.5, 0.5, 0.5),
    ("QT_QS", "Quy trình BIM QS (Khối lượng)", 4, "Thực thi", "Triển khai mô hình theo BOQ, xuất thống kê Excel, link vào BOQ, tính bổ sung ngoài mô hình", "KS/KTS BIM QS (HT, KC, KT, Cơ, Điện)", 5.0, 7.0, 6.0),
    ("QT_QS", "Quy trình BIM QS (Khối lượng)", 5, "Kiểm soát chất lượng", "Tự kiểm tra checklist; Leader kiểm tra chất lượng mô hình, tính hợp lý & lỗi trích xuất", "Leader QS XD & MEPF", 0.5, 0.5, 0.5),
    ("QT_QS", "Quy trình BIM QS (Khối lượng)", 6, "Phát hành", "Phát hành khối lượng chính thức, phân tách theo kế hoạch thi công, đặt hàng, thanh quyết toán", "Leader QS XD & MEPF", 1.0, 1.0, 1.0),
    ("QT_QS", "Quy trình BIM QS (Khối lượng)", 7, "Kết thúc", "Lưu trữ bảng khối lượng đã xuất, phân loại đưa vào cơ sở dữ liệu", "Leader QS XD & MEPF", 0.1, 0.1, 0.1),
]
df_sla = pd.DataFrame(sla_rows, columns=[
    "MaQuyTrinh", "TenQuyTrinh", "BuocSo", "GiaiDoan_LuuDo", "MoTaCongViec",
    "VaiTroPhuTrach", "ThoiGian_Min_Ngay", "ThoiGian_Max_Ngay", "ThoiGian_TrungBinh_Ngay"
])

# 5. Bảng Đánh giá KPI đã sửa lỗi #DIV/0! (06_Fact_KPI_Fixed)
kpi_sheets = [
    ("MTCV_KPI_TBP BIM", "POS_TBP", "Trưởng bộ phận BIM - TK", "Quản lý"),
    ("MTCV_KPI_BIM Kien Truc", "POS_BIM_KT", "Kỹ sư BIM Kiến trúc", "Nhân viên"),
    ("MTCV_KPI_BIM Ket Cau", "POS_BIM_KC", "Kỹ sư BIM Kết cấu", "Nhân viên"),
    ("MTCV_KPI_BIM MEPF", "POS_BIM_MEPF", "Kỹ sư BIM MEPF", "Nhân viên"),
    ("MTCV_KPI_BIM Ha Tang", "POS_BIM_HT", "Kỹ sư BIM Hạ tầng", "Nhân viên"),
]
weights_tbp = [0.15, 0.20, 0.15, 0.10, 0.05, 0.10, 0.10, 0.10, 0.05]
weights_eng = [0.05, 0.05, 0.20, 0.20, 0.15, 0.10, 0.10, 0.05, 0.10]
kpi_rows = []
for sh_name, pos_code, pos_name, level in kpi_sheets:
    ws = wb_src[sh_name]
    for idx, r in enumerate([18, 21, 24, 27], 1):
        crit = clean_text(ws.cell(r, 1).value)
        w_orig = float(ws.cell(r, 27).value or 0.25)
        kpi_rows.append((f"{pos_code}_P1_{idx}", pos_code, pos_name, level, "Phần I - Tinh thần thái độ", idx, crit,
                         "Tuân thủ 100% quy định & văn hóa nội bộ doanh nghiệp", w_orig, w_orig,
                         float(ws.cell(r, 37).value or 0), float(ws.cell(r, 39).value or 0),
                         float(ws.cell(r, 41).value or 0), float(ws.cell(r, 43).value or 0)))
    for idx, r in enumerate(range(38, 47), 1):
        crit = clean_text(ws.cell(r, 2).value)
        out_req = ws.cell(r, 14).value
        out_str = clean_text(out_req) if out_req is not None else "Hoàn thành đúng tiến độ & chất lượng cam kết"
        w_prop = weights_tbp[idx-1] if pos_code == "POS_TBP" else weights_eng[idx-1]
        kpi_rows.append((f"{pos_code}_P2_{idx}", pos_code, pos_name, level, "Phần II - Kết quả công việc (KPI)", idx, crit,
                         out_str, float(ws.cell(r, 27).value or 0.0), w_prop,
                         float(ws.cell(r, 37).value or 4.0), float(ws.cell(r, 39).value or 4.0),
                         float(ws.cell(r, 41).value or 4.0), float(ws.cell(r, 43).value or 4.0)))

df_kpi = pd.DataFrame(kpi_rows, columns=[
    "MaChiTieu", "MaViTri", "TenViTri", "CapBac", "PhanDanhGia", "STT", "NoiDungTieuChi",
    "KetQuaCanCo", "TrongSo_FileGoc", "TrongSo_ChuanHoa_FixDiv0",
    "Diem_Q3_TuDanhGia", "Diem_Q3_CapTren", "Diem_Q4_TuDanhGia", "Diem_Q4_CapTren"
])
df_kpi["DiemQuyDoi_Q3_CapTren"] = (df_kpi["Diem_Q3_CapTren"] / 5.0 * df_kpi["TrongSo_ChuanHoa_FixDiv0"]).round(4)
df_kpi["DiemQuyDoi_Q4_CapTren"] = (df_kpi["Diem_Q4_CapTren"] / 5.0 * df_kpi["TrongSo_ChuanHoa_FixDiv0"]).round(4)

# 6. Bảng Chiến lược & Mục tiêu (01_Fact_ChienLuoc)
cl_rows = [
    ("CL_01", "Định hướng chiến lược", "Ngắn & Dài hạn", "Xây dựng lợi thế cạnh tranh tuyệt đối bằng hệ thống đóng kín, đồng bộ chuỗi giá trị (MKT - Thiết kế/Pháp lý - Đấu thầu - Thi công - Vận hành)", "Tỷ lệ đồng bộ chuỗi giá trị", 1.0, "100%", "Toàn doanh nghiệp"),
    ("CL_02", "Định hướng chiến lược", "Ngắn & Dài hạn", "Nâng cao năng lực lõi cho cán bộ văn phòng (tư duy thiết kế, 6 hóa), hướng tới đa nhiệm, tối ưu, dễ thích nghi", "Tỷ lệ nhân sự đạt chuẩn đa nhiệm & 6 hóa", 1.0, "100%", "Khu vực văn phòng"),
    ("CL_03", "Định hướng chiến lược", "Dài hạn", "Đặt nền tảng thu thập, tổ chức, lưu trữ, khai thác dữ liệu trên toàn chuỗi hoạt động xây dựng", "Mức độ làm chủ CSDL (Big Data)", 1.0, "100%", "Toàn doanh nghiệp"),
    ("MT_01A", "Mục tiêu", "Ngắn hạn (1 năm)", "Tự chủ toàn bộ thiết kế nội bộ (Số lượng dự án/năm)", "Số dự án tự thiết kế/năm", 4.0, "Dự án", "BP Thiết kế - BIM"),
    ("MT_01B", "Mục tiêu", "Ngắn hạn (1 năm)", "Tổng giá trị xây lắp các dự án tự thiết kế trong năm", "Tổng giá trị dự án", 1200.0, "Tỷ VNĐ", "BP Thiết kế - BIM"),
    ("MT_01C", "Mục tiêu", "Ngắn hạn (1 năm)", "Doanh thu thiết kế quy đổi ước tính trong ngắn hạn (1 năm)", "Doanh thu thiết kế ước tính", 10.0, "Tỷ VNĐ", "BP Thiết kế - BIM"),
    ("MT_02A", "Mục tiêu", "Dài hạn (>1 năm)", "Chuẩn hóa, tự động hóa nhiệm vụ trọng yếu; tỷ lệ chuyển hóa dự án tự thiết kế sang thắng thầu tối thiểu", "Tỷ lệ thắng thầu tối thiểu (Min Target)", 0.60, "60%", "BP Thiết kế - Đấu thầu"),
    ("MT_02B", "Mục tiêu", "Dài hạn (>1 năm)", "Hướng đến mục tiêu tối đa dự án tự thiết kế thắng thầu và chuyển sang thi công", "Tỷ lệ thắng thầu mục tiêu (Stretch Target)", 0.90, "90%", "BP Thiết kế - Đấu thầu"),
    ("MT_03", "Mục tiêu", "Dài hạn (>1 năm)", "Đưa Thiết kế từng bước trở thành bộ phận trực tiếp mang thêm lợi nhuận qua hợp đồng Thiết kế - BIM thương mại", "Chuyển đổi sang Profit Center", 1.0, "Có lợi nhuận độc lập", "BP Thiết kế - BIM"),
    ("NV_01", "Nhiệm vụ trọng yếu", "Thường xuyên", "Tư vấn, định hướng khách hàng theo phương án thiết kế chiến lược có ưu thế khi đấu thầu, thi công", "Tỷ lệ dự án định hướng theo chuẩn nội bộ", 1.0, "100%", "Chủ trì Thiết kế & TBP"),
    ("NV_02", "Nhiệm vụ trọng yếu", "Thường xuyên", "Tự thiết kế tối ưu các dự án D&B, Thiết kế - Đấu thầu - Thi công trên góc nhìn mang lại lợi thế cho doanh nghiệp", "Tối ưu hóa chi phí & BPTC", 1.0, "100%", "BP Thiết kế - BIM"),
    ("NV_03", "Nhiệm vụ trọng yếu", "Thường xuyên", "Quản lý chuẩn hóa hồ sơ thiết kế chuyển đổi sang mô hình BIM nội bộ", "Tỷ lệ dự án thiết kế tuân thủ chuẩn BIM nội bộ", 1.0, "100%", "Chủ trì Thiết kế"),
    ("NV_04", "Nhiệm vụ trọng yếu", "Thường xuyên", "Thiết kế, tư vấn hỗ trợ kỹ thuật cho toàn bộ dự án đang thi công (100% dự án tự TK & các vấn đề trọng yếu dự án ngoài)", "Tỷ lệ xử lý vướng mắc dự án tự thiết kế", 1.0, "100%", "BP Thiết kế - BIM"),
    ("NV_05", "Nhiệm vụ trọng yếu", "Ngắn & Trung hạn", "Chuẩn hóa thiết kế tối ưu cho công ty (chi tiết 2D, 3D, tiêu chuẩn, quy định, số liệu) gồm 118 danh mục tài liệu", "Số lượng tài liệu chuẩn hóa hoàn thành", 118.0, "Tài liệu", "6 Bộ môn Thiết kế"),
    ("NV_06", "Nhiệm vụ trọng yếu", "Ngắn & Trung hạn", "Kết hợp BIM - Thiết kế tối ưu nguồn lực bóc khối lượng, Shop, Combine (vẽ BIM từ đầu để tái sử dụng dữ liệu giai đoạn thi công)", "Tỷ lệ tiết kiệm nguồn lực / tái sử dụng dữ liệu", 0.70, "70%", "Liên quân BIM - Thiết kế"),
    ("NV_07", "Nhiệm vụ trọng yếu", "Ngắn & Trung hạn", "Tham gia chuẩn hóa biểu BOQ, Spec và các tài liệu hỗ trợ thiết kế - đấu thầu - thi công", "Tỷ lệ đồng bộ BOQ - Family - Tham biến", 1.0, "100%", "BIM QS - Thiết kế - Đấu thầu"),
]
df_cl = pd.DataFrame(cl_rows, columns=[
    "MaChiTieuCL", "PhanLoai", "ChuKyThoiGian", "NoiDungChiTiet",
    "TenChiSoDoLuong", "GiaTriMucTieu", "DonViTinh", "DonViPhuTrach"
])

# 7. Bảng Báo cáo Công việc Thực tế (07_Fact_BaoCaoCongViec)
def clean_task_desc(text):
    if not text:
        return ""
    import re
    t = str(text)
    # Subcontractors
    t = re.sub(r'cùng nhà thầu Fuji', 'cùng Đơn vị gia công kết cấu thép', t, flags=re.IGNORECASE)
    t = re.sub(r'cùng nhà thầu CPT', 'cùng Đơn vị gia công kết cấu thép', t, flags=re.IGNORECASE)
    t = re.sub(r'cùng nhà thầu Đại Dũng', 'cùng Đơn vị gia công kết cấu thép', t, flags=re.IGNORECASE)
    
    # Specific codes and packages with assigned Du An Mau
    t = re.sub(r'trạm nước thải2\.1a-BP16\.1a', 'trạm xử lý nước thải (Dự Án Mẫu 02)', t)
    t = re.sub(r'trạm nước thải\s+2\.1a-BP16\.1a', 'trạm xử lý nước thải (Dự Án Mẫu 02)', t)
    t = re.sub(r'vách bể\s+2\.1a-BP16\.1a', 'vách bể trạm xử lý nước thải (Dự Án Mẫu 02)', t)
    t = re.sub(r'vách bể BP15\.2', 'vách bể kỹ thuật (Dự Án Mẫu 02)', t)
    t = re.sub(r'trạm nước thải BP15\.1', 'trạm xử lý nước thải (Dự Án Mẫu 02)', t)
    t = re.sub(r'nhà xỉ than BP12', 'nhà phụ trợ kỹ thuật (Dự Án Mẫu 02)', t)
    t = re.sub(r'nhà nồi hơi BP12', 'nhà nồi hơi kỹ thuật (Dự Án Mẫu 02)', t)
    t = re.sub(r'hạng mục\s+BP3, BP12', 'các hạng mục kết cấu thép (Dự Án Mẫu 03)', t)
    t = re.sub(r'hạng mục\s+BP3', 'hạng mục mái xưởng A (Dự Án Mẫu 03)', t)
    t = re.sub(r'hạng mục\s+MS1', 'hạng mục xưởng sản xuất (Dự Án Mẫu 03)', t)
    t = re.sub(r'NP42', 'khu nhà điều hành (Dự Án Mẫu 03)', t)
    t = re.sub(r'TH2', 'khu nhà xưởng B (Dự Án Mẫu 04)', t)
    t = re.sub(r'TH1', 'khu nhà xưởng A (Dự Án Mẫu 04)', t)
    t = re.sub(r'nhà văn phòng các xưởng', 'khu văn phòng xưởng (Dự Án Mẫu 01)', t)
    t = re.sub(r'văn phòng các xưởng', 'khu văn phòng xưởng (Dự Án Mẫu 01)', t)
    t = re.sub(r'nhà phụ trợ 1', 'nhà phụ trợ kỹ thuật (Dự Án Mẫu 01)', t)
    t = re.sub(r'nhà xưởng E, G, H', 'cụm nhà xưởng mở rộng (Dự Án Mẫu 01)', t)
    t = re.sub(r'các xưởng A, B, C, D, F', 'cụm nhà xưởng sản xuất chính (Dự Án Mẫu 01)', t)
    t = re.sub(r'2 gói 3\.2B và 3\.2C', 'các phân đoạn móng (Dự Án Mẫu 07)', t)
    t = re.sub(r'3\.2B và 3\.2C', 'các phân đoạn móng (Dự Án Mẫu 07)', t)
    t = re.sub(r'(?:nhà\s+trạm|(?<!n)hà\s+trạm)\s*1,2,3,4', 'nhà trạm kỹ thuật (Dự Án Mẫu 06)', t)
    t = re.sub(r'(?:nhà\s+trạm\s+nguồn|trạm\s+nguồn)\s*1,2,3,4', 'trạm nguồn điện kỹ thuật (Dự Án Mẫu 06)', t)
    t = re.sub(r'trạm nguồn(?!\s+điện)', 'trạm nguồn điện kỹ thuật (Dự Án Mẫu 06)', t)
    t = re.sub(r'nhà vệ sinh\s*1,2', 'khu vệ sinh (Dự Án Mẫu 01)', t)
    t = re.sub(r'nhà\s+bảo vệ\s*1,2', 'nhà bảo vệ (Dự Án Mẫu 01)', t)
    t = re.sub(r'thay đổi thiết kế dự án', 'thay đổi thiết kế dự án mẫu', t)
    t = re.sub(r'phục vụ triển khai IPC1', 'phục vụ hồ sơ nghiệm thu IPC (Dự Án Mẫu 05)', t)
    t = re.sub(r'phục vụ IPC', 'phục vụ hồ sơ nghiệm thu IPC (Dự Án Mẫu 05)', t)
    
    t = re.sub(r'\s+', ' ', t).strip()
    return t

task_rows = []
if os.path.exists(SRC_FILE_TASKS):
    wb_tasks = openpyxl.load_workbook(SRC_FILE_TASKS, data_only=True)
    if "P. BIM" in wb_tasks.sheetnames:
        ws_t = wb_tasks["P. BIM"]
        cur_project = ""
        for r in range(3, ws_t.max_row + 1):
            hm = ws_t.cell(r, 2).value
            cv = ws_t.cell(r, 3).value
            if hm and str(hm).strip():
                p_text = clean_text(hm)
                if p_text.startswith("Dự án"):
                    project_mapping = {
                        "Dự án Mega": "Dự Án Mẫu 01",
                        "Dự án Kim Tín giai đoạn 3": "Dự Án Mẫu 02",
                        "Dự án APF": "Dự Án Mẫu 03",
                        "Dự án CasaFlora2": "Dự Án Mẫu 04",
                        "Dự án Suncasa": "Dự Án Mẫu 05",
                        "Dự án các trạm Phú Quốc": "Dự Án Mẫu 06",
                        "Dự án BB052": "Dự Án Mẫu 07"
                    }
                    cur_project = project_mapping.get(p_text, p_text.replace("Dự án ", "Dự Án Mẫu - "))
                else:
                    cur_project = p_text
            if cv and str(cv).strip():
                pic = clean_text(ws_t.cell(r, 1).value or "P. BIM")
                st = str(ws_t.cell(r, 4).value or "Chưa thực hiện").strip()
                d_start = ws_t.cell(r, 5).value
                d_end = ws_t.cell(r, 6).value
                d_due = ws_t.cell(r, 7).value
                progress = clean_text(ws_t.cell(r, 8).value)
                quality = clean_text(ws_t.cell(r, 9).value)
                risk = clean_text(ws_t.cell(r, 10).value)
                opt = clean_text(ws_t.cell(r, 11).value)
                note = clean_text(ws_t.cell(r, 13).value)

                if cur_project == "Dự án Mẫu" or cur_project.startswith("Dự án"):
                    cur_project = "Dự Án Mẫu"
                    group_type = "Dự Án Mẫu (Thi công & Triển khai)"
                elif any(cur_project.startswith(x) for x in ["Kiến Trúc", "Kết cấu", "Hệ thống điện", "Điều hoà", "Cấp thoát", "Phòng cháy"]):
                    group_type = "Chuẩn hóa Bộ môn Thiết kế"
                else:
                    group_type = "Quản trị & Tổ chức"

                task_rows.append({
                    "MaCongViec": f"TSK_{len(task_rows)+1:03d}",
                    "NhomCongViec": group_type,
                    "HangMuc_DuAn": cur_project,
                    "NoiDungCongViec": clean_task_desc(clean_text(cv)),
                    "TinhTrang": st,
                    "PIC": pic,
                    "NgayBatDau": str(d_start)[:10] if d_start else "",
                    "NgayKetThuc": str(d_end)[:10] if d_end else "",
                    "HanHoanThanh": str(d_due)[:10] if d_due else "",
                    "TienDoChiTiet": clean_task_desc(progress),
                    "KetQuaChatLuong": clean_task_desc(quality),
                    "RuiRo_KhoKhan": clean_task_desc(risk),
                    "ToiUu_GiaiPhap": clean_task_desc(opt),
                    "GhiChu": clean_task_desc(note)
                })

df_tasks = pd.DataFrame(task_rows)

# 8. Bảng Hướng dẫn DAX (00_PowerBI_Dashboard_DAX)
dax_rows = [
    ("Tong Dinh Bien", "02_Fact_NhanSu", "Tong Dinh Bien = SUM('02_Fact_NhanSu'[DinhBienKeHoach])", "Card / Clustered Column Chart"),
    ("Nhan Su Hien Tai", "02_Fact_NhanSu", "Nhan Su Hien Tai = SUM('02_Fact_NhanSu'[NhanSuConLai])", "Card / Gauge Chart"),
    ("Thieu Hut Nhan Su", "02_Fact_NhanSu", "Thieu Hut Nhan Su = [Tong Dinh Bien] - [Nhan Su Hien Tai]", "Card (Cảnh báo thiếu 6 nhân sự)"),
    ("Ty Le Lap Day Nhan Su", "02_Fact_NhanSu", "Ty Le Lap Day Nhan Su = DIVIDE([Nhan Su Hien Tai], [Tong Dinh Bien], 0)", "Gauge / Donut Chart (80.0%)"),
    ("Tong Tai Lieu Chuan Hoa", "05_Fact_TaiLieuTK", "Tong Tai Lieu Chuan Hoa = COUNTROWS('05_Fact_TaiLieuTK')", "Card / Bar Chart theo 6 Bộ môn (115 mục)"),
    ("Tien Do Chuan Hoa TB", "05_Fact_TaiLieuTK", "Tien Do Chuan Hoa TB = AVERAGE('05_Fact_TaiLieuTK'[TiLeHoanThanh_UocTinh])", "Progress Bar / Matrix theo Chủ trì"),
    ("Ty Le Ganh Nang R_A", "03_Fact_RACI", "Ty Le Ganh Nang R_A = DIVIDE(CALCULATE(COUNTROWS('03_Fact_RACI'), '03_Fact_RACI'[VaiTro_RACI] IN {\"R\", \"A\"}), COUNTROWS('03_Fact_RACI'), 0)", "100% Stacked Bar phân tích tải TBP"),
    ("Diem KPI Quy Doi Q4", "06_Fact_KPI_Fixed", "Diem KPI Quy Doi = SUM('06_Fact_KPI_Fixed'[DiemQuyDoi_Q4_CapTren])", "Clustered Bar so sánh các vị trí"),
    ("Chu Ky Quy Trinh TB", "04_Fact_QuyTrinhSLA", "Chu Ky Quy Trinh TB = SUM('04_Fact_QuyTrinhSLA'[ThoiGian_TrungBinh_Ngay])", "Stacked Bar Chart (SLA 7 bước)"),
    ("Tong Cong Viec Thuc Te", "07_Fact_BaoCaoCongViec", "Tong Cong Viec Thuc Te = COUNTROWS('07_Fact_BaoCaoCongViec')", "Card tổng số 214 nhiệm vụ"),
    ("Ty Le Hoan Thanh Du An", "07_Fact_BaoCaoCongViec", "Ty Le Hoan Thanh Du An = DIVIDE(CALCULATE(COUNTROWS('07_Fact_BaoCaoCongViec'), '07_Fact_BaoCaoCongViec'[TinhTrang] = \"Đã hoàn thành\", '07_Fact_BaoCaoCongViec'[NhomCongViec] = \"Dự án Mẫu (Thi công & Triển khai)\"), CALCULATE(COUNTROWS('07_Fact_BaoCaoCongViec'), '07_Fact_BaoCaoCongViec'[NhomCongViec] = \"Dự án Mẫu (Thi công & Triển khai)\"), 0)", "Gauge Chart tiến độ Dự Án Mẫu"),
    ("Cong Viec Qua Han", "07_Fact_BaoCaoCongViec", "Cong Viec Qua Han = CALCULATE(COUNTROWS('07_Fact_BaoCaoCongViec'), '07_Fact_BaoCaoCongViec'[TinhTrang] = \"Quá hạn\")", "Card cảnh báo sự cố rủi ro"),
]
df_dax = pd.DataFrame(dax_rows, columns=["Ten_Measure_PowerBI", "Bang_Chua", "Cong_Thuc_DAX", "Ung_Dung_Visual"])

# Xuất file Excel 8 Sheet Star Schema
with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
    df_dax.to_excel(writer, sheet_name="00_PowerBI_Dashboard_DAX", index=False)
    df_cl.to_excel(writer, sheet_name="01_Fact_ChienLuoc", index=False)
    df_hr.to_excel(writer, sheet_name="02_Fact_NhanSu", index=False)
    df_raci.to_excel(writer, sheet_name="03_Fact_RACI", index=False)
    df_sla.to_excel(writer, sheet_name="04_Fact_QuyTrinhSLA", index=False)
    df_docs.to_excel(writer, sheet_name="05_Fact_TaiLieuTK", index=False)
    df_kpi.to_excel(writer, sheet_name="06_Fact_KPI_Fixed", index=False)
    df_tasks.to_excel(writer, sheet_name="07_Fact_BaoCaoCongViec", index=False)

# Mã hóa Base64 file Excel để nhúng thẳng nút Download
with open(OUT_XLSX, "rb") as f:
    b64_xlsx = base64.b64encode(f.read()).decode("utf-8")

# Xuất file HTML Interactive Dashboard (Dark Mode)
html_content = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Power BI Executive Dashboard - BP BIM & Thiết Kế</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg-main: #0b0f19; --bg-card: #111827; --border-color: #1f2937;
    --text-primary: #f8fafc; --text-secondary: #94a3b8;
    --accent-cyan: #06b6d4; --accent-blue: #3b82f6; --accent-emerald: #10b981;
    --accent-amber: #f59e0b; --accent-rose: #f43f5e; --accent-purple: #8b5cf6;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }}
  body {{ background-color: var(--bg-main); color: var(--text-primary); display: flex; min-height: 100vh; overflow-x: hidden; }}
  .sidebar {{ width: 270px; background: #0f172a; border-right: 1px solid var(--border-color); display: flex; flex-direction: column; flex-shrink: 0; }}
  .brand {{ padding: 18px 20px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; gap: 12px; }}
  .brand-icon {{ width: 34px; height: 34px; border-radius: 8px; background: linear-gradient(135deg, #06b6d4, #3b82f6); display: flex; align-items: center; justify-content: center; font-weight: 800; color: #ffffff; font-size: 15px; }}
  .brand-text h1 {{ font-size: 14px; font-weight: 700; color: #f8fafc; }}
  .brand-text p {{ font-size: 11px; color: var(--text-secondary); }}
  .nav-menu {{ padding: 14px 10px; display: flex; flex-direction: column; gap: 6px; flex: 1; }}
  .nav-btn {{ background: transparent; border: none; color: var(--text-secondary); padding: 11px 14px; border-radius: 8px; text-align: left; font-size: 13px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: all 0.2s; }}
  .nav-btn:hover {{ background: rgba(255,255,255,0.05); color: #fff; }}
  .nav-btn.active {{ background: rgba(6, 182, 212, 0.15); color: var(--accent-cyan); border-left: 3px solid var(--accent-cyan); }}
  .slicer-box {{ padding: 14px; margin: 10px; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 8px; display: flex; flex-direction: column; gap: 8px; }}
  .slicer-box label {{ display: block; font-size: 11px; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 4px; font-weight: 700; }}
  .slicer-select {{ width: 100%; background: #0b0f19; color: #f8fafc; border: 1px solid #334155; padding: 7px 10px; border-radius: 6px; font-size: 12px; outline: none; }}
  .main {{ flex: 1; display: flex; flex-direction: column; padding: 20px 24px; gap: 18px; max-width: calc(100vw - 270px); }}
  .topbar {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 14px; flex-wrap: wrap; gap: 12px; }}
  .topbar-title h2 {{ font-size: 20px; font-weight: 700; color: #f8fafc; }}
  .topbar-title span {{ font-size: 12px; color: var(--text-secondary); }}
  .badge-bar {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
  .badge {{ background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); color: #34d399; padding: 5px 12px; border-radius: 999px; font-size: 12px; font-weight: 600; }}
  .badge.warn {{ background: rgba(245, 158, 11, 0.12); border-color: rgba(245, 158, 11, 0.35); color: #fbbf24; }}
  .badge.info {{ background: rgba(59, 130, 246, 0.12); border-color: rgba(59, 130, 246, 0.35); color: #60a5fa; }}
  .btn-dl {{ background: linear-gradient(135deg, #10b981, #059669); color: #fff; text-decoration: none; padding: 7px 14px; border-radius: 8px; font-size: 12.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 6px; }}
  .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; }}
  .kpi-card {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 16px; position: relative; overflow: hidden; }}
  .kpi-card::before {{ content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--accent-cyan); }}
  .kpi-card.amber::before {{ background: var(--accent-amber); }}
  .kpi-card.emerald::before {{ background: var(--accent-emerald); }}
  .kpi-card.rose::before {{ background: var(--accent-rose); }}
  .kpi-card.purple::before {{ background: var(--accent-purple); }}
  .kpi-card.blue::before {{ background: var(--accent-blue); }}
  .kpi-title {{ font-size: 11px; text-transform: uppercase; color: var(--text-secondary); font-weight: 700; margin-bottom: 8px; }}
  .kpi-val {{ font-size: 24px; font-weight: 800; color: #fff; margin-bottom: 4px; }}
  .kpi-sub {{ font-size: 11.5px; color: var(--text-secondary); }}
  .tab-page {{ display: none; flex-direction: column; gap: 18px; }}
  .tab-page.active {{ display: flex; }}
  .chart-grid-2 {{ display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 16px; }}
  .chart-grid-equal {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  @media (max-width: 1100px) {{ .chart-grid-2, .chart-grid-equal {{ grid-template-columns: 1fr; }} }}
  .panel {{ background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 16px; display: flex; flex-direction: column; gap: 12px; }}
  .panel-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px; }}
  .panel-header h3 {{ font-size: 14.5px; font-weight: 700; color: #e2e8f0; }}
  .panel-header span {{ font-size: 11.5px; color: var(--text-secondary); }}
  .chart-container {{ position: relative; height: 290px; width: 100%; }}
  .table-wrap {{ overflow-x: auto; max-height: 400px; border-radius: 8px; border: 1px solid var(--border-color); }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
  th {{ background: #1e293b; color: #f8fafc; position: sticky; top: 0; padding: 10px 12px; text-align: left; font-weight: 700; border-bottom: 1px solid #334155; z-index: 2; }}
  td {{ padding: 9px 12px; border-bottom: 1px solid var(--border-color); color: #cbd5e1; }}
  tr:hover td {{ background: rgba(255,255,255,0.03); }}
  .pill {{ padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; display: inline-block; }}
  .pill-p1 {{ background: rgba(244, 63, 94, 0.18); color: #fb7185; }}
  .pill-p2 {{ background: rgba(59, 130, 246, 0.18); color: #60a5fa; }}
  .pill-r {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
  .pill-a {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; }}
  .pill-overdue {{ background: rgba(244, 63, 94, 0.25); color: #f87171; border: 1px solid rgba(244, 63, 94, 0.5); }}
  .pill-progress {{ background: rgba(59, 130, 246, 0.2); color: #60a5fa; }}
  .pill-done {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
  .pill-pending {{ background: rgba(148, 163, 184, 0.2); color: #94a3b8; }}
</style>
</head>
<body>
<aside class="sidebar">
  <div class="brand">
    <div class="brand-icon">BIM</div>
    <div class="brand-text"><h1>BAN BIM - THIẾT KẾ</h1><p>BIM & Design Analytics</p></div>
  </div>
  <div class="nav-menu">
    <button id="btnNavExec" class="nav-btn active" onclick="switchTab('tab-exec', this)">📊 1. Chiến lược & Tổ chức</button>
    <button id="btnNavRaci" class="nav-btn" onclick="switchTab('tab-raci', this)">🎯 2. Ma trận RACI & SLA</button>
    <button id="btnNavDocs" class="nav-btn" onclick="switchTab('tab-docs', this)">📁 3. Hệ thống 115 Tài liệu</button>
    <button id="btnNavKpi" class="nav-btn" onclick="switchTab('tab-kpi', this)">🏆 4. Đánh giá KPI</button>
    <button id="btnNavTasks" class="nav-btn" onclick="switchTab('tab-tasks', this)">🚀 5. Tiến độ Dự án Mẫu</button>
  </div>
  <div class="slicer-box">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
      <span style="font-size:11px; text-transform:uppercase; font-weight:800; color:var(--accent-cyan);">⚡ Bộ lọc Tương tác</span>
      <button onclick="resetAllFilters()" style="background:rgba(255,255,255,0.08); border:1px solid #334155; color:#94a3b8; font-size:10.5px; padding:2px 8px; border-radius:4px; cursor:pointer;" title="Khôi phục toàn bộ">Đặt lại</button>
    </div>
    
    <div>
      <label>🎯 Lọc Nhân sự (Tab 2: RACI)</label>
      <select id="slicerPerson" class="slicer-select" onchange="updateRaciFilter(true)">
        <option value="ALL">-- Tất cả Vai trò / Nhân sự --</option>
        <option value="Trưởng bộ phận BIM - TK">Trưởng bộ phận BIM - TK</option>
        <option value="Lead BIM Kiến Trúc">Lead BIM Kiến Trúc</option>
        <option value="Lead BIM MEPF">Lead BIM MEPF</option>
        <option value="Kỹ sư BIM Kiến Trúc 1">Kỹ sư BIM Kiến Trúc 1</option>
        <option value="Kỹ sư BIM Kiến Trúc 2">Kỹ sư BIM Kiến Trúc 2</option>
        <option value="Kỹ sư BIM Kết Cấu 1">Kỹ sư BIM Kết Cấu 1</option>
        <option value="Kỹ sư BIM Kết Cấu 2">Kỹ sư BIM Kết Cấu 2</option>
        <option value="Kỹ sư BIM MEPF">Kỹ sư BIM MEPF</option>
        <option value="Kỹ sư BIM Hạ Tầng & CDE">Kỹ sư BIM Hạ Tầng & CDE</option>
      </select>
    </div>

    <div>
      <label>🚀 Lọc Dự án Mẫu / Hạng mục (Tab 5: Tiến độ)</label>
      <select id="slicerTaskProject" class="slicer-select" onchange="updateTasksFilter(true)">
        <option value="ALL">-- Tất cả 7 Dự án Mẫu & Hạng mục (214 Việc) --</option>
        <optgroup label="7 Dự Án Mẫu Thực Chiến (87 Việc)">
          <option value="Dự Án Mẫu 01">Dự Án Mẫu 01 (24 Việc)</option>
          <option value="Dự Án Mẫu 02">Dự Án Mẫu 02 (18 Việc)</option>
          <option value="Dự Án Mẫu 03">Dự Án Mẫu 03 (15 Việc)</option>
          <option value="Dự Án Mẫu 04">Dự Án Mẫu 04 (12 Việc)</option>
          <option value="Dự Án Mẫu 05">Dự Án Mẫu 05 (9 Việc)</option>
          <option value="Dự Án Mẫu 06">Dự Án Mẫu 06 (7 Việc)</option>
          <option value="Dự Án Mẫu 07">Dự Án Mẫu 07 (2 Việc)</option>
        </optgroup>
        <optgroup label="Chuẩn Hóa Hệ Thống & Quản Trị (127 Việc)">
          <option value="Chuẩn hóa Bộ môn Thiết kế">Chuẩn hóa 6 Bộ môn (115 Việc)</option>
          <option value="Quản trị & Tổ chức">Quản trị & Văn hóa (12 Việc)</option>
        </optgroup>
      </select>
    </div>

    <div>
      <label>📁 Lọc Bộ môn (Tab 3: Tài liệu)</label>
      <select id="slicerBoMon" class="slicer-select" onchange="updateDocsFilter(true)">
        <option value="ALL">-- Tất cả 6 Bộ môn (115) --</option>
        <option value="KC">Thiết kế Kết cấu (23)</option>
        <option value="KT">Thiết kế Kiến trúc (20)</option>
        <option value="DIEN">Thiết kế Điện (18)</option>
        <option value="HVAC">Thiết kế HVAC (18)</option>
        <option value="CTN">Thiết kế Cấp thoát nước (18)</option>
        <option value="PCCC">Thiết kế PCCC (18)</option>
      </select>
    </div>
  </div>
</aside>

<main class="main">
  <div class="topbar">
    <div class="topbar-title">
      <h2>Power BI Executive Dashboard — Chiến lược, Tổ chức & Tiến độ Dự án Mẫu BP BIM - TK (2027)</h2>
      <span>Kế hoạch Chiến lược Niên độ 2027 | Danh tính nhân sự & doanh nghiệp đã được bảo mật</span>
    </div>
    <div class="badge-bar">
      <a class="btn-dl" download="BIM_TK_PowerBI_DataModel_2026.xlsx" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_xlsx}">📥 Tải File Excel 8 Sheet Chuẩn Power BI (.xlsx)</a>
      <a class="btn-dl" href="Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2027.pdf" target="_blank" style="background: linear-gradient(135deg, #0284c7, #0369a1);">📄 Tải Báo Cáo Chiến Lược PDF 2027 (Trình Lãnh Đạo)</a>
      <span class="badge">✔ Star Schema 8 Bảng</span>
      <span class="badge info">👥 24 Nhân sự Vận hành</span>
    </div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card emerald"><div class="kpi-title">Tiến độ 7 Dự Án Mẫu</div><div class="kpi-val">75.9%</div><div class="kpi-sub">66 / 87 việc hoàn thành (7 Dự Án Mẫu)</div></div>
    <div class="kpi-card blue"><div class="kpi-title">Tự chủ Shop Drawing</div><div class="kpi-val">100%</div><div class="kpi-sub">Làm chủ 6 bộ môn, chuyển đổi toàn diện lên BIM</div></div>
    <div class="kpi-card rose"><div class="kpi-title">Phát sinh Sửa chữa CT</div><div class="kpi-val">&lt; 1%</div><div class="kpi-sub">Xóa 100% va chạm trước khi đổ bê tông</div></div>
    <div class="kpi-card amber"><div class="kpi-title">Tài liệu Chuẩn hóa Thiết kế</div><div class="kpi-val">115 Mục</div><div class="kpi-sub">6 Bộ môn (KC, KT, Điện, HVAC, CTN, PCCC)</div></div>
    <div class="kpi-card purple"><div class="kpi-title">Mô hình Điều phối Cụm</div><div class="kpi-val">4 Squads</div><div class="kpi-sub">Tối ưu theo Leader bộ môn hiện hữu</div></div>
  </div>

  <!-- TAB 1: CHIEN LUOC & TO CHUC -->
  <section id="tab-exec" class="tab-page active">
    <div class="chart-grid-2">
      <div class="panel">
        <div class="panel-header"><h3>Phân bổ Định biên Kế hoạch vs. Nhân sự Thực tế Còn lại</h3><span>Tổng Định biên: 30 | Hiện có: 26 | Còn lại: 24</span></div>
        <div class="chart-container"><canvas id="chartHR"></canvas></div>
      </div>
      <div class="panel">
        <div class="panel-header"><h3>Lộ trình Chuyển đổi Giá trị Chiến lược</h3><span>Tích hợp chuỗi giá trị MKT - Thiết kế - Đấu thầu - Thi công</span></div>
        <div class="table-wrap"><table><thead><tr><th>Mã</th><th>Nhóm</th><th>Nội dung Chiến lược / Nhiệm vụ</th><th>Mục tiêu</th></tr></thead><tbody id="tblStrategyBody"></tbody></table></div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-header"><h3>Bảng Chi tiết Định biên Tổ chức & Trạng thái Nhân sự Chủ chốt Hiện tại</h3><span>Đủ 4 Chủ trì Thiết kế (KT, KC, Điện-Cơ, HVAC) & 2 Trưởng nhóm BIM</span></div>
      <div class="table-wrap"><table><thead><tr><th>Nhóm Chuyên môn</th><th>Vị trí</th><th>Nhân sự Chủ chốt</th><th>Cấp bậc</th><th>Định biên</th><th>Hiện có</th><th>Nghỉ T04</th><th>Còn lại</th><th>Thiếu hụt</th><th>Trạng thái</th></tr></thead><tbody id="tblHRBody"></tbody></table></div>
    </div>
    
    <!-- PHƯƠNG ÁN ĐIỀU PHỐI VẬN HÀNH DỰA THEO LEADER TỪNG BỘ MÔN -->
    <div class="panel" style="border: 1px solid rgba(59, 130, 246, 0.4); background: linear-gradient(180deg, #111827, #0f172a);">
      <div class="panel-header">
        <div>
          <h3 style="color:var(--accent-blue);">🔄 Phương án Setup Điều phối Vận hành theo Leader Từng Bộ môn (4 Cụm Squads Hiện tại)</h3>
          <span style="color:#94a3b8;">Giữ nguyên quy mô hiện tại — Tối ưu hóa điều phối, phân quyền tự chủ kỹ thuật và gắn kết quả cam kết SLA cho từng Leader</span>
        </div>
        <span class="badge info">Cơ cấu Setup Mới</span>
      </div>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:12px; margin-top:8px;">
        <div style="background:rgba(255,255,255,0.03); border:1px solid #1f2937; border-radius:8px; padding:12px;">
          <div style="font-size:11px; text-transform:uppercase; color:#60a5fa; font-weight:700; margin-bottom:4px;">Cụm 1: Kết cấu & Biện pháp (SLA Shop: 5 Ngày)</div>
          <div style="font-size:12.5px; font-weight:700; color:#fff;">Lead: Lead Bộ Môn Kết Cấu</div>
          <div style="font-size:11px; color:#94a3b8; margin-top:4px;">• Đội ngũ KS BIM Kết Cấu thực chiến<br/>• Mô hình BTCT, đà kiềng, móng, vách bể<br/>• Xuất bản vẽ Shop cốt thép & ván khuôn, AI bóc BOQ</div>
        </div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid #1f2937; border-radius:8px; padding:12px;">
          <div style="font-size:11px; text-transform:uppercase; color:#34d399; font-weight:700; margin-bottom:4px;">Cụm 2: Kiến trúc & Tạo hình 3D</div>
          <div style="font-size:12.5px; font-weight:700; color:#fff;">Lead: Lead Bộ Môn Kiến Trúc</div>
          <div style="font-size:11px; color:#94a3b8; margin-top:4px;">• Đội ngũ KTS & KS BIM Kiến Trúc thực chiến<br/>• Mô hình kiến trúc LOD 300-350, chi tiết cấu tạo<br/>• Diễn họa 3D/VR, video tiến độ 4D hỗ trợ đấu thầu</div>
        </div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid #1f2937; border-radius:8px; padding:12px;">
          <div style="font-size:11px; text-transform:uppercase; color:#fbbf24; font-weight:700; margin-bottom:4px;">Cụm 3: Cơ điện MEPF & Va chạm (SLA Combine: 3 Ngày - AI Agent)</div>
          <div style="font-size:12.5px; font-weight:700; color:#fff;">Lead: Lead Bộ Môn BIM MEPF</div>
          <div style="font-size:11px; color:#94a3b8; margin-top:4px;">• Đội ngũ KS BIM MEPF thực chiến<br/>• Mô hình 4 hệ: Điện, HVAC, Cấp thoát, PCCC<br/>• AI Agent gom nhóm & lọc va chạm, giải quyết xung đột 3 ngày</div>
        </div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid #1f2937; border-radius:8px; padding:12px;">
          <div style="font-size:11px; text-transform:uppercase; color:#f472b6; font-weight:700; margin-bottom:4px;">Cụm 4: Hạ tầng & CDE (SLA QS: 3 Ngày - AI Agent)</div>
          <div style="font-size:12.5px; font-weight:700; color:#fff;">Lead: Lead Kỹ Thuật Hạ Tầng & CDE</div>
          <div style="font-size:11px; color:#94a3b8; margin-top:4px;">• San nền, giao thông, hạ tầng ngoài nhà (Civil 3D)<br/>• Quản trị phân quyền CDE & liên kết đa bộ môn<br/>• AI Agent bóc tách khối lượng 5D BOQ tự động trong 3 ngày</div>
        </div>
      </div>
    </div>
  </section>

  <!-- TAB 2: RACI & SLA -->
  <section id="tab-raci" class="tab-page">
    <!-- CẨM NANG CHUẨN HÓA VẬN HÀNH RACI & SLA -->
    <div class="panel" style="border: 1px solid rgba(139, 92, 246, 0.35); background: linear-gradient(180deg, #111827, #0f172a);">
      <div class="panel-header">
        <div>
          <h3 style="color:#a78bfa;">📘 Cẩm nang Chuẩn hóa Vận hành: Khung Ma trận RACI & Cam kết Dịch vụ SLA</h3>
          <span style="color:#94a3b8;">Xóa bỏ tình trạng đùn đẩy trách nhiệm và làm việc tùy hứng giữa Phòng BIM, Ban Đấu thầu và Công trường</span>
        </div>
        <span class="badge info">Chuẩn ISO / Vận hành Quốc tế</span>
      </div>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:16px;">
        <div style="background:rgba(255,255,255,0.02); border:1px solid #1f2937; border-radius:8px; padding:12px;">
          <div style="font-size:12px; font-weight:700; color:#e2e8f0; margin-bottom:8px;">🎯 Ý NGHĨA 4 VAI TRÒ TRONG MA TRẬN RACI</div>
          <div style="font-size:11.5px; line-height:1.6; color:#cbd5e1;">
            • <b style="color:#34d399;">R (Responsible - Trực tiếp làm):</b> Người trực tiếp mở Revit/Navisworks dựng mô hình, xuất bản vẽ.<br/>
            • <b style="color:#fbbf24;">A (Accountable - Duyệt cuối):</b> Người duy nhất ký duyệt và chịu trách nhiệm tối cao trước Lãnh đạo.<br/>
            • <b style="color:#60a5fa;">S (Support - Hỗ trợ):</b> Đội ngũ kỹ sư phối hợp, hỗ trợ chia việc cùng người giữ vai trò R.<br/>
            • <b style="color:#94a3b8;">I (Informed - Nhận tin):</b> Các bên liên quan (BCH, CĐT) nhận kết quả sau khi duyệt.
          </div>
        </div>
        <div style="background:rgba(255,255,255,0.02); border:1px solid #1f2937; border-radius:8px; padding:12px;">
          <div style="font-size:12px; font-weight:700; color:#e2e8f0; margin-bottom:8px;">⏱️ Ý NGHĨA CAM KẾT MỨC DỊCH VỤ SLA 7 BƯỚC</div>
          <div style="font-size:11.5px; line-height:1.6; color:#cbd5e1;">
            • <b>SLA (Service Level Agreement):</b> Hợp đồng cam kết tiến độ và chất lượng nghiệm thu giữa Phòng BIM với Công trường.<br/>
            • <b>Quy trình Shop Drawing (Chuẩn 5 Ngày):</b> Rà soát & BEP (4h+4h) ➔ Dựng Model & Shop (3 ngày) ➔ QC & Ký duyệt (8h+4h).<br/>
            • <b>Quy trình Combine MEPF (Chuẩn 3 Ngày - AI Agent):</b> AI Agent quét & ma trận va chạm (1 ngày) ➔ Họp xử lý & tối ưu tuyến (1 ngày) ➔ Khóa mô hình & phát hành (1 ngày).<br/>
            • <b>Quy trình QS Bóc Khối Lượng (Chuẩn 3 Ngày - AI Agent):</b> AI Agent rà soát model & mapping (1 ngày) ➔ Tự động bóc 5D BOQ bằng AI Agent (1 ngày) ➔ Đối soát sai số & Bàn giao (1 ngày).
          </div>
        </div>
      </div>
    </div>
    <div class="chart-grid-equal">
      <div class="panel">
        <div class="panel-header"><h3>Phân tích Tải Công việc theo Ma trận RACI</h3><span id="raciChartTitle">Số lượng đầu việc theo vai trò R, A, S, I</span></div>
        <div class="chart-container"><canvas id="chartRACI"></canvas></div>
      </div>
      <div class="panel">
        <div class="panel-header"><h3>Định mức Thời gian Chuẩn (SLA) 3 Quy trình: Shop, Combine, QS</h3><span>Đơn vị: Ngày làm việc theo Lưu đồ 7 bước</span></div>
        <div class="chart-container"><canvas id="chartSLA"></canvas></div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-header"><h3>Chi tiết Ma trận Phân công Trách nhiệm RACI</h3><span id="raciCountLabel" style="color:var(--accent-cyan); font-weight:700;"></span></div>
      <div class="table-wrap"><table><thead><tr><th>Nhóm Nhiệm vụ</th><th>Mã</th><th>Tên Nhiệm vụ</th><th>Họ tên Nhân sự</th><th>Bộ môn</th><th>Vai trò RACI</th><th>Diễn giải</th></tr></thead><tbody id="tblRACIBody"></tbody></table></div>
    </div>
  </section>

  <!-- TAB 3: 115 TAI LIEU CHUAN HOA -->
  <section id="tab-docs" class="tab-page">
    <div class="chart-grid-equal">
      <div class="panel">
        <div class="panel-header"><h3>Số lượng Tài liệu Chuẩn hóa theo 6 Bộ môn Thiết kế</h3><span>Tổng cộng: 115 Danh mục tài liệu kỹ thuật</span></div>
        <div class="chart-container"><canvas id="chartDocsDept"></canvas></div>
      </div>
      <div class="panel">
        <div class="panel-header"><h3>Cơ cấu Tài liệu theo Nhóm Công cụ & Mức độ Ưu tiên</h3><span>Tập trung vào Template Revit/CAD, BOQ & Tự động hóa</span></div>
        <div class="chart-container"><canvas id="chartDocsType"></canvas></div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-header"><h3>Danh mục Hệ thống Tài liệu Thiết kế</h3><span id="docsCountLabel" style="color:var(--accent-cyan); font-weight:700;"></span></div>
      <div class="table-wrap"><table><thead><tr><th>Mã</th><th>Bộ môn</th><th>Chủ trì Phụ trách</th><th>Tên Tài liệu Chuẩn hóa</th><th>Phân nhóm</th><th>Ưu tiên</th><th>Trạng thái</th><th>Ghi chú Rà soát</th></tr></thead><tbody id="tblDocsBody"></tbody></table></div>
    </div>
  </section>

  <!-- TAB 4: KPI FIX -->
  <section id="tab-kpi" class="tab-page">
    <div class="chart-grid-2">
      <div class="panel">
        <div class="panel-header"><h3>So sánh Điểm Đánh giá KPI Quý IV (Đã chuẩn hóa Trọng số)</h3><span>Đánh giá kết quả thực hiện theo trọng số chuẩn hóa</span></div>
        <div class="chart-container"><canvas id="chartKPI"></canvas></div>
      </div>
      <div class="panel">
        <div class="panel-header"><h3>Bảng Dữ liệu Đánh giá KPI Chi tiết (5 Vị trí)</h3><span>TBP, BIM KT, BIM KC, BIM MEPF, BIM Hạ tầng</span></div>
        <div class="table-wrap"><table><thead><tr><th>Vị trí</th><th>Phần</th><th>STT</th><th>Nội dung Tiêu chí</th><th>Trọng số</th><th>Tự ĐG</th><th>Cấp trên</th><th>Quy đổi</th></tr></thead><tbody id="tblKPIBody"></tbody></table></div>
      </div>
    </div>
  </section>

  <!-- TAB 5: TIEN DO DU AN MAU & THUC THI -->
  <section id="tab-tasks" class="tab-page">
    <div class="chart-grid-equal">
      <div class="panel">
        <div class="panel-header"><h3>Tiến độ Thực hiện theo 7 Dự Án Mẫu Thực Tế</h3><span id="projChartSubtitle">So sánh Tỷ lệ Hoàn thành vs Đang thực hiện của 7 Dự Án Mẫu</span></div>
        <div class="chart-container"><canvas id="chartProjects"></canvas></div>
      </div>
      <div class="panel">
        <div class="panel-header"><h3>Cơ cấu Trạng thái Công việc</h3><span>Tỷ lệ Đã hoàn thành, Đang triển khai, Quá hạn</span></div>
        <div class="chart-container"><canvas id="chartTaskStatus"></canvas></div>
      </div>
    </div>
    <div class="panel">
      <div class="panel-header"><h3>Chi tiết Tiến độ Công việc (7 Dự Án Mẫu & Hệ thống)</h3><span id="tasksCountLabel" style="color:var(--accent-cyan); font-weight:700;"></span></div>
      <div class="table-wrap"><table><thead><tr><th>Mã</th><th>Nhóm</th><th>Dự Án Mẫu / Hạng mục</th><th>Nội dung Công việc</th><th>Tình trạng</th><th>Bắt đầu</th><th>Kết thúc</th><th>Hạn</th><th>Tiến độ & Kết quả</th><th>Rủi ro / Ghi chú</th></tr></thead><tbody id="tblTasksBody"></tbody></table></div>
    </div>
  </section>
</main>

<script>
const hrData = {json.dumps(df_hr.to_dict(orient="records"), ensure_ascii=False)};
const raciData = {json.dumps(df_raci.to_dict(orient="records"), ensure_ascii=False)};
const docsData = {json.dumps(df_docs.to_dict(orient="records"), ensure_ascii=False)};
const slaData = {json.dumps(df_sla.to_dict(orient="records"), ensure_ascii=False)};
const kpiData = {json.dumps(df_kpi.to_dict(orient="records"), ensure_ascii=False)};
const clData = {json.dumps(df_cl.to_dict(orient="records"), ensure_ascii=False)};
const taskData = {json.dumps(df_tasks.to_dict(orient="records"), ensure_ascii=False)};

Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255,255,255,0.06)';

let chartHRInstance = null;
let chartRACIInstance = null;
let chartSLAInstance = null;
let chartDocsDeptInstance = null;
let chartDocsTypeInstance = null;
let chartKPIInstance = null;
let chartProjectsInstance = null;
let chartTaskStatusInstance = null;

function switchTab(tabId, btn) {{
  document.querySelectorAll('.tab-page').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
  const target = document.getElementById(tabId);
  if (target) target.classList.add('active');
  if (btn) btn.classList.add('active');
}}

function initTables() {{
  document.getElementById('tblStrategyBody').innerHTML = clData.map(r => `
    <tr><td><b>${{r.MaChiTieuCL}}</b></td><td><span class="pill pill-p2">${{r.PhanLoai}}</span></td><td>${{r.NoiDungChiTiet}}</td><td><b>${{r.DonViTinh}}</b></td></tr>
  `).join('');

  document.getElementById('tblHRBody').innerHTML = hrData.map(r => `
    <tr>
      <td><b>${{r.TenNhom}}</b></td><td>${{r.ViTri}}</td><td>${{r.NhanSuChuChot}}</td>
      <td><span class="pill ${{r.CapBac==='Lead Bộ Môn'?'pill-a':(r.CapBac==='Quản lý'?'pill-p1':'pill-p2')}}">${{r.CapBac}}</span></td>
      <td><b>${{r.DinhBienKeHoach}}</b></td><td>${{r.NhanSuHienTai_T04_2026}}</td>
      <td style="color:${{r.NghiViec_T04_2026>0?'#fb7185':'#94a3b8'}}">${{r.NghiViec_T04_2026}}</td>
      <td><b>${{r.NhanSuConLai}}</b></td>
      <td style="color:${{r.ThieuHutDinhBien>0?'#fbbf24':'#34d399'}}"><b>${{r.ThieuHutDinhBien}}</b></td>
      <td>${{r.GhiChuTrangThai}}</td>
    </tr>
  `).join('');

  document.getElementById('tblKPIBody').innerHTML = kpiData.map(r => `
    <tr>
      <td><b>${{r.TenViTri}}</b></td><td>${{r.PhanDanhGia}}</td><td>${{r.STT}}</td><td>${{r.NoiDungTieuChi}}</td>
      <td><b>${{(r.TrongSo_ChuanHoa_FixDiv0*100).toFixed(0)}}%</b></td><td>${{r.Diem_Q4_TuDanhGia}}</td>
      <td><b>${{r.Diem_Q4_CapTren}}</b></td><td><span class="pill pill-r">${{r.DiemQuyDoi_Q4_CapTren.toFixed(3)}}</span></td>
    </tr>
  `).join('');

  updateDocsFilter(false);
  updateRaciFilter(false);
  updateTasksFilter(false);
}}

function updateDocsFilter(autoSwitch = false) {{
  const bm = document.getElementById('slicerBoMon').value;
  if (autoSwitch && bm !== 'ALL') {{
    switchTab('tab-docs', document.getElementById('btnNavDocs'));
  }}
  const filtered = bm === 'ALL' ? docsData : docsData.filter(d => d.MaBoMon === bm);
  const leadMap = {{ KC: 'Nhân sự D', KT: 'Nhân sự E', DIEN: 'Nhân sự F', HVAC: 'Nhân sự G', CTN: 'Nhân sự F', PCCC: 'Nhân sự F' }};
  const labelEl = document.getElementById('docsCountLabel');
  if (labelEl) {{
    labelEl.innerText = bm === 'ALL'
      ? `Đang hiển thị toàn bộ 115 tài liệu chuẩn hóa 6 bộ môn`
      : `Đang lọc Bộ môn: ${{bm}} (${{filtered.length}} tài liệu) | Lead phụ trách: ${{leadMap[bm] || 'Chưa định danh'}}`;
  }}

  document.getElementById('tblDocsBody').innerHTML = filtered.map(r => `
    <tr>
      <td><b>${{r.MaTaiLieu}}</b></td><td>${{r.TenBoMon}}</td><td><b>${{r.LeadPhuTrach}}</b></td><td>${{r.TenTaiLieu}}</td>
      <td>${{r.NhomTaiLieu}}</td><td><span class="pill ${{r.MucDoUuTien.startsWith('P1')?'pill-p1':'pill-p2'}}">${{r.MucDoUuTien}}</span></td>
      <td>${{r.TrangThaiTrienKhai}}</td><td style="color:${{r.GhiChuRasoát.includes('Lưu ý')?'#fbbf24':'#94a3b8'}}">${{r.GhiChuRasoát}}</td>
    </tr>
  `).join('');

  if (chartDocsTypeInstance) {{
    const types = [...new Set(filtered.map(d => d.NhomTaiLieu))];
    chartDocsTypeInstance.data.labels = types;
    chartDocsTypeInstance.data.datasets[0].data = types.map(t => filtered.filter(d => d.NhomTaiLieu === t).length);
    chartDocsTypeInstance.update();
  }}
}}

function updateRaciFilter(autoSwitch = false) {{
  const p = document.getElementById('slicerPerson').value;
  if (autoSwitch && p !== 'ALL') {{
    switchTab('tab-raci', document.getElementById('btnNavRaci'));
  }}
  const filtered = p === 'ALL' ? raciData : raciData.filter(d => d.HoTenNhanSu === p);
  const labelEl = document.getElementById('raciCountLabel');
  if (labelEl) {{
    labelEl.innerText = p === 'ALL'
      ? `Đang hiển thị toàn bộ 9 nhân sự (${{raciData.length}} lượt phân công)`
      : `Đang lọc: ${{p}} (${{filtered.length}} nhiệm vụ được giao trên ma trận RACI)`;
  }}

  document.getElementById('tblRACIBody').innerHTML = filtered.map(r => `
    <tr>
      <td>${{r.NhomNhiemVu}}</td><td><b>${{r.MaNhiemVu}}</b></td><td>${{r.TenNhiemVu}}</td><td><b>${{r.HoTenNhanSu}}</b></td>
      <td>${{r.BoMon}}</td><td><span class="pill ${{r.VaiTro_RACI==='R'?'pill-r':(r.VaiTro_RACI==='A'?'pill-a':'pill-p2')}}">${{r.VaiTro_RACI}}</span></td>
      <td>${{r.MoTaVaiTro}}</td>
    </tr>
  `).join('');

  if (chartRACIInstance) {{
    const people = p === 'ALL' ? [...new Set(raciData.map(r => r.HoTenNhanSu))] : [p];
    const countRole = (pers, role) => raciData.filter(r => r.HoTenNhanSu === pers && r.VaiTro_RACI === role).length;
    chartRACIInstance.data.labels = people;
    chartRACIInstance.data.datasets[0].data = people.map(pers => countRole(pers, 'R'));
    chartRACIInstance.data.datasets[1].data = people.map(pers => countRole(pers, 'A'));
    chartRACIInstance.data.datasets[2].data = people.map(pers => countRole(pers, 'S'));
    chartRACIInstance.data.datasets[3].data = people.map(pers => countRole(pers, 'I'));
    chartRACIInstance.update();
  }}
}}

function updateTasksFilter(autoSwitch = false) {{
  const proj = document.getElementById('slicerTaskProject').value;
  if (autoSwitch && proj !== 'ALL') {{
    switchTab('tab-tasks', document.getElementById('btnNavTasks'));
  }}
  let filtered = taskData;
  if (proj !== 'ALL') {{
    if (proj === 'Dự Án Mẫu') {{
      filtered = filtered.filter(t => t.HangMuc_DuAn === 'Dự Án Mẫu' || t.NhomCongViec === 'Dự Án Mẫu (Thi công & Triển khai)');
    }} else if (proj === 'Chuẩn hóa Bộ môn Thiết kế' || proj === 'Quản trị & Tổ chức') {{
      filtered = filtered.filter(t => t.NhomCongViec === proj);
    }} else {{
      filtered = filtered.filter(t => t.HangMuc_DuAn === proj);
    }}
  }}

  const doneCount = filtered.filter(t => t.TinhTrang === 'Đã hoàn thành').length;
  const inProgCount = filtered.filter(t => t.TinhTrang === 'Đang thực hiện').length;
  const overdueCount = filtered.filter(t => t.TinhTrang === 'Quá hạn').length;
  const pendingCount = filtered.filter(t => t.TinhTrang === 'Chưa thực hiện').length;
  const pct = filtered.length > 0 ? ((doneCount / filtered.length) * 100).toFixed(1) : 0;

  const labelEl = document.getElementById('tasksCountLabel');
  if (labelEl) {{
    labelEl.innerHTML = proj === 'ALL'
      ? `Đang hiển thị toàn bộ 214 công việc (7 Dự Án Mẫu & Hệ thống) | Hoàn thành: ${{doneCount}} | Đang làm: ${{inProgCount}} | Quá hạn: ${{overdueCount}}`
      : `<b style="color:var(--accent-cyan); font-size:13px;">${{proj}}</b>: ${{filtered.length}} việc | Hoàn thành: <b style="color:#34d399">${{doneCount}} (${{pct}}%)</b> | Đang làm: ${{inProgCount}}${{overdueCount > 0 ? ` | Quá hạn: <b style="color:#f87171">${{overdueCount}}</b>` : ''}}`;
  }}

  document.getElementById('tblTasksBody').innerHTML = filtered.map(r => {{
    let pillClass = 'pill-progress';
    if (r.TinhTrang === 'Đã hoàn thành') pillClass = 'pill-done';
    else if (r.TinhTrang === 'Quá hạn') pillClass = 'pill-overdue';
    else if (r.TinhTrang === 'Chưa thực hiện') pillClass = 'pill-pending';
    return `
      <tr>
        <td><b>${{r.MaCongViec}}</b></td>
        <td><span class="pill pill-p2">${{r.NhomCongViec}}</span></td>
        <td><b>${{r.HangMuc_DuAn}}</b></td>
        <td>${{r.NoiDungCongViec}}</td>
        <td><span class="pill ${{pillClass}}">${{r.TinhTrang}}</span></td>
        <td>${{r.NgayBatDau}}</td>
        <td>${{r.NgayKetThuc}}</td>
        <td>${{r.HanHoanThanh}}</td>
        <td>${{r.TienDoChiTiet || r.KetQuaChatLuong || '-'}}</td>
        <td style="color:${{r.RuiRo_KhoKhan ? '#fbbf24' : '#94a3b8'}}">${{r.RuiRo_KhoKhan || r.GhiChu || '-'}}</td>
      </tr>
    `;
  }}).join('');

  if (chartProjectsInstance) {{
    if (proj === 'ALL') {{
      const projNames = ['Dự Án Mẫu (87 việc)', 'Chuẩn hóa 6 Bộ môn (115 việc)', 'Quản trị & Văn hóa (12 việc)'];
      const projGroupKeys = ['Dự Án Mẫu (Thi công & Triển khai)', 'Chuẩn hóa Bộ môn Thiết kế', 'Quản trị & Tổ chức'];
      chartProjectsInstance.data.labels = projNames;
      chartProjectsInstance.data.datasets[0].data = projGroupKeys.map(k => taskData.filter(t => t.NhomCongViec === k && t.TinhTrang === 'Đã hoàn thành').length);
      chartProjectsInstance.data.datasets[1].data = projGroupKeys.map(k => taskData.filter(t => t.NhomCongViec === k && (t.TinhTrang === 'Đang thực hiện' || t.TinhTrang === 'Quá hạn' || t.TinhTrang === 'Chưa thực hiện')).length);
    }} else {{
      chartProjectsInstance.data.labels = [proj];
      chartProjectsInstance.data.datasets[0].data = [doneCount];
      chartProjectsInstance.data.datasets[1].data = [inProgCount + overdueCount + pendingCount];
    }}
    chartProjectsInstance.update();
  }}

  if (chartTaskStatusInstance) {{
    chartTaskStatusInstance.data.datasets[0].data = [doneCount, inProgCount, overdueCount, pendingCount];
    chartTaskStatusInstance.update();
  }}
}}

function resetAllFilters() {{
  document.getElementById('slicerPerson').value = 'ALL';
  document.getElementById('slicerTaskProject').value = 'ALL';
  document.getElementById('slicerBoMon').value = 'ALL';
  updateRaciFilter(false);
  updateTasksFilter(false);
  updateDocsFilter(false);
}}

window.addEventListener('DOMContentLoaded', () => {{
  // 1. Chart HR
  const hrGroups = {{}};
  hrData.forEach(r => {{
    if (!hrGroups[r.TenNhom]) hrGroups[r.TenNhom] = {{ plan: 0, rem: 0 }};
    hrGroups[r.TenNhom].plan += r.DinhBienKeHoach;
    hrGroups[r.TenNhom].rem += r.NhanSuConLai;
  }});
  const hrLabels = Object.keys(hrGroups);
  chartHRInstance = new Chart(document.getElementById('chartHR'), {{
    type: 'bar',
    data: {{
      labels: hrLabels,
      datasets: [
        {{ label: 'Định biên Kế hoạch (30)', data: hrLabels.map(k => hrGroups[k].plan), backgroundColor: '#3b82f6', borderRadius: 5 }},
        {{ label: 'Nhân sự Còn lại T04/2026 (24)', data: hrLabels.map(k => hrGroups[k].rem), backgroundColor: '#10b981', borderRadius: 5 }}
      ]
    }},
    options: {{ responsive: true, maintainAspectRatio: false }}
  }});

  // 2. Chart RACI
  const people = [...new Set(raciData.map(r => r.HoTenNhanSu))];
  const countRole = (p, role) => raciData.filter(r => r.HoTenNhanSu === p && r.VaiTro_RACI === role).length;
  chartRACIInstance = new Chart(document.getElementById('chartRACI'), {{
    type: 'bar',
    data: {{
      labels: people,
      datasets: [
        {{ label: 'R (Trực tiếp thực hiện)', data: people.map(p => countRole(p, 'R')), backgroundColor: '#10b981' }},
        {{ label: 'A (Chịu trách nhiệm cuối)', data: people.map(p => countRole(p, 'A')), backgroundColor: '#f59e0b' }},
        {{ label: 'S (Hỗ trợ)', data: people.map(p => countRole(p, 'S')), backgroundColor: '#3b82f6' }},
        {{ label: 'I (Được thông báo)', data: people.map(p => countRole(p, 'I')), backgroundColor: '#475569' }}
      ]
    }},
    options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: {{ x: {{ stacked: true }}, y: {{ stacked: true }} }} }}
  }});

  // 3. Chart SLA
  chartSLAInstance = new Chart(document.getElementById('chartSLA'), {{
    type: 'bar',
    data: {{
      labels: ['1. Tiếp nhận (2h)', '2. Hoạch định (2h)', '3. Phân công (2h)', '4. Thực thi & AI (1-2d)', '5. QA/QC & Model Health (4h)', '6. Nghiệm thu & Duyệt (2h)', '7. Đóng CDE (1h)'],
      datasets: [
        {{ label: 'QT BIM Shop (Chuẩn 5 Ngày)', data: [0.5, 0.5, 0.5, 2.5, 0.5, 0.4, 0.1], backgroundColor: '#06b6d4' }},
        {{ label: 'QT BIM Combine (Chuẩn 3 Ngày - AI Agent)', data: [0.25, 0.25, 0.25, 1.5, 0.4, 0.25, 0.1], backgroundColor: '#8b5cf6' }},
        {{ label: 'QT BIM QS (Chuẩn 3 Ngày - AI Agent)', data: [0.25, 0.25, 0.25, 1.5, 0.4, 0.25, 0.1], backgroundColor: '#f59e0b' }}
      ]
    }},
    options: {{ responsive: true, maintainAspectRatio: false }}
  }});

  // 4. Chart Docs Dept
  const depts = ['Thiết kế Kết cấu', 'Thiết kế Kiến trúc', 'Thiết kế Điện', 'Thiết kế HVAC', 'Thiết kế Cấp thoát nước', 'Thiết kế PCCC'];
  chartDocsDeptInstance = new Chart(document.getElementById('chartDocsDept'), {{
    type: 'bar',
    data: {{
      labels: depts,
      datasets: [{{ label: 'Số lượng Tài liệu Chuẩn hóa', data: [23, 20, 18, 18, 18, 18], backgroundColor: ['#06b6d4', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#f43f5e'], borderRadius: 6 }}]
    }},
    options: {{ responsive: true, maintainAspectRatio: false }}
  }});

  // 5. Chart Docs Type
  const types = [...new Set(docsData.map(d => d.NhomTaiLieu))];
  chartDocsTypeInstance = new Chart(document.getElementById('chartDocsType'), {{
    type: 'doughnut',
    data: {{
      labels: types,
      datasets: [{{ data: types.map(t => docsData.filter(d => d.NhomTaiLieu === t).length), backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4'] }}]
    }},
    options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ position: 'right' }} }} }}
  }});

  // 6. Chart KPI
  chartKPIInstance = new Chart(document.getElementById('chartKPI'), {{
    type: 'bar',
    data: {{
      labels: ['Phần I: Tinh thần Thái độ (Thang 5)', 'Phần II: Kết quả Công việc KPI (Thang 5)', 'Tổng Điểm Xếp Hạng Năm (Hệ 1.0)'],
      datasets: [
        {{ label: 'Tự đánh giá (Trung bình)', data: [4.75, 4.75, 0.95], backgroundColor: '#3b82f6', borderRadius: 5 }},
        {{ label: 'Cấp trên đánh giá (Nhân sự A)', data: [4.00, 4.25, 0.83], backgroundColor: '#10b981', borderRadius: 5 }}
      ]
    }},
    options: {{ responsive: true, maintainAspectRatio: false }}
  }});

  // 7. Chart Projects
  const projNames = ['Dự Án Mẫu (87 việc)', 'Chuẩn hóa 6 Bộ môn (115 việc)', 'Quản trị & Văn hóa (12 việc)'];
  const projGroupKeys = ['Dự Án Mẫu (Thi công & Triển khai)', 'Chuẩn hóa Bộ môn Thiết kế', 'Quản trị & Tổ chức'];
  chartProjectsInstance = new Chart(document.getElementById('chartProjects'), {{
    type: 'bar',
    data: {{
      labels: projNames,
      datasets: [
        {{ label: 'Đã hoàn thành', data: projGroupKeys.map(k => taskData.filter(t => t.NhomCongViec === k && t.TinhTrang === 'Đã hoàn thành').length), backgroundColor: '#10b981', borderRadius: 4 }},
        {{ label: 'Đang triển khai / Quá hạn', data: projGroupKeys.map(k => taskData.filter(t => t.NhomCongViec === k && (t.TinhTrang === 'Đang thực hiện' || t.TinhTrang === 'Quá hạn' || t.TinhTrang === 'Chưa thực hiện')).length), backgroundColor: '#3b82f6', borderRadius: 4 }}
      ]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      scales: {{ x: {{ stacked: true }}, y: {{ stacked: true }} }}
    }}
  }});

  // 8. Chart Task Status
  const stLabels = ['Đã hoàn thành', 'Đang thực hiện', 'Quá hạn', 'Chưa thực hiện'];
  chartTaskStatusInstance = new Chart(document.getElementById('chartTaskStatus'), {{
    type: 'doughnut',
    data: {{
      labels: stLabels,
      datasets: [{{
        data: stLabels.map(s => taskData.filter(t => t.TinhTrang === s).length),
        backgroundColor: ['#10b981', '#3b82f6', '#f43f5e', '#64748b'],
        borderWidth: 0
      }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{ legend: {{ position: 'right' }} }}
    }}
  }});

  initTables();
}});
</script>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(OUT_HTML_DASHBOARD, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ 1. Đã cập nhật file Excel DataModel: {os.path.abspath(OUT_XLSX)}")
print(f"✅ 2. Đã cập nhật Web Dashboard HTML  : {os.path.abspath(OUT_HTML)}")
print(f"✅ 3. Đã tạo bản sao index.html        : {os.path.abspath(OUT_HTML_DASHBOARD)}")

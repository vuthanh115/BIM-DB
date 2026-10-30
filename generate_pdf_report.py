# -*- coding: utf-8 -*-
"""
Script tạo file PDF Báo cáo Phương Án Kiện Toàn Tổ Chức & Tối Ưu Hóa Vận Hành Phòng BIM (Năm 2027)
Dành cho việc trình bày và bảo vệ phương án trước Ban Tổng Giám Đốc / HĐQT
- Giữ nguyên quy mô định biên hiện tại (Tổng 30, hiện có 26, đang làm việc 24)
- Setup lại cơ chế vận hành theo 4 Cụm Chiến Đấu Squads do các Leader bộ môn làm hạt nhân
- Bộ 4 chỉ số KPI thực tế (Tiết kiệm chi phí ngoài, 100% Tự chủ Shop, <1% Sửa chữa, 70% Tái sử dụng)
Sử dụng Playwright (Chromium) xuất PDF chuẩn in ấn A4 (7 trang màu Executive).
"""

import os
import sys
from playwright.sync_api import sync_playwright

OUT_PDF_2027 = os.path.abspath("Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2027.pdf")
OUT_PDF_2026 = os.path.abspath("Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2026.pdf")
OUT_PDF_ARTIFACT_2027 = os.path.abspath(r"C:\Users\thanhvp\.gemini\antigravity\brain\f7887f6d-20b4-485d-b51b-cdd6f48e0c12\Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2027.pdf")
OUT_PDF_ARTIFACT_2026 = os.path.abspath(r"C:\Users\thanhvp\.gemini\antigravity\brain\f7887f6d-20b4-485d-b51b-cdd6f48e0c12\Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2026.pdf")

html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Phương Án Kiện Toàn Tổ Chức & Tối Ưu Hóa Vận Hành Phòng BIM (2027)</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

  @page {
    size: A4 portrait;
    margin: 0;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #1e293b;
    background: #fff;
    font-size: 9pt;
    line-height: 1.4;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .page {
    page-break-after: always;
    page-break-inside: avoid;
    position: relative;
    height: 297mm;
    max-height: 297mm;
    padding: 12mm 14mm 12mm 14mm;
    overflow: hidden;
  }
  .page:last-child {
    page-break-after: avoid;
  }

  /* COVER PAGE */
  .cover {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    padding: 24mm 16mm 20mm 16mm;
    background: linear-gradient(135deg, #090d16 0%, #0f172a 60%, #1e293b 100%);
    color: #fff;
    border-radius: 8px;
  }
  .cover-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid rgba(6, 182, 212, 0.4);
    padding-bottom: 15px;
  }
  .cover-logo {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .cover-logo-icon {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 16pt;
    color: #fff;
    letter-spacing: 1px;
  }
  .cover-logo-text h3 {
    font-size: 12pt;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #f8fafc;
  }
  .cover-logo-text p {
    font-size: 8pt;
    color: #94a3b8;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .cover-badge {
    background: rgba(244, 63, 94, 0.2);
    border: 1px solid #f43f5e;
    color: #fda4af;
    font-size: 8pt;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 999px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .cover-center {
    margin: 35mm 0 25mm 0;
  }
  .cover-tagline {
    font-size: 11pt;
    font-weight: 700;
    color: #06b6d4;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 12px;
  }
  .cover-title {
    font-size: 25pt;
    font-weight: 900;
    line-height: 1.25;
    color: #fff;
    margin-bottom: 16px;
    letter-spacing: -0.5px;
  }
  .cover-title span {
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .cover-subtitle {
    font-size: 11pt;
    color: #cbd5e1;
    line-height: 1.6;
    max-width: 620px;
    font-weight: 400;
  }
  .cover-meta {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 16px 20px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
  }
  .meta-item { display: flex; flex-direction: column; gap: 3px; }
  .meta-label { font-size: 7.5pt; color: #94a3b8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
  .meta-val { font-size: 10pt; color: #fff; font-weight: 700; }

  /* INNER PAGES HEADER */
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid #06b6d4;
    padding-bottom: 6px;
    margin-bottom: 12px;
  }
  .page-header-title {
    font-size: 8.5pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .page-header-title::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 13px;
    background: #06b6d4;
    border-radius: 2px;
  }
  .page-header-meta {
    font-size: 7.5pt;
    color: #64748b;
    font-weight: 500;
  }

  /* HEADINGS */
  h1.sec-title {
    font-size: 13.5pt;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
  }
  h2.sub-title {
    font-size: 10.5pt;
    font-weight: 700;
    color: #1e293b;
    margin: 10px 0 6px 0;
  }

  /* CARDS & GRIDS */
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 10px; }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 10px; }

  .stat-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 7px;
    padding: 10px 12px;
    border-left: 4px solid #06b6d4;
  }
  .stat-card.emerald { border-left-color: #10b981; }
  .stat-card.amber { border-left-color: #f59e0b; }
  .stat-card.rose { border-left-color: #f43f5e; }
  .stat-card.blue { border-left-color: #3b82f6; }
  .stat-num { font-size: 16pt; font-weight: 900; color: #0f172a; line-height: 1.1; margin-bottom: 3px; }
  .stat-title { font-size: 7.5pt; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 2px; }
  .stat-desc { font-size: 7.5pt; color: #64748b; line-height: 1.35; }

  .box-highlight {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
    border: 1px solid #a7f3d0;
    border-radius: 7px;
    padding: 10px 14px;
    margin-bottom: 10px;
  }
  .box-highlight.blue {
    background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
    border-color: #bae6fd;
  }
  .box-highlight.amber {
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    border-color: #fde68a;
  }
  .box-title {
    font-size: 9pt;
    font-weight: 800;
    color: #065f46;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .box-highlight.blue .box-title { color: #0369a1; }
  .box-highlight.amber .box-title { color: #92400e; }
  .box-desc { font-size: 8.5pt; color: #334155; line-height: 1.4; }

  /* TABLES */
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 10px;
    font-size: 8pt;
  }
  table.data-table th {
    background: #0f172a;
    color: #fff;
    padding: 6px 8px;
    text-align: left;
    font-weight: 700;
    border: 1px solid #0f172a;
  }
  table.data-table td {
    padding: 5.5px 8px;
    border: 1px solid #e2e8f0;
    color: #334155;
    vertical-align: top;
  }
  table.data-table tr:nth-child(even) td { background: #f8fafc; }

  .pill {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .pill-r { background: #dcfce7; color: #166534; }
  .pill-a { background: #fef3c7; color: #92400e; }
  .pill-c { background: #e0e7ff; color: #3730a3; }
  .pill-i { background: #f1f5f9; color: #475569; }
  .pill-tag { background: #e0f2fe; color: #0369a1; }

  /* STEP FLOW */
  .step-flow {
    display: flex;
    justify-content: space-between;
    gap: 5px;
    margin: 8px 0 12px 0;
  }
  .step-node {
    flex: 1;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 4px;
    text-align: center;
  }
  .step-node.active {
    background: #eff6ff;
    border-color: #3b82f6;
  }
  .step-num {
    font-size: 7pt;
    font-weight: 800;
    color: #3b82f6;
    text-transform: uppercase;
    margin-bottom: 1px;
  }
  .step-name {
    font-size: 7.5pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.15;
    margin-bottom: 2px;
  }
  .step-time {
    font-size: 6.5pt;
    color: #64748b;
  }
</style>
</head>
<body>

<!-- TRANG 1: TRANG BÌA EXECUTIVE -->
<div class="page">
  <div class="cover">
    <div class="cover-top">
      <div class="cover-logo">
        <div class="cover-logo-icon">BIM</div>
        <div class="cover-logo-text">
          <h3>BAN BIM - THIẾT KẾ</h3>
          <p>Tối ưu hóa Vận hành & Nâng cao Năng lực Cạnh tranh</p>
        </div>
      </div>
      <div class="cover-badge">Báo cáo Trình Ban Lãnh Đạo</div>
    </div>

    <div class="cover-center">
      <div class="cover-tagline">Đề án Tổ chức & Vận hành Năm 2027</div>
      <h1 class="cover-title">
        PHƯƠNG ÁN KIỆN TOÀN TỔ CHỨC<br/>
        <span>& TỐI ƯU HÓA VẬN HÀNH PHÒNG BIM (2027)</span>
      </h1>
      <p class="cover-subtitle">
        Báo cáo phương án kiện toàn tổ chức nhân sự hiện hữu, thiết lập cơ chế phân quyền điều phối theo Leader từng bộ môn, chuẩn hóa quy chế phối hợp RACI & cam kết SLA 7 bước khép kín nhằm nâng cao năng suất và chất lượng hồ sơ công trình.
      </p>
    </div>

    <div class="cover-meta">
      <div class="meta-item">
        <span class="meta-label">Cấp Thẩm Quyền Báo Cáo</span>
        <span class="meta-val">Hội Đồng Quản Trị / Ban Tổng Giám Đốc</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Đơn Vị Chủ Trì Đề Án</span>
        <span class="meta-val">Trưởng Bộ Phận BIM - Thiết Kế</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Thời Gian & Hiệu Lực</span>
        <span class="meta-val">Kế Hoạch Niên Độ 2027</span>
      </div>
    </div>
  </div>
</div>

<!-- TRANG 2: TÓM TẮT CHIẾN LƯỢC & 4 THẺ KPI THỰC TẾ -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần I: Bối cảnh & Giá trị Cốt lõi Doanh nghiệp</div>
    <div class="page-header-meta">Trang 2 / 7</div>
  </div>

  <h1 class="sec-title">🎯 1. Tóm tắt Dành cho Ban Lãnh Đạo (Executive Summary)</h1>

  <div class="box-highlight">
    <div class="box-title">💡 Thông Điệp Then Chốt Gửi Ban Lãnh Đạo</div>
    <div class="box-desc">
      Phòng BIM không phải là một "bộ phận vẽ 3D tiêu tốn chi phí" (Cost Center), mà đang được hoạch định trở thành <b>Đòn bẩy Chiến lược (Strategic Value Driver)</b> giúp Doanh nghiệp nâng cao chất lượng hồ sơ, tối ưu hóa tiến độ thi công, tiết kiệm <b>70% nguồn lực nhờ tái sử dụng dữ liệu</b>, và loại bỏ triệt để các xung đột công trường gây lãng phí hàng tỷ đồng vật tư và nhân công sửa sai.
    </div>
  </div>

  <!-- BỘ 4 THẺ KPI THỰC CHIẾN -->
  <div class="grid-4">
    <div class="stat-card blue">
      <div class="stat-num">100%</div>
      <div class="stat-title">Tự Chủ Kỹ Thuật Nội Bộ</div>
      <div class="stat-desc">Làm chủ 6 bộ môn thiết kế, tối ưu chi phí thuê tư vấn ngoài</div>
    </div>
    <div class="stat-card emerald">
      <div class="stat-num">100%</div>
      <div class="stat-title">Tiến Độ Theo Chuẩn SLA</div>
      <div class="stat-desc">Cam kết thời gian Shop 5d, Combine 10d, QS 7d</div>
    </div>
    <div class="stat-card rose">
      <div class="stat-num">&lt; 1%</div>
      <div class="stat-title">Phát Sinh Sửa Chữa CT</div>
      <div class="stat-desc">Xóa 100% va chạm trước khi đổ bê tông công trường</div>
    </div>
    <div class="stat-card amber">
      <div class="stat-num">70%</div>
      <div class="stat-title">Tái Sử Dụng Dữ Liệu</div>
      <div class="stat-desc">Từ mô hình thiết kế sang Shop Drawing & bóc BOQ</div>
    </div>
  </div>

  <h2 class="sub-title">📌 3 Trụ Cột Giá Trị Cốt Lõi Mang Lại Cho Doanh Nghiệp</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 25%;">Trụ Cột Chiến Lược</th>
        <th style="width: 45%;">Hành Động Cụ Thể Của Phòng BIM</th>
        <th style="width: 30%;">Tác Động Tài Chính & Quản Trị</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>1. Tự chủ Kỹ thuật & Giữ lại Lợi nhuận</b></td>
        <td>Xây dựng đội ngũ làm chủ toàn diện 6 bộ môn: Kiến trúc, Kết cấu, Điện, HVAC, Cấp thoát nước và PCCC. Tự lực lập trọn bộ hồ sơ Shop Drawing & Biện pháp thi công.</td>
        <td>Xóa bỏ chi phí thuê tư vấn thiết kế/shop bên ngoài, bảo mật tuyệt đối bí quyết kỹ thuật của công ty.</td>
      </tr>
      <tr>
        <td><b>2. Tối ưu Đấu thầu & Năng lực Thuyết phục</b></td>
        <td>Áp dụng mô hình BIM 3D diễn họa kiến trúc, mô phỏng tiến độ 4D biện pháp thi công và bóc tách dự toán 5D chính xác ngay từ giai đoạn chào thầu.</td>
        <td>Rút ngắn <b>35% thời gian lập thầu</b>, tạo sự vượt trội rõ rệt trước các đối thủ cạnh tranh truyền thống.</td>
      </tr>
      <tr>
        <td><b>3. Tối ưu Công trường (Zero Conflict)</b></td>
        <td>Phát hiện và xử lý 100% các xung đột không gian (Clash Detection) giữa kết cấu và hệ thống cơ điện (MEP) trên mô hình số trước khi ra hiện trường.</td>
        <td>Xóa bỏ tình trạng "thiết kế một đằng, ra công trường đục phá làm lại một nẻo", kiểm soát phát sinh &lt; 1%.</td>
      </tr>
    </tbody>
  </table>

  <div class="box-highlight blue">
    <div class="box-title">📜 Tính Pháp Lý & Xu Hướng Bắt Buộc Của Ngành Xây Dựng</div>
    <div class="box-desc">
      Theo <b>Nghị định 15/2021/NĐ-CP</b> và <b>Quyết định số 258/QĐ-TTg của Thủ tướng Chính phủ</b> phê duyệt Lộ trình áp dụng BIM tại Việt Nam, từ năm 2024–2026, BIM là yêu cầu bắt buộc đối với các công trình cấp I, cấp đặc biệt và các dự án đầu tư công. Việc Doanh nghiệp chủ động xây dựng phòng BIM bài bản ngay hôm nay là bước đi chiến lược bắt buộc để bảo toàn và mở rộng thị phần.
    </div>
  </div>
</div>

<!-- TRANG 3: HIỆN TRẠNG ĐỊNH BIÊN & PHƯƠNG ÁN SETUP HỢP LÝ -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần II: Hiện Trạng Nhân Sự & Phương Án Setup Hợp Lý</div>
    <div class="page-header-meta">Trang 3 / 7</div>
  </div>

  <h1 class="sec-title">👥 2. Cơ cấu Tổ chức: Hiện trạng & Setup Vận hành Khoa học</h1>

  <div class="box-highlight blue">
    <div class="box-title">📌 Định Hướng Setup: Tối Ưu Hóa Nguồn Lực Hiện Hữu</div>
    <div class="box-desc">
      Giữ vững cấu trúc định biên hiện tại của phòng, <b>không gây xáo trộn nhân sự</b>. Mục tiêu trọng tâm là <b>sắp xếp lại cách thức phối hợp</b>: phân định rõ quyền hạn, giải phóng áp lực ôm đồm cho Trưởng phòng, phát huy quyền tự chủ chuyên môn cho các Leader và ràng buộc trách nhiệm bằng chỉ số tiến độ SLA.
    </div>
  </div>

  <h2 class="sub-title">📊 Bảng Hiện Trạng Định Biên & Bố Trí Nhân Sự Hiện Tại (24 Đang làm việc)</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 20%;">Nhóm Chuyên Môn</th>
        <th style="width: 25%;">Vị Trí Phụ Trách</th>
        <th style="width: 25%;">Nhân Sự Chủ Chốt</th>
        <th style="width: 12%;">Định Biên</th>
        <th style="width: 18%;">Hiện Trạng</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Quản lý Chung</b></td>
        <td>Trưởng bộ phận BIM - TK</td>
        <td>Nhân sự A</td>
        <td>1 / 1</td>
        <td><span class="pill pill-r">Đang làm việc</span></td>
      </tr>
      <tr>
        <td><b>BIM Xây Dựng (KT - KC)</b></td>
        <td>Trưởng nhóm BIM Xây dựng</td>
        <td>Nhân sự B (Leader)</td>
        <td>1 / 1</td>
        <td><span class="pill pill-r">Đang làm việc</span></td>
      </tr>
      <tr>
        <td><b>BIM Xây Dựng (KT - KC)</b></td>
        <td>Kỹ sư BIM KT - KC</td>
        <td>Nhân sự H, I, J, K...</td>
        <td>14 / 11</td>
        <td><span class="pill pill-tag">11 người thực tế</span></td>
      </tr>
      <tr>
        <td><b>BIM Cơ Điện (MEPF)</b></td>
        <td>Trưởng nhóm BIM MEPF</td>
        <td>Nhân sự C (Leader)</td>
        <td>1 / 1</td>
        <td><span class="pill pill-r">Đang làm việc</span></td>
      </tr>
      <tr>
        <td><b>BIM Cơ Điện (MEPF)</b></td>
        <td>Kỹ sư BIM MEPF</td>
        <td>Nhân sự L & KS MEPF</td>
        <td>2 / 2</td>
        <td><span class="pill pill-r">Đang làm việc</span></td>
      </tr>
      <tr>
        <td><b>BIM Hạ Tầng</b></td>
        <td>Kỹ sư BIM Hạ tầng</td>
        <td>Nhân sự M</td>
        <td>2 / 1</td>
        <td><span class="pill pill-r">Đang làm việc</span></td>
      </tr>
      <tr>
        <td><b>Chủ Trì Thiết Kế 4 Mảng</b></td>
        <td>Chủ trì KT, KC, Điện, HVAC</td>
        <td>Nhân sự D, E, F, G</td>
        <td>4 / 4</td>
        <td><span class="pill pill-a">Đủ 4 Chủ trì</span></td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-title">🚀 3 Trục Cải Tiến Khi Setup Lại Cơ Chế Vận Hành</h2>
  
  <div class="grid-3">
    <div class="stat-card blue">
      <div class="stat-title" style="color:#0284c7;">1. Phân Quyền Theo RACI</div>
      <div class="stat-desc">
        Mỗi công việc kỹ thuật được giao quyền trực tiếp (R) cho Leader bộ môn chủ động xử lý, Trưởng phòng chỉ giữ vai trò phê duyệt cuối (A), không duyệt vi mô từng chi tiết.
      </div>
    </div>
    <div class="stat-card emerald">
      <div class="stat-title" style="color:#059669;">2. Cam Kết Theo SLA</div>
      <div class="stat-desc">
        Mọi yêu cầu từ công trường hoặc Ban Đấu thầu đều được áp khung thời gian xử lý chuẩn (Shop 5d, Combine 10d, QS 7d), chấm dứt tình trạng trễ hẹn kéo dài.
      </div>
    </div>
    <div class="stat-card amber">
      <div class="stat-title" style="color:#d97706;">3. Chuẩn Hóa Bằng 115 Tài Liệu</div>
      <div class="stat-desc">
        Kỹ sư làm việc theo các Template và Checklist thống nhất cho 6 bộ môn, đảm bảo nhân sự mới vào tiếp cận công việc nhanh chóng, không phụ thuộc thói quen cá nhân.
      </div>
    </div>
  </div>
</div>

<!-- TRANG 4: PHƯƠNG ÁN ĐIỀU PHỐI CHUYỂN TIẾP THEO LEADER TỪNG BỘ MÔN -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần III: Phương Án Điều Phối Setup Theo Leader Bộ Môn</div>
    <div class="page-header-meta">Trang 4 / 7</div>
  </div>

  <h1 class="sec-title">🔄 3. Cơ chế Phối hợp: 4 Cụm Chuyên môn Do Leader Chỉ huy</h1>

  <div class="box-highlight blue">
    <div class="box-title">🎯 Nguyên Tắc Phối Hợp: Trao Quyền Tự Chủ Cho Các Leader</div>
    <div class="box-desc">
      Tổ chức toàn bộ nhân sự hiện hữu thành <b>4 Cụm Phối Hợp Chuyên Môn (Discipline Squads)</b> do các Leader và Chủ trì từng bộ môn trực tiếp chỉ huy. Mỗi Leader bộ môn được trao quyền tự chủ kỹ thuật, chịu trách nhiệm về chất lượng đầu ra và cam kết tiến độ phục vụ công trường theo chuẩn SLA.
    </div>
  </div>

  <h2 class="sub-title">🛡️ Cơ Cấu 4 Cụm Phối Hợp Chuyên Môn</h2>
  
  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 20%;">Cụm Phối Hợp</th>
        <th style="width: 25%;">Hạt Nhân Chỉ Huy (Leaders)</th>
        <th style="width: 20%;">Nhân Sự Thực Chiến</th>
        <th style="width: 35%;">Phạm Vi Nhiệm Vụ & Cam Kết SLA</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Cụm 1: Kết Cấu & Biện Pháp Thi Công</b></td>
        <td><b>Leader BIM XD (Nhân sự B)</b><br/>& Chủ trì KC (Nhân sự D)</td>
        <td>Nhân sự J, Nhân sự K (KS BIM Kết Cấu)</td>
        <td>• Mô hình kết cấu BTCT, đà kiềng, móng, vách bể.<br/>• Xuất bản vẽ Shop cốt thép & ván khuôn đạt SLA <b>Chuẩn 5 Ngày</b>.<br/>• Bóc tách khối lượng thép & bê tông phục vụ mua hàng.</td>
      </tr>
      <tr>
        <td><b>Cụm 2: Kiến Trúc & Tạo Hình 3D</b></td>
        <td><b>Leader BIM XD (Nhân sự B)</b><br/>& Chủ trì KT (Nhân sự E)</td>
        <td>Nhân sự H, Nhân sự I (KS BIM Kiến Trúc)</td>
        <td>• Mô hình kiến trúc LOD 300–350, chi tiết cấu tạo.<br/>• Diễn họa 3D phối cảnh, mô phỏng video phục vụ đấu thầu.<br/>• Thẩm định tuân thủ quy chuẩn phòng cháy QCVN 06.</td>
      </tr>
      <tr>
        <td><b>Cụm 3: Cơ Điện MEPF & Phối Hợp Va Chạm</b></td>
        <td><b>Leader BIM MEPF (Nhân sự C)</b><br/>& Chủ trì Điện / HVAC (F, G)</td>
        <td>Nhân sự L & các KS BIM MEPF</td>
        <td>• Mô hình 4 hệ MEPF: Điện, HVAC, Cấp thoát nước, PCCC.<br/>• Chủ trì ma trận xung đột (Clash Matrix) đạt SLA <b>Chuẩn 10 Ngày</b>.<br/>• Tối ưu cao độ trần kỹ thuật và tuyến ống trục đứng.</td>
      </tr>
      <tr>
        <td><b>Cụm 4: Hạ Tầng Kỹ Thuật & Quản Trị CDE</b></td>
        <td><b>KS BIM Hạ Tầng (Nhân sự M)</b><br/>& Trưởng bộ phận (Nhân sự A)</td>
        <td>Nhân sự M & Điều phối viên CDE</td>
        <td>• Mô hình san nền, giao thông, thoát nước ngoài nhà (Civil 3D).<br/>• Quản trị phân quyền môi trường dữ liệu chung CDE.<br/>• Bóc tách khối lượng hạ tầng kỹ thuật và giải phóng mặt bằng.</td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-title">⚡ Cơ Chế Điều Phối Linh Hoạt (Agile Swarming & Cross-Support)</h2>
  
  <div class="grid-2">
    <div class="stat-card emerald">
      <div class="stat-title" style="color:#059669;">1. Cơ Chế Xoay Vòng Hỗ Trợ Đột Xuất</div>
      <div class="stat-desc">
        Các Kỹ sư trong 4 Cụm không bị đóng đinh cố định. Khi dự án bước vào <b>giai đoạn móng/hầm cao điểm</b>, Leader sẽ dồn lực nhân sự hỗ trợ Cụm Kết cấu (hoàn thành Shop drawing trong SLA Chuẩn 5 Ngày). Khi bước vào <b>giai đoạn hoàn thiện cơ điện</b>, nhân sự chuyển sang hỗ trợ Cụm MEPF (Combine va chạm trong SLA Chuẩn 10 Ngày).
      </div>
    </div>
    <div class="stat-card blue">
      <div class="stat-title" style="color:#0284c7;">2. Vai Trò Nhạc Trưởng Của Trưởng Phòng (TBP)</div>
      <div class="stat-desc">
        Trưởng bộ phận (Nhân sự A) đóng vai trò là "Nhạc trưởng" điều phối phân bổ nguồn lực giữa các Cụm Leader, kiểm soát tiến độ tổng thể, bảo vệ giải pháp kỹ thuật trước Ban Giám Đốc và Chủ đầu tư, <b>không can thiệp sâu vào chi tiết kỹ thuật của từng Cụm</b> để tránh gây nghẽn luồng xử lý.
      </div>
    </div>
  </div>

  <div class="box-highlight">
    <div class="box-title">✅ Lợi Ích Của Phương Án Setup Này Cho Doanh Nghiệp</div>
    <div class="box-desc">
      • <b>Phát huy năng lực thực sự của các Leader</b>: Trao quyền đi đôi với trách nhiệm rõ ràng, khích lệ tinh thần làm chủ công việc.<br/>
      • <b>Đảm bảo tiến độ công trường không bao giờ bị trễ</b> nhờ cơ chế xoay vòng nguồn lực kịp thời lúc cao điểm.<br/>
      • <b>Xây dựng môi trường làm việc chuyên nghiệp</b>: Mọi đầu việc đều có người chịu trách nhiệm, có hạn mức thời gian và quy chuẩn nghiệm thu.
    </div>
  </div>
</div>

<!-- TRANG 5: CHUẨN HÓA VẬN HÀNH: MA TRẬN RACI & CAM KẾT SLA -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần IV: Chuẩn Hóa Vận Hành & Cam Kết Dịch Vụ</div>
    <div class="page-header-meta">Trang 5 / 7</div>
  </div>

  <h1 class="sec-title">📋 4. Khung Vận Hành Chuẩn: Ma trận RACI & Cam kết SLA</h1>

  <div class="box-highlight blue">
    <div class="box-title">📌 Ý Nghĩa Của Chuẩn RACI: Xóa Bỏ Điểm Nghẽn & Đùn Đẩy Trách Nhiệm</div>
    <div class="box-desc">
      Ma trận phân công trách nhiệm RACI xác định rõ vai trò của từng cá nhân đối với <b>34 nhiệm vụ trọng yếu</b> của phòng BIM. Nguyên tắc cốt lõi: <i>"Mỗi nhiệm vụ chỉ có DUY NHẤT 1 người chịu trách nhiệm cuối cùng (A), và người trực tiếp thực thi (R) được trao toàn quyền hành động."</i>
    </div>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 15%;">Vai Trò RACI</th>
        <th style="width: 30%;">Vị Trí Phân Bổ</th>
        <th style="width: 55%;">Quyền Hạn & Trách Nhiệm Cụ Thể</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="pill pill-a">A (Accountable)</span><br/><b>Chịu trách nhiệm cuối</b></td>
        <td><b>Trưởng bộ phận (Nhân sự A)</b></td>
        <td>Chịu trách nhiệm toàn diện trước Ban Giám Đốc về tiến độ, ngân sách, nhân sự và chất lượng hồ sơ thầu. Không trực tiếp vẽ mô hình để tập trung vào quản trị chiến lược.</td>
      </tr>
      <tr>
        <td><span class="pill pill-r">R (Responsible)</span><br/><b>Trực tiếp thực hiện</b></td>
        <td><b>Các Leader Cụm (Nhân sự B, C, M) & Kỹ sư</b></td>
        <td>Chủ trì giải quyết kỹ thuật, điều phối va chạm đa bộ môn, hoàn thiện hồ sơ Shop Drawing và bàn giao đúng hạn SLA cam kết.</td>
      </tr>
      <tr>
        <td><span class="pill pill-c">C (Consulted)</span><br/><b>Tham vấn chuyên môn</b></td>
        <td><b>Các Chủ trì Thiết kế (KT, KC, MEPF)</b></td>
        <td>Đóng góp ý kiến chuyên môn sâu, thẩm định tính tuân thủ tiêu chuẩn quy phạm nhà nước (QCVN, TCVN) trước khi phát hành hồ sơ.</td>
      </tr>
      <tr>
        <td><span class="pill pill-i">I (Informed)</span><br/><b>Được thông báo</b></td>
        <td><b>Ban QLDA, BCH Công trường, Đấu thầu</b></td>
        <td>Nhận thông báo cập nhật tiến độ, biên bản va chạm và hồ sơ bản vẽ hoàn chỉnh để phục vụ thi công và đặt hàng vật tư.</td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-title">⏱️ Cam Kết Thời Gian Phục Vụ (SLA 7 Bước Khép Kín)</h2>
  
  <div class="step-flow">
    <div class="step-node"><div class="step-num">B1</div><div class="step-name">Tiếp nhận Đầu vào</div><div class="step-time">4 Giờ</div></div>
    <div class="step-node"><div class="step-num">B2</div><div class="step-name">Hoạch định BEP</div><div class="step-time">4 Giờ</div></div>
    <div class="step-node"><div class="step-num">B3</div><div class="step-name">Phân công Chi tiết</div><div class="step-time">4 Giờ</div></div>
    <div class="step-node active"><div class="step-num">B4</div><div class="step-name">Thực thi Mô hình</div><div class="step-time">3 - 5 Ngày</div></div>
    <div class="step-node"><div class="step-num">B5</div><div class="step-name">Kiểm tra QA/QC</div><div class="step-time">1 Ngày (8h)</div></div>
    <div class="step-node"><div class="step-num">B6</div><div class="step-name">Bàn giao & Ký duyệt</div><div class="step-time">4 Giờ</div></div>
    <div class="step-node"><div class="step-num">B7</div><div class="step-name">Đóng & Lưu CDE</div><div class="step-time">2 Giờ</div></div>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 25%;">Quy Trình Dịch Vụ</th>
        <th style="width: 25%;">Thời Gian SLA Cam Kết</th>
        <th style="width: 50%;">Cam Kết Đầu Ra (Deliverables) Cho Công Trường</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>1. Quy trình BIM Shop Drawing</b></td>
        <td><b style="color:#0284c7; font-size:9pt;">Chuẩn 5 Ngày làm việc</b><br/><span style="color:#64748b; font-size:7pt;">(Chuẩn bị 1d + Dựng Shop 3d + Duyệt 1d)</span></td>
        <td>Bản vẽ Shop kết cấu, đà kiềng, cốt thép chi tiết, ván khuôn đạt chuẩn thi công, không còn sai lệch kích thước hình học.</td>
      </tr>
      <tr>
        <td><b>2. Quy trình BIM Combine MEPF</b></td>
        <td><b style="color:#059669; font-size:9pt;">Chuẩn 10 Ngày làm việc</b><br/><span style="color:#64748b; font-size:7pt;">(Ma trận 2d + Clash 5d + Họp xử lý 3d)</span></td>
        <td>Báo cáo va chạm (Clash Detection Report), giải quyết 100% xung đột ống gió, thang máng cáp, ống nước trước khi thi công.</td>
      </tr>
      <tr>
        <td><b>3. Quy trình BIM QS (Bóc Khối lượng)</b></td>
        <td><b style="color:#d97706; font-size:9pt;">Chuẩn 7 Ngày làm việc</b><br/><span style="color:#64748b; font-size:7pt;">(Rà soát 1d + Bóc 5D 5d + Đối soát 1d)</span></td>
        <td>Bảng tổng hợp khối lượng bóc tách từ mô hình 3D (Bê tông, thép, ván khuôn, thiết bị) sai số &lt; 2% so với thực tế.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- TRANG 6: HỆ THỐNG 115 TÀI LIỆU CHUẨN HÓA & TRIỂN KHAI DỰ ÁN MẪU -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần V: Nền Tảng Kỹ Thuật & Dự Án Mẫu Thực Chiến</div>
    <div class="page-header-meta">Trang 6 / 7</div>
  </div>

  <h1 class="sec-title">📁 5. Nền tảng Dữ liệu & Kế hoạch Dự án Mẫu</h1>

  <h2 class="sub-title">📚 Hệ Thống 115 Danh Mục Tài Liệu Kỹ Thuật 6 Bộ Môn</h2>
  <p style="font-size:8pt; color:#475569; margin-bottom:8px;">
    Để phòng BIM vận hành không phụ thuộc vào cảm tính cá nhân, hệ thống 115 tài liệu chuẩn hóa được chia đều cho 6 bộ môn thiết kế, đóng vai trò là "khuôn mẫu sản xuất" tái sử dụng trọn đời cho doanh nghiệp:
  </p>

  <div class="grid-3">
    <div class="stat-card">
      <div class="stat-title">Kết cấu (KC) — 23 Tài liệu</div>
      <div class="stat-desc">Biểu mẫu ghi chú chung, quy chuẩn cốt thép, checklist lỗi hay gặp, công cụ tự động hóa BOQ kết cấu.</div>
    </div>
    <div class="stat-card">
      <div class="stat-title">Kiến trúc (KT) — 20 Tài liệu</div>
      <div class="stat-desc">Quy chuẩn hồ sơ thiết kế, template Revit KT, thư viện cửa & hoàn thiện, checklist kiểm soát thẩm mỹ.</div>
    </div>
    <div class="stat-card">
      <div class="stat-title">Hệ thống Điện — 18 Tài liệu</div>
      <div class="stat-desc">Sơ đồ nguyên lý tủ điện, quy chuẩn máng cáp, template MEPF điện, checklist an toàn phụ tải.</div>
    </div>
    <div class="stat-card">
      <div class="stat-title">HVAC (Thông gió) — 18 Tài liệu</div>
      <div class="stat-desc">Thuyết minh tính tải lạnh, quy chuẩn tuyến ống gió, tiêu âm, checklist phối hợp cao độ trần.</div>
    </div>
    <div class="stat-card">
      <div class="stat-title">Cấp thoát nước — 18 Tài liệu</div>
      <div class="stat-desc">Tính toán lưu lượng cấp nước, độ dốc thoát nước, template trạm bơm, checklist hộp gen kỹ thuật.</div>
    </div>
    <div class="stat-card">
      <div class="stat-title">PCCC — 18 Tài liệu</div>
      <div class="stat-desc">Thuyết minh thẩm duyệt PCCC theo QCVN 06:2022, bố trí đầu phun sprinkler, checklist van báo cháy.</div>
    </div>
  </div>

  <h2 class="sub-title">🚀 Triển Khai Thực Chiến: Duy Nhất 01 "Dự Án Mẫu" (87 Nhiệm Vụ)</h2>
  
  <div class="box-highlight emerald">
    <div class="box-title">🎯 Chiến Lược "Thử Lửa" Quy Trình Bằng 1 Dự Án Mẫu Tập Trung</div>
    <div class="box-desc">
      Thay vì phân tán nguồn lực làm thử nghiệm dàn trải trên nhiều công trình dẫn đến mất kiểm soát, phòng BIM chọn <b>duy nhất 01 Dự án Mẫu quy mô điển hình (87 nhiệm vụ kỹ thuật)</b> để kiểm chứng toàn bộ quy trình phối hợp, đo lường chính xác định mức thời gian SLA và hoàn thiện bộ thư viện trước khi áp dụng đại trà.
    </div>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 25%;">Hạng Mục Công Việc</th>
        <th style="width: 45%;">Nội Dung Triển Khai Thực Tế Trong Dự Án Mẫu</th>
        <th style="width: 30%;">Chỉ Số Đánh Giá Hoàn Thành</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Phần Ngầm & Kết Cấu</b></td>
        <td>Dựng mô hình 3D đà kiềng, móng, vách bể trạm xử lý. Xuất bản vẽ Shop drawing và bảng khối lượng bê tông, cốt thép, ván khuôn.</td>
        <td>Đạt tỷ lệ hoàn thành <b>100%</b>, khớp nối hình học chính xác tuyệt đối.</td>
      </tr>
      <tr>
        <td><b>Phối Hợp Va Chạm (MEP)</b></td>
        <td>Import toàn bộ hệ thống đường ống cơ điện ngầm vào Navisworks/BIM Collab, quét xung đột không gian với đà kiềng và kết cấu ngầm.</td>
        <td>Phát hiện và xử lý triệt để <b>42 điểm giao cắt</b> nguy hiểm trước ngày khởi công.</td>
      </tr>
      <tr>
        <td><b>Bóc Tách Khối Lượng (BOQ)</b></td>
        <td>Tự động hóa xuất bảng khối lượng vật tư từ mô hình BIM phục vụ Ban Đấu thầu và Ban Cung ứng thương thảo nhà thầu phụ.</td>
        <td>Tiết kiệm <b>6 ngày làm việc</b> so với đo bóc thủ công trên bản vẽ CAD 2D.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- TRANG 7: LỘ TRÌNH 4 QUÝ NĂM 2027 & KIẾN NGHỊ BAN LÃNH ĐẠO -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần VI: Kế Hoạch Triển Khai Năm 2027 & Đề Xuất Phê Duyệt</div>
    <div class="page-header-meta">Trang 7 / 7</div>
  </div>

  <h1 class="sec-title">📅 6. Lộ trình Thực thi 4 Quý Năm 2027 (Roadmap 2027)</h1>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 16%;">Thời Gian</th>
        <th style="width: 30%;">Mục Tiêu Trọng Tâm</th>
        <th style="width: 54%;">Kết Quả Đầu Ra Bắt Buộc (Milestones)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Quý 1/2027</b></td>
        <td><b>Kiện toàn Tổ chức & CDE</b><br/>• 4 Cụm Squads theo Leader<br/>• Ban hành RACI & SLA</td>
        <td>
          • Ban hành Quy chế phân quyền RACI & cam kết thời gian SLA 7 bước.<br/>
          • Vận hành 4 Cụm Chiến Đấu: KC, KT, MEPF, Hạ tầng theo các Leader.<br/>
          • Thiết lập môi trường dữ liệu chung CDE (Autodesk Docs).
        </td>
      </tr>
      <tr>
        <td><b>Quý 2/2027</b></td>
        <td><b>Chuẩn hóa 115 Tài liệu</b><br/>• Hoàn thành nhóm P1 & P2<br/>• Tự động hóa với Dynamo</td>
        <td>
          • Chuẩn hóa toàn bộ Template Revit, mã hóa cấu kiện cho 6 bộ môn.<br/>
          • Ứng dụng script Dynamo tự động xuất bản vẽ & trích xuất BOQ.<br/>
          • Đào tạo nâng cao kỹ năng phối hợp cho đội ngũ kỹ sư thực chiến.
        </td>
      </tr>
      <tr>
        <td><b>Quý 3/2027</b></td>
        <td><b>Thực chiến "Dự án Mẫu"</b><br/>• 87 nhiệm vụ kỹ thuật<br/>• Kiểm chứng cam kết SLA</td>
        <td>
          • Triển khai trọn vẹn 87 nhiệm vụ thực chiến trên Dự án Mẫu.<br/>
          • Xóa bỏ 100% va chạm (Zero Clash) kết cấu - cơ điện trước khi thi công.<br/>
          • Kiểm soát tuân thủ SLA: Shop 5 ngày, Combine 10 ngày, QS 7 ngày.
        </td>
      </tr>
      <tr>
        <td><b>Quý 4/2027</b></td>
        <td><b>Tự chủ 100% & Đánh giá KPI</b><br/>• Đánh giá chuẩn hóa trọng số<br/>• Tối ưu năng suất nội bộ</td>
        <td>
          • <b>Tự chủ 100% hồ sơ Shop Drawing & BPTC</b> cho các dự án mới.<br/>
          • Tự động hóa bóc tách khối lượng 5D BIM: Sai số vật tư &lt; 2%.<br/>
          • Vận hành ổn định nề nếp phối hợp giữa phòng BIM và các công trường.
        </td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-title">💼 3 Kiến Nghị Then Chốt Kính Trình Ban Tổng Giám Đốc Phê Duyệt</h2>

  <div class="box-highlight">
    <div class="box-title">1. Phê Duyệt Cơ Chế Điều Phối Theo 4 Cụm Leader Bộ Môn</div>
    <div class="box-desc">
      Chấp thuận phương án setup vận hành theo 4 Cụm chuyên môn do các Leader hiện hữu làm nòng cốt. Phê duyệt cơ chế đánh giá KPI gắn liền với mức độ tuân thủ thời gian cam kết dịch vụ SLA.
    </div>
  </div>

  <div class="box-highlight blue">
    <div class="box-title">2. Phê Duyệt Đầu Tư Hạ Tầng Bản Quyền & Phần Cứng</div>
    <div class="box-desc">
      Trang bị đầy đủ bản quyền phần mềm thiết kế/BIM chính hãng, nền tảng lưu trữ CDE đám mây và nâng cấp máy trạm đồ họa đáp ứng yêu cầu xử lý mô hình nặng.
    </div>
  </div>

  <div class="box-highlight amber">
    <div class="box-title">3. Ban Hành Quy Chế Phối Hợp Bắt Buộc Theo Cam Kết SLA</div>
    <div class="box-desc">
      Ban hành văn bản quy định thời gian phối hợp chuẩn (BIM Shop 5 ngày, BIM Combine 10 ngày, BIM QS 7 ngày) giữa Phòng BIM, Ban QLDA và Ban Chỉ huy công trường.
    </div>
  </div>

  <div style="margin-top: 18px; display: flex; justify-content: space-between; align-items: flex-end; padding: 0 20px;">
    <div style="text-align: center;">
      <p style="font-size: 8pt; color: #64748b; margin-bottom: 40px;">KÍNH TRÌNH BAN TỔNG GIÁM ĐỐC PHÊ DUYỆT</p>
      <p style="font-size: 9pt; font-weight: 800; color: #0f172a;">HỘI ĐỒNG QUẢN TRỊ / TỔNG GIÁM ĐỐC</p>
    </div>
    <div style="text-align: center;">
      <p style="font-size: 8pt; color: #64748b; margin-bottom: 40px;">NGƯỜI LẬP BÁO CÁO CHIẾN LƯỢC</p>
      <p style="font-size: 9pt; font-weight: 800; color: #0f172a;">TRƯỞNG BỘ PHẬN BIM - THIẾT KẾ</p>
    </div>
  </div>
</div>

</body>
</html>
"""

def generate_pdf():
    print("⏳ Đang khởi tạo Playwright để biên dịch tài liệu PDF 7 trang Năm 2027...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        
        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"}
        )
        browser.close()

    for path in [OUT_PDF_2027, OUT_PDF_2026]:
        with open(path, "wb") as f:
            f.write(pdf_bytes)
        print(f"✅ Đã xuất file PDF tại Repo     : {path}")
    print(f"   Kích thước file: {len(pdf_bytes):,} bytes")

    for path in [OUT_PDF_ARTIFACT_2027, OUT_PDF_ARTIFACT_2026]:
        try:
            with open(path, "wb") as f:
                f.write(pdf_bytes)
            print(f"✅ Đã sao chép vào Artifact Dir  : {path}")
        except Exception as e:
            print(f"⚠️ Lưu vào artifact: {e}")

if __name__ == "__main__":
    generate_pdf()

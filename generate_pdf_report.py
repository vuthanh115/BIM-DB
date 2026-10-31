# -*- coding: utf-8 -*-
"""
Script tạo file PDF Báo cáo Phương Án Kiện Toàn Tổ Chức & Tối Ưu Hóa Vận Hành Phòng BIM (Năm 2027)
Dành cho việc trình bày và bảo vệ phương án trước Ban Tổng Giám Đốc / HĐQT
- Giữ nguyên quy mô định biên hiện tại (24 nhân sự đang làm việc)
- Setup lại cơ chế vận hành theo 4 Cụm Chiến Đấu Squads do các Leader bộ môn làm hạt nhân
- Bộ 4 chỉ số KPI thực tế (Tiết kiệm chi phí ngoài, 100% Tự chủ Shop, <1% Sửa chữa, 70% Tái sử dụng)
Sử dụng Playwright (Chromium) xuất PDF chuẩn in ấn A4 (7 trang màu Executive).
"""

import os
import sys
# from playwright.sync_api import sync_playwright (optional)

OUT_PDF_2027 = os.path.abspath("Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2027.pdf")
OUT_PDF_2026 = os.path.abspath("Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2026.pdf")
OUT_PDF_ARTIFACT_2027 = os.path.abspath(r"C:\Users\vophi\.gemini\antigravity\brain\1112d6b2-e52a-494a-9fe7-3e83ca48e8e4\Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2027.pdf")
OUT_PDF_ARTIFACT_2026 = os.path.abspath(r"C:\Users\vophi\.gemini\antigravity\brain\1112d6b2-e52a-494a-9fe7-3e83ca48e8e4\Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2026.pdf")

html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Phương Án Kiện Toàn Tổ Chức & Tối Ưu Hóa Vận Hành Phòng BIM (2027)</title>
<style>
  @page {
    size: A4 portrait;
    margin: 0;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
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
  .title-icon { width: 14pt; height: 14pt; vertical-align: -2px; margin-right: 6px; display: inline-block; }
  .box-icon { width: 11pt; height: 11pt; vertical-align: -1.5px; margin-right: 6px; display: inline-block; }
  .sub-icon { width: 11pt; height: 11pt; vertical-align: -1.5px; margin-right: 6px; display: inline-block; }
  .sec-title {
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
        Báo cáo phương án kiện toàn tổ chức nhân sự hiện hữu, thiết lập cơ chế phân quyền điều phối theo 4 Cụm Lead bộ môn, tự động hóa bằng AI Agent, triển khai song song dự án mẫu thực chiến và cam kết chuẩn dịch vụ SLA tinh gọn (Shop 5d, Combine 3d, QS 3d) nhằm nâng cao năng suất và chất lượng hồ sơ công trình.
      </p>
    </div>

    <div class="cover-meta">
      <div class="meta-item">
        <span class="meta-label">Cấp Thẩm Quyền Báo Cáo</span>
        <span class="meta-val">Hội Đồng Quản Trị / Ban Tổng Giám Đốc</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Đơn Vị Lập Đề Án</span>
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

  <h1 class="sec-title"><svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> 1. Tóm tắt Dành cho Ban Lãnh Đạo (Executive Summary)</h1>

  <div class="box-highlight">
    <div class="box-title"><svg class="box-icon" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6m-4 3h2m-5-8.5a6 6 0 1 1 8 0c-1 1-1.5 2-1.5 3.5h-5c0-1.5-.5-2.5-1.5-3.5z"/></svg> Thông Điệp Then Chốt Gửi Ban Lãnh Đạo</div>
    <div class="box-desc">
      Phòng BIM không phải là một "bộ phận vẽ 3D tiêu tốn chi phí" (Cost Center), mà đang được hoạch định trở thành <b>Đòn bẩy Chiến lược (Strategic Value Driver)</b> giúp Doanh nghiệp nâng cao chất lượng hồ sơ, tối ưu hóa tiến độ thi công, tiết kiệm <b>70% nguồn lực nhờ tái sử dụng dữ liệu</b>, và loại bỏ triệt để các xung đột công trường gây lãng phí hàng tỷ đồng vật tư và nhân công sửa sai.
    </div>
  </div>

  <!-- BỘ 4 THẺ KPI THỰC CHIẾN -->
  <div class="grid-4">
    <div class="stat-card blue">
      <div class="stat-num">100%</div>
      <div class="stat-title">Tự Chủ Kỹ Thuật Nội Bộ</div>
      <div class="stat-desc">Làm chủ 6 bộ môn thiết kế trên nền tảng 3D BIM</div>
    </div>
    <div class="stat-card emerald">
      <div class="stat-num">100%</div>
      <div class="stat-title">Tiến Độ Theo Chuẩn SLA</div>
      <div class="stat-desc">Cam kết thời gian Shop 5d, Combine 3d, QS 3d</div>
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

  <h2 class="sub-title"><svg class="sub-icon" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="17" x2="12" y2="22"/><path d="M5 17h14l-2-7V4h1V2H6v2h1v6z"/></svg> 3 Trụ Cột Giá Trị Cốt Lõi Mang Lại Cho Doanh Nghiệp</h2>
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
        <td>Nâng cấp toàn bộ năng lực từ thiết kế 2D truyền thống lên mô hình BIM 3D, gia tăng năng lực cạnh tranh và bảo mật bí quyết kỹ thuật.</td>
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
    <div class="box-title"><svg class="box-icon" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v1m2 13a2 2 0 0 1-2-2V7m2 13a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2"/></svg> Tính Pháp Lý & Xu Hướng Bắt Buộc Của Ngành Xây Dựng</div>
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

  <h1 class="sec-title"><svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> 2. Cơ cấu Tổ chức: Hiện trạng & Setup Vận hành Khoa học</h1>

  <div class="box-highlight blue">
    <div class="box-title"><svg class="box-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="17" x2="12" y2="22"/><path d="M5 17h14l-2-7V4h1V2H6v2h1v6z"/></svg> Định Hướng Setup: Tối Ưu Hóa Nguồn Lực Hiện Hữu</div>
    <div class="box-desc">
      Tận dụng tối đa bộ máy hiện có <b>(24 nhân sự đang làm việc)</b>. Là <b>công ty thiết kế chuyển đổi số toàn diện lên BIM</b>, <b>11 kỹ sư BIM chuyên trách được điều phối chia đều về các bộ môn thiết kế</b> (3 KS Kết cấu, 3 KS Kiến trúc, 3 KS Cơ điện MEPF, 2 KS Hạ tầng & CDE) cùng làm việc trực tiếp với các Lead bộ môn để triển khai mô hình 3D ngay từ đầu, xóa bỏ hoàn toàn độ trễ giữa thiết kế và BIM.
    </div>
  </div>

  <h2 class="sub-title"><svg class="sub-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg> Bảng Hiện Trạng Định Biên & Bố Trí Nhân Sự Hiện Tại (24 Đang làm việc)</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 24%;">Bộ Môn / Khối Chuyên Môn</th>
        <th style="width: 26%;">Hạt Nhân Chỉ Huy</th>
        <th style="width: 30%;">Nhân Sự Thiết Kế & BIM (Chia Đều 11 KS)</th>
        <th style="width: 8%;">Định Biên</th>
        <th style="width: 12%;">Hiện Trạng</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Quản lý Điều hành</b></td>
        <td>Trưởng bộ phận BIM - TK</td>
        <td>Điều hành chung, hoạch định chiến lược & kiểm soát SLA</td>
        <td>1 / 1</td>
        <td><span class="pill pill-r">1 Đang làm</span></td>
      </tr>
      <tr>
        <td><b>Thiết kế & BIM Kết Cấu</b></td>
        <td>Lead Bộ Môn Kết Cấu</td>
        <td>2 KS Thiết kế TK + <b>3 KS BIM Kết Cấu</b></td>
        <td>8 / 7</td>
        <td><span class="pill pill-r">7 Đang làm</span></td>
      </tr>
      <tr>
        <td><b>Thiết kế & BIM Kiến Trúc</b></td>
        <td>Lead Bộ Môn Kiến Trúc</td>
        <td>1 KTS Thiết kế + <b>3 KS BIM Kiến Trúc</b></td>
        <td>6 / 5</td>
        <td><span class="pill pill-tag">4 Đang làm</span></td>
      </tr>
      <tr>
        <td><b>Thiết kế & BIM Cơ Điện (MEPF)</b></td>
        <td>Lead Bộ Môn BIM MEPF</td>
        <td>1 KS Thiết kế TK + 1 KS MEP + <b>3 KS BIM MEP</b></td>
        <td>7 / 7</td>
        <td><span class="pill pill-r">7 Đang làm</span></td>
      </tr>
      <tr>
        <td><b>Thiết kế & BIM HVAC</b></td>
        <td>Lead Bộ Môn HVAC</td>
        <td>1 KS Triển khai HVAC chuyên trách</td>
        <td>3 / 2</td>
        <td><span class="pill pill-r">2 Đang làm</span></td>
      </tr>
      <tr>
        <td><b>BIM Hạ Tầng & Quản trị CDE</b></td>
        <td>Lead Kỹ Thuật Hạ Tầng & CDE</td>
        <td>2 KS BIM Hạ tầng & Quản trị dữ liệu CDE</td>
        <td>5 / 4</td>
        <td><span class="pill pill-r">3 Đang làm</span></td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-title"><svg class="sub-icon" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg> 3 Trục Cải Tiến Khi Setup Lại Cơ Chế Vận Hành</h2>
  
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

  <h1 class="sec-title"><svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg> 3. Cơ chế Phối hợp: 4 Cụm Chuyên môn Do Lead Bộ Môn Chỉ huy</h1>

  <div class="box-highlight blue">
    <div class="box-title"><svg class="box-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> Nguyên Tắc Phối Hợp: Trao Quyền Tự Chủ Cho Các Lead Bộ Môn</div>
    <div class="box-desc">
      Tổ chức toàn bộ nhân sự hiện hữu thành <b>4 Cụm Phối Hợp Chuyên Môn (Discipline Squads)</b> do các Lead từng bộ môn trực tiếp chỉ huy. Mỗi Lead bộ môn được trao quyền tự chủ kỹ thuật, nắm trọn vẹn từ thiết kế đến mô hình BIM, chịu trách nhiệm về chất lượng đầu ra và cam kết tiến độ phục vụ công trường theo chuẩn SLA.
    </div>
  </div>

  <h2 class="sub-title"><svg class="sub-icon" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> Cơ Cấu 4 Cụm Phối Hợp Chuyên Môn</h2>
  
  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 20%;">Cụm Phối Hợp</th>
        <th style="width: 25%;">Hạt Nhân Chỉ Huy (Leads)</th>
        <th style="width: 20%;">Nhân Sự Thực Chiến</th>
        <th style="width: 35%;">Phạm Vi Nhiệm Vụ & Cam Kết SLA</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Cụm 1: Kết Cấu & Biện Pháp Thi Công</b></td>
        <td><b>Lead Bộ Môn Kết Cấu</b></td>
        <td>Đội ngũ KS BIM Kết Cấu thực chiến</td>
        <td>• Mô hình kết cấu BTCT, đà kiềng, móng, vách bể.<br/>• Xuất bản vẽ Shop cốt thép & ván khuôn đạt SLA <b>Chuẩn 5 Ngày</b>.<br/>• AI Agent trích xuất BOQ thép & bê tông phục vụ mua hàng.</td>
      </tr>
      <tr>
        <td><b>Cụm 2: Kiến Trúc & Tạo Hình 3D</b></td>
        <td><b>Lead Bộ Môn Kiến Trúc</b></td>
        <td>Đội ngũ KTS & KS BIM Kiến Trúc thực chiến</td>
        <td>• Mô hình kiến trúc LOD 300–350, chi tiết cấu tạo.<br/>• Diễn họa 3D phối cảnh, mô phỏng video phục vụ đấu thầu.<br/>• Thẩm định tuân thủ quy chuẩn phòng cháy QCVN 06.</td>
      </tr>
      <tr>
        <td><b>Cụm 3: Cơ Điện MEPF & Phối Hợp Va Chạm</b></td>
        <td><b>Lead Bộ Môn BIM Cơ Điện (MEPF)</b></td>
        <td>Đội ngũ KS BIM MEPF thực chiến</td>
        <td>• Mô hình 4 hệ MEPF: Điện, HVAC, Cấp thoát nước, PCCC.<br/>• Ứng dụng AI Agent phân loại và xử lý xung đột đạt SLA <b>Chuẩn 3 Ngày</b>.<br/>• Tối ưu cao độ trần kỹ thuật và tuyến ống trục đứng.</td>
      </tr>
      <tr>
        <td><b>Cụm 4: Hạ Tầng Kỹ Thuật & Quản Trị CDE</b></td>
        <td><b>Lead Kỹ Thuật Hạ Tầng & CDE</b></td>
        <td>Đội ngũ KS BIM Hạ tầng & Quản trị CDE</td>
        <td>• Mô hình san nền, giao thông, thoát nước ngoài nhà (Civil 3D).<br/>• Quản trị phân quyền môi trường dữ liệu chung CDE.<br/>• AI Agent bóc tách khối lượng hạ tầng kỹ thuật đạt SLA <b>Chuẩn 3 Ngày</b>.</td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-title"><svg class="sub-icon" viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg> Cơ Chế Điều Phối Linh Hoạt (Agile Swarming & Cross-Support)</h2>
  
  <div class="grid-2">
    <div class="stat-card emerald">
      <div class="stat-title" style="color:#059669;">1. Cơ Chế Xoay Vòng Hỗ Trợ Đột Xuất</div>
      <div class="stat-desc">
        Các Kỹ sư trong 4 Cụm không bị đóng đinh cố định. Khi dự án bước vào <b>giai đoạn móng/hầm cao điểm</b>, Leader sẽ dồn lực nhân sự hỗ trợ Cụm Kết cấu (hoàn thành Shop drawing trong SLA Chuẩn 5 Ngày). Khi bước vào <b>giai đoạn hoàn thiện cơ điện</b>, nhân sự chuyển sang hỗ trợ Cụm MEPF (Combine va chạm với AI Agent trong SLA Chuẩn 3 Ngày).
      </div>
    </div>
    <div class="stat-card blue">
      <div class="stat-title" style="color:#0284c7;">2. Vai Trò Nhạc Trưởng Của Trưởng Phòng (TBP)</div>
      <div class="stat-desc">
        Trưởng bộ phận BIM - TK đóng vai trò là "Nhạc trưởng" điều phối phân bổ nguồn lực giữa các Cụm Leader, kiểm soát tiến độ tổng thể, bảo vệ giải pháp kỹ thuật trước Ban Giám Đốc và Chủ đầu tư, <b>không can thiệp sâu vào chi tiết kỹ thuật của từng Cụm</b> để tránh gây nghẽn luồng xử lý.
      </div>
    </div>
  </div>

  <div class="box-highlight">
    <div class="box-title"><svg class="box-icon" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> Lợi Ích Của Phương Án Setup Này Cho Doanh Nghiệp</div>
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

  <h1 class="sec-title"><svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg> 4. Khung Vận Hành Chuẩn: Ma trận RACI & Cam kết SLA</h1>

  <div class="box-highlight blue">
    <div class="box-title"><svg class="box-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="17" x2="12" y2="22"/><path d="M5 17h14l-2-7V4h1V2H6v2h1v6z"/></svg> Ý Nghĩa Của Chuẩn RACI: Xóa Bỏ Điểm Nghẽn & Đùn Đẩy Trách Nhiệm</div>
    <div class="box-desc">
      Ma trận phân công trách nhiệm RACI xác định rõ vai trò của từng cá nhân đối với <b>34 nhiệm vụ trọng yếu</b> của phòng BIM. Nguyên tắc cốt lõi: <i>"Người trực tiếp thực thi (R) được trao quyền hành động tự chủ, và mỗi nhiệm vụ có DUY NHẤT 1 người chịu trách nhiệm phê duyệt cuối cùng (A)."</i>
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
        <td><span class="pill pill-r">R (Responsible)</span><br/><b>Trực tiếp thực hiện</b></td>
        <td><b>Các Lead Bộ Môn & Đội ngũ Kỹ sư Chuyên môn</b></td>
        <td>Trực tiếp giải quyết kỹ thuật, ứng dụng AI Agent xử lý va chạm đa bộ môn, kiểm soát mô hình, hoàn thiện hồ sơ Shop Drawing và bàn giao đúng hạn SLA cam kết.</td>
      </tr>
      <tr>
        <td><span class="pill pill-a">A (Accountable)</span><br/><b>Chịu trách nhiệm cuối</b></td>
        <td><b>Trưởng bộ phận BIM - TK</b></td>
        <td>Chịu trách nhiệm toàn diện trước Ban Giám Đốc về tiến độ, ngân sách, nhân sự và chất lượng hồ sơ thầu. Duyệt phát hành hồ sơ và quản trị chiến lược.</td>
      </tr>
      <tr>
        <td><span class="pill pill-c">C (Consulted)</span><br/><b>Tham vấn chuyên môn</b></td>
        <td><b>Chuyên gia Cố vấn / Ban Kỹ thuật</b></td>
        <td>Đóng góp ý kiến chuyên môn sâu, thẩm định tính tuân thủ tiêu chuẩn quy phạm nhà nước (QCVN, TCVN) trước khi phát hành hồ sơ.</td>
      </tr>
      <tr>
        <td><span class="pill pill-i">I (Informed)</span><br/><b>Được thông báo</b></td>
        <td><b>Ban QLDA, BCH Công trường, Đấu thầu</b></td>
        <td>Nhận thông báo cập nhật tiến độ, biên bản va chạm và hồ sơ bản vẽ hoàn chỉnh để phục vụ thi công và đặt hàng vật tư.</td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-title"><svg class="sub-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> Cam Kết Thời Gian Phục Vụ (SLA 7 Bước Khép Kín)</h2>
  
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
        <td><b style="color:#059669; font-size:9pt;">Chuẩn 3 Ngày làm việc</b><br/><span style="color:#64748b; font-size:7pt;">(AI Agent quét xung đột 1d + Họp xử lý tuyến 1d + Khóa mô hình 1d)</span></td>
        <td>Báo cáo va chạm (Clash Detection Report), giải quyết 100% xung đột ống gió, thang máng cáp, ống nước trước khi thi công nhờ trợ lực từ AI Agent.</td>
      </tr>
      <tr>
        <td><b>3. Quy trình BIM QS (Bóc Khối lượng)</b></td>
        <td><b style="color:#d97706; font-size:9pt;">Chuẩn 3 Ngày làm việc</b><br/><span style="color:#64748b; font-size:7pt;">(AI Agent rà soát model 1d + Tự động bóc 5D 1d + Đối soát BOQ 1d)</span></td>
        <td>Bảng tổng hợp khối lượng bóc tách tự động từ mô hình 3D (Bê tông, thép, ván khuôn, thiết bị) sai số &lt; 2% so với thực tế.</td>
      </tr>
    </tbody>
  </table>
  <div class="box-highlight emerald" style="margin-top: 6px;">
    <div class="box-title"><svg class="box-icon" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10H12V2z"/></svg> Đột Phá Năng Suất Nhờ Tự Động Hóa Bằng AI Agent</div>
    <div class="box-desc">
      Ứng dụng <b>AI Agent chuyên trách</b> tự động gom nhóm và lọc va chạm (giảm 70% thời gian họp xử lý clash), tự động rà soát Model Health, và mapping bóc tách khối lượng 5D BOQ tức thì — giúp rút ngắn kỷ lục thời gian bàn giao <b>Combine MEPF còn 3 ngày</b> và <b>QS bóc khối lượng còn 3 ngày</b>.
    </div>
  </div>
</div>

<!-- TRANG 6: HỆ THỐNG 115 TÀI LIỆU CHUẨN HÓA & TRIỂN KHAI DỰ ÁN MẪU -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần V: Nền Tảng Kỹ Thuật & Dự Án Mẫu Thực Chiến</div>
    <div class="page-header-meta">Trang 6 / 7</div>
  </div>

  <h1 class="sec-title"><svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg> 5. Nền tảng Dữ liệu & Kế hoạch Dự Án Mẫu</h1>

  <h2 class="sub-title"><svg class="sub-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg> Danh Mục Hệ Thống Tài Liệu Thiết Kế (115 Mục Chuẩn Hóa 6 Bộ Môn)</h2>
  
  <table class="data-table" style="margin-bottom: 8px;">
    <thead>
      <tr>
        <th style="width: 7%;">Mã</th>
        <th style="width: 22%;">Bộ Môn Thiết Kế</th>
        <th style="width: 17%;">Lead Phụ Trách</th>
        <th style="width: 9%;">Số Lượng</th>
        <th style="width: 45%;">Danh Mục Chuẩn Hóa Trọng Tâm (5 Phân Nhóm Cốt Lõi)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>KC</b></td>
        <td><b>Thiết kế Kết Cấu</b></td>
        <td>Lead Kết Cấu</td>
        <td><b>23 Mục</b></td>
        <td>Template Revit KC, Biểu mẫu ghi chú chung, Quy chuẩn cốt thép, Checklist lỗi hay gặp, Script Dynamo trích xuất BOQ bê tông/thép.</td>
      </tr>
      <tr>
        <td><b>KT</b></td>
        <td><b>Thiết kế Kiến Trúc</b></td>
        <td>Lead Kiến Trúc</td>
        <td><b>20 Mục</b></td>
        <td>Template Revit KT, Quy chuẩn mã cấu kiện, Thư viện cửa & hoàn thiện, Thẩm tra PCCC QCVN 06, Phối cảnh 3D/VR đấu thầu.</td>
      </tr>
      <tr>
        <td><b>DIEN</b></td>
        <td><b>Thiết kế Hệ Thống Điện</b></td>
        <td>Lead Hệ Thống Điện</td>
        <td><b>18 Mục</b></td>
        <td>Template Revit Điện, Sơ đồ nguyên lý tủ điện, Quy chuẩn máng cáp, Bảng tính phụ tải, Checklist an toàn đóng cắt.</td>
      </tr>
      <tr>
        <td><b>HVAC</b></td>
        <td><b>Thiết kế Điều Hòa - TG</b></td>
        <td>Lead Điều Hòa - TG</td>
        <td><b>18 Mục</b></td>
        <td>Template Revit HVAC, Bảng tính tải lạnh, Quy chuẩn ống gió, Tiêu chuẩn tiêu âm, Checklist phối hợp cao độ trần kỹ thuật.</td>
      </tr>
      <tr>
        <td><b>CTN</b></td>
        <td><b>Thiết kế Cấp Thoát Nước</b></td>
        <td>Lead Cấp Thoát Nước</td>
        <td><b>18 Mục</b></td>
        <td>Template Revit CTN, Tính lưu lượng cấp & thoát, Quy chuẩn độ dốc, Thiết kế trạm bơm & hố ga, Checklist hộp gen trục đứng.</td>
      </tr>
      <tr>
        <td><b>PCCC</b></td>
        <td><b>Thiết kế Phòng Cháy CC</b></td>
        <td>Lead Phòng Cháy CC</td>
        <td><b>18 Mục</b></td>
        <td>Thuyết minh thẩm duyệt PCCC QCVN 06:2022, Bố trí hệ thống Sprinkler, Màng ngăn Drencher, Trạm bơm chữa cháy, Checklist van.</td>
      </tr>
      <tr style="background: #f8fafc; font-weight: 700;">
        <td colspan="3" style="text-align: right; padding-right: 8px;"><b>TỔNG CỘNG 6 BỘ MÔN CHUẨN HÓA:</b></td>
        <td><b style="color: #2563eb;">115 Mục</b></td>
        <td><b>Bộ "Khuôn mẫu dữ liệu" chuẩn hóa tái sử dụng 70% tài nguyên thiết kế - thi công</b></td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-title"><svg class="sub-icon" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg> Triển Khai Thực Chiến: 7 "Dự Án Mẫu" Tiêu Biểu (87 Nhiệm Vụ)</h2>
  
  <div class="box-highlight emerald">
    <div class="box-title"><svg class="box-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> Chiến Lược "Thử Lửa" Quy Trình Qua 7 Dự Án Mẫu Thực Tế</div>
    <div class="box-desc">
      Phòng BIM phân kỳ kiểm chứng quy trình trên <b>7 Dự Án Mẫu điển hình (tổng 87 nhiệm vụ kỹ thuật)</b> gồm đầy đủ các loại hình: nhà xưởng chính (Mẫu 01), trạm xử lý (Mẫu 02), kết cấu thép (Mẫu 03), kiến trúc hoàn thiện (Mẫu 04), hạ tầng ngoài nhà (Mẫu 05), trạm nguồn (Mẫu 06) và phần móng (Mẫu 07).
    </div>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 25%;">Hạng Mục Thực Chiến</th>
        <th style="width: 45%;">Nội Dung Phân Khai Trên 7 Dự Án Mẫu</th>
        <th style="width: 30%;">Chỉ Số Đánh Giá Hoàn Thành</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Phần Ngầm & Kết Cấu</b><br/><span style="font-size:7.5pt; color:#64748b;">(Dự Án Mẫu 01, 02, 07)</span></td>
        <td>Dựng mô hình 3D đà kiềng, móng, vách bể kỹ thuật; xuất hồ sơ Shop drawing và bảng khối lượng thép/bê tông chuẩn SLA 5 Ngày.</td>
        <td>Đạt tỷ lệ hoàn thành <b>100%</b>, khớp nối hình học chính xác tuyệt đối.</td>
      </tr>
      <tr>
        <td><b>Phối Hợp Va Chạm (MEP)</b><br/><span style="font-size:7.5pt; color:#64748b;">(Dự Án Mẫu 03, 04)</span></td>
        <td>Import đường ống đa hệ MEPF và kết cấu thép mái vào Navisworks/BIM Collab, ứng dụng AI Agent phân loại và kiểm soát xung đột theo SLA Chuẩn 3 Ngày.</td>
        <td>Phát hiện và xử lý triệt để <b>42 điểm giao cắt</b> nguy hiểm trước ngày khởi công.</td>
      </tr>
      <tr>
        <td><b>Bóc Tách BOQ & Hạ Tầng</b><br/><span style="font-size:7.5pt; color:#64748b;">(Dự Án Mẫu 05, 06)</span></td>
        <td>Tự động hóa bóc khối lượng đào đắp, thoát nước ngoài nhà, trạm nguồn và cảnh quan theo SLA Chuẩn 3 Ngày nhờ AI Agent tự động bóc tách BOQ phục vụ đấu thầu.</td>
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

  <h1 class="sec-title"><svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> 6. Lộ trình Thực thi 4 Quý Năm 2027 (Roadmap 2027)</h1>

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
        <td><b>Kiện toàn Tổ chức, CDE & Triển khai Song Song Dự Án Mẫu</b><br/>• 4 Cụm Squads theo Lead bộ môn & CDE<br/>• Triển khai song song 01 Dự Án Mẫu<br/>• Ban hành khung RACI & Cam kết SLA</td>
        <td>
          • Ban hành Quy chế phân quyền RACI & cam kết thời gian SLA tinh gọn (Shop 5d, Combine 3d, QS 3d).<br/>
          • Vận hành 4 Cụm Chiến Đấu: KC, KT, MEPF, Hạ tầng theo các Lead bộ môn trên 24 nhân sự hiện hữu.<br/>
          • <b>Triển khai SONG SONG 01 Dự Án Mẫu (Pilot Project) ngay trong quá trình setup</b> để kiểm chứng quy trình, huấn luyện AI Agent và đo lường SLA thực tế.<br/>
          • Thiết lập và chuẩn hóa môi trường dữ liệu chung CDE.
        </td>
      </tr>
      <tr>
        <td><b>Quý 2/2027</b></td>
        <td><b>Chuẩn hóa 115 Tài liệu & Tự động hóa bằng AI Agent</b><br/>• Hoàn thành nhóm P1 & P2 quy chuẩn<br/>• Tự động hóa với AI Agent & Tooling</td>
        <td>
          • Chuẩn hóa toàn bộ Template Revit, mã hóa cấu kiện cho 6 bộ môn đúc kết từ Dự Án Mẫu.<br/>
          • Ứng dụng AI Agent tự động hóa rà soát model, phân loại va chạm và trích xuất dữ liệu BOQ.<br/>
          • Đào tạo nâng cao kỹ năng phối hợp cho đội ngũ kỹ sư thực chiến 4 cụm.
        </td>
      </tr>
      <tr>
        <td><b>Quý 3/2027</b></td>
        <td><b>Thực chiến 01 Dự Án Mẫu</b><br/>• Triển khai trọn vẹn đa bộ môn<br/>• Kiểm chứng cam kết SLA tinh gọn</td>
        <td>
          • Triển khai thực chiến trọn vẹn trên 01 Dự Án Mẫu (từ Thiết kế 3D, Combine MEPF, Shop Drawing đến bóc tách BOQ).<br/>
          • Xóa bỏ 100% va chạm (Zero Clash) kết cấu - cơ điện trước khi thi công.<br/>
          • Kiểm soát nghiêm ngặt tuân thủ SLA: <b>Shop 5 ngày, Combine 3 ngày, QS 3 ngày</b>.
        </td>
      </tr>
      <tr>
        <td><b>Quý 4/2027</b></td>
        <td><b>Tự chủ 100%, Hoàn thiện AI Agent & Đánh giá KPI</b><br/>• Tự chủ 100% Shop & BPTC<br/>• Vận hành AI Agent quy chuẩn & Đánh giá KPI</td>
        <td>
          • <b>Tự chủ 100% hồ sơ Shop Drawing & BPTC</b> cho các dự án mới của công ty.<br/>
          • AI Agent bóc tách khối lượng 5D BIM tự động: Sai số vật tư &lt; 2%.<br/>
          • Vận hành ổn định nề nếp phối hợp giữa phòng BIM và các công trường, chứng minh ROI rõ rệt.
        </td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-title"><svg class="sub-icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg> 3 Kiến Nghị Then Chốt Kính Trình Ban Tổng Giám Đốc Phê Duyệt</h2>

  <div class="box-highlight">
    <div class="box-title">1. Phê Duyệt Cơ Chế Điều Phối Theo 4 Cụm Lead Bộ Môn & Triển Khai Song Song Dự Án Mẫu</div>
    <div class="box-desc">
      Chấp thuận phương án setup vận hành theo 4 Cụm chuyên môn do các Lead bộ môn hiện hữu trực tiếp chỉ huy trên 24 nhân sự. Phê duyệt việc <b>triển khai song song 01 Dự Án Mẫu (Pilot Project)</b> ngay trong giai đoạn setup để thử nghiệm quy trình thực chiến.
    </div>
  </div>

  <div class="box-highlight blue">
    <div class="box-title">2. Phê Duyệt Đầu Tư Hạ Tầng Bản Quyền, CDE & Tự Động Hóa Bằng AI Agent</div>
    <div class="box-desc">
      Trang bị đầy đủ bản quyền phần mềm thiết kế/BIM chính hãng, nền tảng lưu trữ CDE đám mây và triển khai công nghệ <b>AI Agent tự động hóa</b> rà soát model, phân loại va chạm và trích xuất khối lượng BOQ.
    </div>
  </div>

  <div class="box-highlight amber">
    <div class="box-title">3. Ban Hành Quy Chế Phối Hợp Bắt Buộc Theo Cam Kết SLA</div>
    <div class="box-desc">
      Ban hành văn bản quy định thời gian phối hợp chuẩn (BIM Shop 5 ngày, BIM Combine 3 ngày, BIM QS 3 ngày với trợ lực từ AI Agent) giữa các Lead Bộ Môn BIM, Ban QLDA và Ban Chỉ huy công trường.
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
    print("Dang khoi tao bien dich tai lieu PDF 7 trang Executive...")
    import subprocess
    
    temp_html = os.path.abspath("_temp_report.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    browser_exe = next((p for p in edge_paths if os.path.exists(p)), None)
    
    temp_pdf = os.path.abspath("_temp_out.pdf")
    if browser_exe:
        print(f"Su dung trinh duyet headless: {browser_exe}")
        cmd = [
            browser_exe,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={temp_pdf}",
            temp_html
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if not os.path.exists(temp_pdf) or os.path.getsize(temp_pdf) == 0:
            raise RuntimeError(f"Loi render PDF: {res.stderr}")
        with open(temp_pdf, "rb") as f:
            pdf_bytes = f.read()
        try:
            os.remove(temp_pdf)
        except:
            pass
    else:
        from playwright.sync_api import sync_playwright
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
    
    if os.path.exists(temp_html):
        try:
            os.remove(temp_html)
        except:
            pass

    for path in [OUT_PDF_2027, OUT_PDF_2026]:
        with open(path, "wb") as f:
            f.write(pdf_bytes)
        print(f"Da xuat file PDF tai Repo     : {path}")
    print(f"Kich thuoc file: {len(pdf_bytes):,} bytes")

    for path in [OUT_PDF_ARTIFACT_2027, OUT_PDF_ARTIFACT_2026]:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(pdf_bytes)
            print(f"Da sao chep vao Artifact Dir  : {path}")
        except Exception as e:
            print(f"Luu vao artifact: {e}")

if __name__ == "__main__":
    generate_pdf()

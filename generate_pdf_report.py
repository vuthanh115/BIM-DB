# -*- coding: utf-8 -*-
"""
Script tạo file PDF Báo cáo Chiến lược Xây dựng Phòng BIM Tinh gọn 2026
Dành cho việc trình bày và diễn giải với Ban Lãnh Đạo
Sử dụng Playwright (Chromium) để xuất PDF chất lượng cao, định dạng A4 chuẩn in ấn.
"""

import os
import sys
from playwright.sync_api import sync_playwright

OUT_PDF_REPO = os.path.abspath("Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2026.pdf")
OUT_PDF_ARTIFACT = os.path.abspath(r"C:\Users\thanhvp\.gemini\antigravity\brain\f7887f6d-20b4-485d-b51b-cdd6f48e0c12\Bao_Cao_Chien_Luoc_Xay_Dung_Phong_BIM_2026.pdf")

html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Chiến lược Xây dựng Phòng BIM Tinh gọn 2026</title>
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
    font-size: 9.5pt;
    line-height: 1.45;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .page {
    page-break-after: always;
    page-break-inside: avoid;
    position: relative;
    height: 297mm;
    max-height: 297mm;
    padding: 14mm 14mm 14mm 14mm;
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
    margin: 40mm 0 30mm 0;
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
    font-size: 26pt;
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
    font-size: 12pt;
    color: #cbd5e1;
    line-height: 1.6;
    max-width: 600px;
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

  /* INNER PAGES HEADER / FOOTER */
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid #06b6d4;
    padding-bottom: 8px;
    margin-bottom: 16px;
  }
  .page-header-title {
    font-size: 9pt;
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
    height: 14px;
    background: #06b6d4;
    border-radius: 2px;
  }
  .page-header-meta {
    font-size: 8pt;
    color: #64748b;
    font-weight: 500;
  }

  /* HEADINGS */
  h1.sec-title {
    font-size: 15pt;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 6px;
  }
  h2.sub-title {
    font-size: 11.5pt;
    font-weight: 700;
    color: #1e293b;
    margin: 14px 0 8px 0;
  }

  /* CARDS & GRIDS */
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 14px; }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 14px; }

  .stat-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 14px;
    border-left: 4px solid #06b6d4;
  }
  .stat-card.emerald { border-left-color: #10b981; }
  .stat-card.amber { border-left-color: #f59e0b; }
  .stat-card.rose { border-left-color: #f43f5e; }
  .stat-card.blue { border-left-color: #3b82f6; }
  .stat-num { font-size: 18pt; font-weight: 900; color: #0f172a; line-height: 1.1; margin-bottom: 4px; }
  .stat-title { font-size: 8.5pt; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 2px; }
  .stat-desc { font-size: 8pt; color: #64748b; }

  .box-highlight {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
    border: 1px solid #a7f3d0;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 14px;
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
    font-size: 10pt;
    font-weight: 800;
    color: #065f46;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .box-highlight.blue .box-title { color: #0369a1; }
  .box-highlight.amber .box-title { color: #92400e; }
  .box-desc { font-size: 9pt; color: #334155; line-height: 1.45; }

  /* TABLES */
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 14px;
    font-size: 8.5pt;
  }
  table.data-table th {
    background: #0f172a;
    color: #fff;
    padding: 7px 10px;
    text-align: left;
    font-weight: 700;
    border: 1px solid #0f172a;
  }
  table.data-table td {
    padding: 6.5px 10px;
    border: 1px solid #e2e8f0;
    color: #334155;
    vertical-align: top;
  }
  table.data-table tr:nth-child(even) td { background: #f8fafc; }
  table.data-table tr.highlight td { background: #f0fdf4; font-weight: 600; }

  .pill {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .pill-r { background: #dcfce7; color: #166534; }
  .pill-a { background: #fef3c7; color: #92400e; }
  .pill-c { background: #e0e7ff; color: #3730a3; }
  .pill-i { background: #f1f5f9; color: #475569; }
  .pill-tag { background: #e0f2fe; color: #0369a1; }

  /* LISTS */
  ul.bullet-list { margin-left: 18px; margin-bottom: 12px; }
  ul.bullet-list li { margin-bottom: 5px; font-size: 9pt; color: #334155; }
  ul.bullet-list li b { color: #0f172a; }

  /* STEP FLOW */
  .step-flow {
    display: flex;
    justify-content: space-between;
    gap: 6px;
    margin: 12px 0 16px 0;
  }
  .step-node {
    flex: 1;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 6px;
    text-align: center;
    position: relative;
  }
  .step-node.active {
    background: #eff6ff;
    border-color: #3b82f6;
  }
  .step-num {
    font-size: 7.5pt;
    font-weight: 800;
    color: #3b82f6;
    text-transform: uppercase;
    margin-bottom: 2px;
  }
  .step-name {
    font-size: 8pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
    margin-bottom: 3px;
  }
  .step-time {
    font-size: 7pt;
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
      <div class="cover-tagline">Đề án Chiến lược Năm 2026 - 2027</div>
      <h1 class="cover-title">
        HOẠCH ĐỊNH XÂY DỰNG<br/>
        <span>PHÒNG BIM TINH GỌN (LEAN BIM)</span>
      </h1>
      <p class="cover-subtitle">
        Báo cáo đề xuất mô hình cơ cấu tổ chức 12 – 14 nhân sự đa nhiệm, chuẩn hóa quy chế phân quyền RACI & cam kết SLA 7 bước, cùng kế hoạch triển khai Dự án Mẫu nhằm tiết kiệm ~5.5 tỷ VNĐ/năm chi phí nhân lực cố định.
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
        <span class="meta-val">Q2/2026 — Niên độ 2026 - 2027</span>
      </div>
    </div>
  </div>
</div>

<!-- TRANG 2: TÓM TẮT CHIẾN LƯỢC & GIÁ TRỊ CỐT LÕI (ROI) -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần I: Bối cảnh & Giá trị Cốt lõi Doanh nghiệp</div>
    <div class="page-header-meta">Báo cáo Chiến lược BIM 2026</div>
  </div>

  <h1 class="sec-title">🎯 1. Tóm tắt Dành cho Ban Lãnh Đạo (Executive Summary)</h1>

  <div class="box-highlight">
    <div class="box-title">💡 Thông Điệp Then Chốt Gửi Ban Lãnh Đạo</div>
    <div class="box-desc">
      Phòng BIM không phải là một "bộ phận vẽ 3D tiêu tốn chi phí" (Cost Center), mà đang được hoạch định trở thành <b>Đòn bẩy Chiến lược (Strategic Value Driver)</b> giúp Doanh nghiệp nâng cao tỷ lệ trúng thầu Design & Build (D&B), tiết kiệm <b>70% nguồn lực thi công nhờ tái sử dụng dữ liệu</b>, và loại bỏ triệt để các rủi ro xung đột công trường gây lãng phí hàng tỷ đồng đục phá/sửa chữa.
    </div>
  </div>

  <div class="grid-4">
    <div class="stat-card emerald">
      <div class="stat-num">1.200 Tỷ</div>
      <div class="stat-title">Giá trị Xây lắp Tự chủ</div>
      <div class="stat-desc">Đảm nhận thiết kế 4 dự án D&B/năm</div>
    </div>
    <div class="stat-card blue">
      <div class="stat-num">~5.5 Tỷ</div>
      <div class="stat-title">Tiết kiệm Quỹ Lương/Năm</div>
      <div class="stat-desc">Mô hình Lean 12-14 người vs 30 người</div>
    </div>
    <div class="stat-card amber">
      <div class="stat-num">>85%</div>
      <div class="stat-title">Tỷ lệ Trúng Thầu D&B</div>
      <div class="stat-desc">Nhờ mô phỏng 3D/4D/5D thuyết phục CĐT</div>
    </div>
    <div class="stat-card rose">
      <div class="stat-num">70%</div>
      <div class="stat-title">Tái Sử Dụng Dữ Liệu</div>
      <div class="stat-desc">Từ thiết kế sang Shop Drawing & BOQ</div>
    </div>
  </div>

  <h2 class="sub-title">📌 3 Trụ Cột Giá Trị Cốt Lõi Mang Lại Cho Doanh Nghiệp</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 25%;">Trụ Cột Chiến Lược</th>
        <th style="width: 45%;">Hành Động Cụ Thể Của Phòng BIM</th>
        <th style="width: 30%;">Tác Động Tài Chính & Kinh Doanh</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>1. Tự chủ Thiết kế & Giữ lại Lợi nhuận</b></td>
        <td>Xây dựng đội ngũ làm chủ toàn diện 6 bộ môn: Kiến trúc, Kết cấu, Điện, HVAC, Cấp thoát nước và PCCC. Tự lực lập hồ sơ thiết kế kỹ thuật thi công.</td>
        <td>Giữ lại trong doanh nghiệp từ <b>8 - 10 tỷ VNĐ</b> chi phí thuê tư vấn thiết kế ngoài hàng năm.</td>
      </tr>
      <tr>
        <td><b>2. Vũ khí Thắng thầu Design & Build</b></td>
        <td>Áp dụng mô hình BIM 3D diễn họa kiến trúc, mô phỏng tiến độ 4D biện pháp thi công và bóc tách dự toán 5D chính xác ngay từ giai đoạn chào thầu.</td>
        <td>Tạo sự vượt trội trước các đối thủ cạnh tranh truyền thống; nâng tỷ lệ thắng thầu từ 60% lên trên 85%.</td>
      </tr>
      <tr>
        <td><b>3. Tối ưu Công trường (Zero Conflict)</b></td>
        <td>Phát hiện và xử lý 100% các xung đột không gian (clash detection) giữa kết cấu và hệ thống cơ điện (MEP) trên mô hình số trước khi đổ bê tông.</td>
        <td>Xóa bỏ tình trạng "thiết kế một đằng, ra công trường đục phá làm lại một nẻo", giảm phát sinh chi phí < 1%.</td>
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

<!-- TRANG 3: BÀI TOÁN CƠ CẤU NHÂN SỰ TINH GỌN (LEAN 12 - 14 NS) -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần II: Tái Cấu Trúc & Định Biên Nhân Sự Tinh Gọn</div>
    <div class="page-header-meta">Báo cáo Chiến lược BIM 2026</div>
  </div>

  <h1 class="sec-title">👥 2. Cơ cấu Tổ chức: Bài toán 12 - 14 Người vs. 30 Người Cũ</h1>

  <div class="box-highlight amber">
    <div class="box-title">⚠️ Đánh Giá Mô Hình Cũ (30 Người - Tham Chiếu Doanh Nghiệp A)</div>
    <div class="box-desc">
      Mô hình định biên 30 người của Doanh nghiệp A bộc lộ nhiều điểm nghẽn nghiêm trọng: <b>(1) Quỹ lương cồng kềnh</b> (~9.6 tỷ/năm), <b>(2) Nhân sự chuyên môn hóa đơn lẻ</b> (14 kỹ sư dựng hình chỉ biết 1 phần mềm/1 bộ môn) dẫn đến lãng phí thời gian chết khi dự án vào giai đoạn thấp điểm, <b>(3) Trưởng bộ phận ôm đồm</b> trở thành nút thắt cổ chai của toàn bộ luồng phê duyệt.
    </div>
  </div>

  <h2 class="sub-title">🚀 Sơ Đồ Cơ Cấu Tổ Chức Tinh Gọn 3 Tầng (12 - 14 Nhân Sự Đa Nhiệm)</h2>
  
  <div class="grid-3">
    <div class="stat-card blue">
      <div class="stat-title" style="color:#0284c7;">Tầng 1: Quản Trị & Chiến Lược</div>
      <div class="stat-num" style="font-size:14pt;">01 BIM Manager</div>
      <div class="stat-desc" style="margin-top:6px;">
        • Quản trị CDE (Common Data Environment)<br/>
        • Lập Kế hoạch BEP/EIR dự án<br/>
        • Bảo vệ phương án kỹ thuật với Ban Lãnh Đạo & Chủ Đầu Tư
      </div>
    </div>
    <div class="stat-card emerald">
      <div class="stat-title" style="color:#059669;">Tầng 2: Điều Phối & Công Nghệ</div>
      <div class="stat-num" style="font-size:14pt;">03 Coordinator / R&D</div>
      <div class="stat-desc" style="margin-top:6px;">
        • <b>1 Coord Xây dựng:</b> Kiến trúc + Kết cấu + Shop drawing<br/>
        • <b>1 Coord Cơ điện:</b> MEPF + Phối hợp va chạm (Clash)<br/>
        • <b>1 Chuyên viên R&D:</b> Viết script Dynamo, Family chuẩn
      </div>
    </div>
    <div class="stat-card amber">
      <div class="stat-title" style="color:#d97706;">Tầng 3: Sản Xuất Đa Nhiệm (T-Shaped)</div>
      <div class="stat-num" style="font-size:14pt;">08 - 10 Kỹ Sư Thực Chiến</div>
      <div class="stat-desc" style="margin-top:6px;">
        • <b>2-3 KS Kết cấu:</b> Dựng hình 3D + Shop cốt thép<br/>
        • <b>2 KS Kiến trúc:</b> Dựng hình + Diễn họa 3D/VR<br/>
        • <b>2-3 KS Cơ điện:</b> Mô hình MEPF + BPTC cơ điện<br/>
        • <b>1-2 KS QS & Hạ tầng:</b> Bóc tách khối lượng + Civil 3D
      </div>
    </div>
  </div>

  <h2 class="sub-title">📊 Bảng So Sánh Hiệu Quả Kinh Tế: Tinh Gọn Tiết Kiệm ~5.5 Tỷ VNĐ/Năm</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 28%;">Chỉ Số Đánh Giá</th>
        <th style="width: 26%;">Mô Hình Cũ (Cty A - 30 Người)</th>
        <th style="width: 26%;">Mô Hình Tinh Gọn (12 - 14 Người)</th>
        <th style="width: 20%;">Chênh Lệch / Tối Ưu</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Tổng Số Lượng Định Biên</b></td>
        <td>30 người (Phân tán nhiều vị trí)</td>
        <td><b>12 - 14 người</b> (Đa nhiệm T-Shaped)</td>
        <td><span class="pill pill-r">Giảm 55% nhân sự</span></td>
      </tr>
      <tr>
        <td><b>Quỹ Lương Ước Tính/Năm</b></td>
        <td>~9.6 Tỷ VNĐ / năm (TB 26.6 tr/người/tháng)</td>
        <td><b>~4.1 Tỷ VNĐ / năm</b> (TB 25 - 28 tr/người/tháng)</td>
        <td><span class="pill pill-r">Tiết kiệm ~5.5 Tỷ/năm</span></td>
      </tr>
      <tr>
        <td><b>Chi Phí Bản Quyền & Máy Móc</b></td>
        <td>~1.8 Tỷ VNĐ (Trang bị cho 30 máy trạm)</td>
        <td><b>~800 Triệu VNĐ</b> (Tập trung cho 14 máy)</td>
        <td><span class="pill pill-r">Tiết kiệm ~1.0 Tỷ</span></td>
      </tr>
      <tr>
        <td><b>Đòn Bẩy Năng Suất</b></td>
        <td>Thao tác thủ công, phụ thuộc cá nhân</td>
        <td><b>Tự động hóa Dynamo</b> + Thư viện 115 tài liệu</td>
        <td><span class="pill pill-a">Tăng năng suất 250%</span></td>
      </tr>
      <tr>
        <td><b>Khả Năng Thích Ứng Khối Lượng</b></td>
        <td>Dư thừa khi ít việc, áp lực quỹ lương lớn</td>
        <td>Lõi tinh gọn + Thuê ngoài (Outsource) linh hoạt</td>
        <td><span class="pill pill-tag">An toàn tài chính tối đa</span></td>
      </tr>
    </tbody>
  </table>

  <div class="box-highlight">
    <div class="box-title">💡 Giải Pháp Khi Dự Án Tăng Đột Biến: Mô Hình "Lõi Tinh Gọn + Vệ Tinh Thuê Ngoài"</div>
    <div class="box-desc">
      Khi công ty trúng cùng lúc nhiều dự án lớn vượt công suất 12-14 người, bộ phận BIM sẽ <b>không tuyển ồ ạt nhân sự chính thức</b>. Thay vào đó, 3 Điều phối viên (Coordinator) sẽ đóng vai trò quản lý tiêu chuẩn và giao các gói dựng hình khối lượng lớn cho đơn vị gia công bên ngoài (Outsourcing) theo chuẩn BEP nội bộ, sau đó tự kiểm soát chất lượng (QA/QC).
    </div>
  </div>
</div>

<!-- TRANG 4: CHUẨN HÓA VẬN HÀNH: MA TRẬN RACI & CAM KẾT SLA -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần III: Chuẩn Hóa Vận Hành & Cam Kết Dịch Vụ</div>
    <div class="page-header-meta">Báo cáo Chiến lược BIM 2026</div>
  </div>

  <h1 class="sec-title">📋 3. Khung Vận Hành Chuẩn: Ma trận RACI & Cam kết SLA</h1>

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
        <td><b>2 Trưởng nhóm (Nhân sự B, C) & Kỹ sư</b></td>
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
    <div class="step-node"><div class="step-num">B1</div><div class="step-name">Tiếp nhận Đầu vào</div><div class="step-time">0.5 Ngày</div></div>
    <div class="step-node"><div class="step-num">B2</div><div class="step-name">Hoạch định BEP</div><div class="step-time">0.5 Ngày</div></div>
    <div class="step-node"><div class="step-num">B3</div><div class="step-name">Phân công Chi tiết</div><div class="step-time">0.5 Ngày</div></div>
    <div class="step-node active"><div class="step-num">B4</div><div class="step-name">Thực thi Mô hình</div><div class="step-time">3 - 6 Ngày</div></div>
    <div class="step-node"><div class="step-num">B5</div><div class="step-name">Kiểm tra QA/QC</div><div class="step-time">0.5 - 1 Ngày</div></div>
    <div class="step-node"><div class="step-num">B6</div><div class="step-name">Bàn giao & Ký duyệt</div><div class="step-time">0.5 Ngày</div></div>
    <div class="step-node"><div class="step-num">B7</div><div class="step-name">Đóng & Lưu CDE</div><div class="step-time">0.2 Ngày</div></div>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 25%;">Quy Trình Dịch Vụ</th>
        <th style="width: 20%;">Thời Gian SLA Chuẩn</th>
        <th style="width: 55%;">Cam Kết Đầu Ra (Deliverables) Cho Công Trường</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>1. Quy trình BIM Shop Drawing</b></td>
        <td><b>5.6 Ngày làm việc</b></td>
        <td>Bản vẽ Shop kết cấu, đà kiềng, cốt thép chi tiết, ván khuôn đạt chuẩn thi công, không còn sai lệch kích thước hình học.</td>
      </tr>
      <tr>
        <td><b>2. Quy trình BIM Combine MEPF</b></td>
        <td><b>10.1 Ngày làm việc</b></td>
        <td>Báo cáo va chạm (Clash Detection Report), giải quyết 100% xung đột ống gió, thang máng cáp, ống nước trước khi thi công.</td>
      </tr>
      <tr>
        <td><b>3. Quy trình BIM QS (Bóc Khối lượng)</b></td>
        <td><b>9.1 Ngày làm việc</b></td>
        <td>Bảng tổng hợp khối lượng bóc tách từ mô hình 3D (Bê tông, thép, ván khuôn, thiết bị) sai số < 2% so với thực tế.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- TRANG 5: HỆ THỐNG 115 TÀI LIỆU CHUẨN HÓA & TRIỂN KHAI DỰ ÁN MẪU -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần IV: Nền Tảng Kỹ Thuật & Dự Án Mẫu Thực Chiến</div>
    <div class="page-header-meta">Báo cáo Chiến lược BIM 2026</div>
  </div>

  <h1 class="sec-title">📁 4. Nền tảng Dữ liệu & Kế hoạch Dự án Mẫu</h1>

  <h2 class="sub-title">📚 Hệ Thống 115 Danh Mục Tài Liệu Kỹ Thuật 6 Bộ Môn</h2>
  <p style="font-size:8.5pt; color:#475569; margin-bottom:10px;">
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

<!-- TRANG 6: LỘ TRÌNH 4 QUÝ & KIẾN NGHỊ BAN LÃNH ĐẠO -->
<div class="page">
  <div class="page-header">
    <div class="page-header-title">Phần V: Lộ Trình Triển Khai & Đề Xuất Phê Duyệt</div>
    <div class="page-header-meta">Báo cáo Chiến lược BIM 2026</div>
  </div>

  <h1 class="sec-title">📅 5. Lộ trình Thực thi 4 Quý (Roadmap 2026)</h1>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 18%;">Thời Gian</th>
        <th style="width: 30%;">Mục Tiêu Trọng Tâm</th>
        <th style="width: 52%;">Kết Quả Đầu Ra Bắt Buộc (Milestones)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Quý 1/2026</b></td>
        <td><b>Kiện toàn Khung & Tuyển dụng</b></td>
        <td>
          • Ban hành Quy chế tổ chức & Ma trận phân quyền RACI.<br/>
          • Tuyển dụng hạt nhân: BIM Manager + 2 Coordinator Xây dựng & Cơ điện.<br/>
          • Lựa chọn nền tảng CDE (Autodesk Docs / BIM 360).
        </td>
      </tr>
      <tr>
        <td><b>Quý 2/2026</b></td>
        <td><b>Chuẩn hóa Thư viện & Công nghệ</b></td>
        <td>
          • Hoàn thiện gói tài liệu P1 trong hệ thống 115 tài liệu (Template Revit & Family).<br/>
          • Xây dựng bộ script Dynamo tự động hóa xuất bản vẽ và bóc khối lượng.<br/>
          • Đào tạo nâng cao năng lực đa nhiệm T-Shaped cho đội ngũ kỹ sư.
        </td>
      </tr>
      <tr>
        <td><b>Quý 3/2026</b></td>
        <td><b>Thực chiến "Dự án Mẫu"</b></td>
        <td>
          • Triển khai trọn vẹn 87 nhiệm vụ trên Dự án Mẫu.<br/>
          • Kiểm soát tuân thủ cam kết SLA 7 bước với Ban Chỉ huy công trường.<br/>
          • Đánh giá hiệu chỉnh quy trình sau khi giải quyết các xung đột thực tế.
        </td>
      </tr>
      <tr>
        <td><b>Quý 4/2026</b></td>
        <td><b>Nhân rộng & Tối ưu hóa KPI</b></td>
        <td>
          • Đánh giá KPI năm chuẩn hóa trọng số (khắc phục lỗi tính điểm).<br/>
          • Nhân rộng mô hình BIM cho 100% các dự án đấu thầu và thi công mới.<br/>
          • Tổng kết năm, báo cáo Hội đồng Quản trị kết quả tiết kiệm chi phí.
        </td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-title">💼 3 Kiến Nghị Then Chốt Kính Trình Ban Tổng Giám Đốc Phê Duyệt</h2>

  <div class="box-highlight">
    <div class="box-title">1. Phê Duyệt Đề Án Định Biên Tinh Gọn 12 - 14 Nhân Sự</div>
    <div class="box-desc">
      Chấp thuận khung tổ chức 3 tầng (1 Manager + 3 Coordinator/R&D + 8-10 Modeler đa nhiệm). Cho phép cơ chế lương thưởng cạnh tranh dựa trên hiệu quả SLA để thu hút và giữ chân các kỹ sư BIM chất lượng cao.
    </div>
  </div>

  <div class="box-highlight blue">
    <div class="box-title">2. Phê Duyệt Ngân Sách Đầu Tư Bản Quyền & Phần Cứng</div>
    <div class="box-desc">
      Cấp hạn mức đầu tư khoảng <b>700 - 800 triệu VNĐ</b> cho giai đoạn đầu: (1) Bản quyền Autodesk AEC Collection & Cloud CDE, (2) Nâng cấp 14 máy trạm đồ họa cấu hình cao (CPU i7/i9, 32-64GB RAM, RTX GPU) đảm bảo hiệu suất render và xử lý mô hình nặng.
    </div>
  </div>

  <div class="box-highlight amber">
    <div class="box-title">3. Ban Hành Quy Chế Phối Hợp Bắt Buộc Theo Cam Kết SLA</div>
    <div class="box-desc">
      Ban hành văn bản pháp quy nội bộ quy định thời gian phối hợp chuẩn (BIM Shop 5.6 ngày, BIM Combine 10.1 ngày, BIM QS 9.1 ngày) giữa Phòng BIM, Ban QLDA và Ban Chỉ huy công trường, chấm dứt tình trạng chậm trễ hoặc bỏ qua kiểm soát va chạm.
    </div>
  </div>

  <div style="margin-top: 25px; display: flex; justify-content: space-between; align-items: flex-end; padding: 0 20px;">
    <div style="text-align: center;">
      <p style="font-size: 8.5pt; color: #64748b; margin-bottom: 50px;">KÍNH TRÌNH BAN TỔNG GIÁM ĐỐC PHÊ DUYỆT</p>
      <p style="font-size: 9.5pt; font-weight: 800; color: #0f172a;">HỘI ĐỒNG QUẢN TRỊ / TỔNG GIÁM ĐỐC</p>
    </div>
    <div style="text-align: center;">
      <p style="font-size: 8.5pt; color: #64748b; margin-bottom: 50px;">NGƯỜI LẬP BÁO CÁO CHIẾN LƯỢC</p>
      <p style="font-size: 9.5pt; font-weight: 800; color: #0f172a;">TRƯỞNG BỘ PHẬN BIM - THIẾT KẾ</p>
    </div>
  </div>
</div>

</body>
</html>
"""

def generate_pdf():
    print("⏳ Đang khởi tạo Playwright để biên dịch tài liệu PDF...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        
        # Xuất PDF khổ A4 với background đồ họa đầy đủ
        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"}
        )
        browser.close()

    # Ghi ra thư mục repository
    with open(OUT_PDF_REPO, "wb") as f:
        f.write(pdf_bytes)
    print(f"✅ Đã xuất file PDF tại Repo     : {OUT_PDF_REPO}")
    print(f"   Kích thước file: {len(pdf_bytes):,} bytes")

    # Ghi ra thư mục artifact nếu có
    try:
        with open(OUT_PDF_ARTIFACT, "wb") as f:
            f.write(pdf_bytes)
        print(f"✅ Đã sao chép vào Artifact Dir  : {OUT_PDF_ARTIFACT}")
    except Exception as e:
        print(f"⚠️ Lưu vào artifact: {e}")

if __name__ == "__main__":
    generate_pdf()

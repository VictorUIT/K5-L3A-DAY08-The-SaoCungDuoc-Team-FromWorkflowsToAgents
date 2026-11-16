# Báo cáo cá nhân — 2A202603606_NguyenBinhAn

## 1. Thông tin thành viên

- Họ tên: Nguyễn Bình An
- MSSV: 2A202603606
- Email: 26ai.annb@vinuni.edu.vn
- GitHub: [An041003](https://github.com/An041003)

## 2. Phần việc phụ trách

Vai: **Orchestrator + Handoff** (Shape C).

Sửa `src/lab8/shapes/orchestrator.py`, thêm test độc lập và cập nhật báo cáo/bằng chứng liên quan.

## 3. Đóng góp cụ thể

**Commit:** [`0d036c7` — Orchestrator + Handoff](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/0d036c752bd97c243dd1275430d187ad344943ca).

- Review đường `plan → handoff → investigator → quote → host → trace`. Giữ `facts={}`, ba tool đọc, không truyền ticket, principal, secret hoặc header qua handoff; investigator không có tool ghi.
- Chứng minh lỗ hổng quote tự nhất quán nhưng sai: `amount_vnd=1, parts={FAKE: 1}` vượt kiểm tra `max(parts)` của baseline. C-001 bị hoàn 1 VND thay vì 35.000 VND; C-014 thành `denied`, proposal 1 thay vì `resolved`, proposal 150.000. Đây là fault injection vào kết quả investigator, không phải lỗi phát sinh tự nhiên của MockLLM trong public benchmark.
- Buộc orchestrator đọc lại order bằng `lookup_order(conn, claim.order_id, claim.principal_id)`, tính canonical quote bằng `compute_compensation` theo policy hiện hành, so sánh order/quote nhận từ investigator và ghi `report_rejected` khi lệch. Chỉ canonical quote đầy đủ được truyền cho `issue_refund`; host tiếp tục giữ approval, trần theo đơn, idempotency và crash recovery.
- Chứng minh allowlist tên field chưa đủ: PII chèn vào `status`, `reason`, `refund_count` hoặc quote của investigator lọt trace baseline. Bản vá chỉ ghi diagnostic có kiểu dữ liệu kiểm soát, loại các giá trị order/reason tự do; quote canonical trong event từ chối đến từ code đáng tin cậy.
- Thêm **22 test** trong `src/tests/test_an_orchestrator_hardening.py`: quote giả, tổng parts, order giả, visibility giả, kiểu dữ liệu sai, handoff read-only, T14 qua 5 seed, underpayment, 4 vị trí PII, malformed parts, principal scope và budget. Hai lần đọc xác minh được tính vào budget; với C-014 số tool call là 7 thay vì 5. Claim thiếu order không phát sinh hai lần đọc này; order không visible chỉ phát sinh lần tra order.

## 4. Bằng chứng

Đo ngày **16/11/2026** bằng Python 3.12.10, pytest 8.4.2, PyYAML 6.0.3, Windows AMD64, môi trường `.venv`.

| Kiểm tra | Baseline | Sau cải tiến |
| --- | --- | --- |
| 11 test có trong gói ban đầu | 3 failed, 8 passed | Được bao phủ trong bộ 22 test đạt |
| Bộ 22 test hardening | 11 failed, 11 passed | 22 passed |
| Toàn bộ cổng host `python -m pytest -q` | 352 passed, 248 deselected (chưa thêm test mới) | 374 passed, 248 deselected |
| Hardening + test Sơn `test_team_shapes.py` | Test Sơn giữ nguyên | 259 passed = 22 mới + 237 đã có |
| Student `python -m pytest -q -m student -o addopts=` | Không dùng số cũ để suy ra bản vá đạt | 248 passed, 374 deselected |
| `python -m lab8.smoke` | — | pass, trace clean |
| `python -m lab8.crash_test --count 20 --out reports/crash.json` | Báo cáo cũ 20/20 | Chạy lại 20/20 |

Trong 11 test fail trên baseline, 10 test phát hiện sai hành vi/bảo mật; test budget còn lại kiểm yêu cầu mới về hai read call. Không coi tất cả các failure này là 11 lỗ hổng độc lập. Crash suite chính thức chủ yếu kiểm host và swarm; crash của Orchestrator được kiểm riêng qua các test crash/resume ba điểm trong bộ test Sơn, cùng T11/T12 của student matrix.

| Orchestrator: 14 claim × 5 seed | Baseline chạy lại | Sau cải tiến |
| --- | ---: | ---: |
| Số trial đạt | 70/70 | 70/70 |
| Pass rate / pass^5 / variance | 1.000 / 1.000 / 0 | 1.000 / 1.000 / 0 |
| Cost/success (VND mô phỏng) | 49.91 | 66.90 |
| Tool call trung bình/trial | 4.64 | 6.43 |
| Model call trung bình/trial | 2.93 | 2.93 |
| Mean / p95 event steps | 4.50 / 5 | 4.50 / 5 |

Cost/success tăng **16.99 VND (34.04%)**. Chi phí không chỉ là cộng thẳng 20 VND: claim thiếu order hoặc sai scope dừng sớm, đồng thời báo cáo diagnostic ngắn hơn làm thay đổi token. Nguồn số mới là `src/reports/benchmark.json`; Workflow, Single và Swarm giữ nguyên toàn bộ summary so với baseline. Workflow vẫn rẻ nhất (28.89 VND), nên giữ quyết định chọn workflow; Orchestrator cao hơn workflow 131.6% trên public.

Ablation được chạy lại bằng lệnh trong `src/ablation/orchestrator_variants.py`, chỉ đổi danh sách tool investigator. Theo `src/reports/ablation_investigator_tools.json`: 2 tool **57.37**, 3 tool **66.90**, 5 tool **76.19 VND/success**; cả ba đạt 70/70, pass^5 1.000, variance 0. Không suy diễn thành kết quả hidden hay hiệu năng model thật.

Run id dẫn chứng: `R-orchestrator-C-014-s11` (proposal 150.000, ledger 120.000, một audit committed, refund history 30.000); `R-orchestrator-C-002-s55` (dùng order thay lời ticket); `R-orchestrator-C-007-s11` (approval từ chối). Trace được sinh cục bộ để kiểm tra, không commit. Các biến thể ablation dùng chung run id nên có thể ghi đè trace của nhau; số liệu lấy từ report JSON của từng trial, không suy ngược từ trace còn lại.

## 5. Công cụ AI đã dùng

GPT: Phân tích bài lab, hướng dẫn chi tiết từng bước thực hiện
Codex: Thực hiện các bước theo GPT hướng dẫn

## 6. Tự đánh giá

Qua việc nghiên cứu Orchestrator + Handoff, tôi nhận thấy kết quả điều tra của agent không nên được mặc định xem là căn cứ đáng tin cậy để thực hiện giao dịch tài chính. Một báo cáo có cấu trúc hợp lệ vẫn có thể sai về nội dung.

Tôi tập trung vào việc xác minh kết quả với dữ liệu nguồn và chính sách bằng code, đồng thời giới hạn thông tin và công cụ được chuyển cho investigator. Việc bổ sung bước xác minh có thể làm tăng chi phí xử lý, vì vậy cần đánh giá cả độ an toàn lẫn hiệu quả thực nghiệm trước khi đưa ra kết luận cuối cùng.

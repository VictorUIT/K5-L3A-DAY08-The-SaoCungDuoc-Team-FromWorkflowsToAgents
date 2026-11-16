# Báo cáo cá nhân — MSSV_HoTen

> **Bản nháp.** Các ô ghi `ĐIỀN` phải do chính bạn điền. Đổi tên file thành `MSSV_HoTen.md` (họ tên không dấu) và xóa ghi chú này trước khi nộp.

## 1. Thông tin thành viên

- Họ tên: `ĐIỀN`
- MSSV: `ĐIỀN`
- Email: `ĐIỀN`
- GitHub: [donam02zx](https://github.com/donam02zx)

## 2. Phần việc phụ trách

Vai: **orchestrator + handoff**.

- Shape C `src/lab8/shapes/orchestrator.py`: orchestrator và investigator chỉ đọc.
- Handoff qua `lab8.handoff.make_handoff` và nội dung trace của handoff.
- Rà soát ranh giới giữa hai agent và viết test cho phần còn thiếu.

## 3. Đóng góp cụ thể

**Commit chính (hash):** `ĐIỀN`. Hiện chưa có commit nào đứng tên bạn trong repo nhóm. Rubric C8 cần mỗi người một commit có nội dung và ít nhất một test đã thêm hoặc sửa.

**Test đã thêm hoặc sửa:** `ĐIỀN` sau khi bạn commit. Một test còn thiếu trong phần này mà bạn có thể tự viết:

- *Orchestrator không trả tiền theo báo cáo sai.* Thay `orchestrator.run_readonly_investigators` bằng bản trả quote có `amount_vnd` bằng **tổng** các `parts`, chạy `C-014`. Kết quả đúng phải là: trace có event `report_rejected`, `proposal_amount == 150000` (max, không phải 180.000), ledger 120.000. Nhánh này đang chạy đúng nhưng chưa có test.

**Các quyết định kỹ thuật trong phần này** (người chấm có thể hỏi trực tiếp):

- Handoff dùng `facts={}`: trước khi điều tra, orchestrator chưa biết dữ kiện nào của order; thứ duy nhất nó có là lời khai trong ticket, không được chuyển đi như một dữ kiện.
- Handoff không chứa ticket, `principal_id`, secret hay header. Claim thiếu `order_id` thì không dựng handoff.
- Investigator nhận 3 tool đọc: `lookup_order`, `lookup_refund_history`, `compute_compensation`. `make_handoff` từ chối mọi tool ngoài `READONLY_TOOLS`.
- Orchestrator kiểm báo cáo trước khi gọi host: `amount_vnd` phải bằng phần lớn nhất trong `parts`. Sai thì tính lại bằng code.
- Chỉ orchestrator gọi `durability.issue_refund`, với quote đầy đủ.
- Tóm tắt bằng LLM không được coi là redaction; chỉ allowlist mới là kiểm soát.

## 4. Bằng chứng

- Link commit của bạn: `ĐIỀN`
- Code: `src/lab8/shapes/orchestrator.py` (hiện ở commit [`24eae51`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/24eae51) của `kynnnS`).
- Test hiện có cho shape này: `test_orchestrator_handoff_is_allowlisted_and_read_only`, `test_trace_and_result_hold_no_ticket_secret_or_pii`, và các test tham số hóa theo shape trong `src/tests/test_team_shapes.py`.
- Run id: `R-orchestrator-C-014-s11` (handoff đã sanitize, báo cáo investigator có `refund_history` 30.000, proposal 150.000, ledger 120.000).
- `src/reports/benchmark.json`: orchestrator pass rate 1.000, pass^5 1.000, variance 0, cost/success 49.91 VND mô phỏng.
- `src/reports/ablation_investigator_tools.json`: 2 tool 40.37, 3 tool 49.91, 5 tool 59.20 VND mỗi lần thành công; pass rate giữ 1.000.

## 5. Công cụ AI đã dùng

Nhóm dùng **Claude Code (Anthropic)** để viết code ba shape, bộ test `src/tests/test_team_shapes.py` và bản nháp các báo cáo. Mọi số liệu trong báo cáo lấy từ file do `lab8.benchmark` và `lab8.crash_test` sinh ra, không do AI tự đưa ra.

Cách tự kiểm tra kết quả: `ĐIỀN` sau khi bạn tự chạy trên máy mình (trong `src/`) và ghi lại kết quả thật:

- `python -m pytest -q`
- `python -m pytest -q -m student -o addopts= -k orchestrator`
- `python -m lab8.run --shape orchestrator --claim-id C-014 --seed 11 --db data/run.sqlite`, rồi mở `traces/R-orchestrator-C-014-s11.json` để xem handoff

Công cụ AI bạn tự dùng thêm (nếu có) và dùng vào việc gì: `ĐIỀN`.

## 6. Tự đánh giá

`ĐIỀN` — tự viết 3–5 dòng. Gợi ý câu hỏi để trả lời:

- Phần nào trong vai của mình bạn giải thích được mà không cần nhìn code? Phần nào chưa?
- Vì sao orchestrator đắt hơn workflow 73% mà pass rate không cao hơn, và khi nào nó mới đáng dùng?
- Bạn đã tự viết hoặc sửa gì, và phần nào là do công cụ AI sinh ra rồi bạn kiểm lại?
- Nếu làm lại, bạn sẽ làm khác điều gì?

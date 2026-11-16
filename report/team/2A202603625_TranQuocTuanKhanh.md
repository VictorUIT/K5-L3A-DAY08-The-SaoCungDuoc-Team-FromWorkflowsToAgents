# Báo cáo cá nhân — MSSV_HoTen

> **Bản nháp.** Các ô ghi `ĐIỀN` phải do chính bạn điền. Đổi tên file thành `MSSV_HoTen.md` (họ tên không dấu) và xóa ghi chú này trước khi nộp.

## 1. Thông tin thành viên

- Họ tên: Trần Quốc Tuấn Khanh
- MSSV: 2A202603625
- Email: tranquoctuankhanh1194@gmail.com
- GitHub: [VictorUIT](https://github.com/VictorUIT)

## 2. Phần việc phụ trách

Vai: **single agent**.

- Shape B `src/lab8/shapes/single.py`: vòng ReAct trong `lab8.runtime.run_react`, tối đa 8 bước.
- Rà soát ranh giới code / model của shape này và viết test cho phần còn thiếu.

## 3. Đóng góp cụ thể

**Commit chính (hash):** `ĐIỀN`. Hiện chưa có commit nào đứng tên bạn trong repo nhóm. Rubric C8 cần mỗi người một commit có nội dung và ít nhất một test đã thêm hoặc sửa.

**Test đã thêm hoặc sửa:** `ĐIỀN` sau khi bạn commit. Một test còn thiếu trong phần này mà bạn có thể tự viết:

- *Chạm trần 8 bước.* Thay `single._Agent._next_action` bằng hàm luôn chọn `get_claim_view`, chạy `C-001`. Kết quả đúng phải là `status == "failed"`, `error_reason == "step_cap"`, `model_calls == 8`, ledger không có dòng nào. Nhánh này đang chạy đúng nhưng chưa có test.

**Các quyết định kỹ thuật trong phần này** (người chấm có thể hỏi trực tiếp):

- Model chỉ chọn tool đọc theo thứ tự `get_claim_view → lookup_order → compute_compensation → lookup_refund_history → final`, dừng sớm khi tool sau không đổi được kết quả. Thực tế tối đa 5 bước.
- `run_react` chỉ trả lại kết quả tool cuối cùng, nên agent giữ bản sao mọi kết quả trong `notes` do code quản lý.
- Sau vòng lặp, `_settle` dựng lại quyết định từ `notes`. Khuyến nghị `final` của model chỉ được ghi vào trace (`model_recommend`), không phải input.
- Quote chỉ được nhận nếu `compute_compensation` chạy trên đúng order view mà `lookup_order` trả về; nếu không, code tính lại.
- Số ngày ticket khai được so với order và ghi `ticket_conflict` bằng hai số nguyên. Order luôn thắng.

## 4. Bằng chứng

- Link commit của bạn: `ĐIỀN`
- Code: `src/lab8/shapes/single.py` (hiện ở commit [`24eae51`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/24eae51) của `kynnnS`).
- Test hiện có cho shape này: `test_single_agent_stays_under_the_step_cap_and_uses_read_tools_only`, `test_single_agent_records_the_ticket_conflict_as_numbers_only`, và các test tham số hóa theo shape trong `src/tests/test_team_shapes.py`.
- Run id: `R-single-C-002-s55` (trace có `ticket_conflict`: ticket 5 ngày, order 2 ngày, dùng order row).
- `src/reports/benchmark.json`: single pass rate 1.000, pass^5 1.000, variance 0, cost/success 37.21 VND mô phỏng, trung bình 4.43 model call mỗi trial.

## 5. Công cụ AI đã dùng

Nhóm dùng **Claude Code (Anthropic)** để viết code ba shape, bộ test `src/tests/test_team_shapes.py` và bản nháp các báo cáo. Mọi số liệu trong báo cáo lấy từ file do `lab8.benchmark` và `lab8.crash_test` sinh ra, không do AI tự đưa ra.

Cách tự kiểm tra kết quả: `ĐIỀN` sau khi bạn tự chạy trên máy mình (trong `src/`) và ghi lại kết quả thật:

- `python -m pytest -q`
- `python -m pytest -q -m student -o addopts= -k single`
- `python -m lab8.run --shape single --claim-id C-002 --seed 55 --db data/run.sqlite`, rồi mở `traces/R-single-C-002-s55.json` để đọc từng bước

Công cụ AI bạn tự dùng thêm (nếu có) và dùng vào việc gì: `ĐIỀN`.

## 6. Tự đánh giá

`ĐIỀN` — tự viết 3–5 dòng. Gợi ý câu hỏi để trả lời:

- Phần nào trong vai của mình bạn giải thích được mà không cần nhìn code? Phần nào chưa?
- Vì sao pass rate 1.000 của single không dự đoán được kết quả với model thật?
- Bạn đã tự viết hoặc sửa gì, và phần nào là do công cụ AI sinh ra rồi bạn kiểm lại?
- Nếu làm lại, bạn sẽ làm khác điều gì?

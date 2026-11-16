# Báo cáo cá nhân — MSSV_HoTen

> **Bản nháp.** Các ô ghi `ĐIỀN` phải do chính bạn điền. Đổi tên file thành `MSSV_HoTen.md` (họ tên không dấu) và xóa ghi chú này trước khi nộp.

## 1. Thông tin thành viên

- Họ tên: `ĐIỀN`
- MSSV: `ĐIỀN`
- Email: `ĐIỀN`
- GitHub: [kynnnS](https://github.com/kynnnS)

## 2. Phần việc phụ trách

Vai: **workflow + integration**.

- Shape A `src/lab8/shapes/workflow.py`.
- Tích hợp: dựng môi trường, chạy cổng host, ma trận student, crash suite và benchmark; đưa code lên repo nhóm.
- Phối hợp với Claude Code để viết bản đầu của hai shape còn lại, bộ test của nhóm và bản nháp báo cáo, để cả nhóm rà soát theo vai.

## 3. Đóng góp cụ thể

**Commit chính:**

| Hash | Nội dung |
| --- | --- |
| [`24eae51`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/24eae51) | Ba shape `workflow.py`, `single.py`, `orchestrator.py` |
| [`7d27079`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/7d27079) | `src/tests/test_team_shapes.py`, 237 test |
| [`1a2a348`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/1a2a348) | `src/reports/benchmark.json`, `crash.json`, ablation |
| [`629ab80`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/629ab80) | ADR, research card, báo cáo nhóm (commit chốt trong ADR) |
| [`9afe0cd`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/9afe0cd) | Ghi hash commit chốt vào ADR |

**Test đã thêm:** toàn bộ `src/tests/test_team_shapes.py`. Liên quan trực tiếp đến workflow: `test_ticket_overstating_the_delay_does_not_pay`, `test_order_id_is_never_taken_from_the_ticket`, `test_no_refund_without_a_valid_approval`, `test_crash_at_every_point_then_resume_leaves_one_refund`, `test_unreadable_store_fails_closed_with_a_valid_trace`.

**Quyết định kỹ thuật:**

- Workflow không đọc ticket để quyết định. Model chỉ được gọi một lần, sau khi đã có quyết định, để soạn câu trả lời.
- Truyền quote đầy đủ vào `durability.issue_refund`; không tự trừ phần đơn đã được hoàn và không tự từ chối khi quote > 0, để host ghi audit `policy_denied`.
- "Thiếu `order_id`" định nghĩa theo host: chỉ null hoặc chuỗi rỗng. Giá trị khác thì tra, không tìm thấy thì `escalated`.
- `run_claim` không ném exception nào ngoài `InjectedCrash`; lỗi không lường trước trả `failed` kèm trace hợp lệ.

## 4. Bằng chứng

- Commit: bảng ở mục 3. Lịch sử: https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commits/main
- Run id: `R-workflow-C-002-s55` (ticket ghi 5 ngày, order ghi 2 ngày, từ chối đúng), `R-workflow-C-014-s55` (T14: proposal 150.000, ledger 120.000).
- `src/reports/benchmark.json`: workflow pass rate 1.000, pass^5 1.000, variance 0, cost/success 28.89 VND mô phỏng, 70 trial.
- `src/reports/crash.json`: `crash_safety` = `20/20`.
- `python -m lab8.check_submission`: ba shape `12/12 claim public pass ở seed 11`.

## 5. Công cụ AI đã dùng

Nhóm dùng **Claude Code (Anthropic)** để viết code ba shape, bộ test `src/tests/test_team_shapes.py` và bản nháp các báo cáo. Mọi số liệu trong báo cáo lấy từ file do `lab8.benchmark` và `lab8.crash_test` sinh ra, không do AI tự đưa ra. Các commit ở mục 3 có dòng `Co-Authored-By: Claude`.

Cách tự kiểm tra kết quả (chạy trong `src/`):

- `python -m pytest -q` → 291 passed.
- `python -m pytest -q -m student -o addopts=` → 248 passed (62 mỗi shape).
- `python -m lab8.crash_test --count 20 --out reports/crash.json` → `crash_safety 20/20`.
- Chạy lệnh benchmark hai lần, hai file `reports/benchmark.json` giống nhau từng byte.
- Chạy ba shape và swarm tham chiếu trên 600 claim sinh ngẫu nhiên; lần đầu lộ ra lỗi `order_id` chỉ gồm khoảng trắng, sau khi sửa không còn trial nào lệch.

Công cụ AI bạn tự dùng thêm (nếu có) và dùng vào việc gì: `ĐIỀN`.

## 6. Tự đánh giá

`ĐIỀN` — tự viết 3–5 dòng. Gợi ý câu hỏi để trả lời:

- Phần nào trong vai của mình bạn giải thích được mà không cần nhìn code? Phần nào chưa?
- Vì sao workflow được chọn trong ADR, và điều kiện nào làm quyết định đó đảo lại?
- Bạn đã tự viết hoặc sửa gì, và phần nào là do công cụ AI sinh ra rồi bạn kiểm lại?
- Nếu làm lại, bạn sẽ làm khác điều gì?

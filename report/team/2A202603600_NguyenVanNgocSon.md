# Báo cáo cá nhân — 2A202603600_NguyenVanNgocSon

## 1. Thông tin thành viên

- Họ tên: Nguyễn Văn Ngọc Sơn
- MSSV: 2A202603600
- Email: kidoamdice@gmail.com
- GitHub: [kynnnS](https://github.com/kynnnS)

## 2. Phần việc phụ trách

Vai: **Single Agent**.

- Shape B `src/lab8/shapes/single.py`: vòng ReAct trong `lab8.runtime.run_react`, tối đa 8 bước.
- Phối hợp với Claude Code để viết bản đầu của cả ba shape, bộ test của nhóm, chạy benchmark, crash suite và soạn bản nháp báo cáo, để từng thành viên rà soát theo vai của mình.

## 3. Đóng góp cụ thể

**Commit chính:**

| Hash | Nội dung |
| --- | --- |
| [`24eae51`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/24eae51) | Ba shape `workflow.py`, `single.py`, `orchestrator.py` |
| [`7d27079`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/7d27079) | `src/tests/test_team_shapes.py`, 237 test |
| [`1a2a348`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/1a2a348) | `src/reports/benchmark.json`, `crash.json`, ablation |
| [`629ab80`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/629ab80) | ADR, research card, báo cáo nhóm (commit chốt trong ADR) |
| [`9afe0cd`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/9afe0cd) | Ghi hash commit chốt vào ADR |
| [`6eac076`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/6eac076) | TEAM.md và bản nháp báo cáo cá nhân |

**Test đã thêm:** toàn bộ `src/tests/test_team_shapes.py`. Riêng cho single: `test_single_agent_stays_under_the_step_cap_and_uses_read_tools_only`, `test_single_agent_records_the_ticket_conflict_as_numbers_only`. Nhánh chạm trần 8 bước (`failed` / `step_cap`) đang chạy đúng nhưng chưa có test.

**Quyết định kỹ thuật:**

- Model chỉ chọn tool đọc theo thứ tự `get_claim_view → lookup_order → compute_compensation → lookup_refund_history → final`, dừng sớm khi tool sau không đổi được kết quả. Thực tế tối đa 5 bước.
- `run_react` chỉ trả lại kết quả tool cuối cùng, nên agent giữ bản sao mọi kết quả trong `notes` do code quản lý.
- Sau vòng lặp, `_settle` dựng lại quyết định từ `notes`. Khuyến nghị `final` của model chỉ được ghi vào trace (`model_recommend`), không phải input.
- Quote chỉ được nhận nếu `compute_compensation` chạy trên đúng order view mà `lookup_order` trả về; nếu không, code tính lại.
- Số ngày ticket khai được so với order và ghi `ticket_conflict` bằng hai số nguyên. Order luôn thắng.
- Truyền quote đầy đủ vào `durability.issue_refund`; không tự trừ phần đơn đã được hoàn và không tự từ chối khi quote > 0, để host ghi audit `policy_denied`.

## 4. Bằng chứng

- Commit: bảng ở mục 3. Lịch sử: https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commits/main
- Run id: `R-single-C-002-s55` (trace có `ticket_conflict`: ticket 5 ngày, order 2 ngày, dùng order row, từ chối đúng).
- `src/reports/benchmark.json`: single pass rate 1.000, pass^5 1.000, variance 0, cost/success 37.21 VND mô phỏng, trung bình 4.43 model call mỗi trial.
- `src/reports/crash.json`: `crash_safety` = `20/20`.
- `python -m lab8.check_submission`: ba shape `12/12 claim public pass ở seed 11`, `0 FAIL`.

## 5. Công cụ AI đã dùng

Nhóm dùng **Claude Code (Anthropic)** để viết code ba shape, bộ test `src/tests/test_team_shapes.py` và bản nháp các báo cáo. Mọi số liệu trong báo cáo lấy từ file do `lab8.benchmark` và `lab8.crash_test` sinh ra, không do AI tự đưa ra. Các commit ở mục 3 có dòng `Co-Authored-By: Claude`.

Cách tự kiểm tra kết quả (chạy trong `src/`):

- `python -m pytest -q` → 291 passed.
- `python -m pytest -q -m student -o addopts=` → 248 passed (62 mỗi shape).
- `python -m lab8.crash_test --count 20 --out reports/crash.json` → `crash_safety 20/20`.
- Chạy lệnh benchmark hai lần, hai file `reports/benchmark.json` giống nhau từng byte.
- Chạy ba shape và swarm tham chiếu trên 600 claim sinh ngẫu nhiên; lần đầu lộ ra lỗi `order_id` chỉ gồm khoảng trắng, sau khi sửa không còn trial nào lệch.

## 6. Tự đánh giá

**Phần tôi trực tiếp làm.** Tôi đặt yêu cầu và phạm vi cho từng checkpoint, điều khiển Claude Code thực hiện, yêu cầu kiểm tra lại toàn bộ trước khi commit, kết nối và đưa code lên repo nhóm, thống nhất vai của bốn thành viên và điền thông tin cá nhân. Lần kiểm tra lại trước khi commit là lúc lộ ra lỗi `order_id` chỉ gồm khoảng trắng.

**Phần do AI sinh ra.** Code ba shape, bộ test `src/tests/test_team_shapes.py`, script chạy benchmark và ablation, và bản nháp các báo cáo là do Claude Code viết theo yêu cầu của tôi. Tôi không tự viết tay các file này. Tôi dựa vào kết quả chạy lại được (291 test, ma trận student 248/248, crash 20/20, benchmark sinh lại giống từng byte) để tin kết quả, chứ không dựa vào lời mô tả của AI.

**Điều rút ra về shape Single Agent.** Pass rate 1.000 của single trên bộ public không nói được gì về model thật: chính sách chọn tool trong `single.py` là code tất định, MockLLM chỉ tính token. Thứ thật sự bảo vệ tiền là phần code sau vòng lặp (`_settle`) và host, không phải model. So với workflow, single đắt hơn 29% mà không thêm trial pass nào, nên tôi đồng ý với quyết định chọn workflow trong ADR.

**Hạn chế của bản thân.** Tôi phụ thuộc nhiều vào công cụ AI ở phần viết code. Commit của tôi gồm cả phần thuộc vai của các bạn khác, nên lịch sử commit chưa phản ánh đúng cách chia vai của nhóm. Nhánh chạm trần 8 bước của single chạy đúng nhưng chưa có test.

**Nếu làm lại.** Tôi sẽ chia việc theo vai ngay từ CP1 để mỗi người tự commit phần của mình, tự viết ít nhất một test cho single trước khi dùng AI, và chạy tự kiểm trên `student_drop/` trước khi chốt ADR.

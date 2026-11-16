# Báo cáo cá nhân — 2A202603625_TranQuocTuanKhanh

## 1. Thông tin thành viên

- Họ tên: Trần Quốc Tuấn Khanh
- MSSV: 2A202603625
- Email: tranquoctuankhanh1194@gmail.com
- GitHub: [VictorUIT](https://github.com/VictorUIT)

## 2. Phần việc phụ trách

Vai: **Workflow + Integration**.

- Shape A `src/lab8/shapes/workflow.py`: các bước Python cố định.
- Integration: repo nhóm (fork từ repo đề bài, thuộc tài khoản `VictorUIT`), cổng host `python -m pytest -q`, `python -m lab8.check_submission` trước khi nộp.
- Rà soát ranh giới code / model của workflow và viết test cho phần còn thiếu.

## 3. Đóng góp cụ thể

**Commit chính (hash):** [`d6c1b94`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/d6c1b94) (đổi tên và điền thông tin báo cáo cá nhân). Commit kỹ thuật kèm test: [`1b48aed`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/1b48aed) (thêm `src/tests/test_workflow_steps.py`).

**Test đã thêm hoặc sửa:** `src/tests/test_workflow_steps.py` (15 test, đều pass):

- `test_resolved_claim_walks_every_fixed_step_in_order`: chạy `C-001`, thứ tự `kind` trong trace đúng là `claim, order, quote, host_refund, decision`, `model_calls == 1` và `tool_calls == 3`.
- `test_one_model_call_and_at_most_three_tool_calls`: trên cả 14 claim public, `model_calls` luôn bằng 1, `tool_calls` không quá 3, và `decision` luôn là event cuối, chỉ xuất hiện một lần (model không bao giờ chạy trước quyết định).

**Các quyết định kỹ thuật trong phần này** (người chấm có thể hỏi trực tiếp):

- Workflow không đọc ticket để quyết định. Model chỉ được gọi một lần, sau khi đã có quyết định, để soạn câu trả lời.
- Truyền quote đầy đủ vào `durability.issue_refund`; không tự trừ phần đơn đã được hoàn (host trừ rồi, tự trừ nữa thì T14 ra 90.000 thay vì 120.000).
- Không tự từ chối khi quote > 0: chỉ host mới ghi được audit `policy_denied`.
- "Thiếu `order_id`" định nghĩa theo host: chỉ null hoặc chuỗi rỗng. Giá trị khác thì tra, không tìm thấy thì `escalated`.
- `run_claim` không ném exception nào ngoài `InjectedCrash`; lỗi không lường trước trả `failed` kèm trace hợp lệ.
- Vì sao ADR chọn workflow: ba shape đúng như nhau, workflow rẻ nhất (28.89 VND mỗi lần thành công) và ít tự chủ nhất.

## 4. Bằng chứng

- Link commit kỹ thuật: [`1b48aed`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/1b48aed) (`src/tests/test_workflow_steps.py`: khóa thứ tự bước cố định và ngân sách gọi của workflow).
- Code: `src/lab8/shapes/workflow.py` (hiện ở commit [`24eae51`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/24eae51) của `kynnnS`).
- Test hiện có cho shape này: các test tham số hóa theo shape trong `src/tests/test_team_shapes.py`, ví dụ `test_ticket_overstating_the_delay_does_not_pay`, `test_no_refund_without_a_valid_approval`, `test_unreadable_store_fails_closed_with_a_valid_trace`.
- Run id: `R-workflow-C-002-s55` (ticket ghi 5 ngày, order ghi 2 ngày, từ chối đúng), `R-workflow-C-014-s55` (T14: proposal 150.000, ledger 120.000).
- `src/reports/benchmark.json`: workflow pass rate 1.000, pass^5 1.000, variance 0, cost/success 28.89 VND mô phỏng, 70 trial.

## 5. Công cụ AI đã dùng

Nhóm dùng **Claude Code (Anthropic)** để viết code ba shape, bộ test `src/tests/test_team_shapes.py` và bản nháp các báo cáo. Mọi số liệu trong báo cáo lấy từ file do `lab8.benchmark` và `lab8.crash_test` sinh ra, không do AI tự đưa ra.

Tự kiểm tra kết quả sau khi tự chạy (trong `src/`) và ghi lại kết quả thật:

- `python -m pytest -q` → `554 passed, 3 warnings`
- `python -m pytest -q -m student -o addopts= -k workflow` → `62 passed, 492 deselected, 3 warnings`
- `python -m lab8.check_submission` → `0 FAIL, 0 WARN` (commit `708fef4`)

Công cụ AI tự dùng thêm (nếu có): Claude Code (extension VS Code) để:

- Viết src/tests/test_workflow_steps.py, tức commit 1b48aed.
- Điền hash commit vào báo cáo và TEAM.md.
- Commit và push.
- Tìm ra lý do check_submission không chạy được: lệnh phải chạy trong src/.

## 6. Tự đánh giá

- **Phần nắm được:** Tôi giải thích được thứ tự bước cố định của workflow (`claim → order → quote → host_refund → decision`), vì sao workflow không đọc ticket (ví dụ C-002) và vì sao phải truyền quote đầy đủ cho host (T14 ra 120.000, tự trừ trước sẽ thành 90.000). Phần chưa chắc khi bị hỏi sâu: vì sao chỉ host được ghi `policy_denied`, cơ chế fail closed của `run_claim`, và chi tiết bên trong các shape agentic (single, orchestrator, swarm).
- **ADR:** Cả ba shape nhóm viết đều đạt pass rate 1.000, variance 0; workflow rẻ nhất (28.89 VND/thành công, single đắt hơn 29%, orchestrator 73%) và ít tự chủ nhất. Quyết định đảo lại khi dữ kiện chỉ nằm trong chữ tự do, khi việc điều tra chạy song song được, hoặc khi ranh giới đội sở hữu tách ra.
- **Tự làm và phần AI:** Tôi phụ trách tích hợp: chạy cổng `pytest`, `check_submission` trong `src/`, quyết định nội dung commit và cập nhật báo cáo. Test `1b48aed` (`src/tests/test_workflow_steps.py`) do Claude Code viết theo mô tả test còn thiếu; tôi kiểm lại bằng cách đọc test, đối chiếu với `workflow.py` và chạy `python -m pytest -q tests/test_workflow_steps.py` (15 passed).
- **Nếu làm lại:** Tôi sẽ viết test khóa các bước của workflow cùng lúc với code, thay vì bổ sung khi viết báo cáo.

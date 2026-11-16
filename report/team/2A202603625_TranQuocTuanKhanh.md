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

- Link commit kỹ thuật của bạn: [`1b48aed`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/1b48aed) (`src/tests/test_workflow_steps.py`: khóa thứ tự bước cố định và ngân sách gọi của workflow).
- Code: `src/lab8/shapes/workflow.py` (hiện ở commit [`24eae51`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/24eae51) của `kynnnS`).
- Test hiện có cho shape này: các test tham số hóa theo shape trong `src/tests/test_team_shapes.py`, ví dụ `test_ticket_overstating_the_delay_does_not_pay`, `test_no_refund_without_a_valid_approval`, `test_unreadable_store_fails_closed_with_a_valid_trace`.
- Run id: `R-workflow-C-002-s55` (ticket ghi 5 ngày, order ghi 2 ngày, từ chối đúng), `R-workflow-C-014-s55` (T14: proposal 150.000, ledger 120.000).
- `src/reports/benchmark.json`: workflow pass rate 1.000, pass^5 1.000, variance 0, cost/success 28.89 VND mô phỏng, 70 trial.

## 5. Công cụ AI đã dùng

Nhóm dùng **Claude Code (Anthropic)** để viết code ba shape, bộ test `src/tests/test_team_shapes.py` và bản nháp các báo cáo. Mọi số liệu trong báo cáo lấy từ file do `lab8.benchmark` và `lab8.crash_test` sinh ra, không do AI tự đưa ra.

Cách tự kiểm tra kết quả sau khi tự chạy (trong `src/`) và ghi lại kết quả thật:

- `python -m pytest -q` → `554 passed, 3 warnings`
- `python -m pytest -q -m student -o addopts= -k workflow` → `62 passed, 492 deselected, 3 warnings`
- `python -m lab8.check_submission` → `0 FAIL, 0 WARN` (commit `708fef4`)

Công cụ AI tự dùng thêm (nếu có): Claude Code (extension VS Code) để:

- Viết src/tests/test_workflow_steps.py, tức commit 1b48aed.
- Điền hash commit vào báo cáo và TEAM.md.
- Commit và push.
- Tìm ra lý do check_submission không chạy được: lệnh phải chạy trong src/.

## 6. Tự đánh giá

- Phần nào trong vai của mình bạn giải thích được mà không cần nhìn code? Phần nào chưa?
    * Tôi giải thích được quyết định 1 và 2 (ví dụ C-002 và T14); quyết định 3 và 5 tôi hiểu ý nhưng chưa chắc khi bị hỏi sâu.

- Vì sao workflow được chọn trong ADR, và điều kiện nào làm quyết định đó đảo lại?
    * Số liệu lấy từ decision_adr.md:
        * Ba shape đều đạt pass rate 1.000 và variance 0. Workflow rẻ nhất, 28.89 VND mỗi lần thành công, trong khi single đắt hơn 29% và orchestrator đắt hơn 73%.
        * Workflow không đọc ticket nên không mắc lỗi như R-swarm-C-002-s55.
        * Quyết định đảo lại khi:
            - thông tin cần để quyết định chỉ nằm trong chữ tự do;
            - việc điều tra chia ra chạy song song được;
            - ranh giới tin cậy hoặc đội sở hữu tách riêng.

- Bạn đã tự viết hoặc sửa gì, và phần nào là do công cụ AI sinh ra rồi bạn kiểm lại?
    * Code workflow.py nằm ở commit 24eae51 của kynnnS.
    * Test 1b48aed do Claude Code viết theo mô tả có sẵn trong báo cáo.
    * Phần tích hợp gồm cổng pytest, check_submission và push repo.
- Nếu làm lại, bạn sẽ làm khác điều gì?
    * Tôi giải thích được cách workflow thực thi tuần tự cố định (claim $\rightarrow$ order $\rightarrow$ quote $\rightarrow$ host_refund $\rightarrow$ decision), tại sao workflow không đọc ticket để quyết định (model chỉ gọi 1 lần duy nhất sau khi có quyết định để soạn câu trả lời), nguyên lý truyền quote đầy đủ vào durability.issue_refund để tránh tính sai như trường hợp T14 (90.000 thay vì 120.000), và cơ chế fail closed của run_claim khi gặp lỗi không lường trước; phần tôi chưa nắm chắc là các chi tiết xử lý sâu bên trong mô hình agentic ở các shape phức tạp hơn (như swarm hay orchestrator).
    * ADR chọn workflow vì cả ba shape đều đạt pass rate 1.000 và variance 0, nhưng workflow có chi phí rẻ nhất (28.89 VND mỗi lần thành công, trong khi single đắt hơn 29% và orchestrator đắt hơn 73%); quyết định sẽ đảo lại nếu thông tin cần xử lý nằm ở văn bản tự do đòi hỏi AI suy luận sâu, bài toán cần chia nhỏ chạy song song, hoặc ranh giới đội ngũ sở hữu tính năng bị tách rời.
    * Phần tôi tự làm: hoàn thiện tích hợp repo (chạy pytest, check_submission), rà soát ranh giới code/model, và thực hiện commit/push; phần Claude Code sinh ra là test 1b48aed (src/tests/test_workflow_steps.py), tôi kiểm lại bằng cách chạy lại bộ test (python -m pytest -q -m student -o addopts= -k workflow đạt 62/62 passed) và đối chiếu kết quả trace thực tế với benchmark chuẩn (src/reports/benchmark.json).
    * Nếu làm lại, tôi sẽ tối ưu hóa quy trình viết test tự động ngay từ các bước đầu tiên cùng với Claude Code thay vì thực hiện ở giai đoạn hoàn thiện để tiết kiệm thời gian gỡ lỗi lệnh chạy src/.

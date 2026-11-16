# Báo cáo cá nhân — MSSV_HoTen

> **Bản nháp.** Các ô ghi `ĐIỀN` phải do chính bạn điền. Đổi tên file thành `MSSV_HoTen.md` (họ tên không dấu) và xóa ghi chú này trước khi nộp.

## 1. Thông tin thành viên

- Họ tên: `ĐIỀN`
- MSSV: `ĐIỀN`
- Email: `ĐIỀN`
- GitHub: [An041003](https://github.com/An041003)

## 2. Phần việc phụ trách

Vai: **ledger / crash + evaluation**.

- Durability: idempotency, crash và resume của ba shape (`crash_at` truyền vào `durability.issue_refund`).
- Evaluation: benchmark 4 shape × 5 seed, crash suite, ablation; số liệu trong ADR, research card và báo cáo nhóm.
- Rà soát số liệu trong báo cáo so với file trong `src/reports/` và viết test cho phần còn thiếu.

## 3. Đóng góp cụ thể

**Commit chính (hash):** `ĐIỀN`. Hiện chưa có commit nào đứng tên bạn trong repo nhóm. Rubric C8 cần mỗi người một commit có nội dung và ít nhất một test đã thêm hoặc sửa.

**Test đã thêm hoặc sửa:** `ĐIỀN` sau khi bạn commit. Một test còn thiếu trong phần này mà bạn có thể tự viết:

- *Gọi lại với số tiền khác số đã commit.* Chạy `C-001` (ledger 35.000), hạ `approved_vnd` của `A-001` xuống 20.000 trong store, chạy lại `C-001`. Kết quả đúng ở cả ba shape phải là `status == "failed"`, `error_reason == "amount_conflict"`, `proposal_amount == 35000`, ledger vẫn một dòng 35.000 và một audit `refund_committed`. Nhánh này đang chạy đúng nhưng chưa có test.

**Các quyết định kỹ thuật trong phần này** (người chấm có thể hỏi trực tiếp):

- Shape không giữ trạng thái riêng nào về tiền. Ledger với khóa `refund:{claim_id}` là nguồn sự thật duy nhất; checkpoint đơn lẻ không thay được ledger.
- `InjectedCrash` chỉ được bắt để ghi trace rồi ném lại nguyên vẹn.
- `RunResult` tạo bằng `lab8.shapes.common.finish()`, nên `refund_effects` và `committed_audit_count` luôn đọc từ ledger.
- Mỗi event trong trace là một bước thật, để metric `steps` so được giữa ba shape. Báo kèm model call và tool call vì swarm ghi ít event hơn.
- Ablation chỉ đổi một biến: danh sách tool đọc của investigator.

## 4. Bằng chứng

- Link commit của bạn: `ĐIỀN`
- Bằng chứng hiện có trong repo (commit [`1a2a348`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/1a2a348) và [`629ab80`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/629ab80) của `kynnnS`):
  - `src/reports/crash.json`: `crash_safety` = `20/20`.
  - `src/reports/benchmark.json`: workflow / single / orchestrator pass rate 1.000; swarm 0.986, pass^5 0.929, variance 0.000816.
  - `src/reports/ablation_investigator_tools.json`.
- Test hiện có: `test_crash_at_every_point_then_resume_leaves_one_refund`, `test_five_replays_keep_one_ledger_row`, `test_second_claim_on_a_paid_order_is_denied_by_the_order_cap`; T11, T12 trong ma trận student.
- Run id: `R-swarm-C-002-s55` (trial fail duy nhất của swarm: `status resolved != denied`).

## 5. Công cụ AI đã dùng

Nhóm dùng **Claude Code (Anthropic)** để viết code ba shape, bộ test `src/tests/test_team_shapes.py` và bản nháp các báo cáo. Mọi số liệu trong báo cáo lấy từ file do `lab8.benchmark` và `lab8.crash_test` sinh ra, không do AI tự đưa ra.

Cách tự kiểm tra kết quả: `ĐIỀN` sau khi bạn tự chạy trên máy mình (trong `src/`) và ghi lại kết quả thật:

- `python -m pytest -q`
- `python -m pytest -q -m student -o addopts= -k "t11 or t12"`
- `python -m lab8.crash_test --count 20 --out reports/crash.json` và lệnh benchmark trong `src/reports/README.md`; so file sinh ra với file đã commit bằng `git diff --stat src/reports/`

Công cụ AI bạn tự dùng thêm (nếu có) và dùng vào việc gì: `ĐIỀN`.

## 6. Tự đánh giá

`ĐIỀN` — tự viết 3–5 dòng. Gợi ý câu hỏi để trả lời:

- Phần nào trong vai của mình bạn giải thích được mà không cần nhìn code? Phần nào chưa?
- Vì sao swarm có variance khác 0 còn ba shape của nhóm thì không?
- Bạn đã tự viết hoặc sửa gì, và phần nào là do công cụ AI sinh ra rồi bạn kiểm lại?
- Nếu làm lại, bạn sẽ làm khác điều gì?

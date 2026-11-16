# Báo cáo cá nhân — 2A202603621_DoPhuongNam

## 1. Thông tin thành viên

- Họ tên: Đỗ Phương Nam
- MSSV: 2A202603621
- Email: donam02zx@gmail.com
- GitHub: [donam02zx](https://github.com/donam02zx)

## 2. Phần việc phụ trách

Vai: **Ledger + Evaluation**.

- Ledger: idempotency, crash và resume của ba shape (`crash_at` truyền vào `durability.issue_refund`).
- Evaluation: benchmark 4 shape × 5 seed, crash suite, ablation; số liệu trong ADR, research card và báo cáo nhóm.
- Rà soát số liệu trong báo cáo so với file trong `src/reports/` và viết test cho phần còn thiếu.

## 3. Đóng góp cụ thể

**Commit chính (hash):** [`3744137`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/3744137).

**Bonus B5 — Provider idempotency và reconciliation** (báo cáo: [bonus_report.md](bonus_report.md)). Phần này nối tiếp vai Ledger: ledger của lab chỉ bảo vệ dòng ledger, bonus đo chuyện gì xảy ra khi tiền còn phải đi qua một provider bên ngoài.

| File | Nội dung |
| --- | --- |
| `src/bonus/provider.py` | Payment provider giả lập trong bảng SQLite riêng, connection riêng. Hai chế độ: dedupe theo idempotency key và không dedupe (phản ví dụ). Lỗi tiêm tất định: response bị mất, request còn đang bay. |
| `src/bonus/two_phase.py` | Luồng `reserve → provider.refund(key) → confirm → audit` chạy cạnh host, không sửa `lab8/durability.py`. Ba điểm crash mới: `after_reserve_before_provider`, `after_provider_before_confirm`, `after_confirm_before_audit`. Job `reconcile()` đóng các reservation đang treo và void charge trùng. |
| `src/bonus/workflow_provider.py` | Biến thể shape cùng chữ ký `run_claim`, chạy qua `--extra-shape` cạnh workflow và swarm. |
| `src/bonus/provider_crash.py` | Crash suite 16 kịch bản, ma trận luồng × provider × cách phục hồi × điểm crash, phản ví dụ, và safety counts. Sinh `src/reports/bonus_provider_crash.json`. |

**Test đã thêm:**

- `src/tests/test_bonus_provider.py` — 43 test: provider dedupe và không dedupe; crash ở 6 điểm rồi chạy lại; chỉ chạy `reconcile()`; phản ví dụ charge 2 lần; request đang bay; approval bị hạ hoặc thu hồi sau khi provider đã chi; refund lịch sử đã seed không bị trả lại; biến thể khớp nhãn public và khớp workflow trên 14 claim × 5 seed.
- `src/tests/test_ledger_replay_conflict.py` — 3 test (workflow, single, orchestrator): chạy `C-001` (ledger 35.000), hạ `approved_vnd` của `A-001` xuống 20.000, chạy lại. Kết quả `failed` / `amount_conflict`, `proposal_amount == 35000`, ledger vẫn một dòng 35.000, một audit `refund_committed`, một audit `amount_conflict`. Nhánh này trước đó chạy đúng nhưng chưa có test.

**Kết quả đo được** (số lấy từ file JSON trong mục 4):

- Crash suite mới: **16/16** kịch bản kết thúc với đúng 1 charge ở provider và 1 dòng ledger.
- Ledger dedupe một mình không đủ ở đúng một cửa sổ: sau provider, trước confirm. Provider không dedupe mà gửi lại ngay thì **2 charge** (70.000 cho ledger 35.000). Hỏi provider trước khi gửi thì còn 1.
- Ghi ledger trước rồi mới gọi provider: crash ở giữa cho **0 charge / 1 dòng ledger**, khách không nhận tiền.
- Request còn đang bay trên provider không dedupe: 2 charge, trả thừa 35.000 cho tới khi `reconcile()` void 1.
- Biến thể `workflow_provider` so với workflow trên cùng 70 trial: pass rate 1.000 / 1.000, pass^5 1.000 / 1.000, variance 0; cost/success 38.89 so với 28.89 VND; 0 secret leak, 0 approval bypass, 0 trial lệch provider–ledger.

**Các quyết định kỹ thuật trong phần này** (người chấm có thể hỏi trực tiếp):

- Shape không giữ trạng thái riêng nào về tiền. Ledger với khóa `refund:{claim_id}` là nguồn sự thật duy nhất; checkpoint đơn lẻ không thay được ledger.
- `InjectedCrash` chỉ được bắt để ghi trace rồi ném lại nguyên vẹn.
- `RunResult` tạo bằng `lab8.shapes.common.finish()`, nên `refund_effects` và `committed_audit_count` luôn đọc từ ledger.
- Mỗi event trong trace là một bước thật, để metric `steps` so được giữa ba shape. Báo kèm model call và tool call vì swarm ghi ít event hơn.
- Ablation chỉ đổi một biến: danh sách tool đọc của investigator.
- Bonus: reservation được ghi **trước** khi tiền đi và chốt số tiền bằng chính `authorize` của host, nên provider không bao giờ được yêu cầu chi nhiều hơn số host sẽ ghi.
- Bonus: khi chạy lại, authorization được kiểm lại trước. Approval đổi trong lúc reservation còn mở thì void charge cũ rồi làm lại từ đầu; host vẫn là bên quyết định.
- Bonus: dòng ledger không có reservation thì để yên. Đó có thể là refund lịch sử đã seed (`prior_refunds`); trả lại là charge trùng.
- Bonus: provider dùng connection riêng và không bao giờ chung transaction với ledger. Khoảng hở đó chính là thứ được đo.

## 4. Bằng chứng

- Link commit của bạn: https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/3744137
- Bonus B5, lệnh tái lập (trong `src/`):
  - `python -m bonus.provider_crash --out reports/bonus_provider_crash.json` → `exactly_once 16/16   guards 4/4`
  - `python -m lab8.benchmark --shapes workflow,workflow_provider,swarm --extra-shape workflow_provider=bonus.workflow_provider:run_claim --seeds 11,22,33,44,55 --out reports/bonus_benchmark.json`
  - `python -m pytest -q tests/test_bonus_provider.py tests/test_ledger_replay_conflict.py` → `46 passed`
  - `python -m pytest -q` → `352 passed` (306 có sẵn + 46 mới)
- File do script sinh ra, chạy hai lần cho kết quả giống từng byte, trên Python 3.12 và 3.14:
  - `src/reports/bonus_provider_crash.json`: `exactly_once` = `16/16`, `guards_passed` = `4/4`; mục `matrix`, `counterexamples`, `safety`.
  - `src/reports/bonus_benchmark.json`: workflow 1.000 / 28.89 VND; workflow_provider 1.000 / 38.89 VND; swarm 0.986 / 49.57 VND.
- Run id bonus: `R-workflow_provider-C-001-s11`. Kịch bản phản ví dụ: `CE-01` (provider không dedupe, gửi lại ngay, crash `after_provider_before_confirm`) và `CE-in-flight-no-dedupe`.
- Bằng chứng của phần chính đã có trong repo (commit [`1a2a348`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/1a2a348) và [`629ab80`](https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents/commit/629ab80) của `kynnnS`):
  - `src/reports/crash.json`: `crash_safety` = `20/20`.
  - `src/reports/benchmark.json`: workflow / single / orchestrator pass rate 1.000; swarm 0.986, pass^5 0.929, variance 0.000816.
  - `src/reports/ablation_investigator_tools.json`.
- Test có sẵn liên quan: `test_crash_at_every_point_then_resume_leaves_one_refund`, `test_five_replays_keep_one_ledger_row`, `test_second_claim_on_a_paid_order_is_denied_by_the_order_cap`; T11, T12 trong ma trận student.
- Run id: `R-swarm-C-002-s55` (trial fail duy nhất của swarm: `status resolved != denied`).

## 5. Công cụ AI đã dùng

Nhóm dùng **Claude Code (Anthropic)** để viết code ba shape, bộ test `src/tests/test_team_shapes.py` và bản nháp các báo cáo. Mọi số liệu trong báo cáo lấy từ file do `lab8.benchmark` và `lab8.crash_test` sinh ra, không do AI tự đưa ra.

Cách tự kiểm tra kết quả: chạy lại trên máy mình (Windows 11, trong `src/`) ngày 16/11/2026 và ghi kết quả thật:

| Lệnh | Kết quả |
| --- | --- |
| `python -m pytest -q` | `352 passed, 248 deselected` |
| `python -m pytest -q -m student -o addopts= -k "t11 or t12"` | `8 passed` |
| `python -m lab8.crash_test --count 20 --out reports/crash.json` | `crash_safety 20/20` |
| Lệnh benchmark trong `src/reports/README.md` | workflow / single / orchestrator 1.000; swarm 0.986, pass^5 0.929 |
| `git diff --stat src/reports/` sau khi chạy lại | Không có dòng nào khác file đã commit |
| `python -m lab8.check_submission` | `0 FAIL` |

Phần bonus B5 (`src/bonus/`, hai file test mới, `bonus_report.md`) viết cùng **Claude Code (Anthropic)**. Số liệu lấy từ `src/reports/bonus_*.json` do script sinh ra; đã chạy lại hai lần và trên hai phiên bản Python để kiểm số không đổi.

Công cụ AI khác tự dùng thêm: không có.

## 6. Tự đánh giá

- **Giải thích được không cần nhìn code:** vì sao ledger với khóa `refund:{claim_id}` chỉ cho một refund mỗi claim; vì sao refund và audit `refund_committed` phải chung một transaction; ba điểm crash của host và vì sao chạy lại là no-op; và ở bonus, vì sao cửa sổ "sau provider, trước confirm" là chỗ duy nhất ledger không thấy gì. **Chưa chắc:** các nhánh ít gặp trong `two_phase.py` (trạng thái `stuck`, hai claim cùng đơn chạy xen kẽ) mình phải mở code mới lần theo được.
- **Vì sao swarm có variance khác 0:** ở seed 55 swarm lấy số ngày trễ trong ticket thay cho cột `delay_days`, nên `C-002` (ticket ghi 5 ngày, order ghi 2) bị trả 20.000 thay vì từ chối. Ba shape của nhóm không dùng ticket để quyết định tiền nên cả 5 seed cho cùng kết quả.
- **Phần mình làm và phần AI sinh ra:** mình vào việc muộn; bản đầu của ba shape, benchmark và ablation do bạn Sơn chạy cùng Claude Code. Phần đứng tên mình là bonus B5 và test nhánh `amount_conflict`. Code và báo cáo bonus do Claude Code sinh ra theo yêu cầu của mình; mình chạy lại toàn bộ lệnh ở mục 5 trên máy mình và đối chiếu số trong báo cáo với file JSON.
- **Nếu làm lại:** commit sớm từ CP2 thay vì dồn về cuối, tự viết tay crash suite trước khi nhờ AI để hiểu kỹ hơn, và đăng ký sớm để có số hidden trước khi kết luận.

# Báo cáo nhóm — Lab 8 LogiX-VN

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm: The SaoCungDuoc Team
- Thành viên: xem `TEAM.md`
- Commit chốt (trùng `report/team/decision_adr.md`): 629ab80

## 2. Mục tiêu và cách tiếp cận

Bài toán: xử lý claim hoàn phí vận chuyển của LogiX-VN bằng bốn kiến trúc có cùng chữ ký `run_claim`, đo trên cùng claim, cùng seed, cùng bảng giá, rồi chọn kiến trúc ít tự chủ nhất mà vẫn làm đúng.

Nhóm đọc đề theo một nguyên tắc: **quyết định về tiền là một hàm của dữ liệu có cấu trúc, không phải của chữ trong ticket**. Order row và policy hiện hành quyết định số tiền (`compute_compensation`). Host quyết định có được ghi hay không (`durability.issue_refund`: approval, trần theo đơn, idempotency). Model chỉ đọc và soạn chữ. Từ đó, ba shape của nhóm là ba cách sắp xếp khác nhau quanh cùng một đường quyết định, và câu hỏi của lab trở thành: thêm tự chủ cho model thì mua được gì, với giá bao nhiêu.

Thứ tự làm:

1. CP1: cài môi trường, chạy smoke và cổng host, đọc `docs/business_rules.md`, `docs/contracts.md`, `durability.py`, `policy.py`, `runtime.py`, `handoff.py` và swarm tham chiếu.
2. CP2–CP3: viết workflow trước vì nó là đường quyết định trần trụi nhất. Khi workflow qua 62 test student, viết single và orchestrator quanh cùng đường đó. `crash_at` được truyền vào host ngay từ bản đầu của mỗi shape.
3. CP4: chạy crash suite, viết test đối kháng theo danh sách bẫy của bộ hidden.
4. CP5: benchmark 4 shape × 5 seed, ablation cho research card, viết ADR.

## 3. Giải pháp

### Đường quyết định chung

| Bước | Điều kiện | Kết quả |
| --- | --- | --- |
| Đọc claim qua `get_claim_view` | Không có claim | `failed`, proposal 0 |
| Kiểm `order_id` trên claim | Thiếu | `needs_info`. Không lấy mã đơn từ ticket |
| `lookup_order` theo principal của claim | Không thấy đơn hoặc sai chủ | `escalated` |
| `compute_compensation` trên order view | Quote = 0 | `denied`, proposal 0, không gọi host |
| `durability.issue_refund` với **quote đầy đủ** | Host từ chối | `denied`, proposal = quote, host ghi `policy_denied` |
| | Số tiền khác số đã commit | `failed` |
| | Host chấp nhận | `resolved`, proposal = quote |

Nhóm truyền quote đầy đủ vì host tự trừ phần đơn đã được hoàn (`cap_per_order`). Nếu shape trừ trước, host trừ lần nữa: ở T14, 150.000 − 30.000 − 30.000 = 90.000 thay vì 120.000. Shape cũng không tự từ chối khi quote > 0, vì chỉ host mới ghi được audit `policy_denied`.

### Ba shape

| | A workflow | B single | C orchestrator |
| --- | --- | --- | --- |
| Ai chọn bước tiếp theo | Code, thứ tự cố định | Model, trong `run_react` tối đa 8 bước (thực tế tối đa 5) | Orchestrator lập kế hoạch, investigator chạy tool đọc |
| Model làm gì | Một lần gọi soạn câu trả lời, sau khi đã quyết định | Mỗi bước một lần gọi; đọc ticket; chọn tool đọc; đưa khuyến nghị | 3 lần gọi: plan (đọc ticket), investigate (báo cáo), draft |
| Model có tool ghi không | Không | Không. `run_react` từ chối `issue_refund` | Không. `make_handoff` từ chối tool ngoài `READONLY_TOOLS` |
| Ticket ảnh hưởng tiền không | Không được đọc để quyết định | Số ngày ticket khai được ghi lại và so với order; order luôn thắng | Ticket ở lại orchestrator, không vào handoff |
| Code kiểm lại gì trước khi ghi | Không cần, vì code tự làm mọi bước | `_settle` dựng lại quyết định từ kết quả tool do code tự giữ; quote phải là output của `compute_compensation` trên đúng order view đã tra, nếu không thì tính lại | Quote trong báo cáo phải bằng phần lớn nhất trong `parts` (max, không cộng), nếu không thì tính lại |

**Ranh giới code / model.** Code quyết: lọc theo principal, policy hiệu lực, số tiền, approval, trần theo đơn, idempotency, ghi ledger. Model quyết: đọc ticket, thứ tự tool đọc (B), câu chữ trả lời. Khuyến nghị `final` của agent ở B chỉ được ghi vào trace (`model_recommend`), không phải input của quyết định.

**Handoff (C).** `make_handoff(request_id, claim_id, task, facts={}, allowed_tools=[lookup_order, lookup_refund_history, compute_compensation])`. `facts` để rỗng có chủ ý: trước khi điều tra, orchestrator chưa biết dữ kiện nào của order, và thứ duy nhất nó có là lời khai trong ticket, thứ không được chuyển đi như một dữ kiện. Handoff không chứa ticket, `principal_id`, secret hay header. Khi claim thiếu `order_id` thì không dựng handoff.

**An toàn khi crash.** `crash_at` được truyền thẳng vào `issue_refund`. `InjectedCrash` được bắt chỉ để ghi trace rồi ném lại nguyên vẹn. Ledger dùng khóa `refund:{claim_id}` và ghi refund cùng audit `refund_committed` trong một transaction, nên lần chạy lại sau crash là no-op. Shape không giữ trạng thái riêng nào về tiền, vì vậy không có gì để lệch với ledger.

**Fail-closed.** `run_claim` không ném exception nào ngoài `InjectedCrash`. Lỗi không lường trước (store hỏng, tool lỗi) trả `failed`, không ghi tiền, vẫn có trace đúng contract.

**Trace.** Mỗi event là một bước thật. Danh sách event và các field cố ý không ghi: xem mục "Trace và bằng chứng" trong `report/team/decision_adr.md`.

## 4. Kết quả

### Benchmark public: 14 claim × 5 seed (`src/reports/benchmark.json`)

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success (VND) | Mean / p95 steps | Model calls | Tool calls |
| --- | ---: | ---: | --- | ---: | ---: | --- | ---: | ---: |
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 28.89 | 4.43 / 5 | 1.00 | 2.79 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 37.21 | 6.07 / 7 | 4.43 | 3.43 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 49.91 | 4.50 / 5 | 2.93 | 4.64 |
| swarm | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 / 3 | 3.00 | 4.66 |

Cost là VND mô phỏng theo `config/pricing.yaml`, không phải hóa đơn API. Latency: `unavailable`. `steps` là số event trong trace nên phụ thuộc cách mỗi shape ghi trace; swarm ghi ít event hơn chứ không làm ít việc hơn (nó có nhiều tool call nhất).

Đọc bảng:

- Ba shape nhóm viết bằng nhau về độ đúng. Khác biệt chỉ còn là chi phí: single +29%, orchestrator +73% so với workflow.
- Swarm fail một trial trên 70: `R-swarm-C-002-s55`, lý do `status resolved != denied`. Ticket ghi trễ 5 ngày, order ghi 2 ngày, swarm trả 20.000 VND. Cùng claim và seed đó, `R-workflow-C-002-s55` từ chối đúng. Ở single, trace của trial tương ứng ghi `ticket_conflict` (5 so với 2, dùng order row).

### Durability (`src/reports/crash.json`)

Crash safety **20/20**. Ngoài ra, test của nhóm cho mỗi shape crash ở cả ba điểm (`before_effect`, `after_effect_before_checkpoint`, `after_checkpoint`) rồi chạy lại: luôn một dòng ledger 35.000 và một audit `refund_committed`.

### Kiểm thử

| Bộ | Lệnh (trong `src/`) | Kết quả |
| --- | --- | --- |
| Cổng host, gồm test của nhóm | `python -m pytest -q` | 291 passed (54 có sẵn + 237 của nhóm) |
| Ma trận student T01–T14 | `python -m pytest -q -m student -o addopts=` | 248 passed (62 mỗi shape) |

237 test của nhóm (`src/tests/test_team_shapes.py`) dựng các tình huống mà đề nói bộ hidden có: ticket khai quá và khai thiếu số ngày (kể cả seed 5, 10, 55), ticket chèn lệnh và mã đơn, clause cũ và clause tương lai, approval mượn của claim khác, thiếu, không tồn tại, bị thu hồi, hết hạn, bằng 0, approval thấp hơn quote, đơn hủy và đang giao, ship cộng damage, phí ship 0, mã đơn dùng chữ Cyrillic giống chữ Latin, mã đơn chỉ gồm khoảng trắng, sai principal, hai claim trên một đơn, store hỏng, và ticket bị gắn canary cùng SĐT. Nhãn viết tay theo `docs/business_rules.md`.

### Tự kiểm trên `student_drop/`

Chưa chạy. Nhóm chưa nhận thư mục `student_drop/` nên chưa có `src/reports/hidden_selfcheck.json`.

### Ablation (`src/reports/ablation_investigator_tools.json`)

Đổi số read tool giao cho investigator, giữ nguyên mọi thứ khác: 2 tool 40.37 VND, 3 tool 49.91 VND, 5 tool 59.20 VND mỗi lần thành công; pass rate giữ 1.000 ở cả ba mức. Chi tiết trong research card.

Quyết định kiến trúc và lý do: xem `report/team/decision_adr.md`. Phiếu nghiên cứu và ablation: xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

| Vấn đề | Bằng chứng | Cách xử lý |
| --- | --- | --- |
| Máy mặc định Python 3.9.6, lab cần 3.11–3.13 | `python3 --version` → `Python 3.9.6` | Dùng Python 3.12.5 |
| `python3.12 -m venv .venv` lỗi | `Command '[... 'python3.12', '-m', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1` | Tạo venv bằng `uv venv --python 3.12 --seed .venv` rồi cài `requirements.txt`. Smoke in `lab8.smoke pass`, `python 3.12.5 \| Darwin arm64` |
| Cổng host lúc mới clone ra 54 passed, README ghi 52 | `54 passed, 248 deselected` | Không có dòng `failed` nên coi là đạt. Ma trận student ra đúng `186 failed, 62 passed` như đề |
| `run_react` chỉ trả lại kết quả tool cuối cùng | `seen = {"last_tool", "last_result", "claim"}` trong `lab8/runtime.py` | Agent ở shape B giữ bản sao mọi kết quả tool trong `notes` do code quản lý; `_settle` đọc từ đó |
| `order_id` chỉ gồm khoảng trắng: bản đầu trả `needs_info`, host và swarm coi là mã đơn không tìm thấy (`escalated`) | Chạy ba shape và swarm (seed 11) trên 600 claim sinh ngẫu nhiên (script kiểm tra tạm, không nằm trong repo): 165 trên 1.800 trial lệch, tất cả ở đúng trường hợp này | Định nghĩa "thiếu order_id" theo host: chỉ null hoặc chuỗi rỗng. Chạy lại hai lượt, 3.600 trial, 0 lệch, 0 trial lộ PII. Thêm test `blank` |
| `steps` không so trực tiếp được giữa các shape | Swarm 2.80 steps nhưng 4.66 tool call | Ghi mỗi bước thật một event ở ba shape của nhóm, và báo kèm model call, tool call |

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md` (bảng đóng góp) và báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency là `unavailable`.

- **Pass rate 1.000 của B và C một phần là do cách thiết kế.** Chính sách chọn tool của agent là code tất định, MockLLM chỉ tính token. Với model thật, B và C có thể chọn sai tool hoặc dừng sớm. Code của nhóm khi đó trả `failed` chứ không trả tiền sai, nên rủi ro là giảm pass rate, không phải mất tiền. Con số 1.000 không dự đoán được pass rate với model thật.
- **Chưa có số hidden.** Kết luận chọn workflow dựa trên 14 claim public và test tự viết.
- **Chi phí là mô phỏng.** Tỉ lệ +29% và +73% phụ thuộc bảng giá trong `config/pricing.yaml` và độ dài prompt nhóm chọn. Thứ tự A < B < C thì ổn định hơn vì nó theo số lần gọi model và tool.
- **Workflow không xử lý được thông tin chỉ có trong chữ tự do.** Nếu nghiệp vụ cần đọc bằng chứng không cấu trúc, kết luận phải đo lại (điều kiện đảo quyết định trong ADR).
- **`_GuardedTrace` chỉ bắt chuỗi đã biết tên.** Kiểm soát chính vẫn là allowlist.

Hướng cải thiện: chạy `student_drop/` khi có; đo B và C với model thật để biết tỉ lệ chọn sai tool; thử investigator song song với mô hình latency mô phỏng (bonus B1).

## 8. Tài liệu tham khảo

- Kim, Liu và cộng sự, *Towards a Science of Scaling Agent Systems*, arXiv:2512.08296, 2025. https://arxiv.org/abs/2512.08296
- Google Research blog, *Towards a science of scaling agent systems: When and why agent systems work*, 01/2026. https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
- Tài liệu lab: `docs/business_rules.md`, `docs/contracts.md`, `docs/metrics.md`, `docs/architecture.md`.
- Công cụ AI: Claude Code (Anthropic) hỗ trợ viết code ba shape, test và bản nháp báo cáo. Mọi số liệu lấy từ file do `lab8.benchmark` và `lab8.crash_test` sinh ra.

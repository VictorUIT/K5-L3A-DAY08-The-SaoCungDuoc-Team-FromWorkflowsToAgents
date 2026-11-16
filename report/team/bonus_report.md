# Bonus report: B5

- **Topic + nguồn:** Provider idempotency và reconciliation. DBOS, *Durable Workflows and Steps* (slide 36–37); pseudo-code slide 37.
- **CLAIM của nguồn:** checkpoint và ledger dedupe không làm side effect ở hệ thống ngoài thành exactly-once; crash giữa ledger và provider vẫn cần một cơ chế recovery riêng.
- **BOUNDARY:** nguồn nói về workflow engine có step được ghi bền và provider thật qua mạng. Ở đây provider là một bảng SQLite, một process, một luồng, lỗi được tiêm tất định (không timeout thật, không chạy đồng thời).
- **HYPOTHESIS trên LogiX:** ledger với khóa `refund:{claim_id}` chỉ bảo vệ dòng ledger. Khi tiền phải đi qua provider, có đúng một cửa sổ crash mà ledger không thấy gì, và ở đó kết quả phụ thuộc vào provider có dedupe theo key hay không.
- **Biến cố định:** claim `C-001` (quote 35.000 VND), world public, 14 claim × seed 11, 22, 33, 44, 55, MockLLM, bảng giá `config/pricing.yaml`, host `durability.issue_refund` không sửa. **Biến thay đổi:** thứ tự ghi (ledger trước / hai pha), provider (dedupe / không dedupe), cách phục hồi (gửi lại ngay / hỏi provider trước khi gửi), điểm crash.
- **Lệnh tái lập** (trong `src/`, chạy y hệt trên PowerShell, cmd, bash):

```bash
python -m bonus.provider_crash --out reports/bonus_provider_crash.json
python -m lab8.benchmark --shapes workflow,workflow_provider,swarm --extra-shape workflow_provider=bonus.workflow_provider:run_claim --seeds 11,22,33,44,55 --out reports/bonus_benchmark.json
python -m pytest -q tests/test_bonus_provider.py
```

- **File report + run id:** `src/reports/bonus_provider_crash.json`, `src/reports/bonus_benchmark.json`; run id `R-workflow_provider-C-001-s11`. Code: `src/bonus/` (`provider.py`, `two_phase.py`, `workflow_provider.py`, `provider_crash.py`). Test: `src/tests/test_bonus_provider.py` (43 test).

## Kết quả

Luồng hai pha: `reserve` (ghi ý định và số tiền host cho phép) → `provider.refund(key)` → `confirm` (host ghi ledger và audit) → audit `provider_settled`. Ba điểm crash mới nằm giữa các bước đó.

**Crash suite** (`scenarios`): **16/16** kịch bản kết thúc với đúng 1 charge ở provider, 1 dòng ledger, 1 audit `refund_committed`. Gồm 6 điểm crash (3 mới, 3 của host) × 2 cách phục hồi (chạy lại shape; chỉ chạy job `reconcile()`), crash liên tiếp ở cả 6 điểm, 5 lần replay, claim hỏng hàng `C-003` (150.000), và provider không dedupe có hỏi trước khi gửi.

**Cửa sổ nào cần gì** (`matrix`; mỗi ô là số charge / số dòng ledger sau khi phục hồi):

| Luồng | Provider | Phục hồi | Crash sau reserve | Crash sau provider | Crash sau confirm |
| --- | --- | --- | :---: | :---: | :---: |
| Hai pha | dedupe | gửi lại ngay | 1 / 1 | 1 / 1 | 1 / 1 |
| Hai pha | dedupe | hỏi trước khi gửi | 1 / 1 | 1 / 1 | 1 / 1 |
| Hai pha | không dedupe | gửi lại ngay | 1 / 1 | **2 / 1** (70.000 cho ledger 35.000) | 1 / 1 |
| Hai pha | không dedupe | hỏi trước khi gửi | 1 / 1 | 1 / 1 | 1 / 1 |
| Ledger trước | cả hai | gửi lại ngay | crash giữa ledger và provider: **0 / 1** (khách không nhận tiền) | | |

**Request còn đang bay** (`counterexamples`): response bị mất, lúc phục hồi hỏi thì provider chưa thấy charge, sau đó request mới tới nơi.

| Provider | Charge lúc cao nhất | Trả thừa cho tới khi void | `reconcile()` void | Charge cuối |
| --- | ---: | ---: | ---: | ---: |
| không dedupe | 2 | 35.000 | 1 | 1 |
| dedupe | 1 | 0 | 0 | 1 |

**Approval đổi quanh lúc crash** (`guards`, 4/4): approval hạ còn 20.000 sau khi provider đã chi 35.000 → void 35.000, chi lại 20.000, ledger 20.000. Approval bị thu hồi → void, 0 charge, 0 dòng ledger, host ghi `policy_denied`. Claim `C-007` (approval không dùng được) → không reserve, không gọi provider.

**Cùng claim × seed với baseline** (`bonus_benchmark.json`, 70 trial mỗi shape; safety từ mục `safety` của `bonus_provider_crash.json`):

| Shape | Pass rate | Pass^5 | Variance | Cost/success (VND) | Tool calls | Secret leak | Approval bypass | Double charge | Lệch provider–ledger |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| workflow (baseline) | 1.000 | 1.000 | 0.000000 | 28.89 | 2.79 | 0 | 0 | 0 | không có provider |
| workflow_provider | 1.000 | 1.000 | 0.000000 | 38.89 | 3.79 | 0 | 0 | 0 | 0 / 70 |
| swarm | 0.986 | 0.929 | 0.000816 | 49.57 | 4.66 | — | — | — | — |

Biến thể tốn thêm 10,00 VND mỗi lần thành công (+35%): 70 request tới provider trên 35 trial có trả tiền, mỗi trial một `lookup` và một `refund`, tính giá như tool call.

**Tự kiểm trên bộ hidden** (`student_drop/`, 40 claim không nhãn × 5 seed, `src/reports/bonus_hidden_selfcheck.json`):

```bash
python -m lab8.benchmark --shapes workflow,workflow_provider,single,orchestrator --extra-shape workflow_provider=bonus.workflow_provider:run_claim --cases ../student_drop/hidden_claims.jsonl --world ../student_drop/hidden_world_state.json --seeds 11,22,33,44,55 --out reports/bonus_hidden_selfcheck.json
```

| Shape | Trial | Lỗi | Leak nghi ngờ | resolved / denied / escalated / needs_info | Tool calls | Tổng chi phí (VND) |
| --- | ---: | ---: | ---: | :---: | ---: | ---: |
| workflow (baseline) | 200 | 0 | 0 | 90 / 95 / 10 / 5 | 2.90 | 6.006,6 |
| workflow_provider | 200 | 0 | 0 | 90 / 95 / 10 / 5 | 3.80 | 7.806,6 |

Không có nhãn nên không có pass rate. Status của biến thể trùng baseline ở cả 200 cặp claim × seed, và không claim nào đổi status giữa các seed. Kiểm thêm bằng tay (chạy lại hàm `state()` của `provider_crash.py` trên world hidden, script không nằm trong repo): 90 trial có trả tiền, 0 double charge, 0 lệch provider–ledger, số tiền ledger trùng baseline ở 200/200 trial; crash ở cả 6 điểm rồi chạy lại, trên 40 claim (seed 11): 240/240 ra cùng charge, dòng ledger, số tiền và audit như lần chạy không crash.

## Kết luận

**Ủng hộ claim của nguồn, và chỉ ra được đúng chỗ.**

- *Ledger dedupe một mình không đủ ở cửa sổ nào?* Đúng một: **sau provider, trước confirm**. Tiền đã đi, ledger còn trống, nên khóa `refund:{claim_id}` không có gì để so. Hai cửa sổ còn lại an toàn với mọi cấu hình: trước provider chưa có tiền nào đi, sau confirm thì ledger đã có dòng. Ghi ledger trước không tránh được vấn đề mà đổi nó thành mất tiền của khách (0 / 1): ledger báo "đã xong" nên lần chạy lại không gửi gì.
- *Provider không dedupe thì reconciliation cứu tới đâu?* Cứu được mọi crash mà charge đã **nhìn thấy được** lúc phục hồi (hỏi trước khi gửi: 1 / 1). Không cứu được request còn đang bay: hỏi thì chưa thấy, gửi lại thì thành 2 charge. Lúc đó `reconcile()` chỉ phát hiện và void sau, và 35.000 đã nằm ngoài tài khoản trong khoảng đó. Provider có dedupe thì cả hai trường hợp đều 1 charge mà không cần hỏi.

Kết luận đảo ngược khi: (1) provider không cho tra theo key hoặc không cho void, khi đó dòng "hỏi trước khi gửi" mất tác dụng và chỉ còn dedupe phía provider; (2) ledger và provider ghi chung một transaction, khi đó không còn cửa sổ nào và luồng hai pha là thừa; (3) số tiền trả sai rẻ hơn 10 VND mỗi claim thì chi phí thêm không đáng.

## Giới hạn

- **MockLLM.** Phần này không có quyết định nào của model; model chỉ soạn câu trả lời sau khi đã quyết. Pass rate 1.000 của biến thể vì vậy chỉ nói rằng luồng hai pha không làm hỏng đường quyết định, không nói gì về model thật.
- **Provider mô phỏng.** Không có mạng, không có timeout thật, latency `unavailable`. "Request đang bay" là một cờ tất định, không phải race thật. Void luôn thành công ngay; provider thật có thể từ chối hoặc mất vài ngày.
- **Một luồng.** Hai claim trên cùng một đơn chạy xen kẽ chưa được xử lý: reservation chưa tính vào trần theo đơn. Luồng phát hiện ledger và provider lệch số tiền rồi dừng ở trạng thái `stuck` chờ người xử lý, không tự sửa.
- **Mẫu nhỏ.** Ma trận đo trên một claim (`C-001`), suite thêm `C-003`; 14 claim public cho phần so sánh. Bộ hidden chỉ tự kiểm được (không nhãn): không lỗi, không leak, quyết định trùng baseline; pass rate chính thức do grader chấm.
- **Chi phí là mô phỏng.** +10 VND là hai tool call theo `config/pricing.yaml`, không phải phí giao dịch của provider.

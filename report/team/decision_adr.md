# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: 0d036c7
- Run id dẫn chứng: `R-workflow-C-002-s55` (ticket ghi 5 ngày, order ghi 2 ngày, workflow từ chối đúng), `R-swarm-C-002-s55` (cùng claim, cùng seed, swarm trả 20.000 sai), `R-workflow-C-014-s55` (T14, quote 150.000, ledger 120.000). Nguồn: `src/reports/benchmark.json`
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0.000000 trên 14 claim public × 5 seed = 70 trial (`src/reports/benchmark.json`)
- Cost per success (mô phỏng, VND): 28.89 (single 37.21, swarm 49.57, orchestrator 66.90)
- Crash safety: 20/20 (`src/reports/crash.json`)
- Secret leak / approval bypass: 0 / 0 trên bộ public (không trial nào fail vì `forbidden_substring`; T07 approval hết hạn không tạo refund). Số trên bộ hidden do giảng viên chấm, nhóm chưa có

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Vì sao shape này

Trên cùng 14 claim public, cùng 5 seed (11, 22, 33, 44, 55), cùng MockLLM và cùng bảng giá, ba shape nhóm viết đều đạt pass rate 1.000, pass^5 1.000, variance 0. Khi độ đúng bằng nhau, nhóm chọn shape ít tự chủ nhất và rẻ nhất: workflow.

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success (VND) | Mean / p95 steps | Model calls / trial |
| --- | ---: | ---: | --- | ---: | ---: | --- | ---: |
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 28.89 | 4.43 / 5 | 1.00 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 37.21 | 6.07 / 7 | 4.43 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 66.90 | 4.50 / 5 | 2.93 |
| swarm (tham chiếu) | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 / 3 | 3.00 |

Lý do pass rate bằng nhau không phải ngẫu nhiên: ở cả ba shape, mọi quyết định về tiền đều đi qua cùng một đường code (`lookup_order` → `compute_compensation` → `durability.issue_refund`). Model chỉ chọn thứ tự đọc (single), lập kế hoạch và báo cáo (orchestrator), hoặc soạn câu trả lời (workflow). Test `test_three_shapes_agree_on_every_public_claim` kiểm ba shape cho cùng status, cùng proposal và cùng ledger trên cả 70 trial. Vì vậy single đắt hơn workflow 29% và orchestrator đắt hơn 131.6% mà không mua thêm được trial pass nào.

Swarm là shape duy nhất có variance khác 0. Nó fail đúng một trial, `R-swarm-C-002-s55`: ở seed chia hết cho 5, swarm lấy "trễ 5 ngày" trong ticket thay cho `delay_days = 2` của order và trả 20.000 VND. Workflow không đọc ticket để quyết định nên không có đường nào dẫn tới lỗi này.

## Có đáng đổi lấy multi-agent không

Với dữ liệu hiện có thì không: multi-agent không nhỉnh hơn ở pass rate (orchestrator bằng, swarm thấp hơn) mà cost/success cao hơn khoảng 72% (swarm) và 131.6% (orchestrator), và swarm còn thêm variance. Nhóm giữ workflow.

Quyết định sẽ đảo lại khi một trong các điều kiện sau xuất hiện, và phải đo lại trên cùng corpus, cùng seed:

- **Thông tin cần cho quyết định chỉ nằm trong chữ tự do.** Hiện mọi dữ kiện tính tiền đều là cột có cấu trúc của order. Nếu LogiX cần đọc bằng chứng không cấu trúc (ảnh hàng hỏng, hội thoại với shipper) thì bước đọc cần model, và single hoặc orchestrator mới có việc để làm. Ngưỡng nhóm đặt: shape tự chủ hơn phải tăng pass rate ít nhất 5 điểm phần trăm trên bộ có nhãn, pass^5 không giảm, variance vẫn bằng 0 ở phần tiền.
- **Việc điều tra chia song song được.** Luồng claim hiện là chuỗi tuần tự (order → quote → host). Nếu có nhiều nguồn độc lập cần tra cùng lúc (hãng vận chuyển, kho, cổng thanh toán) và latency đo được thật, orchestrator với investigator song song có thể đáng tiền. Lab này để latency là `unavailable` nên chưa kết luận được.
- **Ranh giới tin cậy hoặc đội sở hữu tách ra.** Nếu investigator do đội khác vận hành, handoff allowlist của orchestrator là thứ bắt buộc phải có, dù cost cao hơn.

Trong cả ba trường hợp, phần ghi tiền vẫn ở code và host. Thứ thay đổi chỉ là ai đọc và đọc thế nào.

## Trace và bằng chứng

**Event được ghi** (mỗi event là một bước thật, nên metric `steps` so được giữa các shape):

- workflow: `claim`, `order`, `quote`, `host_refund`, `decision`.
- single: một `react_step` cho mỗi bước ReAct (tool đã quan sát, tool chọn tiếp), rồi `host_refund`, `decision`. Khi số ngày trong ticket khác order, bước đó có thêm `ticket_conflict` gồm hai số nguyên và `used: order_row`.
- orchestrator: `plan`, `handoff` (bản đã qua `make_handoff`), `investigator` (tóm tắt báo cáo), `host_refund`, `decision`; `report_rejected` nếu orchestrator không chấp nhận quote của investigator.
- Cả ba: `crash` khi `InjectedCrash` xảy ra (ghi rồi ném lại, không nuốt), `error` khi gặp lỗi không lường trước.

**Field cố ý không ghi:**

- Chữ trong ticket. Đây là dữ liệu người dùng: có thể chứa SĐT, địa chỉ hoặc chuỗi secret do khách dán vào. Trace chỉ ghi `has_order_id` và, ở single, con số ngày trễ mà ticket khai.
- `principal_id`, `parent_secret`, `raw_headers`. Shape đọc claim qua `get_claim_view` nên hai field sau không bao giờ vào bộ nhớ của shape.
- Dòng order thô. Workflow và single giữ allowlist order sẵn có. Riêng báo cáo investigator của Orchestrator sau hardening chỉ ghi visibility boolean, history số nguyên và diagnostic quote; không ghi các giá trị order/reason tự do. Không ghi `carrier` vì quyết định không dùng đến. SĐT, địa chỉ, ghi chú nội bộ, tên hàng không qua được allowlist của `lookup_order`.
- Câu trả lời do model soạn. Grader không đọc, và ghi ra chỉ thêm bề mặt rò rỉ.

**Kiểm soát:** lớp chính là allowlist (chỉ thêm vào trace những field đã liệt kê). Lớp phụ là `_GuardedTrace`: trước khi ghi file, nếu nội dung có `CANARY_`, `parent_secret`, `raw_headers` hoặc `Bearer ` thì thay toàn bộ event bằng một event `redacted`. Lớp phụ chỉ bắt được chuỗi đã biết tên, nên không thay được allowlist.

**Nếu trace nằm ngoài chỗ scanner quét:** nhóm không ghi file nào ngoài `traces/<run_id>.json` và không in gì ra stdout, nên trường hợp này không xảy ra với code hiện tại. Nếu sau này có log ở nơi khác, cách chứng minh là: (1) mọi lần ghi đi qua một tracer duy nhất có allowlist, kiểm bằng code review và test; (2) test gieo secret giả vào ticket rồi quét mọi artifact, như `test_trace_and_result_hold_no_ticket_secret_or_pii` (14 claim × 3 shape, ticket bị gắn thêm canary, SĐT và địa chỉ); (3) đưa đường dẫn log mới vào phạm vi scanner. Không quét được thì coi là chưa chứng minh được, đúng như cách grader fail-closed.

## Giới hạn

- MockLLM không phải model sản xuất: nó cố định theo seed và không suy luận. Chi phí model của single và orchestrator là mô phỏng theo `config/pricing.yaml`, không phải hóa đơn API. Với model thật, vòng ReAct có thể chọn sai tool hoặc dừng sớm; code của nhóm xử lý việc đó bằng cách trả `failed` chứ không trả tiền, nhưng pass rate khi đó sẽ thấp hơn 1.000.
- Latency là `unavailable`. Nhóm không so tốc độ giữa các shape.
- Số liệu trên là bộ public 14 claim. Pass rate hidden (40 claim × 5 seed) do giảng viên chấm; nhóm chưa có `student_drop/` nên chưa tự kiểm được. Nhóm đã viết thêm 237 test đối kháng trong `src/tests/test_team_shapes.py` theo mô tả của bộ hidden, nhưng đó không phải bộ hidden.
- Các file JSON trong `src/reports/` do công cụ sinh ra và không bị sửa tay. Lượt đo lại này đối chiếu baseline và working tree: summary của workflow, single, swarm giữ nguyên; Orchestrator đổi chi phí vì thêm xác minh độc lập và rút gọn diagnostic.

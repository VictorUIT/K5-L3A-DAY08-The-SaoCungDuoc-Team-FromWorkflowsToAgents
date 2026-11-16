# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R1 · Scaling |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Kim, Liu và cộng sự (Google Research, Google DeepMind, MIT), *Towards a Science of Scaling Agent Systems*, arXiv:2512.08296 (12/2025, bản v2), https://arxiv.org/abs/2512.08296. Loại bằng chứng: benchmark có kiểm soát |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Phối hợp nhiều agent cải thiện kết quả ở task chia song song được và làm giảm kết quả ở task tuần tự (các biến thể multi-agent giảm 39–70% so với single agent ở nhóm task này). Thêm agent không tự động tốt hơn |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | 180 cấu hình có kiểm soát: một baseline single-agent và 4 kiểu phối hợp (independent, centralized, decentralized, hybrid), 3 họ LLM (OpenAI, Google, Anthropic), 4 benchmark agentic, ngân sách token khớp nhau. Kết luận là về model thật trên các benchmark đó, không phải về MockLLM hay task hoàn tiền |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Luồng claim là chuỗi tuần tự order → quote → host. Nếu tăng số read tool giao cho investigator của orchestrator từ 2 lên 3 rồi 5, pass rate và pass^5 không đổi (giữ 1.000), còn cost/success tăng khoảng 10 VND cho mỗi tool thêm (giá `tool_call_vnd` = 10), tức khoảng +25% mỗi nấc |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ cố định: MockLLM, code orchestrator và host, seed 11,22,33,44,55, corpus `data/public_claims.jsonl` (14 claim), `config/pricing.yaml`, evaluator `lab8.metrics`. Biến duy nhất thay đổi: danh sách `allowed_tools` trong handoff. 2 tool: `lookup_order`, `compute_compensation`. 3 tool (shape C nộp): thêm `lookup_refund_history`. 5 tool: thêm `get_claim_view`, `lookup_policy` |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: tool đọc thêm đưa dữ liệu thừa vào báo cáo của investigator và làm lộ PII trong trace, hoặc làm orchestrator quyết định khác đi. Đo bằng pass rate, pass^5, seed variance, cost/success và số trial fail vì `forbidden_substring` |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes orchestrator_min,orchestrator,orchestrator_wide --extra-shape orchestrator_min=ablation.orchestrator_variants:run_claim_min --extra-shape orchestrator_wide=ablation.orchestrator_variants:run_claim_wide --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/ablation_investigator_tools.json` (chạy trong `src/`)
- Run id / file report: `src/reports/ablation_investigator_tools.json`; ví dụ `R-orchestrator_min-C-014-s11`, `R-orchestrator-C-014-s11`, `R-orchestrator_wide-C-014-s11`. Mỗi biến thể có run id và file trace riêng trong `traces/`; trace của shape orchestrator gốc không bị biến thể ghi đè (test `test_each_ablation_variant_keeps_its_own_trace`)
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: Đúng về hướng, gần đúng về độ lớn (dự đoán +25% mỗi nấc, đo lại sau hardening +16.6% và +13.9%). Pass rate, pass^5 và variance giữ nguyên 1.000 / 1.000 / 0 ở cả ba mức. Cost/success: 2 tool 57.37 VND, 3 tool 66.90 VND (+16.6%), 5 tool 76.19 VND (+13.9% so với 3 tool). Số tool call trung bình mỗi trial: 5.50 → 6.43 → 7.36. Không trial nào fail vì `forbidden_substring`. Kết luận trong phạm vi lab: trên luồng tuần tự này, giao thêm việc đọc cho investigator chỉ thêm chi phí, không thêm trial pass. `lookup_refund_history` trong shape C nộp bài có chênh chi phí 9.53 VND mỗi lần thành công và chỉ phục vụ việc giải thích trong trace (T13, T14), không ảnh hưởng quyết định vì host tự áp trần theo đơn. Kết quả cùng hướng với claim của nguồn nhưng không kiểm chứng được con số 39–70%, vì ở đây model không quyết định gì về tiền nên pass rate không thể giảm
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`. Ablation chỉ đổi số tool đọc tuần tự của một investigator, không đo investigator chạy song song, nên không nói được gì về lợi ích latency của việc chia song song. Corpus chỉ có 14 claim public.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).

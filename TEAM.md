# Team

## Thông tin nhóm

- Tên nhóm: The SaoCungDuoc Team
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents, nhánh `main`, commit chốt `629ab80` (trùng `report/team/decision_adr.md`)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Trần Quốc Tuấn Khanh | 2A202603625 | tranquoctuankhanh1194@gmail.com | [VictorUIT](https://github.com/VictorUIT) | Workflow + Integration |
|   2 | Nguyễn Văn Ngọc Sơn | 2A202603600 |       | [kynnnS](https://github.com/kynnnS) | Single Agent |
|   3 | Nguyễn Bình An | 2A202603606 |       | [An041003](https://github.com/An041003) | Orchestrator + Handoff |
|   4 | Đỗ Phương Nam | 2A202603621 | donam02zx@gmail.com | [donam02zx](https://github.com/donam02zx) | Ledger + Evaluation |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Trần Quốc Tuấn Khanh | Workflow + Integration | `d6c1b94` (báo cáo cá nhân); commit kỹ thuật: chưa có | chưa có |
| Nguyễn Văn Ngọc Sơn | Single Agent | `24eae51` (ba shape), `7d27079` (test), `1a2a348` (bằng chứng), `629ab80` (báo cáo) | `src/tests/test_team_shapes.py` (237 test) |
| Nguyễn Bình An | Orchestrator + Handoff | chưa có commit | chưa có |
| Đỗ Phương Nam | Ledger + Evaluation | `ĐIỀN` (bonus B5: provider idempotency + reconciliation, test ledger) | `src/tests/test_bonus_provider.py` (43 test), `src/tests/test_ledger_replay_conflict.py` (3 test) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603625_TranQuocTuanKhanh

Báo cáo cá nhân: [report/team/2A202603625_TranQuocTuanKhanh.md](report/team/2A202603625_TranQuocTuanKhanh.md)

### Phần việc phụ trách

- Workflow + Integration: `src/lab8/shapes/workflow.py`, repo nhóm, cổng host và `check_submission`

### Đóng góp cụ thể

- Commit `d6c1b94` (báo cáo cá nhân). Commit kỹ thuật kèm test: `1b48aed` (thêm `src/tests/test_workflow_steps.py`)

### Bằng chứng

- `src/tests/test_workflow_steps.py`: khóa thứ tự bước cố định của workflow (`claim, order, quote, host_refund, decision`) và ngân sách gọi (1 model call, tối đa 3 tool call) trên 14 claim public. `python -m pytest -q` ở `src/`: 306 passed

## 2A202603600_NguyenVanNgocSon

Báo cáo cá nhân: [report/team/2A202603600_NguyenVanNgocSon.md](report/team/2A202603600_NguyenVanNgocSon.md)

### Phần việc phụ trách

- Single Agent: `src/lab8/shapes/single.py`; bản đầu của ba shape, test, benchmark và bản nháp báo cáo (cùng Claude Code)

### Đóng góp cụ thể

- Commit `24eae51`, `7d27079`, `1a2a348`, `629ab80`, `9afe0cd`, `6eac076`; bộ test `src/tests/test_team_shapes.py`

### Bằng chứng

- `src/reports/benchmark.json`, `src/reports/crash.json`, run id `R-single-C-002-s55`

## 2A202603606_NguyenBinhAn

Báo cáo cá nhân: [report/team/2A202603606_NguyenBinhAn.md](report/team/2A202603606_NguyenBinhAn.md)

### Phần việc phụ trách

- Orchestrator + Handoff: `src/lab8/shapes/orchestrator.py`

### Đóng góp cụ thể

- Chưa có commit đứng tên; điền sau khi commit

### Bằng chứng

- Điền sau khi commit

## 2A202603621_DoPhuongNam

Báo cáo cá nhân: [report/team/2A202603621_DoPhuongNam.md](report/team/2A202603621_DoPhuongNam.md)

### Phần việc phụ trách

- Ledger + Evaluation: crash, idempotency, benchmark, ablation
- Bonus B5: provider idempotency và reconciliation ([report/team/bonus_report.md](report/team/bonus_report.md))

### Đóng góp cụ thể

- Commit `ĐIỀN`
- `src/bonus/`: provider giả lập (dedupe / không dedupe), luồng hai pha `reserve → provider → confirm` cạnh host với 3 điểm crash mới, job `reconcile()`, biến thể shape `workflow_provider`, crash suite 16 kịch bản
- Test: `src/tests/test_bonus_provider.py` (43 test), `src/tests/test_ledger_replay_conflict.py` (3 test, nhánh `amount_conflict` của ba shape)

### Bằng chứng

- `src/reports/bonus_provider_crash.json`: `exactly_once` 16/16, `guards_passed` 4/4; phản ví dụ provider không dedupe charge 2 lần
- `src/reports/bonus_benchmark.json`: workflow_provider pass rate 1.000, cost/success 38.89 VND (workflow 28.89)
- `python -m pytest -q` (trong `src/`): 337 passed; run id `R-workflow_provider-C-001-s11`

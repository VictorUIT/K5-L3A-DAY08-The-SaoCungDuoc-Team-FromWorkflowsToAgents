# Team

## Thông tin nhóm

- Tên nhóm: The SaoCungDuoc Team
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/VictorUIT/K5-L3A-DAY08-The-SaoCungDuoc-Team-FromWorkflowsToAgents, nhánh `main`, commit chốt `629ab80` (trùng `report/team/decision_adr.md`)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 |        |      |       | [kynnnS](https://github.com/kynnnS) | workflow + integration |
|   2 |        |      |       | [VictorUIT](https://github.com/VictorUIT) | single agent |
|   3 |        |      |       | [donam02zx](https://github.com/donam02zx) | orchestrator + handoff |
|   4 |        |      |       | [An041003](https://github.com/An041003) | ledger / crash + evaluation |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| kynnnS | workflow + integration | `24eae51` (ba shape), `7d27079` (test), `1a2a348` (bằng chứng), `629ab80` (báo cáo) | `src/tests/test_team_shapes.py` (237 test) |
| VictorUIT | single agent | chưa có commit | chưa có |
| donam02zx | orchestrator + handoff | chưa có commit | chưa có |
| An041003 | ledger / crash + evaluation | chưa có commit | chưa có |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## MSSV_HoTen (kynnnS)

Báo cáo cá nhân: [report/team/MSSV_HoTen_kynnnS.md](report/team/MSSV_HoTen_kynnnS.md)

### Phần việc phụ trách

- workflow + integration: `src/lab8/shapes/workflow.py`, chạy cổng host, crash suite, benchmark, đưa code lên repo nhóm

### Đóng góp cụ thể

- Commit `24eae51`, `7d27079`, `1a2a348`, `629ab80`, `9afe0cd`; bộ test `src/tests/test_team_shapes.py`

### Bằng chứng

- `src/reports/benchmark.json`, `src/reports/crash.json`, run id `R-workflow-C-002-s55`

## MSSV_HoTen (VictorUIT)

Báo cáo cá nhân: [report/team/MSSV_HoTen_VictorUIT.md](report/team/MSSV_HoTen_VictorUIT.md)

### Phần việc phụ trách

- single agent: `src/lab8/shapes/single.py`

### Đóng góp cụ thể

- Chưa có commit đứng tên; điền sau khi commit

### Bằng chứng

- Điền sau khi commit

## MSSV_HoTen (donam02zx)

Báo cáo cá nhân: [report/team/MSSV_HoTen_donam02zx.md](report/team/MSSV_HoTen_donam02zx.md)

### Phần việc phụ trách

- orchestrator + handoff: `src/lab8/shapes/orchestrator.py`

### Đóng góp cụ thể

- Chưa có commit đứng tên; điền sau khi commit

### Bằng chứng

- Điền sau khi commit

## MSSV_HoTen (An041003)

Báo cáo cá nhân: [report/team/MSSV_HoTen_An041003.md](report/team/MSSV_HoTen_An041003.md)

### Phần việc phụ trách

- ledger / crash + evaluation: crash, idempotency, benchmark, ablation

### Đóng góp cụ thể

- Chưa có commit đứng tên; điền sau khi commit

### Bằng chứng

- Điền sau khi commit

---
description: Chạy toàn bộ vòng đời nghiên cứu học thuật — research → write → review → revise → finalize — dùng bộ skill Academic Research Skills (ARS).
---

## Kích hoạt
Gọi bằng `/ars-pipeline <chủ đề hoặc yêu cầu>`
 
## Input cần có (hỏi nếu thiếu, chỉ 1 câu):
- Chủ đề / câu hỏi nghiên cứu
- Loại output: literature review / full paper / policy brief / fact-check
- Citation style (mặc định APA7 nếu không nêu)
- Mode: guided (dừng xác nhận mỗi bước) hay autonomous (tự chạy hết pipeline)
## Các bước
 
Step 1 — Khởi động pipeline
Gọi `academic-pipeline/agents/pipeline_orchestrator_agent.md`, tham khảo `mode_advisor.md` để chọn mode phù hợp (xem `pipeline_state_machine.md`).
 
Step 2 — Research
Gọi skill `deep-research`:
- Dùng `research_question_agent` để làm rõ câu hỏi nghiên cứu.
- Dùng `research_architect_agent` để lập kế hoạch tìm kiếm.
- Dùng `source_verification_agent` để xác minh mọi nguồn trước khi đưa vào synthesis.
- Dùng `synthesis_agent` để tổng hợp literature.
Output: literature matrix (`literature_matrix_template.md`) hoặc research brief (`research_brief_template.md`).
Step 3 — Write (chỉ chạy nếu output yêu cầu là bài viết, không phải chỉ research brief)
Gọi skill `academic-paper`:
- `intake_agent` → xác nhận scope, structure.
- `literature_strategist_agent` → map literature vào outline.
- `structure_architect_agent` → dựng IMRaD hoặc cấu trúc phù hợp (`paper_structure_patterns.md`).
- `draft_writer_agent` → viết draft từng phần.
- `citation_compliance_agent` → gắn & format citation đúng chuẩn đã chọn.
- `formatter_agent` → format cuối theo target venue.
Step 4 — Review
Gọi skill `academic-paper-reviewer`:
- `methodology_reviewer_agent` + `domain_reviewer_agent` chạy song song.
- `devils_advocate_reviewer_agent` để stress-test luận điểm yếu.
- `editorial_synthesizer_agent` tổng hợp feedback thành 1 báo cáo (`peer_review_report_template.md`).
Step 5 — Revise
Quay lại `academic-paper/revision_coach_agent`, áp dụng `revision_patch_protocol.md`. Nếu revision lớn, chạy `version_family_reconciliation_example.md` để đối chiếu các phiên bản.
 
Step 6 — Integrity gate (bắt buộc trước finalize)
Gọi `academic-pipeline`:
- `claim_ref_alignment_audit_agent` — đối chiếu từng claim với reference thật.
- `integrity_verification_agent` — chạy full integrity check (`integrity_review_protocol.md`, `plagiarism_detection_protocol.md`).
Nếu integrity FAIL → quay lại Step 5, không được bỏ qua.
Step 7 — Finalize
Xuất báo cáo tiến trình (`progress_dashboard_template.md`) + bản thảo cuối. Thông báo rõ trạng thái: đã qua integrity gate, citation style dùng, số vòng revision.
 
## Quy tắc dừng
- Nếu mode = guided: dừng và xin xác nhận người dùng sau mỗi Step trước khi qua step kế tiếp.
- Nếu mode = autonomous: chỉ dừng khi integrity gate ở Step 6 fail, hoặc thiếu dữ liệu bắt buộc.
 

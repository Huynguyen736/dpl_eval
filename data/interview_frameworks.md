# Tài Liệu Đặc Tả Dữ Liệu: `interview_frameworks.json`

## 1. Tổng Quan Dataset
* **Đường dẫn tệp:** `data/interview_frameworks.json`
* **Số lượng bản ghi:** 25 Khung phỏng vấn chuẩn hóa (Standard Interview Frameworks) đại diện cho 25 vị trí công nghệ trọng điểm trên thị trường tuyển dụng CNTT Việt Nam.
* **Mục đích sử dụng:** Đóng vai trò là **"Xương sống tri thức" (Knowledge Base Backbone)** của hệ thống Mock Interview. Bộ dữ liệu này định nghĩa cấu trúc một buổi phỏng vấn chuẩn mực thực tế:
  * Phân kỳ giai đoạn phỏng vấn (`interview_stages`).
  * Trọng số đánh giá các trụ cột năng lực (`evaluation_matrix`).
  * Thang điểm neo (`scoring_anchors` 1–5) và điểm sàn đạt chuẩn theo từng level (`passing_thresholds`).
  * Ngân hàng câu hỏi kỹ thuật kèm đáp án chuẩn và tiêu chí chấm điểm 3 mức (`technical_questions`: poor, acceptable, excellent).
  * Ngân hàng câu hỏi hành vi theo mô hình STAR (`behavioral_questions`) có tiêu chí nhận diện hành vi tích cực/tiêu cực.
  * Ngữ cảnh thị trường tuyển dụng công nghệ Việt Nam (`frequently_asked_by`, `vn_recruitment_process`).
  * Định danh vai trò chuẩn hóa quốc tế (`canonical_role_id`, `canonical_role_name`, `role_family`).

---

## 2. Bảng Mô Tả Chi Tiết Các Trường Dữ Liệu

| Tên trường (Field Name) | Kiểu dữ liệu (Data Type) | Nullable / Missing | Ý nghĩa nghiệp vụ (Business Semantics) | Giá trị mẫu (Sample Value) | Vai trò trong Pipeline Ingestion / Retrieval / Context |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `position_id` | `string` | Không (0/25) | Mã định danh chuẩn của vị trí công việc. | `"IF_FE"`, `"IF_BE_JAVA"`, `"IF_AI"` | Primary Key / Khóa ngoại liên kết giữa JD, hồ sơ ứng viên và framework. |
| `role_title` | `string` | Không (0/25) | Tên chức danh nghề nghiệp đầy đủ kèm tiếng Việt. | `"Frontend Developer (Lập trình viên Frontend)"` | Khớp nối từ khóa tìm kiếm (Full-text / Semantic search). |
| `canonical_role_id` | `string` | Không (0/25) | Mã chuẩn hóa định danh vai trò nghề nghiệp. | `"ROLE_FRONTEND"`, `"ROLE_AI_ENGINEER"` | Khớp nối ontology vai trò giữa các hệ thống tuyển dụng. |
| `canonical_role_name` | `string` | Không (0/25) | Tên vai trò chuẩn hóa. | `"Frontend Developer (Lập trình viên Frontend)"` | Hiển thị chuẩn trên báo cáo và giao diện. |
| `role_family` | `string` | Không (0/25) | Nhóm ngành nghề lớn (Family). | `"Software Engineering"`, `"Data & AI"` | Phân loại phân cấp cấp cao (Hierarchical taxonomy). |
| `major_category` | `string` | Không (0/25) | Phân ngành kỹ thuật chi tiết. | `"Kỹ thuật phần mềm & Phát triển giao diện Web (Frontend Engineering)"` | Nhóm cấp cao để phân loại domain tri thức. |
| `target_levels` | `list[string]` | Không (0/25) | Các cấp bậc mà khung phỏng vấn hướng đến. | `["Intern", "Fresher", "Junior"]` | Bộ lọc cấp bậc để điều chỉnh độ khó của phiên phỏng vấn. |
| `target_competencies` | `list[string]` | Không (0/25) | Các khối năng lực kỹ thuật then chốt mà ứng viên bắt buộc phải có. | `["JavaScript/TypeScript fundamentals", "React Component Lifecycle", "State Management"]` | Làm checklist để AI đối soát độ phủ câu hỏi trong suốt buổi phỏng vấn. |
| `vn_recruitment_process` | `string` | Không (0/25) | Mô tả tổng thể quy trình và văn hóa tuyển dụng thực tế tại Việt Nam. | `"Quy trình tuyển dụng Frontend tại các công ty CNTT Việt Nam (VNG, MoMo, FPT)..."` | Hướng dẫn AI đóng vai trò người phỏng vấn bản địa hóa (Localized Interviewer). |
| `frequently_asked_by` | `list[string]` | Không (0/25) | Danh sách tên công ty thường xuyên sử dụng các bộ câu hỏi dạng này. | `["VNG Corporation", "MoMo", "Viettel AI"]` | Gắn nhãn câu hỏi (Company persona & target employer tag). |
| `interview_stages` | `list[dict]` | Không (0/25) | Các giai đoạn/vòng phỏng vấn theo đúng trình tự thực tế. | Xem mục [3.1](#31-cấu-trúc-interview_stages) | **Điều phối luồng phỏng vấn (Conversation Orchestration Flow)**. |
| `evaluation_matrix` | `list[dict]` | Không (0/25) | Ma trận đánh giá năng lực gồm các trụ cột và trọng số phần trăm tương ứng. | Xem mục [3.2](#32-cấu-trúc-evaluation_matrix) | Tính điểm tổng kết phiên phỏng vấn (Weighted Scoring). |
| `scoring_anchors` | `dict` (Key: `"1"`..`"5"`) | Không (0/25) | Định nghĩa thang điểm từ 1 (Strong No Hire) đến 5 (Strong Hire). | Xem mục [3.3](#33-cấu-trúc-scoring_anchors) | Chuẩn hóa rubric cho LLM đánh giá từng câu trả lời. |
| `passing_thresholds` | `dict` (Levels) | Không (0/25) | Tiêu chí và điểm số tối thiểu để vượt qua phỏng vấn theo từng cấp bậc (`Intern`, `Fresher`, `Junior`). | Xem mục [3.4](#34-cấu-trúc-passing_thresholds) | Quyết định đầu ra: Đỗ (Pass) hay Trượt (Fail) sau buổi phỏng vấn. |
| `evaluation_rubric` | `dict` | Không (0/25) | Bản tổng hợp cấu trúc rubric hoàn chỉnh (kết hợp Pillars, Scale Anchors, Level Thresholds). | Xem mục [3.5](#35-cấu-trúc-evaluation_rubric) | Cung cấp toàn bộ chỉ dẫn chấm điểm vào System Prompt của Agent chấm thi. |
| `technical_questions` | `list[dict]` | Không (0/25) | Ngân hàng câu hỏi kỹ thuật chọn lọc, có đáp án chuẩn và tiêu chí chấm điểm 3 mức. | Xem mục [3.6](#36-cấu-trúc-technical_questions) | **Kho tri thức câu hỏi (RAG retrieval pool)** để AI lựa chọn câu hỏi theo đúng chủ đề. |
| `behavioral_questions` | `list[dict]` | Không (0/25) | Danh sách câu hỏi tình huống hành vi chuẩn STAR. | Xem mục [3.7](#37-cấu-trúc-behavioral_questions) | Đánh giá kỹ năng mềm và độ phù hợp văn hóa ở giai đoạn cuối buổi phỏng vấn. |
| `markdown_file` | `string` | Không (0/25) | Tên tệp markdown gốc lưu trữ chi tiết bài viết của framework. | `"IF_FE_Frontend_Developer.md"` | Truy xuất tài liệu gốc dạng văn bản Markdown nếu cần nạp toàn bộ. |

---

## 3. Cấu Trúc Các Trường Dữ Liệu Phức Tạp (Nested Objects)

### 3.1. Cấu trúc `interview_stages` (Trình tự giai đoạn phỏng vấn)
```json
[
  {
    "stage_name": "CV & Project Screening",
    "weight_percent": 15,
    "description": "Sơ loại hồ sơ và thảo luận các dự án AI/Data đã thực hiện."
  },
  {
    "stage_name": "Technical Deep Dive & Problem Solving",
    "weight_percent": 45,
    "description": "Kiểm tra kiến thức cốt lõi, thuật toán và giải quyết bài toán thực tế."
  }
]
```

### 3.2. Cấu trúc `evaluation_matrix` (Ma trận trọng số đánh giá)
```json
[
  {
    "pillar": "Tư duy giải quyết vấn đề & Phân tích",
    "pillar_en": "Problem Solving & Analytical Thinking",
    "weight_percent": 30,
    "criteria": "Khả năng làm rõ yêu cầu chưa đầy đủ, chia nhỏ bài toán phức tạp thành các module logic, và đề xuất giải pháp tối ưu có căn cứ."
  },
  {
    "pillar": "Năng lực kỹ thuật chuyên môn & Nền tảng CS",
    "pillar_en": "Technical Competency & CS Fundamentals",
    "weight_percent": 30,
    "criteria": "Nắm vững bản chất ngôn ngữ/framework, hiểu cơ chế hoạt động bên dưới (under the hood), áp dụng đúng cấu trúc dữ liệu."
  },
  {
    "pillar": "Chất lượng mã nguồn & Thực hành Kỹ thuật",
    "pillar_en": "Code Quality & Engineering Practices",
    "weight_percent": 20,
    "criteria": "Viết mã sạch (Clean Code), có tư duy phân tách ranh giới trách nhiệm, xử lý lỗi ngoại lệ bài bản."
  },
  {
    "pillar": "Kỹ năng giao tiếp & Độ phù hợp văn hóa",
    "pillar_en": "Communication & Culture Fit",
    "weight_percent": 20,
    "criteria": "Giao tiếp rõ ràng, thái độ đón nhận phản hồi (receptiveness to feedback), tính trung thực và tinh thần cầu tiến."
  }
]
```

### 3.3. Cấu trúc `scoring_anchors` (Thang điểm neo từ 1 đến 5)
* `"1"`: **Strong No Hire (Dưới chuẩn nghiêm trọng)** - Hổng kiến thức nền tảng, không viết được mã, bảo thủ, thiếu trung thực.
* `"2"`: **No Hire (Chưa đạt chuẩn)** - Kiến thức chắp vá, giải quyết bài toán chỉ mang tính sao chép, cần chỉ dẫn liên tục.
* `"3"`: **Borderline / Leaning No Hire (Tiệm cận đạt chuẩn)** - Nắm được lý thuyết cơ bản nhưng lúng túng khi hỏi sâu vào bản chất hoặc gặp bài toán biến thể.
* `"4"`: **Hire (Đạt chuẩn vững vàng)** - Trả lời rõ ràng, hiểu cơ chế bên dưới, chủ động giao tiếp và viết code chuẩn chỉ.
* `"5"`: **Strong Hire (Vượt trội / Xuất sắc)** - Hiểu sâu sắc hệ thống, phân tích thấu đáo trade-off, đưa ra giải pháp mở rộng tối ưu và phong thái tự tin.

### 3.4. Cấu trúc `passing_thresholds` (Ngưỡng đỗ theo cấp bậc)
```json
{
  "Intern": "Điểm trung bình >= 2.8 / 5.0 (Ưu tiên: Tiềm năng tự học, tư duy logic cơ bản, thái độ nghiêm túc)",
  "Fresher": "Điểm trung bình >= 3.2 / 5.0 (Yêu cầu: Nắm chắc kiến thức cốt lõi, hoàn thành đồ án độc lập, không mắc lỗi nghiêm trọng ở CS fundamentals)",
  "Junior": "Điểm trung bình >= 3.6 / 5.0 (Yêu cầu: Kinh nghiệm thực chiến, hiểu biết sâu về luồng dữ liệu, debug thành thạo, viết code có test)"
}
```

### 3.5. Cấu trúc `evaluation_rubric`
Là đối tượng tổng hợp lồng ghép:
* `pillars`: Danh sách các trụ cột chấm điểm.
* `scale_anchors`: Chi tiết mô tả từ điểm 1 đến điểm 5.
* `level_thresholds`: Điểm sàn yêu cầu theo từng vị trí tuyển dụng.

### 3.6. Cấu trúc `technical_questions` (Ngân hàng câu hỏi kỹ thuật)
```json
{
  "id": "AI_Q01",
  "level": "Intern",
  "question": "Phân biệt hiện tượng Overfitting và Underfitting trong Machine Learning. Các kỹ thuật Regularization phổ biến (L1 Lasso, L2 Ridge, Dropout) giúp giải quyết hiện tượng Overfitting như thế nào?",
  "expected_answer": "Underfitting (High Bias) xảy ra khi mô hình quá đơn giản, không học được quy luật dữ liệu... Overfitting (High Variance) xảy ra khi mô hình học vẹt cả nhiễu...",
  "scoring_rubric": {
    "poor": "Chỉ nói Overfitting là train tốt test dở nhưng không nêu được bản chất Bias-Variance và cơ chế của Regularization.",
    "acceptable": "Phân biệt đúng Overfitting/Underfitting, giải thích được L1 ép về 0, L2 co trọng số và Dropout tắt nơ-ron ngẫu nhiên.",
    "excellent": "Phân tích sâu về không gian tối ưu hình học, quan hệ giữa L2 và Gaussian prior, và cách scale activation khi inference với Dropout."
  }
}
```

### 3.7. Cấu trúc `behavioral_questions` (Câu hỏi hành vi chuẩn STAR)
```json
{
  "id": "STAR_01",
  "question": "Hãy kể về một lỗi phần mềm (bug) phức tạp nhất hoặc sự cố kỹ thuật khó khăn nhất mà bạn từng gặp trong một đồ án hoặc công việc trước đây. Bạn đã tìm ra nguyên nhân gốc rễ (root cause) và xử lý nó như thế nào?",
  "evaluation_focus": "Khả năng phân tích nguyên nhân gốc rễ, kỹ năng debug bài bản, tính kiên trì và không hoảng loạn trước áp lực sự cố.",
  "star_criteria": {
    "situation_task": "Ứng viên mô tả rõ bối cảnh sự cố, mức độ ảnh hưởng của lỗi kỹ thuật và trách nhiệm cá nhân cụ thể.",
    "action_positive": "Chủ động sử dụng các công cụ phân tích log, debug từng bước, cô lập nguyên nhân (isolate root cause), và viết test case để tái hiện lỗi trước khi sửa.",
    "action_negative": "Thử nghiệm ngẫu nhiên không có phương pháp, đổ lỗi cho thư viện/môi trường bên ngoài, hoặc bỏ qua không xử lý dứt điểm.",
    "result": "Hệ thống hoạt động ổn định trở lại, có chỉ số cải thiện rõ ràng, và đúc kết thành tài liệu/bài học ngăn ngừa tái diễn."
  }
}
```

---

## 4. Danh Sách 25 Vị Trí Công Nghệ Hiện Có

| STT | Position ID | Tên Vị Trí (Role Title) | Canonical Role ID | Role Family |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `IF_AI` | AI Engineer (Kỹ sư Trí tuệ nhân tạo) | `ROLE_AI_ENGINEER` | Data & AI |
| 2 | `IF_AI_SWE` | AI Software Engineer (Kỹ sư Phần mềm AI) | `ROLE_AI_SOFTWARE_ENGINEER` | Data & AI |
| 3 | `IF_AGENTIC_AI` | Agentic AI Engineer (Kỹ sư AI Tác tử / AI Agent) | `ROLE_AGENTIC_AI` | Data & AI |
| 4 | `IF_DA` | Data Analyst (Chuyên viên Phân tích dữ liệu) | `ROLE_DATA_ANALYST` | Data & AI |
| 5 | `IF_DE` | Data Engineer (Kỹ sư Kỹ thuật dữ liệu) | `ROLE_DATA_ENGINEER` | Data & AI |
| 6 | `IF_DS` | Data Scientist (Nhà Khoa học dữ liệu) | `ROLE_DATA_SCIENTIST` | Data & AI |
| 7 | `IF_QA_QC` | Software QA/QC Engineer (Kỹ sư Kiểm thử phần mềm QA/QC) | `ROLE_QA_QC` | Quality Assurance |
| 8 | `IF_AUTO_QA` | Automation QA/QC Engineer (Kỹ sư Kiểm thử tự động) | `ROLE_AUTO_QA` | Quality Assurance |
| 9 | `IF_FE` | Frontend Developer (Lập trình viên Frontend) | `ROLE_FRONTEND` | Software Engineering |
| 10 | `IF_BE_JAVA` | Backend Developer - Java (Lập trình viên Backend Java) | `ROLE_BACKEND_JAVA` | Software Engineering |
| 11 | `IF_BE_NET` | Backend Developer - .NET (Lập trình viên Backend .NET) | `ROLE_SOFTWARE_ENGINEER` | Software Engineering |
| 12 | `IF_BE_PHP` | Backend Developer - PHP (Lập trình viên Backend PHP) | `ROLE_BACKEND_PHP` | Software Engineering |
| 13 | `IF_BE_GEN` | Backend Developer - Chung (Lập trình viên Backend) | `ROLE_BACKEND_GENERAL` | Software Engineering |
| 14 | `IF_FULLSTACK` | FullStack Developer (Lập trình viên Fullstack) | `ROLE_SOFTWARE_ENGINEER` | Software Engineering |
| 15 | `IF_SWE` | Software Engineer (Kỹ sư Phần mềm) | `ROLE_SOFTWARE_ENGINEER` | Software Engineering |
| 16 | `IF_SWD` | Software Developer (Lập trình viên Phần mềm) | `ROLE_SOFTWARE_ENGINEER` | Software Engineering |
| 17 | `IF_EMBEDDED` | Embedded Software Engineer (Kỹ sư Phần mềm nhúng) | `ROLE_EMBEDDED` | Hardware & Embedded |
| 18 | `IF_BA` | Business Analyst - BA (Chuyên viên Phân tích nghiệp vụ IT) | `ROLE_BA` | Business Analysis & Product |
| 19 | `IF_DEVOPS` | DevOps Engineer (Kỹ sư Vận hành & Phát triển) | `ROLE_DEVOPS` | Infrastructure & Cloud |
| 20 | `IF_MOBILE_ANDROID` | Mobile Developer - Android (Lập trình viên Di động Android) | `ROLE_MOBILE_ANDROID` | Mobile Development |
| 21 | `IF_MOBILE_IOS` | Mobile Developer - iOS (Lập trình viên Di động iOS) | `ROLE_MOBILE_IOS` | Mobile Development |
| 22 | `IF_NETWORK` | Network Engineer (Kỹ sư Quản trị Mạng) | `ROLE_NETWORK_ENGINEER` | Infrastructure & Cloud |
| 23 | `IF_UNITY` | Unity Game Developer (Lập trình viên Game Unity) | `ROLE_SOFTWARE_ENGINEER` | Software Engineering |
| 24 | `IF_ERP` | ERP Developer / Consultant (Chuyên viên Tư vấn / Phát triển ERP) | `ROLE_ERP_CONSULTANT` | Business Analysis & Product |
| 25 | `IF_PRODUCT_ENG` | Product Engineer (Kỹ sư Sản phẩm) | `ROLE_PRODUCT_ENGINEER` | Business Analysis & Product |

---

## 5. Giá Trị & Vai Trò Trong Quy Trình Mock Interview
1. **Orchestrator Blueprint (Kế hoạch kịch bản tổng thể):** Cung cấp cấu trúc tuần tự từng vòng thi, đảm bảo AI không hỏi lộn xộn mà phỏng vấn đúng theo thời gian và trọng tâm (Stage 1 -> Stage 2 -> Stage 3).
2. **Ground Truth & Answer Key (Đáp án và barem chấm điểm khách quan):** Cung cấp `expected_answer` và tiêu chuẩn 3 mức `poor` / `acceptable` / `excellent` để AI đánh giá câu trả lời của ứng viên chính xác, công bằng, hạn chế hiện tượng LLM hallucination.
3. **STAR Evaluation Guide:** Đưa ra các chỉ dấu hành vi tích cực (`action_positive`) và tiêu cực (`action_negative`) để người chấm biết ứng viên có kỹ năng làm việc nhóm và giải quyết vấn đề thực tế hay không.

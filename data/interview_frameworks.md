# Tài Liệu Đặc Tả Dữ Liệu: `interview_frameworks.json`

## 1. Tổng Quan Dataset
* **Đường dẫn tệp:** `data/interview_frameworks.json`
* **Số lượng bản ghi:** 16 Khung phỏng vấn chuẩn hóa (Standard Interview Frameworks) đại diện cho 16 vị trí công nghệ trọng điểm.
* **Mục đích sử dụng:** Đóng vai trò là **"Xương sống tri thức" (Knowledge Base Backbone)** của hệ thống Mock Interview. Bộ dữ liệu này định nghĩa cấu trúc một buổi phỏng vấn chuẩn mực thực tế:
  * Phân kỳ giai đoạn phỏng vấn (`interview_stages`).
  * Trọng số đánh giá các trụ cột năng lực (`evaluation_matrix`).
  * Thang điểm neo (`scoring_anchors` 1–5) và điểm sàn đạt chuẩn theo từng level (`passing_thresholds`).
  * Ngân hàng câu hỏi kỹ thuật kèm đáp án chuẩn và tiêu chí chấm điểm 3 mức (`technical_questions`: poor, acceptable, excellent).
  * Ngân hàng câu hỏi hành vi theo mô hình STAR (`behavioral_questions`) có tiêu chí nhận diện hành vi tích cực/tiêu cực.
  * Ngữ cảnh thị trường tuyển dụng công nghệ Việt Nam (`target_companies_vn`, `vn_recruitment_process`, `vn_community_citations`).

---

## 2. Bảng Mô Tả Chi Tiết Các Trường Dữ Liệu

| Tên trường (Field Name) | Kiểu dữ liệu (Data Type) | Nullable / Missing | Ý nghĩa nghiệp vụ (Business Semantics) | Giá trị mẫu (Sample Value) | Vai trò trong Pipeline Ingestion / Retrieval / Context |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `position_id` | `string` | Không (0/16) | Mã định danh chuẩn của vị trí công việc. | `"IF_FE"`, `"IF_JAVA"`, `"IF_AI"` | Primary Key / Khóa ngoại liên kết giữa JD, hồ sơ ứng viên và framework. |
| `role_title` | `string` | Không (0/16) | Tên chức danh nghề nghiệp đầy đủ. | `"Frontend Developer (React / JavaScript / TypeScript)"` | Khớp nối từ khóa tìm kiếm (Full-text / Semantic search). |
| `major_category` | `string` | Không (0/16) | Phân ngành kỹ thuật lớn. | `"Kỹ thuật phần mềm (Software Engineering)"` | Nhóm cấp cao để phân loại domain tri thức. |
| `target_levels` | `list[string]` | Không (0/16) | Các cấp bậc mà khung phỏng vấn hướng đến. | `["Intern", "Fresher", "Junior (<= 2 năm)"]` | Bộ lọc cấp bậc để điều chỉnh độ khó của phiên phỏng vấn. |
| `target_competencies` | `list[string]` | Không (0/16) | Các khối năng lực kỹ thuật then chốt mà ứng viên bắt buộc phải có. | `["JavaScript/TypeScript fundamentals", "React Component Lifecycle", "State Management"]` | Làm checklist để AI đối soát độ phủ câu hỏi trong suốt buổi phỏng vấn. |
| `target_companies_vn` | `list[dict]` | Không (0/16) | Danh sách các doanh nghiệp công nghệ tiêu biểu tại VN tuyển dụng vị trí này kèm chương trình tuyển dụng sinh viên/fresher. | Xem mục [3.1](#31-cấu-trúc-target_companies_vn) | Tạo persona nhà tuyển dụng (ví dụ: phong cách hỏi của VNG, FPT hay Viettel). |
| `vn_recruitment_process` | `string` | Không (0/16) | Mô tả tổng thể quy trình và văn hóa tuyển dụng thực tế tại Việt Nam. | `"Quy trình tuyển dụng Frontend tại các công ty CNTT Việt Nam (VNG, MoMo, FPT)..."` | Hướng dẫn AI đóng vai trò người phỏng vấn bản địa hóa (Localized Interviewer). |
| `vn_community_citations` | `list[dict]` | Không (0/16) | Các tài liệu, video chia sẻ kinh nghiệm phỏng vấn thực tế từ cộng đồng lập trình viên Việt Nam (F8, Tôi Đi Code Dạo, TopDev,...). | Xem mục [3.2](#32-cấu-trúc-vn_community_citations) | Grounding dữ liệu thực tế, nguồn câu hỏi hay hỏi trong đời thực. |
| `frequently_asked_by` | `list[string]` | Không (0/16) | Danh sách tên công ty thường xuyên sử dụng các bộ câu hỏi dạng này. | `["VNG Corporation", "MoMo", "FPT Software"]` | Gắn nhãn câu hỏi (Company tag). |
| `interview_stages` | `list[dict]` | Không (0/16) | Các giai đoạn/vòng phỏng vấn theo đúng trình tự thực tế. | Xem mục [3.3](#33-cấu-trúc-interview_stages) | **Điều phối luồng phỏng vấn (Conversation Orchestration Flow)**. |
| `evaluation_matrix` | `list[dict]` | Không (0/16) | Ma trận đánh giá năng lực gồm các trụ cột và trọng số phần trăm tương ứng. | Xem mục [3.4](#34-cấu-trúc-evaluation_matrix) | Tính điểm tổng kết phiên phỏng vấn (Weighted Scoring). |
| `scoring_anchors` | `dict` (Key: `"1"`..`"5"`) | Không (0/16) | Định nghĩa thang điểm từ 1 (Strong No Hire) đến 5 (Strong Hire). | Xem mục [3.5](#35-cấu-trúc-scoring_anchors) | Chuẩn hóa rubric cho LLM đánh giá từng câu trả lời. |
| `passing_thresholds` | `dict` (Levels) | Không (0/16) | Tiêu chí và điểm số tối thiểu để vượt qua phỏng vấn theo từng cấp bậc (`Intern`, `Fresher`, `Junior`). | Xem mục [3.6](#36-cấu-trúc-passing_thresholds) | Quyết định đầu ra: Đỗ (Pass) hay Trượt (Fail) sau buổi phỏng vấn. |
| `evaluation_rubric` | `dict` | Không (0/16) | Bản tổng hợp cấu trúc rubric hoàn chỉnh (kết hợp Matrix, Anchors, Thresholds). | Xem mục [3.7](#37-cấu-trúc-evaluation_rubric) | Cung cấp toàn bộ chỉ dẫn chấm điểm vào System Prompt của Agent chấm thi. |
| `technical_questions` | `list[dict]` | Không (0/16) | Ngân hàng câu hỏi kỹ thuật chọn lọc, có đáp án chuẩn và tiêu chí chấm điểm 3 mức. | Xem mục [3.8](#38-cấu-trúc-technical_questions) | **Kho tri thức câu hỏi (RAG retrieval pool)** để AI lựa chọn câu hỏi theo đúng chủ đề. |
| `behavioral_questions` | `list[dict]` | Không (0/16) | Danh sách câu hỏi tình huống hành vi chuẩn STAR. | Xem mục [3.9](#39-cấu-trúc-behavioral_questions) | Đánh giá kỹ năng mềm và độ phù hợp văn hóa ở giai đoạn cuối buổi phỏng vấn. |
| `citations` | `list[dict]` | Không (0/16) | Nguồn tham khảo uy tín quốc tế (GitHub repos, tài liệu chính thức). | `[{"source": "SudheerJ ReactJS", "url": "..."}]` | Nguồn thẩm định tính đúng đắn của đáp án. |
| `markdown_file` | `string` | Không (0/16) | Tên tệp markdown gốc lưu trữ chi tiết bài viết của framework. | `"IF_FE_Frontend_Developer.md"` | Truy xuất tài liệu gốc dạng văn bản Markdown nếu cần nạp toàn bộ. |

---

## 3. Cấu Trúc Các Trường Dữ Liệu Phức Tạp (Nested Objects)

### 3.1. Cấu trúc `target_companies_vn`
```json
[
  {
    "name": "VNG Corporation (Zalo / Zing / VNGGames)",
    "program": "VNG Tech Fresher / Campus Recruitment",
    "career_url": "https://careers.vng.com.vn/"
  }
]
```

### 3.2. Cấu trúc `vn_community_citations`
```json
[
  {
    "source": "Kênh YouTube 'F8 Official' (Sơn Đặng)",
    "type": "YouTube Video Phỏng Vấn Dev",
    "url": "https://www.youtube.com/c/F8VNOfficial",
    "note": "Các video mô phỏng phỏng vấn thực tế vị trí Frontend Intern/Fresher, giải thích sâu về closures, async/await và React lifecycle."
  }
]
```

### 3.3. Cấu trúc `interview_stages` (Trình tự giai đoạn phỏng vấn)
```json
[
  {
    "stage": 1,
    "name": "CV Screening & Phone Cultural Screen",
    "duration": "20 - 30 phút",
    "interviewer": "Technical Recruiter / Talent Acquisition Specialist",
    "focus_areas": [
      "Xác thực thông tin học vấn, đồ án tốt nghiệp, GPA, các chứng chỉ chuyên ngành",
      "Đánh giá động lực nghề nghiệp, sự trung thực và thái độ cầu thị",
      "Kiểm tra khả năng giao tiếp, truyền đạt ý tưởng mạch lạc và ngoại ngữ"
    ],
    "passing_criteria": "Thể hiện tư duy cầu tiến, trung thực, giao tiếp rõ ràng, phù hợp văn hóa kỹ thuật."
  },
  {
    "stage": 2,
    "name": "Technical Fundamentals & Live Problem Solving",
    "duration": "45 - 60 phút",
    "interviewer": "Senior Software Engineer / Tech Lead",
    "focus_areas": [
      "Kiểm tra kiến thức nền tảng (JS/TS fundamentals, DOM, cơ chế bất đồng bộ)",
      "Kiến trúc component, quản lý state và tối ưu hóa hiệu năng",
      "Live Coding hoặc giải quyết bài toán giao diện thực tế"
    ],
    "passing_criteria": "Điểm chuyên môn >= 3.0/5.0, giải thích được bản chất kỹ thuật thay vì chỉ học thuộc."
  }
]
```

### 3.4. Cấu trúc `evaluation_matrix` (Ma trận trọng số đánh giá)
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

### 3.5. Cấu trúc `scoring_anchors` (Thang điểm neo từ 1 đến 5)
* `"1"`: **Strong No Hire (Dưới chuẩn nghiêm trọng)** - Hổng kiến thức nền tảng, không viết được mã, bảo thủ, thiếu trung thực.
* `"2"`: **No Hire (Chưa đạt chuẩn)** - Kiến thức chắp vá, giải quyết bài toán chỉ mang tính sao chép, cần chỉ dẫn liên tục.
* `"3"`: **Borderline / Leaning No Hire (Tiệm cận đạt chuẩn)** - Nắm được lý thuyết cơ bản nhưng lúng túng khi hỏi sâu vào bản chất hoặc gặp bài toán biến thể.
* `"4"`: **Hire (Đạt chuẩn vững vàng)** - Trả lời rõ ràng, hiểu cơ chế bên dưới, chủ động giao tiếp và viết code chuẩn chỉ.
* `"5"`: **Strong Hire (Vượt trội / Xuất sắc)** - Hiểu sâu sắc hệ thống, phân tích thấu đáo trade-off, đưa ra giải pháp mở rộng tối ưu và phong thái tự tin.

### 3.6. Cấu trúc `passing_thresholds` (Ngưỡng đỗ theo cấp bậc)
```json
{
  "Intern": "Điểm trung bình >= 2.8 / 5.0 (Ưu tiên: Tiềm năng tự học, tư duy logic cơ bản, thái độ nghiêm túc)",
  "Fresher": "Điểm trung bình >= 3.2 / 5.0 (Yêu cầu: Nắm chắc kiến thức cốt lõi, hoàn thành đồ án độc lập, không mắc lỗi nghiêm trọng ở CS fundamentals)",
  "Junior": "Điểm trung bình >= 3.6 / 5.0 (Yêu cầu: Kinh nghiệm thực chiến, hiểu biết sâu về luồng dữ liệu, debug thành thạo, viết code có test)"
}
```

### 3.7. Cấu trúc `evaluation_rubric`
Là đối tượng tổng hợp lồng ghép:
* `pillars`: Danh sách các trụ cột chấm điểm.
* `scale_anchors`: Chi tiết mô tả từ điểm 1 đến điểm 5.
* `level_thresholds`: Điểm sàn yêu cầu theo từng vị trí tuyển dụng.

### 3.8. Cấu trúc `technical_questions` (Ngân hàng câu hỏi kỹ thuật)
```json
{
  "id": "FE_Q01",
  "question": "Giải thích cơ chế Virtual DOM và thuật toán Reconciliation (Diffing Algorithm) trong React. Tại sao React lại nhanh hơn việc trực tiếp thao tác DOM?",
  "question_en": "Explain Virtual DOM and the Reconciliation (Diffing Algorithm) in React. Why is it faster than direct real DOM manipulation?",
  "level": "Fresher / Junior",
  "key_concepts": [
    "Virtual DOM tree representation",
    "Batching updates",
    "Heuristic O(n) diffing",
    "Keys in lists"
  ],
  "expected_answer": "Virtual DOM là một đại diện ảo dạng JavaScript Object nhẹ của Real DOM. Khi state thay đổi, React tạo cây Virtual DOM mới, so sánh với cây trước đó (Diffing Algorithm theo 2 giả định: 2 phần tử khác kiểu tạo cây khác nhau; dùng 'key' để ổn định danh sách) và chỉ cập nhật những phần tử thực sự thay đổi lên Real DOM trong commit phase thay vì re-render toàn trang.",
  "scoring_rubric": {
    "poor": "Chỉ nói Virtual DOM nhanh hơn DOM thật nhưng không giải thích được cơ chế diffing hay batching.",
    "acceptable": "Nêu được khái niệm Virtual DOM, so sánh trước sau và cập nhật phần thay đổi.",
    "excellent": "Giải thích tường tận Diffing Algorithm (O(n) heuristic), vai trò sống còn của `key` prop, Render phase vs Commit phase."
  },
  "citation_url": "https://github.com/sudheerj/reactjs-interview-questions#reconciliation-diffing-algorithm"
}
```

### 3.9. Cấu trúc `behavioral_questions` (Câu hỏi hành vi chuẩn STAR)
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

## 4. Danh Sách 16 Vị Trí Công Nghệ Hiện Có
1. `IF_FE`: Frontend Developer (React / JavaScript / TypeScript)
2. `IF_JAVA`: Backend Developer (Java / Spring Boot / Microservices)
3. `IF_PY`: Python Developer (Django / FastAPI / Python Backend)
4. `IF_NET`: .NET Developer (C# / ASP.NET Core / Entity Framework)
5. `IF_QA`: Software QA & Automation Test Engineer (Manual & Automation)
6. `IF_DEVOPS`: DevOps & Cloud Engineer (Docker / Kubernetes / AWS / CI/CD)
7. `IF_AI`: AI & Machine Learning Engineer (Deep Learning / NLP / Computer Vision)
8. `IF_DATA`: Data Scientist & Data Engineer (SQL / ETL / Data Warehousing)
9. `IF_SEC`: Cyber Security & SOC Analyst (Network Security / Pentest)
10. `IF_SEMI`: Semiconductor & IC Design Engineer (Verilog / RTL / FPGA / ASIC)
11. `IF_AUTO`: Embedded Automotive Software Engineer (AUTOSAR / Embedded C / CAN bus)
12. `IF_BA`: IT Business Analyst (Requirements / Agile / UML / BPMN)
13. `IF_ROBOT`: Robotics & Autonomous Systems Engineer (ROS / C++ / Control / SLAM)
14. `IF_UIUX`: UI/UX Designer & Product Designer (Figma / Usability Heuristics)
15. `IF_CHAIN`: Blockchain & Web3 Developer (Solidity / Smart Contracts / Ethereum)
16. `IF_SYS`: Systems & IT Infrastructure Engineer (Linux / Windows Server / Networking)

---

## 5. Giá Trị & Vai Trò Trong Quy Trình Mock Interview
1. **Orchestrator Blueprint (Kế hoạch kịch bản tổng thể):** Cung cấp cấu trúc tuần tự từng vòng thi, đảm bảo AI không hỏi lộn xộn mà phỏng vấn đúng theo thời gian và trọng tâm (Stage 1 -> Stage 2 -> Stage 3).
2. **Ground Truth & Answer Key (Đáp án và barem chấm điểm khách quan):** Cung cấp `expected_answer` và tiêu chuẩn 3 mức `poor` / `acceptable` / `excellent` để AI đánh giá câu trả lời của ứng viên chính xác, công bằng, hạn chế hiện tượng LLM hallucination.
3. **STAR Evaluation Guide:** Đưa ra các chỉ dấu hành vi tích cực (`action_positive`) và tiêu cực (`action_negative`) để người chấm biết ứng viên có kỹ năng làm việc nhóm và giải quyết vấn đề thực tế hay không.

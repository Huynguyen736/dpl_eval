# Báo Cáo Phân Tích Khám Phá Dữ Liệu (EDA Report) - Dự Án Evaludate

> Báo cáo phân tích chuyên sâu 3 tập dữ liệu: `candidates.json`, `jobs_below_mid.json`, và `interview_frameworks.json` phục vụ thiết kế pipeline Ingestion, Persistence, Retrieval và Ragas Benchmark.

## 1. Phân Tích Dữ Liệu Ứng Viên (`candidates.json`)
- **Tổng số ứng viên mẫu:** 300
### 1.1. Phân bố cấp bậc (Levels):
  - `Fresher`: 185 (61.7%)
  - `Mid-level`: 40 (13.3%)
  - `Junior`: 38 (12.7%)
  - `Intern`: 35 (11.7%)
  - `Senior`: 2 (0.7%)

### 1.2. Phân bố 16 nhóm chuyên môn (`category`):
  - **React Developer**: 20 hồ sơ
  - **Web Designing**: 20 hồ sơ
  - **Java Developer**: 20 hồ sơ
  - **Python Developer**: 20 hồ sơ
  - **DotNet Developer**: 20 hồ sơ
  - **Data Science**: 20 hồ sơ
  - **Testing**: 20 hồ sơ
  - **Automation Testing**: 20 hồ sơ
  - **Database**: 20 hồ sơ
  - **ETL Developer**: 20 hồ sơ
  - **Network Security Engineer**: 20 hồ sơ
  - **Blockchain**: 20 hồ sơ
  - **Business Analyst**: 20 hồ sơ
  - **Information Technology**: 20 hồ sơ
  - **DevOps**: 17 hồ sơ
  - **DevOps Engineer**: 3 hồ sơ

### 1.3. Thống kê tỷ lệ khuyết dữ liệu (Missing Rates):
  - `email`: Khuyết 142/300 (47.3%)
  - `phone`: Khuyết 137/300 (45.7%)
  - `location`: Khuyết 75/300 (25.0%)
  - `github`: Khuyết 293/300 (97.7%)
  - `linkedin`: Khuyết 267/300 (89.0%)

### 1.4. Số năm kinh nghiệm (`years_of_experience`):
  - Trung bình: `1.44` năm (Thấp nhất: `0.0`, Cao nhất: `6.0` năm)

### 1.5. Top 20 Kỹ năng kỹ thuật phổ biến nhất của ứng viên:
  `SQL` (183), `Git` (132), `JavaScript` (100), `Linux` (90), `HTML` (89), `Java` (88), `Agile` (88), `Python` (87), `CSS` (75), `MySQL` (69), `Oracle` (67), `JIRA` (61), `Scrum` (47), `AWS` (44), `RESTful API` (42), `Docker` (38), `Selenium` (36), `Jenkins` (33), `PostgreSQL` (32), `Machine Learning` (31)

## 2. Phân Tích Dữ Liệu Việc Làm (`jobs_below_mid.json`)
- **Tổng số bài đăng tuyển dụng (JDs):** 395
### 2.1. Phân bố cấp bậc tuyển dụng (`levels`):
  - `Junior`: 211 (53.4%)
  - `Fresher`: 129 (32.7%)
  - `Intern`: 28 (7.1%)
  - `Fresher, Junior`: 14 (3.5%)
  - `Fresher, Intern`: 13 (3.3%)

### 2.2. Phân bố nhóm ngành (`job_family`):
  - **Software Engineering (Full-Stack)**: 186 việc làm (47.1%)
  - **Quality Assurance & Testing**: 66 việc làm (16.7%)
  - **Artificial Intelligence & Machine Learning**: 26 việc làm (6.6%)
  - **Data Science & Big Data**: 26 việc làm (6.6%)
  - **Embedded Systems & Hardware**: 18 việc làm (4.6%)
  - **Product & Business Analysis**: 18 việc làm (4.6%)
  - **Software Engineering (Backend)**: 17 việc làm (4.3%)
  - **Software Engineering (Frontend)**: 10 việc làm (2.5%)
  - **Mobile Application Development**: 9 việc làm (2.3%)
  - **Cloud & DevOps**: 9 việc làm (2.3%)

### 2.3. Phân bố miền nghiệp vụ (`domain`):
  - **Technology & Software Services**: 199 việc làm (50.4%)
  - **Banking, Financial Services & Insurance (BFSI)**: 71 việc làm (18.0%)
  - **Automotive, IoT & Telecommunications**: 51 việc làm (12.9%)
  - **Enterprise Automation & Smart Manufacturing**: 32 việc làm (8.1%)
  - **Gaming & Digital Entertainment**: 14 việc làm (3.5%)
  - **E-commerce & SaaS Platforms**: 9 việc làm (2.3%)
  - **Hospitality & Services**: 8 việc làm (2.0%)
  - **Food & Beverage / Retail**: 6 việc làm (1.5%)
  - **Software Services & IT Consulting**: 5 việc làm (1.3%)

### 2.4. Yêu cầu kinh nghiệm tối thiểu:
  - Số tin nêu rõ số năm tối thiểu: 395/395 (100.0%)
  - Phân bố: {2: 114, 0: 164, 1: 104, 0.5: 1, 10: 1, 3: 9, 5: 1, 4: 1}

### 2.5. Top 20 Kỹ năng kỹ thuật nhà tuyển dụng đòi hỏi nhiều nhất:
  `SQL` (122), `Python` (89), `CNTT / Kỹ thuật phần mềm` (78), `Machine Learning` (73), `Java` (64), `JavaScript` (52), `Git / GitFlow` (49), `C/C++` (46), `Agile / Scrum` (43), `REST/gRPC` (42), `CAN / LIN Protocols` (41), `C# / .NET` (38), `Embedded Systems` (34), `Linux` (33), `LLM / GenAI` (33), `Docker` (32), `CI/CD` (30), `Data Analytics / BI` (30), `ReactJS` (28), `Business Analysis (BA)` (27)

## 3. Phân Tích Khung Phỏng Vấn Chuẩn (`interview_frameworks.json`)
- **Tổng số vị trí có framework chuẩn:** 25
- **Tổng số câu hỏi kỹ thuật chuẩn hóa:** 350 câu (Trung bình 14.0 câu/vị trí)
- **Tổng số câu hỏi hành vi STAR:** 75 câu (Trung bình 3.0 câu/vị trí)

### 3.1. Danh mục 25 vị trí và quy mô câu hỏi:
| Position ID | Tên Vị Trí (Role Title) | Số Câu Kỹ Thuật | Số Câu STAR | Số Giai Đoạn (Stages) | Trụ Cột Đánh Giá |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `IF_AI` | AI Engineer (Kỹ sư Trí tuệ nhân tạo) | 18 | 3 | 5 | 4 |
| `IF_AI_SWE` | AI Software Engineer (Kỹ sư Phần mềm AI) | 12 | 3 | 5 | 4 |
| `IF_AGENTIC_AI` | Agentic AI Engineer (Kỹ sư AI Tác tử / AI Agent) | 12 | 3 | 5 | 4 |
| `IF_DA` | Data Analyst (Chuyên viên Phân tích dữ liệu) | 12 | 3 | 5 | 4 |
| `IF_DE` | Data Engineer (Kỹ sư Kỹ thuật dữ liệu) | 18 | 3 | 5 | 4 |
| `IF_DS` | Data Scientist (Nhà Khoa học dữ liệu) | 8 | 3 | 5 | 4 |
| `IF_QA_QC` | Software QA/QC Engineer (Kỹ sư Kiểm thử phần mềm QA/QC) | 18 | 3 | 5 | 4 |
| `IF_AUTO_QA` | Automation QA/QC Engineer (Kỹ sư Kiểm thử tự động) | 12 | 3 | 5 | 4 |
| `IF_FE` | Frontend Developer (Lập trình viên Frontend) | 18 | 3 | 5 | 4 |
| `IF_BE_JAVA` | Backend Developer - Java (Lập trình viên Backend Java) | 18 | 3 | 5 | 4 |
| `IF_BE_NET` | Backend Developer - .NET (Lập trình viên Backend .NET) | 8 | 3 | 5 | 4 |
| `IF_BE_PHP` | Backend Developer - PHP (Lập trình viên Backend PHP) | 12 | 3 | 5 | 4 |
| `IF_BE_GEN` | Backend Developer - Chung (Lập trình viên Backend) | 12 | 3 | 5 | 4 |
| `IF_FULLSTACK` | FullStack Developer (Lập trình viên Fullstack) | 18 | 3 | 5 | 4 |
| `IF_SWE` | Software Engineer (Kỹ sư Phần mềm) | 18 | 3 | 5 | 4 |
| `IF_SWD` | Software Developer (Lập trình viên Phần mềm) | 18 | 3 | 5 | 4 |
| `IF_EMBEDDED` | Embedded Software Engineer (Kỹ sư Phần mềm nhúng) | 18 | 3 | 5 | 4 |
| `IF_BA` | Business Analyst - BA (Chuyên viên Phân tích nghiệp vụ IT) | 12 | 3 | 5 | 4 |
| `IF_DEVOPS` | DevOps Engineer (Kỹ sư Vận hành & Phát triển) | 18 | 3 | 5 | 4 |
| `IF_MOBILE_ANDROID` | Mobile Developer - Android (Lập trình viên Di động Android) | 12 | 3 | 5 | 4 |
| `IF_MOBILE_IOS` | Mobile Developer - iOS (Lập trình viên Di động iOS) | 8 | 3 | 5 | 4 |
| `IF_NETWORK` | Network Engineer (Kỹ sư Quản trị Mạng) | 18 | 3 | 5 | 4 |
| `IF_UNITY` | Unity Game Developer (Lập trình viên Game Unity) | 12 | 3 | 5 | 4 |
| `IF_ERP` | ERP Developer / Consultant (Chuyên viên Tư vấn / Phát triển ERP) | 8 | 3 | 5 | 4 |
| `IF_PRODUCT_ENG` | Product Engineer (Kỹ sư Sản phẩm) | 12 | 3 | 5 | 4 |

## 4. Phân Tích Đối Sánh Liên Tập Dữ Liệu (Cross-Dataset Mapping & Alignment)
### 4.1. Khả năng ánh xạ từ Chức danh JD (`normalized_job_title`) sang Framework:
- Số lượng chức danh chuẩn hóa khác nhau trong 395 JDs: `25` danh hiệu.
  - `Software Engineer` (160 bài) -> `IF_SWE`
  - `Software QA/QC Engineer` (64 bài) -> `IF_QA_QC`
  - `Embedded Software Engineer` (18 bài) -> `IF_SWE`
  - `Business Analyst (BA)` (18 bài) -> `IF_BA`
  - `Data Analyst` (18 bài) -> `IF_DA`
  - `AI Engineer` (16 bài) -> `IF_AI`
  - `FullStack Developer` (15 bài) -> `IF_FULLSTACK`
  - `Backend Developer (Java)` (12 bài) -> `IF_BE_JAVA`
  - `Software Developer` (10 bài) -> `IF_SWD`
  - `Frontend Developer` (10 bài) -> `IF_FE`
  - `DevOps Engineer` (9 bài) -> `IF_DEVOPS`
  - `Data Engineer` (8 bài) -> `IF_DE`
  - `Mobile Developer (Android)` (7 bài) -> `IF_DA`
  - `Network Engineer` (4 bài) -> `IF_NETWORK`
  - `AI Software Engineer` (4 bài) -> `IF_AI`

### 4.2. Độ tương đồng từ vựng kỹ năng (Skill Vocabulary Overlap):
- Tổng số kỹ năng độc nhất của Ứng viên: `119`
- Tổng số kỹ năng độc nhất của Nhà tuyển dụng: `69`
- Số kỹ năng giao thoa chính xác (Exact match): `29` kỹ năng
- Chỉ số tương đồng từ vựng Jaccard: `0.182`
- **Nhận định quan trọng:** Chỉ số Jaccard thấp do sự khác biệt trong cách viết từ vựng (ví dụ: `Node.js` vs `NodeJS` vs `Node`, `C#` vs `C-Sharp`, `React` vs `ReactJS`, `C/C++` vs `C` và `C++`).
  $\Rightarrow$ **Cần xây dựng bộ Skill Synonym Normalizer (Từ điển từ đồng nghĩa chuẩn hóa kỹ năng) trong khâu Preprocessing.**

## 5. Kết Luận & Khuyến Nghị Thiết Kế Kiến Trúc (Architecture Directives)
1. **Về Preprocessing:**
   - Cần có module `SkillNormalizer` với bảng alias tra cứu canonical skill names để tăng độ chính xác khi tính Skill Gap.
   - Bóc tách Framework thành các **Entity Chunks độc lập**: Mỗi câu hỏi (`technical_questions`) kèm theo `expected_answer` và `scoring_rubric` tạo thành 1 đơn vị tri thức hoàn chỉnh.
2. **Về Persistence:**
   - Sử dụng **SQLite** làm cơ sở dữ liệu quan hệ lưu trữ Metadata có cấu trúc: `candidates`, `jobs`, `frameworks`, `stages`, `rubrics` để lọc nhanh (`position_id`, `levels`).
   - Sử dụng **Inverted Index / BM25** trên `skill_requirements` và `key_concepts` để tìm kiếm tài liệu chuẩn xác theo từ khóa công nghệ.
3. **Về Retrieval & Blending:**
   - Chiến thuật tối ưu: **Hierarchical Knowledge-Guided Retrieval**:
     - Bước 1: Hard filter theo Role/Level.
     - Bước 2: So khớp CV vs JD để phát hiện Missing Skills.
     - Bước 3: Truy xuất câu hỏi kỹ thuật xoáy sâu vào các Missing Skills và đồ án chính.
   - Format nạp vào AI context phải dùng cấu trúc XML rõ ràng (`<CANDIDATE_PROFILE>`, `<TARGET_JOB>`, `<SKILL_GAP>`, `<INTERVIEW_BLUEPRINT>`, `<RUBRICS>`) giúp AI không bị nhầm lẫn giữa thông tin ứng viên và barem chấm thi.
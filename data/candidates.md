# Tài Liệu Đặc Tả Dữ Liệu: `candidates.json`

## 1. Tổng Quan Dataset
* **Đường dẫn tệp:** `data/candidates.json`
* **Số lượng bản ghi:** 300 hồ sơ ứng viên (Profiles).
* **Mục đích sử dụng:** Đại diện cho dữ liệu đầu vào chuẩn hóa (Standardized Input Artifacts) sau khi bóc tách từ CV dạng PDF hoặc Form nhập liệu của ứng viên. Dữ liệu này dùng để đối sánh năng lực thực tế của ứng viên với yêu cầu của Job Description (JD) và làm căn cứ cá nhân hóa kịch bản phỏng vấn (phỏng vấn xoáy sâu vào đồ án, kinh nghiệm, lỗ hổng kiến thức hoặc điểm mạnh của ứng viên).
* **Nguồn dữ liệu gốc (`source`):** LiveCareer Resume Corpus, Kaggle UpdatedResumeDataSet,... được làm giàu và chuẩn hóa cấu trúc.

---

## 2. Bảng Mô Tả Chi Tiết Các Trường Dữ Liệu

| Tên trường (Field Name) | Kiểu dữ liệu (Data Type) | Nullable / Missing | Ý nghĩa nghiệp vụ (Business Semantics) | Giá trị mẫu (Sample Value) | Vai trò trong Pipeline Ingestion / Retrieval / Context |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `candidate_id` | `string` | Không (0/300) | Định danh duy nhất của ứng viên trong hệ thống. | `"CV_FE_001"` | Primary Key để index, mapping hồ sơ với phiên phỏng vấn. |
| `full_name` | `string` | Không (0/300) | Họ và tên hiển thị của ứng viên. | `"Glenn D Young"` | Hiển thị trên UI và xưng hô trong prompt phỏng vấn. |
| `email` | `string` hoặc `null` | Có (142/300 null) | Địa chỉ email liên hệ. | `"glennyoung@email.com"` | Định danh tài khoản, thông báo kết quả. |
| `phone` | `string` hoặc `null` | Có (137/300 null) | Số điện thoại liên hệ. | `"925-249-2133"` | Liên lạc / xác thực. |
| `location` | `string` hoặc `null` | Có (75/300 null) | Địa điểm cư trú hoặc làm việc hiện tại. | `"Fredericksburg, VA"` | Đối sánh với địa điểm làm việc (`location`) trong JD. |
| `target_role` | `string` | Không (0/300) | Vị trí công việc mục tiêu mà ứng viên ứng tuyển. | `"Frontend Developer (React / JavaScript)"` | **Trường quan trọng**: Dùng để Semantic Search / Exact Filter tìm `interview_frameworks` và JD phù hợp. |
| `category` | `string` | Không (0/300) | Phân loại mảng chuyên môn công nghệ của ứng viên. | `"React Developer"` | Categorical filter (16 nhóm ngành chính). |
| `years_of_experience` | `float` / `int` | Không (0/300) | Số năm kinh nghiệm làm việc tích lũy (YoE). | `1.0` | Đối sánh với khoảng `experience.min_years` / `max_years` của JD. |
| `current_level` | `string` | Không (0/300) | Cấp bậc năng lực hiện tại của ứng viên (`Intern`, `Fresher`, `Junior`, `Mid-level`, `Senior`). | `"Fresher"` | Xác định thang điểm đánh giá (`passing_thresholds`) và độ khó của câu hỏi. |
| `github` | `string` hoặc `null` | Có (293/300 null) | Đường dẫn tới profile GitHub cá nhân. | `"https://github.com/robfr77"` | Phân tích portfolio code (nếu có scraper / crawler). |
| `linkedin` | `string` hoặc `null` | Có (267/300 null) | Đường dẫn tới hồ sơ LinkedIn. | `"https://linkedin.com/in/glennyoung"` | Bổ trợ xác minh kinh nghiệm thực tế. |
| `education` | `dict` (Object) | Không (0/300) | Thông tin học vấn (trường, chuyên ngành, năm tốt nghiệp, GPA). | Xem mục [3.1](#31-cấu-trúc-education) | Đánh giá nền tảng học thuật, dùng ở Stage 1 (Screening). |
| `technical_skills` | `list[string]` | Không (0/300) | Danh sách kỹ năng công nghệ ứng viên khai báo / có trong CV. | `["React", "Redux", "TypeScript", "Node.js"]` | **Trường cốt lõi**: Tính toán Skill Gap Matrix đối chiếu với `skill_requirements` của JD. |
| `soft_skills` | `list[string]` | Không (0/300) | Danh sách kỹ năng mềm được trích xuất. | `["Problem Solving", "Teamwork"]` | Chọn câu hỏi tình huống hành vi (`behavioral_questions`). |
| `behavioral_traits` | `list[string]` | Không (0/300) | Đặc điểm tính cách làm việc quan sát được. | `["Proactive", "Detail-oriented"]` | Cung cấp ngữ cảnh cho AI để đánh giá độ phù hợp văn hóa kỹ thuật. |
| `languages` | `list[string]` | Không (0/300) | Ngoại ngữ và mức độ thông thạo. | `["English (Professional Working Proficiency)"]` | Đối chiếu với `language_requirements` của JD. |
| `certifications` | `list[string]` | Không (0/300) | Chứng chỉ nghề nghiệp, khóa học đã hoàn thành. | `["Free Code Camp Front End Development Certificate"]` | Kiểm tra điều kiện tiên quyết nếu JD đòi hỏi chứng chỉ. |
| `work_experience` | `list[dict]` | Không (0/300) | Lịch sử công tác (công ty, vị trí, thời gian, trách nhiệm). | Xem mục [3.2](#32-cấu-trúc-work_experience) | **Trường cốt lõi**: Nguồn tạo câu hỏi phỏng vấn trải nghiệm thực tế (Project deep dive). |
| `projects` | `list[dict]` | Không (0/300) | Danh sách đồ án, dự án cá nhân hoặc capstone project. | Xem mục [3.3](#33-cấu-trúc-projects) | Cực kỳ quan trọng với `Intern` / `Fresher` ít kinh nghiệm làm việc chính thức. |
| `career_objective` | `string` | Không (0/300) | Mục tiêu phát triển sự nghiệp ngắn/dài hạn của ứng viên. | `"Recent college graduate seeking..."` | Đánh giá định hướng và độ gắn kết văn hóa ở đầu buổi phỏng vấn. |
| `source` | `string` | Không (0/300) | Nguồn trích xuất bản ghi gốc. | `"LiveCareer Resume Corpus"` | Metadata quản trị dữ liệu. |
| `raw_cv` | `string` | Không (0/300) | Toàn bộ văn bản thô (raw text) trích từ PDF gốc. | `"REACT DEVELOPER\nProfessional Summary\n..."` | Cho phép LLM đọc lại ngữ cảnh gốc nếu các trường bóc tách bị thiếu sót. |

---

## 3. Cấu Trúc Các Trường Dữ Liệu Phức Tạp (Nested Objects)

### 3.1. Cấu trúc `education`
```json
{
  "degree": "Bachelor of Arts: Religion, 2015",
  "institution": "University of Mary Washington - Fredericksburg",
  "graduation_year": 2015,
  "gpa": null,
  "honors": null
}
```
* `degree` (*string*): Tên văn bằng hoặc chuyên ngành tốt nghiệp.
* `institution` (*string*): Tên trường đại học, viện đào tạo hoặc cao đẳng.
* `graduation_year` (*int* hoặc *null*): Năm tốt nghiệp.
* `gpa` (*float*, *string* hoặc *null*): Điểm trung bình tích lũy.
* `honors` (*string* hoặc *null*): Xếp loại tốt nghiệp (e.g. Giỏi, Xuất sắc, Cum Laude).

### 3.2. Cấu trúc `work_experience` (Danh sách các vị trí từng làm)
```json
[
  {
    "company": "Technology Solutions Provider",
    "position": "Frontend Developer (React / JavaScript)",
    "period": "1.0 years",
    "responsibilities": [
      "Engaged in technical design, programming, and testing of software modules.",
      "Collaborated within cross-functional teams adhering to Agile engineering best practices."
    ]
  }
]
```
* `company` (*string*): Tên công ty hoặc tổ chức ứng viên đã làm việc.
* `position` (*string*): Chức danh công việc đảm nhiệm.
* `period` (*string*): Thời gian công tác (dạng khoảng ngày tháng hoặc số năm).
* `responsibilities` (*list[string]*): Chi tiết trách nhiệm và thành tựu đã thực hiện.

### 3.3. Cấu trúc `projects` (Danh sách đồ án / dự án cá nhân)
```json
[
  {
    "name": "E-Commerce Web Application",
    "role": "Frontend Developer",
    "tech_stack": ["React", "Redux", "Tailwind CSS", "Node.js"],
    "description": "Developed a full-stack mock shop with user authentication and payment checkout simulation."
  }
]
```
* `name` (*string*): Tên dự án.
* `role` (*string*): Vai trò của ứng viên trong dự án.
* `tech_stack` (*list[string]*): Các công nghệ, thư viện, framework sử dụng trong dự án.
* `description` (*string*): Mô tả bài toán, quy mô, giải pháp kỹ thuật và kết quả.

---

## 4. Đặc Điểm Phân Phối Dữ Liệu Thực Tế
* **Tỉ lệ cấp bậc (`current_level`):**
  * `Fresher`: 185 hồ sơ (~61.7%)
  * `Mid-level`: 40 hồ sơ (~13.3%)
  * `Junior`: 38 hồ sơ (~12.7%)
  * `Intern`: 35 hồ sơ (~11.7%)
  * `Senior`: 2 hồ sơ (~0.7%)
  *(Đa số tập trung vào nhóm dưới Mid-level, rất khớp với bộ JD `jobs_below_mid.json`)*.
* **16 Nhóm ngành (`category`):** Mỗi nhóm có khoảng 18–20 hồ sơ mẫu, trải dài từ Web, Java, Python, .NET, QA, DevOps, AI, Data đến Embedded, Mobile,...

---

## 5. Giá Trị & Vai Trò Trong Quy Trình Mock Interview
1. **Extraction Target (Đích đến khi parse CV/Form):** Khi người dùng tải lên PDF CV hoặc điền form cá nhân, hệ thống parser (OCR/LLM Information Extraction) sẽ chuyển hóa thành schema chuẩn như `candidates.json`.
2. **Context Tailoring (Cá nhân hóa phỏng vấn):**
   * Nếu ứng viên khai `technical_skills` có `React`, `Redux` nhưng JD đòi hỏi `Next.js`, hệ thống sẽ trích xuất ra câu hỏi kiểm tra tư duy chuyển đổi từ CSR sang SSR.
   * Nếu ứng viên là `Intern` / `Fresher` chưa có nhiều `work_experience`, AI sẽ tự động chuyển trọng tâm phỏng vấn kỹ thuật vào `projects` đồ án tốt nghiệp và kiến thức nền tảng (CS fundamentals).
3. **Behavioral Grounding (Tạo câu hỏi STAR):** Dựa vào `work_experience.responsibilities` và `projects.description`, AI sẽ đặt câu hỏi STAR sát với thực tế dự án của ứng viên thay vì hỏi lý thuyết suông.

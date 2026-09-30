# Tài Liệu Đặc Tả Dữ Liệu: `jobs_below_mid.json`

## 1. Tổng Quan Dataset
* **Đường dẫn tệp:** `data/jobs_below_mid.json`
* **Số lượng bản ghi:** 395 tin tuyển dụng việc làm (Job Descriptions - JDs).
* **Phân khúc mục tiêu:** Các vị trí dưới cấp độ Mid-level (`Intern`, `Fresher`, `Junior`, `Fresher, Junior`) trên thị trường tuyển dụng công nghệ Việt Nam (crawled từ các nền tảng tuyển dụng như VietnamWorks, ITviec, TopCV).
* **Mục đích sử dụng:** Đóng vai trò là **"Thước đo thị trường thực tế" (Real-world Market Grounding)**. Bộ dữ liệu này được dùng để:
  * Trích xuất các tiêu chí tuyển dụng phổ biến nhất của doanh nghiệp công nghệ (Must-have vs. Preferred, Tech Stack theo xu hướng hiện tại).
  * Làm cơ sở để đối sánh năng lực của ứng viên (`candidates.json`) với một JD cụ thể (hoặc một nhóm JD cùng vị trí).
  * Đảm bảo kịch bản phỏng vấn của AI có **"Độ phủ kiến thức theo JD" (JD Knowledge Coverage)**, hỏi đúng những gì nhà tuyển dụng thực sự cần.

---

## 2. Bảng Mô Tả Chi Tiết Các Trường Dữ Liệu

| Tên trường (Field Name) | Kiểu dữ liệu (Data Type) | Nullable / Missing | Ý nghĩa nghiệp vụ (Business Semantics) | Giá trị mẫu (Sample Value) | Vai trò trong Pipeline Ingestion / Retrieval / Context |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `job_id` | `string` | Không (0/395) | Mã định danh duy nhất của tin tuyển dụng. | `"vnw_2105350"` | Primary Key quản lý và tham chiếu tin tuyển dụng. |
| `tên job` | `string` | Không (0/395) | Tiêu đề gốc của bài đăng tuyển dụng trên trang việc làm. | `"Telecom Core Network Engineer (C/C++/Linux)"` | Tìm kiếm full-text, hiển thị giao diện người dùng. |
| `normalized_job_title` | `string` | Không (0/395) | Tên vị trí đã được chuẩn hóa theo quy ước ngành. | `"Network Engineer"`, `"Frontend Developer"` | Khóa đối sánh (Mapping key) với `role_title` trong `interview_frameworks.json`. |
| `company` | `string` | Không (0/395) | Tên công ty/doanh nghiệp đang tuyển dụng. | `"BIP Systems Vietnam Co., Ltd"`, `"FPT Software"` | Cung cấp ngữ cảnh công ty và phong cách văn hóa làm việc. |
| `job_family` | `string` | Không (0/395) | Nhóm ngành nghề kỹ thuật lớn. | `"Software Engineering (Full-Stack)"`, `"Embedded Systems & Hardware"` | Phân loại cấp cao, hỗ trợ indexing phân cấp (Hierarchical Clustering). |
| `domain` | `string` | Không (0/395) | Miền nghiệp vụ / Lĩnh vực hoạt động của doanh nghiệp. | `"Banking, Financial Services & Insurance (BFSI)"`, `"Automotive, IoT & Telecommunications"` | Tạo câu hỏi tình huống nghiệp vụ đặc thù miền (Domain-specific questions). |
| `levels` | `string` | Không (0/395) | Cấp bậc tuyển dụng (`Junior`, `Fresher`, `Intern`, `Fresher, Junior`). | `"Junior"`, `"Fresher"` | Xác định kỳ vọng độ khó của câu hỏi phỏng vấn. |
| `mức lương` | `string` | Không (0/395) | Dải thu nhập hoặc thông tin đãi ngộ lương. | `"Thương lượng"`, `"$ 650-2,200 /tháng"` | Thông tin tham khảo cho phiên đàm phán hoặc tư vấn nghề nghiệp. |
| `skill_requirements` | `list[string]` | Không (0/395) | Danh sách kỹ năng/công nghệ then chốt bắt buộc có. | `["C/C++", "Linux", "Embedded Systems"]` | **Trường cốt lõi**: Tính độ phủ kỹ năng (Coverage check) giữa CV và JD. |
| `experience` | `dict` (Object) | Không (0/395) | Yêu cầu số năm kinh nghiệm chi tiết kèm độ tin cậy. | Xem mục [3.1](#31-cấu-trúc-experience) | Đối chiếu điều kiện năm kinh nghiệm của ứng viên (`years_of_experience`). |
| `education_requirements` | `string` hoặc `null` | Có (129/395 null) | Yêu cầu trình độ học vấn, bằng cấp tối thiểu. | `"Minimum bachelor degree in computer science..."` | Lọc điều kiện sàng lọc ban đầu (Pre-screen filter). |
| `language_requirements` | `string` hoặc `null` | Có (238/395 null) | Yêu cầu về trình độ ngoại ngữ (Tiếng Anh, Tiếng Nhật,...). | `"English: Good communication skills. English CVs only."` | Quyết định ngôn ngữ của buổi phỏng vấn (Việt/Anh/Song ngữ). |
| `must_have_requirements` | `list[string]` | Không (0/395) | Các điều kiện bắt buộc mà ứng viên phải đáp ứng. | Xem mục [3.2](#32-cấu-trúc-must_have_requirements) | **Trọng tâm phỏng vấn kỹ thuật**: AI bắt buộc phải hỏi hết các điểm trong mục này. |
| `preferred_requirements` | `list[string]` | Không (0/395) | Các tiêu chí ưu tiên cộng điểm thêm nếu ứng viên có. | Xem mục [3.3](#33-cấu-trúc-preferred_requirements) | Dùng cho các câu hỏi nâng cao (Advanced probe questions) để phân loại ứng viên giỏi. |
| `soft_skills` | `list[string]` | Không (0/395) | Yêu cầu kỹ năng mềm của nhà tuyển dụng. | `["Giao tiếp", "Làm việc nhóm", "Giải quyết vấn đề"]` | Chọn câu hỏi STAR phù hợp với phẩm chất nhà tuyển dụng mong muốn. |
| `behavioral_traits` | `list[string]` | Không (0/395) | Phẩm chất tác phong, tính cách mong đợi. | `["Chịu trách nhiệm", "Tỉ mỉ", "Cầu tiến"]` | Hướng dẫn AI đánh giá phản xạ ứng xử trong buổi phỏng vấn. |
| `certification_requirements` | `string` hoặc `null` | Có (322/395 null) | Yêu cầu chứng chỉ quốc tế hoặc chuyên ngành. | `"Có chứng chỉ AWS Certified Cloud Practitioner là lợi thế"` | Kiểm tra điều kiện cộng điểm hồ sơ. |
| `portfolio_requirements` | `string` hoặc `null` | Có (371/395 null) | Yêu cầu sản phẩm mẫu, GitHub repo, link dự án. | `"Yêu cầu kèm link GitHub các dự án cá nhân đã làm"` | Đòi hỏi ứng viên giải trình chi tiết về code repo cá nhân. |
| `benefits` | `list[string]` | Không (0/395) | Chế độ phúc lợi của công ty (Bảo hiểm, du lịch, thưởng...). | `["Healthcare Plan", "Travel Opportunities"]` | Ngữ cảnh bổ trợ thông tin tuyển dụng. |
| `location` | `string` | Không (0/395) | Nơi làm việc (Hà Nội, Hồ Chí Minh, Đà Nẵng,...). | `"Hà Nội"`, `"Hồ Chí Minh"` | Địa phương hóa thông tin tuyển dụng. |
| `work_mode` | `string` | Không (0/395) | Chế độ làm việc (`On-site`, `Hybrid`, `Remote`). | `"On-site"`, `"Hybrid"` | Phù hợp điều kiện làm việc của ứng viên. |
| `employment_type` | `string` | Không (0/395) | Hình thức làm việc (`Full-time`, `Contract`, `Internship`). | `"Full-time (Toàn thời gian)"` | Phân loại tính chất hợp đồng tuyển dụng. |
| `raw job` | `string` | Không (0/395) | Toàn văn bài đăng tuyển dụng gốc trước khi bóc tách. | `"TIÊU ĐỀ: Telecom Core Network...\nCÔNG TY:..."` | Cung cấp tài liệu gốc hoàn chỉnh cho Vector RAG hoặc Prompt Context. |

---

## 3. Cấu Trúc Các Trường Dữ Liệu Phức Tạp (Nested Objects)

### 3.1. Cấu trúc `experience`
```json
{
  "min_years": 2,
  "max_years": null,
  "raw_text": "Yêu cầu 2 năm kinh nghiệm (Theo thông tin tuyển dụng)",
  "confidence": 0.9
}
```
* `min_years` (*int* hoặc *null*): Số năm kinh nghiệm tối thiểu yêu cầu.
* `max_years` (*int* hoặc *null*): Giới hạn số năm kinh nghiệm tối đa (thường có ở các tin tuyển dụng Intern/Fresher để tránh Overqualified).
* `raw_text` (*string*): Chuỗi ký tự gốc trích xuất từ phần mô tả yêu cầu.
* `confidence` (*float*): Độ tin cậy của thuật toán bóc tách thông tin (từ 0.0 đến 1.0).

### 3.2. Cấu trúc `must_have_requirements` (Yêu cầu bắt buộc)
Dạng mảng chuỗi (`list[string]`), mỗi phần tử là một yêu cầu kỹ thuật hoặc kỹ năng cốt lõi:
```json
[
  "Experience: 2+ years of professional C/C++ language development experience.",
  "Design Skills: Experience creating or thoroughly interpreting Basic/Detailed design documents.",
  "Methodology: Ability to strictly follow internal coding standards and structured processes."
]
```

### 3.3. Cấu trúc `preferred_requirements` (Yêu cầu ưu tiên / Lợi thế)
Dạng mảng chuỗi (`list[string]`), mô tả các điểm cộng:
```json
[
  "Ưu tiên ứng viên có kinh nghiệm về vận hành máy tiện phay CNC hoặc lập trình cơ khí chính xác.",
  "Có kinh nghiệm làm việc với giao thức truyền thông mạng viễn thông (Core Network Protocols)."
]
```

---

## 4. Đặc Điểm Phân Bố Dữ Liệu Thực Tế
* **Phân bố Cấp bậc (`levels`):**
  * `Junior`: 211 việc làm (~53.4%)
  * `Fresher`: 129 việc làm (~32.7%)
  * `Intern`: 28 việc làm (~7.1%)
  * `Fresher, Junior`: 14 việc làm (~3.5%)
  * `Fresher, Intern`: 13 việc làm (~3.3%)
* **Top Nhóm Ngành (`job_family`):**
  * `Software Engineering (Full-Stack / Backend / Frontend)`: >210 việc làm
  * `Quality Assurance & Testing`: 66 việc làm
  * `Artificial Intelligence & Machine Learning`: 26 việc làm
  * `Data Science & Big Data`: 26 việc làm
  * `Embedded Systems & Hardware`: 18 việc làm
  * `Product & Business Analysis`: 18 việc làm
* **Top Lĩnh Vực Doanh Nghiệp (`domain`):**
  * `Technology & Software Services`: 199 việc làm (~50.4%)
  * `Banking, Financial Services & Insurance (BFSI)`: 71 việc làm (~18.0%)
  * `Automotive, IoT & Telecommunications`: 51 việc làm (~12.9%)
  * `Enterprise Automation & Smart Manufacturing`: 32 việc làm (~8.1%)
  * `Gaming & Digital Entertainment`: 14 việc làm (~3.5%)

---

## 5. Giá Trị & Vai Trò Trong Quy Trình Mock Interview
1. **JD Dynamic Parsing & Ingestion Target:** Khi người dùng dán text JD hoặc tải file JD lên, hệ thống sẽ parse nội dung đầu vào này theo đúng cấu trúc của `jobs_below_mid.json`.
2. **Knowledge Coverage Planning (Bảo đảm độ phủ kiến thức):**
   * AI Interviewer sẽ lập danh sách kiểm tra (Interview Agenda) dựa trên `must_have_requirements` và `skill_requirements`.
   * Thứ tự câu hỏi sẽ ưu tiên phủ hết các `must_have_requirements` trước, sau đó nếu ứng viên hoàn thành tốt mới mở rộng sang `preferred_requirements`.
3. **Retrieval Anchor (Điểm neo để truy xuất Framework):**
   * Dựa vào `normalized_job_title` và `levels` của JD, hệ thống truy xuất đúng `position_id` trong `interview_frameworks.json`.
   * Ví dụ: JD có `normalized_job_title = "Frontend Developer"` -> Truy xuất framework `IF_FE`, lấy bộ `interview_stages`, `evaluation_matrix`, và các câu hỏi kỹ thuật tương ứng để nạp vào prompt context.

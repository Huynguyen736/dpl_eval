"""
Exploratory Data Analysis (EDA) Script for Evaludate Knowledge Base.
Analyzes:
1. Candidates dataset (300 records)
2. Jobs below mid dataset (395 records)
3. Interview frameworks dataset (16 records)
4. Cross-dataset mapping & skill overlap
Outputs a structured analysis report to eda/eda_report.md
"""

import os
import json
from collections import Counter
from typing import Dict, List, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
OUTPUT_REPORT = os.path.join(os.path.dirname(__file__), "eda_report.md")

def load_json(filename: str) -> Any:
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_eda():
    candidates = load_json("candidates.json")
    jobs = load_json("jobs_below_mid.json")
    frameworks = load_json("interview_frameworks.json")

    report = []
    report.append("# Báo Cáo Phân Tích Khám Phá Dữ Liệu (EDA Report) - Dự Án Evaludate\n")
    report.append("> Báo cáo phân tích chuyên sâu 3 tập dữ liệu: `candidates.json`, `jobs_below_mid.json`, và `interview_frameworks.json` phục vụ thiết kế pipeline Ingestion, Persistence, Retrieval và Ragas Benchmark.\n")

    # =========================================================================
    # 1. CANDIDATES DATASET ANALYSIS
    # =========================================================================
    report.append("## 1. Phân Tích Dữ Liệu Ứng Viên (`candidates.json`)")
    report.append(f"- **Tổng số ứng viên mẫu:** {len(candidates)}")
    
    cand_levels = Counter(c.get("current_level") for c in candidates)
    report.append("### 1.1. Phân bố cấp bậc (Levels):")
    for lvl, count in cand_levels.most_common():
        report.append(f"  - `{lvl}`: {count} ({count/len(candidates)*100:.1f}%)")

    cand_categories = Counter(c.get("category") for c in candidates)
    report.append("\n### 1.2. Phân bố 16 nhóm chuyên môn (`category`):")
    for cat, count in cand_categories.most_common():
        report.append(f"  - **{cat}**: {count} hồ sơ")

    # Missing value rates
    report.append("\n### 1.3. Thống kê tỷ lệ khuyết dữ liệu (Missing Rates):")
    missing_fields = ["email", "phone", "location", "github", "linkedin"]
    for field in missing_fields:
        null_cnt = sum(1 for c in candidates if c.get(field) is None)
        report.append(f"  - `{field}`: Khuyết {null_cnt}/{len(candidates)} ({null_cnt/len(candidates)*100:.1f}%)")

    # Experience distribution
    yoe_list = [c.get("years_of_experience", 0) for c in candidates]
    avg_yoe = sum(yoe_list) / len(yoe_list)
    min_yoe, max_yoe = min(yoe_list), max(yoe_list)
    report.append(f"\n### 1.4. Số năm kinh nghiệm (`years_of_experience`):")
    report.append(f"  - Trung bình: `{avg_yoe:.2f}` năm (Thấp nhất: `{min_yoe}`, Cao nhất: `{max_yoe}` năm)")

    # Top technical skills
    all_cand_skills = [s.strip() for c in candidates for s in c.get("technical_skills", []) if s]
    top_cand_skills = Counter(all_cand_skills).most_common(20)
    report.append("\n### 1.5. Top 20 Kỹ năng kỹ thuật phổ biến nhất của ứng viên:")
    skill_str = ", ".join([f"`{s}` ({cnt})" for s, cnt in top_cand_skills])
    report.append(f"  {skill_str}\n")

    # =========================================================================
    # 2. JOBS DATASET ANALYSIS
    # =========================================================================
    report.append("## 2. Phân Tích Dữ Liệu Việc Làm (`jobs_below_mid.json`)")
    report.append(f"- **Tổng số bài đăng tuyển dụng (JDs):** {len(jobs)}")

    job_levels = Counter(j.get("levels") for j in jobs)
    report.append("### 2.1. Phân bố cấp bậc tuyển dụng (`levels`):")
    for lvl, count in job_levels.most_common():
        report.append(f"  - `{lvl}`: {count} ({count/len(jobs)*100:.1f}%)")

    job_families = Counter(j.get("job_family") for j in jobs)
    report.append("\n### 2.2. Phân bố nhóm ngành (`job_family`):")
    for fam, count in job_families.most_common(10):
        report.append(f"  - **{fam}**: {count} việc làm ({count/len(jobs)*100:.1f}%)")

    domains = Counter(j.get("domain") for j in jobs)
    report.append("\n### 2.3. Phân bố miền nghiệp vụ (`domain`):")
    for dom, count in domains.most_common():
        report.append(f"  - **{dom}**: {count} việc làm ({count/len(jobs)*100:.1f}%)")

    # Experience requirements
    exp_mins = [j["experience"]["min_years"] for j in jobs if j.get("experience") and j["experience"].get("min_years") is not None]
    report.append(f"\n### 2.4. Yêu cầu kinh nghiệm tối thiểu:")
    report.append(f"  - Số tin nêu rõ số năm tối thiểu: {len(exp_mins)}/{len(jobs)} ({len(exp_mins)/len(jobs)*100:.1f}%)")
    if exp_mins:
        report.append(f"  - Phân bố: {dict(Counter(exp_mins))}")

    # Top required skills
    all_job_skills = [s.strip() for j in jobs for s in j.get("skill_requirements", []) if s]
    top_job_skills = Counter(all_job_skills).most_common(20)
    report.append("\n### 2.5. Top 20 Kỹ năng kỹ thuật nhà tuyển dụng đòi hỏi nhiều nhất:")
    job_skill_str = ", ".join([f"`{s}` ({cnt})" for s, cnt in top_job_skills])
    report.append(f"  {job_skill_str}\n")

    # =========================================================================
    # 3. INTERVIEW FRAMEWORKS DATASET ANALYSIS
    # =========================================================================
    report.append("## 3. Phân Tích Khung Phỏng Vấn Chuẩn (`interview_frameworks.json`)")
    report.append(f"- **Tổng số vị trí có framework chuẩn:** {len(frameworks)}")
    
    total_tech_q = sum(len(f.get("technical_questions", [])) for f in frameworks)
    total_star_q = sum(len(f.get("behavioral_questions", [])) for f in frameworks)
    report.append(f"- **Tổng số câu hỏi kỹ thuật chuẩn hóa:** {total_tech_q} câu (Trung bình {total_tech_q/len(frameworks):.1f} câu/vị trí)")
    report.append(f"- **Tổng số câu hỏi hành vi STAR:** {total_star_q} câu (Trung bình {total_star_q/len(frameworks):.1f} câu/vị trí)")

    report.append(f"\n### 3.1. Danh mục {len(frameworks)} vị trí và quy mô câu hỏi:")
    report.append("| Position ID | Tên Vị Trí (Role Title) | Số Câu Kỹ Thuật | Số Câu STAR | Số Giai Đoạn (Stages) | Trụ Cột Đánh Giá |")
    report.append("| :--- | :--- | :---: | :---: | :---: | :---: |")
    for fw in frameworks:
        pid = fw.get("position_id")
        title = fw.get("role_title")
        t_cnt = len(fw.get("technical_questions", []))
        s_cnt = len(fw.get("behavioral_questions", []))
        stg_cnt = len(fw.get("interview_stages", []))
        mat_cnt = len(fw.get("evaluation_matrix", []))
        report.append(f"| `{pid}` | {title} | {t_cnt} | {s_cnt} | {stg_cnt} | {mat_cnt} |")

    # =========================================================================
    # 4. CROSS-DATASET MAPPING & SKILL OVERLAP
    # =========================================================================
    report.append("\n## 4. Phân Tích Đối Sánh Liên Tập Dữ Liệu (Cross-Dataset Mapping & Alignment)")

    # Mapping Normalized Job Title to Framework Role
    fw_positions = {fw["position_id"]: fw["role_title"] for fw in frameworks}
    job_titles = Counter(j.get("normalized_job_title") for j in jobs)
    report.append("### 4.1. Khả năng ánh xạ từ Chức danh JD (`normalized_job_title`) sang Framework:")
    report.append(f"- Số lượng chức danh chuẩn hóa khác nhau trong 395 JDs: `{len(job_titles)}` danh hiệu.")
    
    # Check simple keyword overlap between job title and framework titles
    mapped_count = 0
    mapping_sample = []
    for jt, cnt in job_titles.most_common(15):
        # find matching framework
        matched_fw = None
        jt_lower = jt.lower()
        for pid, title in fw_positions.items():
            if any(w in jt_lower for w in ["frontend", "react", "web"]) and pid == "IF_FE":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["backend", "java"]) and pid == "IF_BE_JAVA":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["python", "django", "fastapi"]) and pid == "IF_BE_GEN":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in [".net", "c#", "dotnet"]) and pid == "IF_BE_NET":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["automation test", "automation qc"]) and pid == "IF_AUTO_QA":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["qa", "test", "tester", "qc"]) and pid == "IF_QA_QC":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["devops", "cloud", "sre"]) and pid == "IF_DEVOPS":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["ai", "machine learning", "ml", "nlp", "vision"]) and pid == "IF_AI":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["data engineer", "etl", "database", "dba"]) and pid == "IF_DE":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["data analyst", "bi"]) and pid == "IF_DA":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["data science", "data scientist"]) and pid == "IF_DS":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["embedded", "automotive", "autosar"]) and pid == "IF_EMBEDDED":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["business analyst", "ba"]) and pid == "IF_BA":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["system", "network", "infrastructure"]) and pid == "IF_NETWORK":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["fullstack", "full-stack"]) and pid == "IF_FULLSTACK":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["software engineer"]) and pid == "IF_SWE":
                matched_fw = pid
                break
            elif any(w in jt_lower for w in ["developer", "lập trình"]) and pid == "IF_SWD":
                matched_fw = pid
                break
        
        status = f"-> `{matched_fw}`" if matched_fw else "-> *(Cần fallback/semantic search)*"
        mapping_sample.append(f"  - `{jt}` ({cnt} bài) {status}")

    report.extend(mapping_sample)

    # Skill overlap between Candidate profile and JD requirements
    cand_skill_set = set(s.lower() for s in all_cand_skills)
    job_skill_set = set(s.lower() for s in all_job_skills)
    intersection = cand_skill_set.intersection(job_skill_set)
    jaccard = len(intersection) / len(cand_skill_set.union(job_skill_set)) if cand_skill_set.union(job_skill_set) else 0

    report.append(f"\n### 4.2. Độ tương đồng từ vựng kỹ năng (Skill Vocabulary Overlap):")
    report.append(f"- Tổng số kỹ năng độc nhất của Ứng viên: `{len(cand_skill_set)}`")
    report.append(f"- Tổng số kỹ năng độc nhất của Nhà tuyển dụng: `{len(job_skill_set)}`")
    report.append(f"- Số kỹ năng giao thoa chính xác (Exact match): `{len(intersection)}` kỹ năng")
    report.append(f"- Chỉ số tương đồng từ vựng Jaccard: `{jaccard:.3f}`")
    report.append(f"- **Nhận định quan trọng:** Chỉ số Jaccard thấp do sự khác biệt trong cách viết từ vựng (ví dụ: `Node.js` vs `NodeJS` vs `Node`, `C#` vs `C-Sharp`, `React` vs `ReactJS`, `C/C++` vs `C` và `C++`).")
    report.append(r"  $\Rightarrow$ **Cần xây dựng bộ Skill Synonym Normalizer (Từ điển từ đồng nghĩa chuẩn hóa kỹ năng) trong khâu Preprocessing.**")

    # =========================================================================
    # 5. KEY TAKEAWAYS FOR INGESTION & RETRIEVAL
    # =========================================================================
    report.append("\n## 5. Kết Luận & Khuyến Nghị Thiết Kế Kiến Trúc (Architecture Directives)")
    report.append("1. **Về Preprocessing:**")
    report.append("   - Cần có module `SkillNormalizer` với bảng alias tra cứu canonical skill names để tăng độ chính xác khi tính Skill Gap.")
    report.append("   - Bóc tách Framework thành các **Entity Chunks độc lập**: Mỗi câu hỏi (`technical_questions`) kèm theo `expected_answer` và `scoring_rubric` tạo thành 1 đơn vị tri thức hoàn chỉnh.")
    report.append("2. **Về Persistence:**")
    report.append("   - Sử dụng **SQLite** làm cơ sở dữ liệu quan hệ lưu trữ Metadata có cấu trúc: `candidates`, `jobs`, `frameworks`, `stages`, `rubrics` để lọc nhanh (`position_id`, `levels`).")
    report.append("   - Sử dụng **Inverted Index / BM25** trên `skill_requirements` và `key_concepts` để tìm kiếm tài liệu chuẩn xác theo từ khóa công nghệ.")
    report.append("3. **Về Retrieval & Blending:**")
    report.append("   - Chiến thuật tối ưu: **Hierarchical Knowledge-Guided Retrieval**:")
    report.append("     - Bước 1: Hard filter theo Role/Level.")
    report.append("     - Bước 2: So khớp CV vs JD để phát hiện Missing Skills.")
    report.append("     - Bước 3: Truy xuất câu hỏi kỹ thuật xoáy sâu vào các Missing Skills và đồ án chính.")
    report.append("   - Format nạp vào AI context phải dùng cấu trúc XML rõ ràng (`<CANDIDATE_PROFILE>`, `<TARGET_JOB>`, `<SKILL_GAP>`, `<INTERVIEW_BLUEPRINT>`, `<RUBRICS>`) giúp AI không bị nhầm lẫn giữa thông tin ứng viên và barem chấm thi.")

    output_text = "\n".join(report)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"EDA Report generated successfully at: {OUTPUT_REPORT}")

if __name__ == "__main__":
    run_eda()

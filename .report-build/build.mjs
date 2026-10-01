import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation, PresentationFile} from '@oai/artifact-tool';
process.env.RUNTIME_NODE_MODULES='C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const base='C:/Users/Admin/NNH/Projects/VScode/evaludate/.report-build';
const skill='C:/Users/Admin/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.11814/skills/presentations';
const {finalizePresentation}=await import(pathToFileURL(skill+'/container_tools/artifact_tool_utils.mjs'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const blue='#1635FF',ink='#14192F',muted='#566078',pale='#EDF0FF',yellow='#FFF293';
function shape(s,x,y,w,h,fill,geom='rect'){return s.shapes.add({geometry:geom,position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}})}
function text(s,t,x,y,w,h,size=25,color=ink,bold=false){const a=shape(s,x,y,w,h,'none','textbox');a.text=t;a.text.style={typeface:'Arial',fontSize:size,color,bold,autoFit:'none'};return a}
function slide(title,active,page){const s=p.slides.add();s.background.fill='#FFFFFF';['Tổng quan','Thu thập','EDA','Đánh giá'].forEach((t,i)=>{const x=40+i*152;if(i===active)shape(s,x,20,140,34,blue,'roundRect');text(s,t,x+12,24,128,28,19,i===active?'#FFFFFF':muted,i===active)});shape(s,0,68,1280,62,blue);text(s,title,40,78,1200,50,34,'#FFFFFF',true);text(s,String(page).padStart(2,'0'),1183,675,60,25,17,blue,true);return s}
function foot(s,t){text(s,t,40,676,1120,25,14,muted)}
function table(s,values,x,y,width,height,widths,highlight=-1){const tb=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width,height,columnWidths:widths,values});tb.borders.assign({fill:'#FFFFFF',width:2});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const z=tb.getCell(r,c);z.fill=r===0?blue:r===highlight?yellow:r%2?pale:'#F8F9FD';z.text.style={typeface:'Arial',fontSize:r===0?23:25,color:r===0?'#FFFFFF':ink,bold:r===0||r===highlight};}return tb}
let s=slide('Ngữ cảnh cho AI phỏng vấn kỹ thuật',0,1);
text(s,'Bài toán',40,151,160,34,25,blue,true);text(s,'Câu hỏi chung chung, lệch JD/cấp độ, thiếu tiêu chí chấm',204,150,1030,42,27,ink);
const xs=[40,466,886],ws=[350,344,354];
[['ĐẦU VÀO','Hồ sơ ứng viên đã chuẩn hóa','Kỹ năng, dự án, kinh nghiệm\nJD, vị trí và cấp độ mục tiêu'],['XỬ LÝ','Chọn đúng kiến thức cần hỏi','Chuẩn hóa kỹ năng\nKhớp vị trí và skill gap\nChọn câu hỏi và rubric'],['ĐẦU RA','Context XML cho AI phỏng vấn','3 câu kỹ thuật + 1 câu STAR\nĐáp án, rubric, các chặng hỏi\nMốc chấm điểm 1–5']].forEach((a,i)=>{text(s,a[0],xs[i],227,ws[i],30,20,blue,true);shape(s,xs[i],266,ws[i],3,blue);text(s,a[1],xs[i],284,ws[i],70,28,ink,true);text(s,a[2],xs[i],366,ws[i],135,25)});
shape(s,409,327,36,25,blue,'rightArrow');shape(s,830,327,36,25,blue,'rightArrow');
shape(s,40,528,1200,98,pale);[['300','CV'],['395','JD'],['25','framework'],['350','câu hỏi kỹ thuật']].forEach((a,i)=>{text(s,a[0],62+i*297,539,250,46,36,blue,true);text(s,a[1],62+i*297,584,260,32,23)});
text(s,'Phạm vi: prototype truy xuất ngữ cảnh. AI thực hiện buổi phỏng vấn ở bước sau.',40,639,1190,30,21,muted);
foot(s,'Nguồn: dữ liệu project evaludate và pipeline tạo context');
s.speakerNotes.textFrame.setText('Nguồn trong repository C:/Users/Admin/NNH/Projects/VScode/evaludate: data/*.json và pipeline src/. Số liệu do audit repository xác nhận: 300 CV, 395 JD, 25 frameworks, 350 technical questions. Input là profile có cấu trúc đã chuẩn hóa, không khẳng định đã triển khai parser PDF. Output là context XML chứa bộ câu hỏi, rubric và interview stages để AI interviewer downstream sử dụng. 350 chỉ đếm câu hỏi kỹ thuật.');
s=slide('EDA định hướng lưu trữ và truy xuất',2,3);
text(s,'300 CV, 395 JD và 25 framework cho thấy ba điểm cần xử lý',40,149,1200,40,26,ink);
table(s,[['Bằng chứng từ dữ liệu','Insight','Cách lưu và truy xuất'],['18,2% trùng từ vựng kỹ năng\nCV 119, JD 69, chung 29','Cần đối soát tên và\nnhóm kỹ năng','Chuẩn hóa alias trước\nkhi xác định skill gap'],['350 câu hỏi kỹ thuật\nđều có đáp án + rubric 3 mức','Câu hỏi cần đi cùng\ntiêu chí chấm','Lưu nguyên bộ câu hỏi\nKhóa: vị trí + question_id'],['61,7% CV là Fresher\n53,4% JD là Junior','Phân bố cấp độ lệch nhau\n14% CV ngoài framework','Lọc role, ưu tiên level\nFallback khi thiếu dữ liệu']],40,213,1200,301,[395,370,435]);
text(s,'Lưu trữ hiện tại',40,541,255,33,24,blue,true);text(s,'SQLite + JSON',300,541,274,33,25,ink,true);text(s,'Chỉ mục BM25 và TF-IDF/SVD lưu ra tệp',609,542,631,33,23,ink);
text(s,'CV Fresher',40,596,165,27,20);shape(s,214,602,250,16,pale);shape(s,214,602,154.25,16,blue);text(s,'61,7%',480,596,100,27,20,blue,true);text(s,'JD Junior',40,627,165,27,20);shape(s,214,633,250,16,pale);shape(s,214,633,133.5,16,blue);text(s,'53,4%',480,627,100,27,20,blue,true);shape(s,626,591,614,66,yellow);text(s,'EDA định hướng thiết kế. Benchmark kiểm tra hiệu quả truy xuất.',642,598,585,55,23,ink,true);
foot(s,'Nguồn: data/*.json. Jaccard dùng tên kỹ năng viết thường chính xác, không phải skill gap từng CV.');
s.speakerNotes.textFrame.setText('Nguồn audit dữ liệu repository evaludate/data/*.json. CV có119 tên kỹ năng khác nhau, JD69, giao29; Jaccard29/(119+69-29)=18.23899%. Đây là so khớp exact lowercase và là overlap từ vựng tổng thể, không phải khoảng thiếu kỹ năng của một ứng viên. 185/300CV Fresher=61.7%;211/395JD Junior=53.4%;42/300CV mid/senior=14% nằm ngoài framework. 350technical questions có answer và rubric3mức. question_id cần đi với position_id. Persistence hiện tại SQLite records+JSON, index BM25 cùng TF-IDF/SVD vector files; không phải pretrained neural embedding. EDA là căn cứ thiết kế, chưa chứng minh tối ưu toàn cục.');
s=slide('Benchmark nội bộ: Skill-gap có độ phủ cao nhất',3,4);
text(s,'Pilot: 8 CV React/Fresher × 4 chiến lược = 32 lượt đánh giá, chỉ 3 JD khác nhau',40,151,1200,40,25,ink);
table(s,[['Chiến lược','Độ phủ kỹ năng','Khớp vị trí/cấp độ','Đủ rubric'],['S1  BM25','25,0%','61,7%','40,0%'],['S2  Metadata','30,0%','75,0%','100%'],['S3  Skill-gap','55,0%','95,0%','100%'],['S4  Hybrid RRF','32,5%','95,0%','100%']],40,216,1200,279,[362,280,328,230],3);
text(s,'+22,5 điểm phần trăm',40,518,395,52,32,blue,true);text(s,'độ phủ của S3 so với S4.\nHybrid chưa tốt hơn trên mẫu thử này.',448,515,780,66,26,ink,true);
text(s,'Độ phủ: so chuỗi với 5 kỹ năng JD đầu. Khớp: 60% vị trí + 40% cấp độ.\nĐủ rubric: kiểm tra cấu trúc nội dung.',40,590,1200,53,20,muted);
text(s,'Chỉ số tự xây dựng, chưa phải Ragas chuẩn hoặc đánh giá phỏng vấn đầu cuối.',40,650,1195,27,20,ink,true);
foot(s,'Nguồn: batch_evaluation_results.csv và src/evaluation/metrics.py');
s.speakerNotes.textFrame.setText('Nguồn: C:/Users/Admin/NNH/Projects/VScode/evaludate/batch_evaluation_results.csv và src/evaluation/metrics.py. Benchmark pilot8CV React/Fresher×4strategies=32evaluations,3uniqueJD. Custom metrics: coverage S1=.25,S2=.30,S3=.55,S4=.325; alignment .617,.75,.95,.95; rubric .40,1,1,1. S3 coverage exceeds S4 by22.5percentage points. Coverage uses substring presence for first5JD skills; alignment60%role+40%level; rubric is structural. Excludes faithfulness and composite because mixed hardcoded and LLM-derived values. Results are neither standard Ragas evaluation nor end-to-end interview quality. Generalization to all roles/levels is unverified.');
await (await PresentationFile.exportPptx(p)).save(base+'/staging/candidate.pptx');
for(let i=0;i<3;i++){const blob=await p.export({slide:p.slides.items[i],format:'png',scale:1});await fs.writeFile(base+`/staging/slide-${[1,3,4][i]}.png`,new Uint8Array(await blob.arrayBuffer()));}
await finalizePresentation({workspaceDir:base,candidatePath:base+'/staging/candidate.pptx',finalPath:base+'/output/eval-report-slides-v3.pptx',pythonExecutable:'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--require-native-table-slide','2','--require-native-table-slide','3'],explicitTotalSlideCount:3,requiredNativeTableOwnerSlides:[2,3],fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:base+'/staging/validation-v3.json'});
console.log('DONE '+base+'/output/eval-report-slides-v3.pptx');




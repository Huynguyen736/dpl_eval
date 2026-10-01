import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation, PresentationFile} from '@oai/artifact-tool';
process.env.RUNTIME_NODE_MODULES='C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const base='C:/Users/Admin/NNH/Projects/VScode/evaludate/.report-build';
const skill='C:/Users/Admin/.codex/plugins/cache/openai-primary-runtime/presentations/26.905.11957/skills/presentations';
const {finalizePresentation}=await import(pathToFileURL(skill+'/container_tools/artifact_tool_utils.mjs'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const blue='#1635FF',ink='#14192F',muted='#566078',pale='#EDF0FF',yellow='#FFF293';
function shape(s,x,y,w,h,fill,geom='rect'){return s.shapes.add({geometry:geom,position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}})}
function text(s,t,x,y,w,h,size=25,color=ink,bold=false){const a=shape(s,x,y,w,h,'none','textbox');a.text=t;a.text.style={typeface:'Arial',fontSize:size,color,bold,autoFit:'none'};return a}
function slide(title,active,page){const s=p.slides.add();s.background.fill='#FFFFFF';['Tổng quan','Thu thập','EDA','Đánh giá'].forEach((t,i)=>{const x=40+i*152;if(i===active)shape(s,x,20,140,34,blue,'roundRect');text(s,t,x+12,24,128,28,19,i===active?'#FFFFFF':muted,i===active)});shape(s,0,68,1280,62,blue);text(s,title,40,78,1200,50,34,'#FFFFFF',true);text(s,String(page).padStart(2,'0'),1183,675,60,25,17,blue,true);return s}
function foot(s,t){text(s,t,40,676,1120,25,14,muted)}
function table(s,values,x,y,width,height,widths,highlight=-1){const tb=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width,height,columnWidths:widths,values});tb.borders.assign({fill:'#FFFFFF',width:2});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const z=tb.getCell(r,c);z.fill=r===0?blue:r===highlight?yellow:r%2?pale:'#F8F9FD';z.text.style={typeface:'Arial',fontSize:r===0?23:25,color:r===0?'#FFFFFF':ink,bold:r===0||r===highlight};}return tb}
let s=slide('Từ CV đến bộ ngữ cảnh phỏng vấn',0,1);
text(s,'Làm sao chọn câu hỏi đúng với ứng viên và vị trí ứng tuyển?',40,153,1200,45,29,ink,true);
text(s,'INPUT',40,226,300,30,20,blue,true);
text(s,'CV ứng viên',40,274,330,43,32,ink,true);
text(s,'Kỹ năng, dự án, kinh nghiệm\nVị trí, cấp độ, công ty mục tiêu',40,337,350,110,25);
shape(s,408,309,45,25,blue,'rightArrow');
text(s,'CẦN BIẾT THÊM',480,226,335,30,20,blue,true);
text(s,'Vị trí này yêu cầu gì?\nỨng viên còn thiếu gì?\nHỏi gì và chấm thế nào?',480,274,345,167,29,ink,true);
shape(s,837,309,45,25,blue,'rightArrow');
text(s,'OUTPUT',910,226,320,30,20,blue,true);
text(s,'Context cho AI phỏng vấn',910,274,330,85,29,ink,true);
text(s,'Câu hỏi theo CV và JD\nĐáp án, rubric, thang điểm\nCác chặng của buổi phỏng vấn',910,376,332,114,24);
shape(s,40,503,1200,3,blue);
text(s,'Dữ liệu cần thu thập',40,529,335,44,29,blue,true);
text(s,'JD theo vị trí và cấp độ • Khung kiến thức / năng lực\nCâu hỏi kỹ thuật và tình huống STAR • Đáp án, tiêu chí chấm\nVí dụ phỏng vấn theo công ty, nếu tìm được nguồn',396,526,844,120,25);
s.speakerNotes.textFrame.setText('Input pipeline hiện tại là profile có cấu trúc đã chuẩn hóa cùng JD; output là XML context cho AI interviewer. Bộ context chứa câu hỏi kỹ thuật và STAR, expected answers, rubric, interview stages và score anchors. Ví dụ phỏng vấn công ty là nhu cầu thu thập, không khẳng định dữ liệu hiện có đã có nguồn xác thực. Không đưa số lượng dữ liệu trên trang tổng quan.');
s=slide('CV thiên về Fresher, JD thiên về Junior',2,3);
text(s,'Phân bố cấp độ',40,153,540,40,27,ink,true);
text(s,'CV (n = 300)',40,205,230,30,22,blue,true);text(s,'JD (n = 395)',320,205,245,30,22,blue,true);
const levels=['Intern','Fresher','Junior','Mid / Senior'];
const cv=[11.7,61.7,12.7,14],jd=[7.1,32.7,53.4,0];
levels.forEach((l,i)=>{const y=252+i*52;text(s,l,40,y,126,27,19);shape(s,170,y+5,126*cv[i]/65,17,blue);text(s,String(cv[i]).replace('.',',')+'%',170,y+24,126,23,16,blue);shape(s,320,y+5,126*jd[i]/65,17,'#91A0FF');text(s,String(jd[i]).replace('.',',')+'%',320,y+24,126,23,16,muted);});
text(s,'JD có 6,8% nhãn cấp độ kết hợp.',40,475,540,30,18,muted);
text(s,'Lọc vị trí trước, ưu tiên cấp độ.\n42 CV Mid/Senior chưa có framework tương ứng.',40,527,540,78,24,ink,true);
shape(s,597,158,2,475,pale);
text(s,'Tên kỹ năng: chỉ 29 tên trùng nhau',635,153,600,40,27,ink,true);
const segments=[['Chỉ CV',90,blue],['Chung',29,'#91A0FF'],['Chỉ JD',40,'#D8DEFF']];let at=635;
segments.forEach(([l,n,c])=>{const w=600*n/159;shape(s,at,220,w,65,c);text(s,String(n),at+10,234,w-20,35,27,c===blue?'#FFFFFF':ink,true);text(s,l,at,300,w,30,20);at+=w;});
text(s,'119 tên trong CV • 69 tên trong JD',635,349,600,34,23,muted);
text(s,'React ↔ ReactJS\nGit ↔ Git/GitFlow',635,401,600,85,28,ink,true);
text(s,'Chuẩn hóa tên trước khi so kỹ năng CV–JD.',635,510,600,65,25,blue,true);
shape(s,40,617,1200,38,pale);text(s,'SQLite + JSON • Khóa câu hỏi: (position_id, question_id) • Chỉ mục BM25 + TF-IDF/SVD',52,623,1180,30,22);
foot(s,'Nguồn: data/*.json. Kỹ năng so theo tên viết thường; thanh phân bố dùng cùng thang 0–65%.');
s.speakerNotes.textFrame.setText('CV:185Fresher,38Junior,35Intern,40Mid,2Senior trên300. JD:211Junior,129Fresher,28Intern,14Fresher/Junior,13Fresher/Intern trên395. Các thanh có cùng thang0–65%. JD nhãn kết hợp27/395=6.8%. Framework chỉ Intern/Fresher/Junior;42CV Mid/Senior ngoài phạm vi. Tên kỹ năng lowercase:CV119,JD69,giao29;chỉCV90,chỉJD40,union159,Jaccard18.24%. Đây là overlap từ vựng tổng thể không phải skillgap từngCV. Các alias minh họa cần đối soát ngữ nghĩa trước chuẩn hóa. Có350technicalquestions và342question_idunique;composite(position_id,question_id)350unique. SQLite metadata+JSON;BM25 vàTFIDF/SVD64 chiều lưu file.');
s=slide('Skill-gap đạt độ phủ 55% trên mẫu benchmark',3,4);
text(s,'8 CV React/Fresher × 4 chiến lược = 32 lượt • 3 JD khác nhau',40,156,1200,42,26);
table(s,[['Chiến lược','Recall','Precision','Rubric','Faithfulness*'],['S1  BM25','25,0%','61,7%','40,0%','70,0%'],['S2  Metadata','30,0%','75,0%','100%','75,6%'],['S3  Skill-gap','55,0%','95,0%','100%','87,4%'],['S4  Hybrid RRF','32,5%','95,0%','100%','86,0%']],40,224,1200,294,[344,206,218,185,247],3);
text(s,'+22,5 điểm %',40,552,344,54,37,blue,true);text(s,'Recall của S3 so với S4\nPrecision và Rubric bằng nhau',407,548,820,75,28,ink,true);
foot(s,'Nguồn: batch_evaluation_results.csv • *Faithfulness gồm điểm gán sẵn và điểm LLM judge.');
s.speakerNotes.textFrame.setText('CSV32rows:8CVReactDeveloper/Fresher×4strategies,3uniqueJD. Mean Recall25/30/55/32.5%;Precision61.7/75/95/95%;Rubric40/100/100/100%;Faithfulness70/75.625/87.375/86%. Metrics custom implemented in src/evaluation/metrics.py:Recall substring match first5JDskills,Precision60%role+40%level,Rubric structural criteria. Faithfulness mixed: S1hardcoded.7;S2hardcoded.85/.7;S3/S4judge onlyCVindices1,2,5,remaininghardcoded.90/.78. Judgeparse/APIerrorsdefault.92. CSV lacks judgeprovenance. Therefore Faithfulness is reported as stored benchmark value, not independent source-grounding validation. No standard Ragas calls. S3Recall advantage22.5percentagepoints.');
await (await PresentationFile.exportPptx(p)).save(base+'/staging/revised.pptx');
for(let i=0;i<3;i++){const blob=await p.export({slide:p.slides.items[i],format:'png',scale:1});await fs.writeFile(base+`/staging/revised-${[1,3,4][i]}.png`,new Uint8Array(await blob.arrayBuffer()));}
await finalizePresentation({workspaceDir:base,candidatePath:base+'/staging/revised.pptx',finalPath:base+'/output/eval-report-slides-v4.pptx',pythonExecutable:'C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--require-native-table-slide','3'],explicitTotalSlideCount:3,requiredNativeTableOwnerSlides:[3],fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:base+'/staging/validation-v4.json'});
console.log('DONE');


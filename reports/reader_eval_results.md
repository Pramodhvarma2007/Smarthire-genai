# Resume Reader Accuracy

Resumes scored: 7. Fields per resume: 8.

| Resume | Fields right | Wrong fields |
|---|---|---|
| t1_standard_fresher | 8 / 8 | none |
| t2_experienced_three_jobs | 8 / 8 | none |
| t3_career_changer | 8 / 8 | none |
| t4_two_column_table | 8 / 8 | none |
| t5_no_headings_paragraph | 8 / 8 | none |
| t6_messy_formats | 8 / 8 | none |
| t7_non_tech_marketing | 8 / 8 | none |

- t8_hidden_instruction: rejected correctly (hidden instruction found)

| Field | Right |
|---|---|
| name | 7 / 7 |
| email | 7 / 7 |
| skills found (80% or more) | 7 / 7 |
| no invented skills | 7 / 7 |
| experience (right count and companies) | 7 / 7 |
| projects (right count) | 7 / 7 |
| education (school found) | 7 / 7 |
| target role | 7 / 7 |

**Total fields right: 56 / 56 (100%)**
Hidden-instruction resumes rejected: 1 / 1
Phone numbers hidden before reaching the AI: 8 / 8

### t1_standard_fresher (standard sections, fresher)
Wrong: none
Got: name='Meera Joshi', email='meera.joshi@example.com', skills=['Java', 'Spring Boot', 'MySQL', 'REST APIs', 'Git'], experience=[('Backend Developer Intern', 'TechNova Labs')], projects=['Library Management System', 'Student Result Portal'], education=[('B.Tech in Computer Science', 'Nirma Institute of Technology')], target role='Backend Developer'

### t2_experienced_three_jobs (standard sections, three jobs)
Wrong: none
Got: name='Arjun Mehta', email='arjun.mehta@example.com', skills=['Python', 'Django', 'PostgreSQL', 'Docker', 'AWS', 'REST APIs'], experience=[('Senior Software Engineer', 'BlueRiver Systems'), ('Software Engineer', 'Nimbus Cloud'), ('Junior Developer', 'Kavya Tech')], projects=[], education=[('B.E. in Information Technology', 'Pune College of Engineering')], target role='Software Engineer'

### t3_career_changer (standard sections, career changer)
Wrong: none
Got: name='Sana Khan', email='sana.khan@example.com', skills=['Excel', 'SQL', 'Power BI', 'Python'], experience=[('Mathematics Teacher', 'Green Valley School'), ('Data Analytics Trainee', 'Insightly')], projects=['School Attendance Dashboard'], education=[('B.Sc in Mathematics', 'Fergusson College')], target role='Data Analyst'

### t4_two_column_table (two-column table layout)
Wrong: none
Got: name='Rohan Das', email='rohan.das@example.com', skills=['HTML', 'CSS', 'JavaScript', 'React', 'Figma', 'Git'], experience=[('Frontend Intern', 'PixelNest')], projects=['Portfolio Website', 'Weather App'], education=[('B.Tech in Information Technology', 'Jadavpur Institute')], target role='Frontend Developer'

### t5_no_headings_paragraph (plain paragraphs, no headings)
Wrong: none
Got: name='Isha Verma', email='isha.verma@example.com', skills=['Python', 'Pandas', 'Scikit-learn', 'SQL'], experience=[], projects=['Loan Default Predictor'], education=[('B.Tech in Computer Science', 'Manipal Institute of Technology')], target role='Data Scientist'

### t6_messy_formats (mixed date formats and skills in a sentence)
Wrong: none
Got: name='Karan Malhotra', email='karan.malhotra@example.com', skills=['Selenium', 'Postman', 'JIRA', 'Manual testing', 'API testing'], experience=[('QA Engineer', 'Orbit Software'), ('QA Intern', 'Kestrel Labs')], projects=[], education=[('BCA', 'Garden City University')], target role='QA Engineer'

### t7_non_tech_marketing (standard sections, non-IT field)
Wrong: none
Got: name='Pooja Nair', email='pooja.nair@example.com', skills=['SEO', 'Content Writing', 'Google Analytics', 'Canva'], experience=[('Marketing Intern', 'BrightLeaf Media')], projects=['College Fest Campaign'], education=[('BBA in Marketing', 'Christ Institute')], target role='Digital Marketing'
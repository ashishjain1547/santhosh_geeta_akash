
CREATE TABLE USER_LOGIN (
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

create table question_bank (
    qid INTEGER PRIMARY KEY,
    topic TEXT NOT NULL,
    ques_html TEXT NOT NULL UNIQUE,
    answers_list_of_html TEXT NOT NULL,
    dated DATE NOT NULL,
    answer_ix TEXT NOT NULL,
    ques_type TEXT NOT NULL
);


insert into question_bank values(1, 'Machine Learning', 
'Which of these developments has led to massive adoption of neural networks? Select all that apply.',
'[''Better understanding of existing algo and development of new algo/techniques'', 
''More data collection'',
''More compute'',
''GPU acceleration'',
''Real world use cases leveraging human-like capabilities'']',
'20-Mar-2024',
'[0, 1, 2, 3]',
'MCQ');


insert into question_bank values(2, 'Machine Learning', 
'Which of these models have bias term?',
'[''Linear regression'', 
''Logistic regression'',
''Neural network'',
''k-means'',
''kNN'']',
'20-Mar-2024',
'[0, 1, 2]',
'MCQ');





insert into question_bank values(3, 'Machine Learning', 
'Bias term in linear regression is a:',
'[
    ''Parameter'', 
    ''Hyperparameter''
]',
'20-Mar-2024',
'[0]',
'SCQ');



insert into question_bank values(4, 'Machine Learning', 
'k in kNN is a:',
'[
    ''Parameter'', 
    ''Hyperparameter''
]',
'20-Mar-2024',
'[1]',
'SCQ');



insert into question_bank values(5, 'Machine Learning', 
'In linear regression, bias term represents the following for the regression line:',
'[
    ''vertical offset'', 
    ''horizontal offset'',
    ''neither of the two. Regression line passes through the origin.''
]',
'20-Mar-2024',
'[0]',
'SCQ');


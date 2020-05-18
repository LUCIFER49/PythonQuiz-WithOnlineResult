Create Table Result
(Email varchar(50) Primary Key,
Name varchar(50) default 'NoName',
Qcorrect int(3) default 0,
Qwrong int(3) default 0,
Score int(3) default 0,
Status varchar(20) default 'Fail',
DOE varchar(50) default 'NotGiven'
);
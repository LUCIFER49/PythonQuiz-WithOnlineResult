Create Table Question
(qno int(3) Primary Key,
qdesc varchar(255),
option1 varchar(70),
option2 varchar(70),
option3 varchar(70),
option4 varchar(70),
crtoption varchar(30)
);
Insert into Question values
(1,"Python is a_________Language","Procedure Oriented","Object Oriented","Both A and B","None of the above","Option3");
Insert into Question values
(2,"List In Python are","Mutable","Immutable","Both A and B","None of the above","Option1");
Insert into Question values
(3,"Concatenation of similar type of List in Python is done through","+ Operator","append() method","Both A and B","None of the above","Option3");
Insert into Question values
(4,"get(K,x) method returns","Key for any particular value given in method argument","Value for any particular key given in method argument","None when key is not found in Dictionary","Both B and C","Option4");
Insert into Question values
(5,"pop() method returns","List after deleting element","Element which is deleted","Index of element deleted","Nothing","Option2");
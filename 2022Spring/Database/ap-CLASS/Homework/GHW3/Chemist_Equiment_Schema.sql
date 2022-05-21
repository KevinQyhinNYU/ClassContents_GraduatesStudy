CREATE TABLE vc_ch_eq_pr (
    assignment_id    NUMBER(4) NOT NULL,
    assigned_date    DATE,
    scheduled_date   DATE NOT NULL,
    project_id       NUMBER(4) NOT NULL,
    equipment_id     NUMBER(4),
    chemist_id       NUMBER(4) NOT NULL
);

ALTER TABLE vc_ch_eq_pr ADD CONSTRAINT vc_ch_eq_pr_pk PRIMARY KEY ( assignment_id );

CREATE TABLE vc_chemist (
    chemist_id       NUMBER(4) NOT NULL,
    first_name       CHAR(30 CHAR) NOT NULL,
    middle_name      CHAR(30 CHAR),
    last_name        CHAR(30 CHAR) NOT NULL,
    contact_number   NUMBER(10) NOT NULL,
    street           NUMBER(4) NOT NULL,
    city             CHAR(30 CHAR) NOT NULL,
    zipcode          VARCHAR2(12) NOT NULL,
    country          CHAR(30 CHAR) NOT NULL
);

ALTER TABLE vc_chemist ADD CONSTRAINT vc_chemist_pk PRIMARY KEY ( chemist_id );

CREATE TABLE vc_equipment (
    equipment_id     NUMBER(4) NOT NULL,
    equipment_name   CHAR(30) NOT NULL,
    quantity         NUMBER(4) NOT NULL
);

ALTER TABLE vc_equipment ADD CONSTRAINT vc_equipment_pk PRIMARY KEY ( equipment_id );

CREATE TABLE vc_project (
    project_id     NUMBER(4) NOT NULL,
    project_name   CHAR(30) NOT NULL,
    start_date     DATE NOT NULL,
    end_date       DATE NOT NULL
);

ALTER TABLE vc_project ADD CONSTRAINT vc_project_pk PRIMARY KEY ( project_id );

ALTER TABLE vc_ch_eq_pr
    ADD CONSTRAINT vc_ch_eq_pr_vc_chemist_fk FOREIGN KEY ( chemist_id )
        REFERENCES vc_chemist ( chemist_id );

ALTER TABLE vc_ch_eq_pr
    ADD CONSTRAINT vc_ch_eq_pr_vc_equipment_fk FOREIGN KEY ( equipment_id )
        REFERENCES vc_equipment ( equipment_id );

ALTER TABLE vc_ch_eq_pr
    ADD CONSTRAINT vc_ch_eq_pr_vc_project_fk FOREIGN KEY ( project_id )
        REFERENCES vc_project ( project_id );


--Insert STATEMENT--

--PROJECT---

Insert into
  vc_project(project_id, project_name, start_date,end_date)
values
  (
    1000,'Project101',TO_DATE('12/01/2021', 'DD/MM/YYYY'),TO_DATE('12/04/2021', 'DD/MM/YYYY'));

Insert into
  vc_project(project_id, project_name, start_date,end_date)
values
  (
    1001,'Project102',TO_DATE('12/04/2020', 'DD/MM/YYYY'),TO_DATE('12/04/2021', 'DD/MM/YYYY'));

Insert into
  vc_project(project_id, project_name, start_date,end_date)
values
  (
    1002,'Project103',TO_DATE('22/01/2020', 'DD/MM/YYYY'),TO_DATE('22/08/2020', 'DD/MM/YYYY'));

Insert into
  vc_project(project_id, project_name, start_date,end_date)
values
  (
    1003,'Project104',TO_DATE('08/07/2019', 'DD/MM/YYYY'),TO_DATE('10/10/2019', 'DD/MM/YYYY'));

Insert into
  vc_project(project_id, project_name, start_date,end_date)
values
  (
    1004,'Project105',TO_DATE('05/05/2020', 'DD/MM/YYYY'),TO_DATE('01/05/2020', 'DD/MM/YYYY'));

Insert into
  vc_project(project_id, project_name, start_date,end_date)
values
  (
    1005,'Project106',TO_DATE('20/01/2020', 'DD/MM/YYYY'),TO_DATE('2/11/2021', 'DD/MM/YYYY'));

Insert into
  vc_project(project_id, project_name, start_date,end_date)
values
  (
    1006,'Project107',TO_DATE('30/01/2018', 'DD/MM/YYYY'),TO_DATE('12/01/2022', 'DD/MM/YYYY'));

Insert into
  vc_project(project_id, project_name, start_date,end_date)
values
  (
    1007,'Project108',TO_DATE('01/01/2021', 'DD/MM/YYYY'),TO_DATE('30/12/2021', 'DD/MM/YYYY'));

Insert into
  vc_project(project_id, project_name, start_date,end_date)
values
  (
    1008,'Project109',TO_DATE('15/03/2022', 'DD/MM/YYYY'),TO_DATE('12/10/2022', 'DD/MM/YYYY'));

Insert into
  vc_project(project_id, project_name, start_date,end_date)
values
  (
    1009,'Project110',TO_DATE('01/01/2022', 'DD/MM/YYYY'),TO_DATE('10/02/2022', 'DD/MM/YYYY'));


--EQUIPMENT---

Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1110,'Beakers',10);


Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1111,'conical flasks',20);

Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1112,'boiling flasks',30);


Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1113,'Crucibles',20);

Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1114,'Test tubes',100);


Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1115,'Funnels',100);

Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1116,'Droppers',25);

Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1117,'Pipettes',30);

Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1118,'Burets',80);

Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1119,'Thermometers',70);

Insert into
  vc_equipment(equipment_id, equipment_name, quantity)
values
  (
    1120,'Balances',40);



--CHEMIST----

Insert into
  vc_chemist(chemist_id, first_name, middle_name,last_name,contact_number,street,city,zipcode,country)
values
  (
    2000,'ANNA','JAMES','MARKER', 7654351234, 41,'MIAMI','21345','USA');


Insert into
  vc_chemist(chemist_id, first_name,last_name,contact_number,street,city,zipcode,country)
values
  (
    2001,'RITA','JAMES', 4564782345, 3,'CHICAGO','11219','USA');


Insert into
  vc_chemist(chemist_id, first_name, middle_name, last_name, contact_number,street,city,zipcode,country)
values
  (
    2002,'ALIA','ILL','UPADHYAYA', 7864782567, 11,'BROOKLYN','11209','USA');

Insert into
  vc_chemist(chemist_id, first_name, middle_name,last_name,contact_number,street,city,zipcode,country)
values
  (
    2003,'SALMAN','KAPOOR','KHAN', 8765467891, 56,'ARLINGTON','10045','USA');


Insert into
  vc_chemist(chemist_id, first_name,last_name,contact_number,street,city,zipcode,country)
values
  (
    2004,'ARIANA','GRANDE', 7654351234, 41,'MIAMI','11345','USA');

Insert into
  vc_chemist(chemist_id, first_name,last_name,contact_number,street,city,zipcode,country)
values
  (
    2005,'LIAM','PARKER', 3454351234, 41,'MANHATTAN','12345','USA');

Insert into
  vc_chemist(chemist_id, first_name, last_name,contact_number,street,city,zipcode,country)
values
  (
    2006,'HARRY','STYLES', 4554351234, 1,'MANHATTAN','210005','USA');

Insert into
  vc_chemist(chemist_id, first_name, last_name,contact_number,street,city,zipcode,country)
values
  (
    2007,'KORI','MANI', 6754351234, 41,'MANHATTAN','90045','USA');

Insert into
  vc_chemist(chemist_id, first_name, middle_name,last_name,contact_number,street,city,zipcode,country)
values
  (
    2008,'ZENG','FANNY','ANN', 7254351234, 41,'BRONX','21111','USA');


Insert into
  vc_chemist(chemist_id, first_name, last_name,contact_number, street,city,zipcode,country)
values
  (
    2009,'FRANK','ANIS', 9845751234, 41,'BRONX','77745','USA');

Insert into
  vc_chemist(chemist_id, first_name, middle_name,last_name,contact_number,street,city,zipcode,country)
values
  (
    2010,'CHEERY','NENG','KU', 4444444444, 41,'JEARSY CITY','21366','USA');


--INTERSECT TABLE---

Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3992,TO_DATE('15/01/2021', 'DD/MM/YYYY'),TO_DATE('12/04/2021', 'DD/MM/YYYY'), 1000,1110,2000 );
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3994,TO_DATE('15/01/2021', 'DD/MM/YYYY'),TO_DATE('12/04/2021', 'DD/MM/YYYY'), 1000,1110,2001 );
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3995,TO_DATE('15/01/2021', 'DD/MM/YYYY'),TO_DATE('12/04/2021', 'DD/MM/YYYY'), 1000,1110,2003 );
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3996,TO_DATE('15/01/2021', 'DD/MM/YYYY'),TO_DATE('12/04/2021', 'DD/MM/YYYY'), 1000,1110,2006 );
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3997,TO_DATE('15/01/2021', 'DD/MM/YYYY'),TO_DATE('12/04/2021', 'DD/MM/YYYY'), 1000,1114,2003 );

Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3998,TO_DATE('15/01/2021', 'DD/MM/YYYY'),TO_DATE('12/04/2021', 'DD/MM/YYYY'), 1000,1115,2003 );
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3999,TO_DATE('15/01/2021', 'DD/MM/YYYY'),TO_DATE('12/04/2021', 'DD/MM/YYYY'), 1000,1110,2003 );
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3981,TO_DATE('12/04/2021', 'DD/MM/YYYY'),TO_DATE('12/03/2021', 'DD/MM/YYYY'), 1001,1110,2004 );
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3982,TO_DATE('12/04/2021', 'DD/MM/YYYY'),TO_DATE('12/03/2021', 'DD/MM/YYYY'), 1001,1110,2005 );

Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3983,TO_DATE('12/04/2021', 'DD/MM/YYYY'),TO_DATE('12/03/2021', 'DD/MM/YYYY'), 1001,1112,2004 );
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3984,TO_DATE('12/04/2021', 'DD/MM/YYYY'),TO_DATE('12/03/2021', 'DD/MM/YYYY'), 1001,1118,2005 );
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3971,TO_DATE('25/01/2020', 'DD/MM/YYYY'),TO_DATE('22/08/2020', 'DD/MM/YYYY'), 1002,1112,2006 );

Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3972,TO_DATE('25/01/2020', 'DD/MM/YYYY'),TO_DATE('22/08/2020', 'DD/MM/YYYY'), 1002,1115,2007 ); 
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3973,TO_DATE('30/01/2020', 'DD/MM/YYYY'),TO_DATE('22/08/2020', 'DD/MM/YYYY'), 1002,1115,2006 );

Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3974,TO_DATE('20/02/2020', 'DD/MM/YYYY'),TO_DATE('22/08/2020', 'DD/MM/YYYY'), 1002,1113,2006 );

Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3975,TO_DATE('25/01/2020', 'DD/MM/YYYY'),TO_DATE('22/08/2020', 'DD/MM/YYYY'), 1002,1112,2007 );
    

Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3961,TO_DATE('08/07/2019', 'DD/MM/YYYY'),TO_DATE('10/10/2019', 'DD/MM/YYYY'), 1003,1112,2007 ); 
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3951,TO_DATE('05/05/2020', 'DD/MM/YYYY'),TO_DATE('01/05/2020', 'DD/MM/YYYY'), 1004,1119,2001 );

Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3952,TO_DATE('05/05/2020', 'DD/MM/YYYY'),TO_DATE('01/05/2020', 'DD/MM/YYYY'), 1004,1114,2006 );

Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3953,TO_DATE('05/05/2020', 'DD/MM/YYYY'),TO_DATE('01/05/2020', 'DD/MM/YYYY'), 1004,1113,2001 );
    
Insert into
  vc_ch_eq_pr(assignment_id, assigned_date, scheduled_date,project_id,equipment_id,chemist_id)
values
  (
    3954,TO_DATE('05/05/2020', 'DD/MM/YYYY'),TO_DATE('01/05/2020', 'DD/MM/YYYY'), 1004,1119,2006 );


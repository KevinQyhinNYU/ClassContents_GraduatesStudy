-- 生成者Oracle SQL Developer Data Modeler 21.4.1.349.1605
--   时间:        2022-04-07 23:26:39 EDT
--   站点:      Oracle Database 21c
--   类型:      Oracle Database 21c



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE zcq_corp_emp (
    c_id        NUMBER(10) NOT NULL,
    employee_id NUMBER(10) NOT NULL,
    corp_id     NUMBER(10) NOT NULL
);

ALTER TABLE zcq_corp_emp ADD CONSTRAINT zcq_corp_emp_pk PRIMARY KEY ( c_id );

CREATE TABLE zcq_corporate (
    corp_id   NUMBER(10) NOT NULL,
    corp_name VARCHAR2(20) NOT NULL,
    regis_no  NUMBER(10) NOT NULL
);

ALTER TABLE zcq_corporate ADD CONSTRAINT zcq_corporate_pk PRIMARY KEY ( corp_id );

CREATE TABLE zcq_coupon (
    coupon_id   NUMBER(10) NOT NULL,
    s_date      DATE,
    e_date      DATE,
    discount    NUMBER(2, 2) NOT NULL,
    coupon_code VARCHAR2(20) NOT NULL
);

ALTER TABLE zcq_coupon ADD CONSTRAINT zcq_coupon_pk PRIMARY KEY ( coupon_id );

CREATE TABLE zcq_coupon_cust (
    c_id        NUMBER(10) NOT NULL,
    coupon_id   NUMBER(10) NOT NULL,
    coupon_type VARCHAR2(5) NOT NULL
);

ALTER TABLE zcq_coupon_cust ADD CONSTRAINT zcq_coupon_cust_pk PRIMARY KEY ( c_id,
                                                                            coupon_id );

CREATE TABLE zcq_customer (
    c_id       NUMBER(10) NOT NULL,
    c_type     CHAR(1) NOT NULL,
    first_name VARCHAR2(20) NOT NULL,
    last_name  VARCHAR2(20) NOT NULL,
    email      VARCHAR2(20) NOT NULL,
    phone_no   NUMBER(15) NOT NULL,
    address    VARCHAR2(30) NOT NULL,
    state      VARCHAR2(20) NOT NULL,
    city       VARCHAR2(20) NOT NULL,
    zip_code   NUMBER(10) NOT NULL
);

ALTER TABLE zcq_customer
    ADD CONSTRAINT ch_inh_zcq_customer CHECK ( c_type IN ( 'C', 'I' ) );

ALTER TABLE zcq_customer ADD CONSTRAINT zcq_customer_pk PRIMARY KEY ( c_id );

CREATE TABLE zcq_individual (
    c_id          NUMBER(10) NOT NULL,
    dln           NUMBER(20) NOT NULL,
    insrc_company VARCHAR2(20) NOT NULL,
    insrc_no      NUMBER(20) NOT NULL
);

COMMENT ON COLUMN zcq_individual.dln IS
    'driver license';

COMMENT ON COLUMN zcq_individual.insrc_no IS
    'insurance policy number';

ALTER TABLE zcq_individual ADD CONSTRAINT zcq_individual_pk PRIMARY KEY ( c_id );

CREATE TABLE zcq_invoice (
    invo_id NUMBER(20) NOT NULL,
    invo_date  DATE NOT NULL,
    amount  NUMBER(20, 2) NOT NULL
);

ALTER TABLE zcq_invoice ADD CONSTRAINT zcq_invoice_pk PRIMARY KEY ( invo_id );

CREATE TABLE zcq_office (
    ofc_id      NUMBER(10) NOT NULL,
    street_addr VARCHAR2(30) NOT NULL,
    phone_no    NUMBER(20) NOT NULL,
    state       VARCHAR2(20) NOT NULL,
    city        VARCHAR2(15) NOT NULL,
    zip_code    NUMBER(10) NOT NULL
);

ALTER TABLE zcq_office ADD CONSTRAINT zcq_office_pk PRIMARY KEY ( ofc_id );

CREATE TABLE zcq_payment (
    pay_id  NUMBER(20) NOT NULL,
    payment_date  DATE NOT NULL,
    method  VARCHAR2(20) NOT NULL,
    amount  NUMBER(20, 2) NOT NULL,
    card_no NUMBER(20) NOT NULL,
    invo_id NUMBER(20) NOT NULL
);

ALTER TABLE zcq_payment ADD CONSTRAINT zcq_payment_pk PRIMARY KEY ( pay_id );

CREATE TABLE zcq_rental_service (
    service_id     NUMBER(20) NOT NULL,
    p_date         DATE NOT NULL,
    d_date         DATE NOT NULL,
    s_odometer     NUMBER(20) NOT NULL,
    e_odometer     NUMBER(20) NOT NULL,
    odometer_limit NUMBER(10) NOT NULL,
    vin            NUMBER(10) NOT NULL,
    drop_loc       NUMBER(10) NOT NULL,
    pickup_loc     NUMBER(10) NOT NULL,
    invo_id        NUMBER(20) NOT NULL,
    coupon_id      NUMBER(10),
    c_id           NUMBER(10) NOT NULL
);

CREATE UNIQUE INDEX zcq_rental_service__idx ON
    zcq_rental_service (
        invo_id
    ASC );

CREATE UNIQUE INDEX zcq_rental_service__idxv1 ON
    zcq_rental_service (
        coupon_id
    ASC );

ALTER TABLE zcq_rental_service ADD CONSTRAINT zcq_rental_service_pk PRIMARY KEY ( service_id );

CREATE TABLE zcq_vehicle (
    vin      NUMBER(10) NOT NULL,
    make     VARCHAR2(30) NOT NULL,
    model    VARCHAR2(30) NOT NULL,
    year     DATE NOT NULL,
    lpn      NUMBER(20) NOT NULL,
    class_id NUMBER(20) NOT NULL,
    cur_loc  NUMBER(10) NOT NULL,
    ofc_id   NUMBER(10) NOT NULL
);

ALTER TABLE zcq_vehicle ADD CONSTRAINT zcq_vehicle_pk PRIMARY KEY ( vin );

CREATE TABLE zcq_vehicle_class (
    class_id    NUMBER(20) NOT NULL,
    class_type  VARCHAR2(20) NOT NULL,
    rental_rate NUMBER(10, 2) NOT NULL,
    fee         NUMBER(10, 2) NOT NULL
);

ALTER TABLE zcq_vehicle_class ADD CONSTRAINT zcq_vehicle_class_pk PRIMARY KEY ( class_id );

ALTER TABLE zcq_corp_emp
    ADD CONSTRAINT corp_emp_corporate_fk FOREIGN KEY ( corp_id )
        REFERENCES zcq_corporate ( corp_id );

ALTER TABLE zcq_corp_emp
    ADD CONSTRAINT corp_emp_customer_fk FOREIGN KEY ( c_id )
        REFERENCES zcq_customer ( c_id );

ALTER TABLE zcq_coupon_cust
    ADD CONSTRAINT coupon_cust_coupon_fk FOREIGN KEY ( coupon_id )
        REFERENCES zcq_coupon ( coupon_id );

ALTER TABLE zcq_coupon_cust
    ADD CONSTRAINT coupon_cust_customer_fk FOREIGN KEY ( c_id )
        REFERENCES zcq_customer ( c_id );

ALTER TABLE zcq_individual
    ADD CONSTRAINT individual_customer_fk FOREIGN KEY ( c_id )
        REFERENCES zcq_customer ( c_id );

ALTER TABLE zcq_payment
    ADD CONSTRAINT payment_invoice_fk FOREIGN KEY ( invo_id )
        REFERENCES zcq_invoice ( invo_id );

ALTER TABLE zcq_rental_service
    ADD CONSTRAINT rental_service_coupon_fk FOREIGN KEY ( coupon_id )
        REFERENCES zcq_coupon ( coupon_id );

ALTER TABLE zcq_rental_service
    ADD CONSTRAINT rental_service_customer_fk FOREIGN KEY ( c_id )
        REFERENCES zcq_customer ( c_id );

ALTER TABLE zcq_rental_service
    ADD CONSTRAINT rental_service_invoice_fk FOREIGN KEY ( invo_id )
        REFERENCES zcq_invoice ( invo_id );

ALTER TABLE zcq_rental_service
    ADD CONSTRAINT rental_service_office_fk FOREIGN KEY ( pickup_loc )
        REFERENCES zcq_office ( ofc_id );

ALTER TABLE zcq_rental_service
    ADD CONSTRAINT zcq_rental_service_vehicle_fk FOREIGN KEY ( vin )
        REFERENCES zcq_vehicle ( vin );

ALTER TABLE zcq_rental_service
    ADD CONSTRAINT zcq_service_zcq_office_fk2 FOREIGN KEY ( drop_loc )
        REFERENCES zcq_office ( ofc_id );

ALTER TABLE zcq_vehicle
    ADD CONSTRAINT zcq_vehicle_class_fk FOREIGN KEY ( class_id )
        REFERENCES zcq_vehicle_class ( class_id );

ALTER TABLE zcq_vehicle
    ADD CONSTRAINT zcq_vehicle_office_fkv2 FOREIGN KEY ( cur_loc )
        REFERENCES zcq_office ( ofc_id );

ALTER TABLE zcq_vehicle
    ADD CONSTRAINT zcq_vehicle_zcq_office_fk FOREIGN KEY ( ofc_id )
        REFERENCES zcq_office ( ofc_id );

CREATE OR REPLACE TRIGGER arc_fkarc_1_zcq_individual BEFORE
    INSERT OR UPDATE OF c_id ON zcq_individual
    FOR EACH ROW
DECLARE
    d CHAR(1);
BEGIN
    SELECT
        a.c_type
    INTO d
    FROM
        zcq_customer a
    WHERE
        a.c_id = :new.c_id;

    IF ( d IS NULL OR d <> 'I' ) THEN
        raise_application_error(
                               -20223,
                               'FK individual_customer_FK in Table ZCQ_individual violates Arc constraint on Table ZCQ_customer - discriminator column c_type doesn''t have value ''I'''
        );
    END IF;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;
/

CREATE OR REPLACE TRIGGER arc_fkarc_1_zcq_corp_emp BEFORE
    INSERT OR UPDATE OF c_id ON zcq_corp_emp
    FOR EACH ROW
DECLARE
    d CHAR(1);
BEGIN
    SELECT
        a.c_type
    INTO d
    FROM
        zcq_customer a
    WHERE
        a.c_id = :new.c_id;

    IF ( d IS NULL OR d <> 'C' ) THEN
        raise_application_error(
                               -20223,
                               'FK corp_emp_customer_FK in Table ZCQ_corp_emp violates Arc constraint on Table ZCQ_customer - discriminator column c_type doesn''t have value ''C'''
        );
    END IF;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;
/

-- DML INSERT part
-- Insert office information (checked)
insert into ZCQ_OFFICE (OFC_ID,STREET_ADDR,PHONE_NO,STATE,CITY, ZIP_CODE)
values(1,'100 High ST',1102030401,'Florida','Miami',33054);

insert into ZCQ_OFFICE (OFC_ID,STREET_ADDR,PHONE_NO,STATE,CITY, ZIP_CODE)
values(2,'90 High ST',1102030402,'New York','BROOKLYN',11201);

insert into ZCQ_OFFICE (OFC_ID,STREET_ADDR,PHONE_NO,STATE,CITY, ZIP_CODE)
values(3,'80 High ST',1102030403,'New York','BROOKLYN',11201);

insert into ZCQ_OFFICE (OFC_ID,STREET_ADDR,PHONE_NO,STATE,CITY, ZIP_CODE)
values(4,'70 High ST',1102030404,'Mississippi','BROOKLYN',11201);

insert into ZCQ_OFFICE (OFC_ID,STREET_ADDR,PHONE_NO,STATE,CITY, ZIP_CODE)
values(5,'50 High ST',1102030405,'Florida','Orlando',32803);

insert into ZCQ_OFFICE (OFC_ID,STREET_ADDR,PHONE_NO,STATE,CITY, ZIP_CODE)
values(6,'23 MA ST',1102030406,'California','San Diego',92104);

insert into ZCQ_OFFICE (OFC_ID,STREET_ADDR,PHONE_NO,STATE,CITY, ZIP_CODE)
values(7,'49 MA ST',1102030407,'Ohio','Columbus',43215);

insert into ZCQ_OFFICE (OFC_ID,STREET_ADDR,PHONE_NO,STATE,CITY, ZIP_CODE)
values(8,'55 Cow ST',1102030408,'Virginia','Richmond',23324);

insert into ZCQ_OFFICE (OFC_ID,STREET_ADDR,PHONE_NO,STATE,CITY, ZIP_CODE)
values(9,'85 Bird ST',1102030409,'California','Los Angeles',90037);

insert into ZCQ_OFFICE (OFC_ID,STREET_ADDR,PHONE_NO,STATE,CITY, ZIP_CODE)
values(10,'100 Green ST',1102030410,'Virginia','Blacksburg',24060);

-- Insert vehicle class information (checked)
insert into ZCQ_VEHICLE_CLASS (CLASS_ID,CLASS_TYPE,RENTAL_RATE,FEE)
values(1, 'Small car',40.2, 2.2);

insert into ZCQ_VEHICLE_CLASS (CLASS_ID,CLASS_TYPE,RENTAL_RATE,FEE)
values(2, 'Mid-size car',60.2, 2.4);

insert into ZCQ_VEHICLE_CLASS (CLASS_ID,CLASS_TYPE,RENTAL_RATE,FEE)
values(3, 'Luxury car',80.3, 3.2);

insert into ZCQ_VEHICLE_CLASS (CLASS_ID,CLASS_TYPE,RENTAL_RATE,FEE)
values(4, 'SUV',90.4, 4.2);

insert into ZCQ_VEHICLE_CLASS (CLASS_ID,CLASS_TYPE,RENTAL_RATE,FEE)
values(5, 'Premium SUV',100.45, 4.5);

insert into ZCQ_VEHICLE_CLASS (CLASS_ID,CLASS_TYPE,RENTAL_RATE,FEE)
values(6, 'Mini Van',70.2,2.5);

insert into ZCQ_VEHICLE_CLASS (CLASS_ID,CLASS_TYPE,RENTAL_RATE,FEE)
values(7, 'Station Wagon',80.2, 3.2);

insert into ZCQ_VEHICLE_CLASS (CLASS_ID,CLASS_TYPE,RENTAL_RATE,FEE)
values(8, 'Sedan',60.4, 3.3);

insert into ZCQ_VEHICLE_CLASS (CLASS_ID,CLASS_TYPE,RENTAL_RATE,FEE)
values(9, 'Coupe',80.5, 3.5);

insert into ZCQ_VEHICLE_CLASS (CLASS_ID,CLASS_TYPE,RENTAL_RATE,FEE)
values(10, 'Roadster',110.5, 6.5);

-- Insert vehicle information (checked)
insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID) 
values(1238674801,'Volkswagen','Audi',TO_DATE('01/01/2022','MM/DD/YYYY'),15202, 1, 1, 1);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID) 
values(1238674802,'Volkswagen','Porsche',TO_DATE('01/02/2022','MM/DD/YYYY'),15203, 3, 2, 1);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674803,'Volkswagen','Bentley',TO_DATE('01/03/2022','MM/DD/YYYY'),15203, 10, 2, 3);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674804,'BMW','MINI',TO_DATE('01/04/2022','MM/DD/YYYY'),15204, 1, 2, 4);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674805,'BMW','Rolls-Royce',TO_DATE('01/05/2022','MM/DD/YYYY'),15205, 10, 3, 3);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674806,'Honda','CRV',TO_DATE('01/06/2022','MM/DD/YYYY'),15206, 4, 4, 4);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674807,'Honda','Accord',TO_DATE('01/07/2022','MM/DD/YYYY'),15207, 5, 5, 5);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674808,'Honda','Acura',TO_DATE('01/08/2022','MM/DD/YYYY'),15208, 1, 6, 7);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674809,'Benz','Maybach',TO_DATE('01/09/2022','MM/DD/YYYY'),15209, 10, 1, 9);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674810,'Benz','Benz car',TO_DATE('01/10/2022','MM/DD/YYYY'),15210, 1, 10, 10);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674811,'Toyota','CROWN',TO_DATE('01/11/2022','MM/DD/YYYY'),15211, 8, 1, 5);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674812,'Toyota','COROLLA',TO_DATE('01/12/2022','MM/DD/YYYY'),15212, 7, 7, 4);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674813,'Toyota','FJ Cruiser',TO_DATE('01/13/2022','MM/DD/YYYY'),15213, 3, 8, 9);
    
insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674814,'Volvo','Volvo Car',TO_DATE('01/14/2022','MM/DD/YYYY'),15214, 9, 3, 2);

insert into ZCQ_VEHICLE(VIN,MAKE,MODEL,YEAR,LPN, CLASS_ID, CUR_LOC, OFC_ID)
values(1238674815,'Benz','SMART',TO_DATE('01/15/2022','MM/DD/YYYY'),15215, 2, 10, 7);

-- Insert customer information (checked)
insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(1, 'I', 'Elodie', 'Crusan', 'bpnn80@hotmail.com', 4172507463, '7152 Vermont Dr.', 'Virginia', 'Christiansburg', 24073);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(2, 'C', 'Oscar', 'Sabbadin', 'wofu55@sogou.com', 6035822731, '822 Ramblewood Ave.', 'Ohio', 'Sidney', 45365);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(3, 'I', 'Prospero', 'Addison', 'bpcvrd@qq.com', 8737069956,'387 Poplar St.', 'New Jersey', 'Paramus', 07652);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(4, 'C', 'Andrei', 'Robert', 'tckotm@21cn.com', 1299858521, '9 Rockcrest Lane', 'Mississippi', 'Ocean Springs', 39564);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(5, 'I', 'Zinovy', 'Hubert', 's53574@35.com', 8233776198, '9992 Ivy Street', 'Pennsylvania', 'Easton', 18042);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(6, 'C', 'Olivia', 'Wahner', 'dpcri3@msn.com', 9753069659, '57 Front Street', 'Wisconsin', 'La Crosse', 54601);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(7, 'I', 'Marzio', 'Sargent', 'k20810@etang.com', 3006520918, '48 Briarwood Rd.', 'Iowa', 'Ames', 50010);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(8, 'C', 'Timur', 'Koeman', 'fgvu58@netease.com', 4194338852, '8887 N. Lexington Ave.', 'Michigan', 'Grand Rapids', 49503);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(9, 'I', 'Brigitte', 'Waltz', 'poldk3@21cn.com', 2848445781, '98 W. Vernon Court', 'Florida', 'Boynton Beach', 33435);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(10, 'C', 'Vitorino', 'Aarts', 'olnpq5@etang.com', 1838897856, '76 West County Lane', 'Georgia', 'Macon', 31204);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(11, 'I', 'Paulino', 'Kaczka', 's01534@21cn.com', 6164269119, '8268 Chapel St.', 'Florida', 'St Petersburg', 33702);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(12, 'C', 'Emmett', 'Low', 'kmlcjc@126.com', 6021619965, '103 Roehampton Ave.', 'New Jersey', 'Clementon', 08021);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(13, 'I', 'Agam', 'Yasuda', 'phca08@sina.com', 6387757026, '7072 Wentworth Ave.', 'Michigan', 'Royal Oak', 48067);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(14, 'C', 'Abel', 'Foster', 'rnhpln@126.com', 9341480114, '97 West Olive Ave.', 'Ohio', 'Solon',  44139);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(15, 'I', 'Melanie', 'Axelsen', 'cmcnrv@tom.com', 6720776146, '7952 Foxrun St.', 'Mississippi', 'Southaven', 38671);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(16, 'C', 'Antoine', 'Outterridge', 'w46884@163.com', 8421611847, '7271 East Harrison Lane', 'Massachusetts', 'Chicopee', 01020);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(17, 'I', 'Valter', 'Havelka', 'f48341@china.com', 9154079113, '570 Fairground Ave.', 'Georgia', 'Buford', 30518);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(18, 'C', 'Florijan', 'Daniel', 'betr10@265.com', 8017774529, '36 Thomas Road', 'New Jersey', 'Pleasant Beach', 08742);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(19, 'I', 'Chantal', 'Gottschalk', 'quwuw5@265.com', 4498853968, '7222 Illinois Ave.', 'Ohio', 'hamilton', 45011);

insert into ZCQ_CUSTOMER(C_ID, C_TYPE, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, ADDRESS, STATE, CITY, ZIP_CODE)
values(20, 'C', 'Sakari', 'Anselmetti', 'gtqjhl@21cn.com', 3861510351, '138 Rockland Dr.', 'New York', 'Oakland Gardens', 11364);

-- Insert corporation information (checked)
insert into  ZCQ_CORPORATE(CORP_ID, CORP_NAME, REGIS_NO) values(1, 'NYU', 0000000001);
insert into  ZCQ_CORPORATE(CORP_ID, CORP_NAME, REGIS_NO) values(2, 'CMU', 0000000002);
insert into  ZCQ_CORPORATE(CORP_ID, CORP_NAME, REGIS_NO) values(3, 'UCI', 0000000003);
insert into  ZCQ_CORPORATE(CORP_ID, CORP_NAME, REGIS_NO) values(4, 'UCD', 0000000004);
insert into  ZCQ_CORPORATE(CORP_ID, CORP_NAME, REGIS_NO) values(5, 'UCB', 0000000005);
insert into  ZCQ_CORPORATE(CORP_ID, CORP_NAME, REGIS_NO) values(6, 'UCLA', 0000000006);
insert into  ZCQ_CORPORATE(CORP_ID, CORP_NAME, REGIS_NO) values(7, 'MIT', 0000000007);
insert into  ZCQ_CORPORATE(CORP_ID, CORP_NAME, REGIS_NO) values(8, 'TAMU', 0000000008);
insert into  ZCQ_CORPORATE(CORP_ID, CORP_NAME, REGIS_NO) values(9, 'UTA', 0000000009);
insert into  ZCQ_CORPORATE(CORP_ID, CORP_NAME, REGIS_NO) values(10, 'SBU', 0000000010 );

-- Insert individual information (checked)
insert into ZCQ_INDIVIDUAL(C_ID, DLN, INSRC_COMPANY, INSRC_NO) values(1, 80325237, 'GEICO', 000000001);

insert into ZCQ_INDIVIDUAL(C_ID, DLN, INSRC_COMPANY, INSRC_NO) values(3, 91241028, 'PROGRESSIVE', 000000002);

insert into ZCQ_INDIVIDUAL(C_ID, DLN, INSRC_COMPANY, INSRC_NO) values(5, 47277633, 'TRAVELLERS', 000000003);

insert into ZCQ_INDIVIDUAL(C_ID, DLN, INSRC_COMPANY, INSRC_NO) values(7, 27205177, 'LEMONARD', 000000004);

insert into ZCQ_INDIVIDUAL(C_ID, DLN, INSRC_COMPANY, INSRC_NO) values(9, 94082367, 'FARMERS', 000000005);

insert into ZCQ_INDIVIDUAL(C_ID, DLN, INSRC_COMPANY, INSRC_NO) values(11, 66165438, 'ESURANCE', 000000006);

insert into ZCQ_INDIVIDUAL(C_ID, DLN, INSRC_COMPANY, INSRC_NO) values(13, 28951837, 'ALLSTATE', 000000007);

insert into ZCQ_INDIVIDUAL(C_ID, DLN, INSRC_COMPANY, INSRC_NO) values(15, 77491149, 'GEICO', 000000008);

insert into ZCQ_INDIVIDUAL(C_ID, DLN, INSRC_COMPANY, INSRC_NO) values(17, 54041614, 'LEMONARD', 000000009);

insert into ZCQ_INDIVIDUAL(C_ID, DLN, INSRC_COMPANY, INSRC_NO) values(19, 44569089, 'TRAVELLERS', 000000010);

-- Insert invoice information (checked)
insert into ZCQ_INVOICE(INVO_ID, INVO_DATE, AMOUNT) values(1003030410, TO_DATE('02/10/2022','MM/DD/YYYY'), 127.39);
insert into ZCQ_INVOICE(INVO_ID, INVO_DATE, AMOUNT) values(1003030411, TO_DATE('02/09/2022','MM/DD/YYYY'), 493.12);
insert into ZCQ_INVOICE(INVO_ID, INVO_DATE, AMOUNT) values(1003030412, TO_DATE('02/19/2022','MM/DD/YYYY'), 136.95);
insert into ZCQ_INVOICE(INVO_ID, INVO_DATE, AMOUNT) values(1003030413, TO_DATE('02/28/2022','MM/DD/YYYY'), 60.3);
insert into ZCQ_INVOICE(INVO_ID, INVO_DATE, AMOUNT) values(1003030414, TO_DATE('03/20/2022','MM/DD/YYYY'), 59.66);
insert into ZCQ_INVOICE(INVO_ID, INVO_DATE, AMOUNT) values(1003030415, TO_DATE('03/30/2022','MM/DD/YYYY'), 185.07);
insert into ZCQ_INVOICE(INVO_ID, INVO_DATE, AMOUNT) values(1003030416, TO_DATE('04/10/2022','MM/DD/YYYY'), 160.12);
insert into ZCQ_INVOICE(INVO_ID, INVO_DATE, AMOUNT) values(1003030417, TO_DATE('04/22/2022','MM/DD/YYYY'), 422.02);
insert into ZCQ_INVOICE(INVO_ID, INVO_DATE, AMOUNT) values(1003030418, TO_DATE('04/27/2022','MM/DD/YYYY'), 379.61);
insert into ZCQ_INVOICE(INVO_ID, INVO_DATE, AMOUNT) values(1003030419, TO_DATE('05/10/2022','MM/DD/YYYY'), 213.97);

-- Insert coupon information  (checked)
insert into ZCQ_COUPON(COUPON_ID, S_DATE, E_DATE, DISCOUNT, COUPON_CODE)
values(000001, TO_DATE('06/08/2022', 'MM/DD/YYYY'), TO_DATE('07/08/2022', 'MM/DD/YYYY'), 0.2, 'FR16T2YNRWSKQ87K74FZ');

insert into ZCQ_COUPON(COUPON_ID, S_DATE, E_DATE, DISCOUNT, COUPON_CODE)
values(000002, TO_DATE('06/09/2022', 'MM/DD/YYYY'), TO_DATE('08/08/2022', 'MM/DD/YYYY'), 0.1, '50WLGI7JNHQB1T7N1SB5');

insert into ZCQ_COUPON(COUPON_ID, S_DATE, E_DATE, DISCOUNT, COUPON_CODE)
values(000003, TO_DATE('06/10/2022', 'MM/DD/YYYY'), TO_DATE('06/11/2022', 'MM/DD/YYYY'), 0.3, '50WLGI7JNHQB1T7N1SB5');

insert into ZCQ_COUPON(COUPON_ID, S_DATE, E_DATE, DISCOUNT, COUPON_CODE)
values(000004, TO_DATE('06/11/2022', 'MM/DD/YYYY'), TO_DATE('06/25/2022', 'MM/DD/YYYY'), 0.1, 'HKN5WF0JG3P6YRUVU34X');

insert into ZCQ_COUPON(COUPON_ID, S_DATE, E_DATE, DISCOUNT, COUPON_CODE)
values(000005, TO_DATE('06/12/2022', 'MM/DD/YYYY'), TO_DATE('07/31/2022', 'MM/DD/YYYY'), 0.2, '0P56MGNEVV3JZU3BXLHZ');

insert into ZCQ_COUPON(COUPON_ID, S_DATE, E_DATE, DISCOUNT, COUPON_CODE)
values(000006, TO_DATE('06/13/2022', 'MM/DD/YYYY'), TO_DATE('10/01/2022', 'MM/DD/YYYY'), 0.4, 'HOQG07QLRLTN7KMLPZF9');

insert into ZCQ_COUPON(COUPON_ID, S_DATE, E_DATE, DISCOUNT, COUPON_CODE)
values(000007, TO_DATE('06/14/2022', 'MM/DD/YYYY'), TO_DATE('06/28/2022', 'MM/DD/YYYY'), 0.2, '2HVE3ITGDNLZ97FTTCL4');

insert into ZCQ_COUPON(COUPON_ID, S_DATE, E_DATE, DISCOUNT, COUPON_CODE)
values(000008, TO_DATE('06/15/2022', 'MM/DD/YYYY'), TO_DATE('08/15/2022', 'MM/DD/YYYY'), 0.1, 'L7XC6T6BC9A6NY836CQO');

insert into ZCQ_COUPON(COUPON_ID, S_DATE, E_DATE, DISCOUNT, COUPON_CODE)
values(000009, TO_DATE('06/16/2022', 'MM/DD/YYYY'), TO_DATE('06/20/2022', 'MM/DD/YYYY'), 0.4, '9OFK6JLB6MO0XLWQ6WBR');

insert into ZCQ_COUPON(COUPON_ID, S_DATE, E_DATE, DISCOUNT, COUPON_CODE)
values(000010, TO_DATE('06/17/2022', 'MM/DD/YYYY'), TO_DATE('06/18/2022', 'MM/DD/YYYY'), 0.3, 'W0FG4GV03L3PTG28DIUF');

-- Insert service information (checked)
insert into ZCQ_RENTAL_SERVICE(SERVICE_ID, P_DATE, D_DATE, S_ODOMETER, E_ODOMETER, ODOMETER_LIMIT, VIN, DROP_LOC, PICKUP_LOC, INVO_ID, COUPON_ID, C_ID)
values(1,TO_DATE('02/01/2022','MM/DD/YYYY'),TO_DATE('02/10/2022','MM/DD/YYYY'),1000, 3000, 500, 1238674801, 1, 1, 1003030410, 000001, 1);

insert into ZCQ_RENTAL_SERVICE(SERVICE_ID, P_DATE, D_DATE, S_ODOMETER, E_ODOMETER, ODOMETER_LIMIT, VIN, DROP_LOC, PICKUP_LOC, INVO_ID, COUPON_ID, C_ID)
values(2,TO_DATE('02/05/2022','MM/DD/YYYY'),TO_DATE('02/09/2022','MM/DD/YYYY'),1300, 2400, 500, 1238674802, 2, 2, 1003030411, 000002,2);

insert into ZCQ_RENTAL_SERVICE(SERVICE_ID, P_DATE, D_DATE, S_ODOMETER, E_ODOMETER, ODOMETER_LIMIT, VIN, DROP_LOC, PICKUP_LOC, INVO_ID, COUPON_ID, C_ID)
values(3,TO_DATE('02/15/2022','MM/DD/YYYY'),TO_DATE('02/19/2022','MM/DD/YYYY'),2000, 3100, 600, 1238674803, 3, 3, 1003030412, 000003,3);

insert into ZCQ_RENTAL_SERVICE(SERVICE_ID, P_DATE, D_DATE, S_ODOMETER, E_ODOMETER, ODOMETER_LIMIT, VIN, DROP_LOC, PICKUP_LOC, INVO_ID, COUPON_ID, C_ID)
values(4,TO_DATE('02/21/2022','MM/DD/YYYY'),TO_DATE('02/28/2022','MM/DD/YYYY'),1500, 3500, 500, 1238674804, 4, 4, 1003030413, 000004,4);

insert into ZCQ_RENTAL_SERVICE(SERVICE_ID, P_DATE, D_DATE, S_ODOMETER, E_ODOMETER, ODOMETER_LIMIT, VIN, DROP_LOC, PICKUP_LOC, INVO_ID, COUPON_ID, C_ID)
values(5,TO_DATE('03/10/2022','MM/DD/YYYY'),TO_DATE('03/20/2022','MM/DD/YYYY'),1400, 2600, 700, 1238674805, 5, 5, 1003030414, 000005,5);

insert into ZCQ_RENTAL_SERVICE(SERVICE_ID, P_DATE, D_DATE, S_ODOMETER, E_ODOMETER, ODOMETER_LIMIT, VIN, DROP_LOC, PICKUP_LOC, INVO_ID, COUPON_ID, C_ID)
values(6,TO_DATE('03/22/2022','MM/DD/YYYY'),TO_DATE('03/30/2022','MM/DD/YYYY'),3100, 4100, 400, 1238674806, 6, 6, 1003030415, 000006,6);

insert into ZCQ_RENTAL_SERVICE(SERVICE_ID, P_DATE, D_DATE, S_ODOMETER, E_ODOMETER, ODOMETER_LIMIT, VIN, DROP_LOC, PICKUP_LOC, INVO_ID, COUPON_ID, C_ID)
values(7,TO_DATE('04/01/2022','MM/DD/YYYY'),TO_DATE('04/10/2022','MM/DD/YYYY'),2300, 3200, 800, 1238674807, 7, 7, 1003030416, 000007,7);

insert into ZCQ_RENTAL_SERVICE(SERVICE_ID, P_DATE, D_DATE, S_ODOMETER, E_ODOMETER, ODOMETER_LIMIT, VIN, DROP_LOC, PICKUP_LOC, INVO_ID, COUPON_ID, C_ID)
values(8,TO_DATE('04/13/2022','MM/DD/YYYY'),TO_DATE('04/22/2022','MM/DD/YYYY'),1400, 2000, 600, 1238674808, 8, 8, 1003030417, 000008,8);

insert into ZCQ_RENTAL_SERVICE(SERVICE_ID, P_DATE, D_DATE, S_ODOMETER, E_ODOMETER, ODOMETER_LIMIT, VIN, DROP_LOC, PICKUP_LOC, INVO_ID, COUPON_ID, C_ID)
values(9,TO_DATE('04/23/2022','MM/DD/YYYY'),TO_DATE('04/27/2022','MM/DD/YYYY'),2300, 3000, 900, 1238674809, 9, 9, 1003030418, 000009,9);

insert into ZCQ_RENTAL_SERVICE(SERVICE_ID, P_DATE, D_DATE, S_ODOMETER, E_ODOMETER, ODOMETER_LIMIT, VIN, DROP_LOC, PICKUP_LOC, INVO_ID, COUPON_ID, C_ID)
values(10,TO_DATE('05/01/2022','MM/DD/YYYY'),TO_DATE('05/10/2022','MM/DD/YYYY'),3000, 4200, 800, 1238674810, 10, 10, 1003030419, 000010,10);

-- Insert employee-corporate information (checked)
insert into  ZCQ_CORP_EMP(C_ID, EMPLOYEE_ID, CORP_ID) values(2, 000000001, 1);
insert into  ZCQ_CORP_EMP(C_ID, EMPLOYEE_ID, CORP_ID) values(4, 000000002, 2);
insert into  ZCQ_CORP_EMP(C_ID, EMPLOYEE_ID, CORP_ID) values(6, 000000003, 3);
insert into  ZCQ_CORP_EMP(C_ID, EMPLOYEE_ID, CORP_ID) values(8, 000000004, 4);
insert into  ZCQ_CORP_EMP(C_ID, EMPLOYEE_ID, CORP_ID) values(10, 000000005, 5);
insert into  ZCQ_CORP_EMP(C_ID, EMPLOYEE_ID, CORP_ID) values(12, 000000006, 6);
insert into  ZCQ_CORP_EMP(C_ID, EMPLOYEE_ID, CORP_ID) values(14, 000000007, 7);
insert into  ZCQ_CORP_EMP(C_ID, EMPLOYEE_ID, CORP_ID) values(16, 000000008, 8);
insert into  ZCQ_CORP_EMP(C_ID, EMPLOYEE_ID, CORP_ID) values(18, 000000009, 9);
insert into  ZCQ_CORP_EMP(C_ID, EMPLOYEE_ID, CORP_ID) values(20, 000000010, 10);

-- Insert payment information (checked)
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(1, TO_DATE('02/12/2022','MM/DD/YYYY'), 'C', 127.39, 5511321232412, 1003030410);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(2, TO_DATE('02/13/2022','MM/DD/YYYY'), 'C', 493.12, 5511321222413, 1003030411);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(3, TO_DATE('02/22/2022','MM/DD/YYYY'), 'C', 100.00, 5511321242414, 1003030412);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(4, TO_DATE('02/23/2022','MM/DD/YYYY'), 'C', 36.95, 5511321211412, 1003030412);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(5, TO_DATE('02/28/2022','MM/DD/YYYY'), 'D', 60.3, 5511321244127, 1003030413);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(6, TO_DATE('03/21/2022','MM/DD/YYYY'), 'D', 30.00, 5511321222432, 1003030414);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(7, TO_DATE('03/22/2022','MM/DD/YYYY'), 'D', 29.66, 5511321222429, 1003030414);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(8, TO_DATE('03/31/2022','MM/DD/YYYY'), 'D', 100.00, 551132124131, 1003030415);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(9, TO_DATE('04/01/2022','MM/DD/YYYY'), 'C', 85.07, 573212424132, 1003030415);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(10, TO_DATE('04/12/2022','MM/DD/YYYY'), 'C', 100.00, 551138224133, 1003030416);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(11, TO_DATE('04/13/2022','MM/DD/YYYY'), 'G', 60.12, 5511912224134, 1003030416);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(12, TO_DATE('04/23/2022','MM/DD/YYYY'), 'G', 422.02, 5517212224135, 1003030417);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(13, TO_DATE('04/29/2022','MM/DD/YYYY'), 'G', 379.61, 5543212424143, 1003030418);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(14, TO_DATE('05/12/2022','MM/DD/YYYY'), 'G', 100.00, 5713212434144, 1003030419);
insert into ZCQ_PAYMENT(PAY_ID, PAYMENT_DATE, METHOD, AMOUNT, CARD_NO, INVO_ID) values(15, TO_DATE('05/13/2022','MM/DD/YYYY'), 'G', 113.97, 5913212424145, 1003030419);

-- Insert coupon-customer information (checked)
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (1, 000001, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (2, 000001, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (3, 000001, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (4, 000002, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (5, 000003, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (6, 000003, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (7, 000004, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (8, 000005, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (9, 000006, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (10, 000007, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (11, 000008, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (12, 000008, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (13, 000009, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (14, 000010, 'I');
insert into ZCQ_COUPON_CUST(C_ID, COUPON_ID, COUPON_TYPE) values (15, 000010, 'I');

ALTER TABLE ZCQ_CORPORATE ADD CONSTRAINT C_CORP_NAME CHECK(CORP_NAME = UPPER(CORP_NAME));
ALTER TABLE ZCQ_VEHICLE_CLASS ADD CONSTRAINT C_RENTAL_RATE CHECK(RENTAL_RATE >= 0);
ALTER TABLE ZCQ_VEHICLE_CLASS ADD CONSTRAINT C_FEE CHECK(FEE >= 0);
ALTER TABLE ZCQ_RENTAL_SERVICE ADD CONSTRAINT C_S_ODOMETER CHECK (S_ODOMETER >= 0);
ALTER TABLE ZCQ_RENTAL_SERVICE ADD CONSTRAINT C_E_ODOMETER CHECK (E_ODOMETER <= 50000);
ALTER TABLE ZCQ_PAYMENT ADD CONSTRAINT C_METHOD CHECK (METHOD IN('C','D','G')); 
ALTER TABLE ZCQ_COUPON ADD CONSTRAINT C_DATE CHECK (E_DATE>=S_DATE);
ALTER TABLE ZCQ_COUPON ADD CONSTRAINT C_DISCOUNT CHECK(DISCOUNT >= 0);
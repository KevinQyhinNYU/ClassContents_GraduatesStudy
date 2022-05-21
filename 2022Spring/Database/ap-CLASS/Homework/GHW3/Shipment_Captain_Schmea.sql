REM   Script: Shipment_CASE_DDL
REM   Shipment_CASE_DDL

CREATE TABLE captain (
    captain_id           NUMBER(5) NOT NULL,
    captain_first_name   VARCHAR2(20) NOT NULL,
    captain_last_name    VARCHAR2(30) NOT NULL
);

ALTER TABLE captain ADD CONSTRAINT captain_pk PRIMARY KEY ( captain_id );

CREATE TABLE item (
    item_number   NUMBER(5) NOT NULL,
    item_type     VARCHAR2(10) NOT NULL,
    description   VARCHAR2(200) NOT NULL,
    weight        NUMBER(4) NOT NULL
);

ALTER TABLE item ADD CONSTRAINT item_pk PRIMARY KEY ( item_number );

CREATE TABLE shipment (
    shipment_id           NUMBER(6) NOT NULL,
    shipment_dt           DATE NOT NULL,
    expected_arrival_dt   DATE NOT NULL,
    origin                VARCHAR2(30) NOT NULL,
    destination           VARCHAR2(30) NOT NULL,
    ship_number           NUMBER(4) NOT NULL,
    captain_id            NUMBER(5) NOT NULL
);

ALTER TABLE shipment ADD CONSTRAINT shipment_pk PRIMARY KEY ( shipment_id );

CREATE TABLE shipment_item (
    quantity      NUMBER(6) NOT NULL,
    shipment_id   NUMBER(6) NOT NULL,
    item_number   NUMBER(5) NOT NULL
);

ALTER TABLE shipment_item ADD CONSTRAINT shipment_item_pk PRIMARY KEY ( shipment_id,
                                                                          item_number );

ALTER TABLE shipment
    ADD CONSTRAINT shipment_captain_fk FOREIGN KEY ( captain_id )
        REFERENCES captain ( captain_id );

ALTER TABLE shipment_item
    ADD CONSTRAINT shipment_item_item_fk FOREIGN KEY ( item_number )
        REFERENCES item ( item_number );

ALTER TABLE shipment_item
    ADD CONSTRAINT shipment_item_shipment_fk FOREIGN KEY ( shipment_id )
        REFERENCES shipment ( shipment_id );

REM   Script: Shipment_CASE_DML
REM   Shipment_CASE_DML

insert into captain(captain_id,captain_first_name,captain_last_name) values(10000,'Jayson','Tatum');

insert into captain(captain_id,captain_first_name,captain_last_name) values(10001,'Jaylen','Brown');

insert into captain(captain_id,captain_first_name,captain_last_name) values(10002,'Marcus','Smart');

insert into captain(captain_id,captain_first_name,captain_last_name) values(10003,'Gordon','Hayward');

insert into captain(captain_id,captain_first_name,captain_last_name) values(10004,'Daniel','Theis');

insert into captain(captain_id,captain_first_name,captain_last_name) values(10005,'Brad','Wanamaker');

insert into captain(captain_id,captain_first_name,captain_last_name) values(10006,'Grant','Williams');

insert into captain(captain_id,captain_first_name,captain_last_name) values(10007,'Romeo','Langford');

insert into captain(captain_id,captain_first_name,captain_last_name) values(10008,'Robert','Williams');

insert into captain(captain_id,captain_first_name,captain_last_name) values(10009,'Kemba','Walker');

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100000,date'2019-02-28',date'2019-03-12','Beijing','New York',200,10000);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100001,date'2019-03-28',date'2019-04-12','Boston','Los Angeles',254,10001);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100002,date'2017-12-28',date'2017-12-29','San Francisco','New York',2,10002);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100003,date'2020-02-28',date'2020-03-08','Shanghai','Dallas',45,10003);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100004,date'2020-01-01',date'2020-01-12','Atlanta','New York',200,10004);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100005,date'2019-02-28',date'2019-03-01','Utah','Houston',10,10005);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100006,date'2020-02-28',date'2019-03-01','Seattle','New York',4500,10006);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100007,date'2019-02-20',date'2019-02-22','Denver','New York',20,10007);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100008,date'2019-12-28',date'2019-12-29','Beijing','New York',5,10008);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100009,date'2017-01-28',date'2017-03-12','London','New York',20,10009);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100010,date'2019-10-10',date'2019-10-12','Paris','Bali',50,10000);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100011,date'2014-02-21',date'2015-03-12','Utah','New York',10,10000);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100012,date'2020-02-28',date'2020-02-29','Beijing','New York',4000,10001);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100013,date'2018-02-28',date'2019-01-12','Shanghai','Beijing',200,10003);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100014,date'2019-02-28',date'2019-04-12','Pheonix','Charlotte',190,10009);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100015,date'2012-02-27',date'2013-03-12','New Jersey','Houston',990,10007);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100016,date'2017-02-28',date'2017-12-12','Beijing','New Jersey',2000,10005);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100017,date'2016-02-28',date'2016-11-10','Arizona','New York',200,10000);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100018,date'2018-12-28',date'2018-12-30','Baltimore','New York',1900,10000);

insert into shipment(shipment_id,shipment_dt,expected_arrival_dt,origin,destination,ship_NUMBER,captain_id)
values(100019,date'2019-03-11',date'2019-03-12','Beijing','New York',1997,10005);

insert into item(item_NUMBER,item_type,description,weight) values(10000,'Medicine','Help people stay healthy','4000');

insert into item(item_NUMBER,item_type,description,weight) values(10001,'Masks','Prevent virus from spreading','200');

insert into item(item_NUMBER,item_type,description,weight) values(10002,'Toiletroll','Famous item recently','9999');

insert into item(item_NUMBER,item_type,description,weight) values(10003,'Keyboard','useful for students','100');

insert into item(item_NUMBER,item_type,description,weight) values(10004,'Mouse','Something or a kind of animal','300');

insert into item(item_NUMBER,item_type,description,weight) values(10005,'Panda','Rare animal','4700');

insert into item(item_NUMBER,item_type,description,weight) values(10006,'iPad','Can protect eyes','10');

insert into item(item_NUMBER,item_type,description,weight) values(10007,'Screen','We can watch games with it','90');

insert into item(item_NUMBER,item_type,description,weight) values(10008,'Basketball','A smaller globe','4000');

insert into item(item_NUMBER,item_type,description,weight) values(10009,'Toys','Make babies happy','9000');

insert into item(item_NUMBER,item_type,description,weight) values(10010,'Orange','Yellow and delicious','1');

insert into item(item_NUMBER,item_type,description,weight) values(10011,'Watermelon','Sweet melon','4000');

insert into item(item_NUMBER,item_type,description,weight) values(10012,'bamboorat','$3 for 1, $10 for 3','100');

insert into item(item_NUMBER,item_type,description,weight) values(10013,'Laptop','Smaller brain','990');

insert into item(item_NUMBER,item_type,description,weight) values(10014,'Duck','Not chicken','100');

insert into item(item_NUMBER,item_type,description,weight) values(10015,'CD','Give me a piece of old CD','1');

insert into item(item_NUMBER,item_type,description,weight) values(10016,'Arrow','Cupid likes it','4000');

insert into item(item_NUMBER,item_type,description,weight) values(10017,'Dog','Not cat','1');

insert into item(item_NUMBER,item_type,description,weight) values(10018,'Clothes','Nike Addidas Under Armor','1000');

insert into item(item_NUMBER,item_type,description,weight) values(10019,'Watches','Rolex makes millionnaires life boring','4000');

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(100,100000,10000);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(100,100001,10001);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(50,100002,10002);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(50,100003,10003);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(1,100004,10004);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(1,100005,10005);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(199,100006,10006);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(150,100007,10007);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(100,100008,10008);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(150,100009,10009);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(110,100010,10010);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(100,100011,10000);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(10,100012,10000);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(99,100013,10000);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(14,100014,10007);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(15,100015,10019);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(15,100016,10015);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(100,100017,10017);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(99,100018,10018);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(100,100019,10002);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(12,100001,10015);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(12,100001,10000);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(12,100003,10007);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(13,100016,10009);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(12,100007,10008);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(12,100009,10007);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(17,100015,10010);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(17,100011,10011);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(17,100019,10012);

insert into shipment_item(quantity,shipment_id,item_NUMBER) values(100,100000,10001);

commit;



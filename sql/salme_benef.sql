drop table govt.nuwakot_benef;
create table govt.nuwakot_benef
(
	master_serial varchar,
	district varchar,
	vdc_num varchar,
	vdc varchar,	
	ward varchar,
	tol varchar,
	reg_no varchar,
	cont_serial varchar,
	hoh_name varchar,
	hoh_gender varchar,
	enroll_type varchar
);


--this command won't work on the AWS RDS. http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Procedural.Importing.html
COPY govt.nuwakot_benef (master_serial,district,vdc_num,vdc,ward,tol,reg_no,cont_serial,hoh_name,hoh_gender,enroll_type)
FROM 'path' DELIMITER ',' CSV;

create schema if not exists surveys_edit;

drop table if exists surveys_edit.baseline_salme;
create table surveys_edit.baseline_salme 
select * from surveys.baseline_reconstruction b
LEFT JOIN 
(
	select
		master_serial as "govt_master_serial",
		district as "govt_district",
		vdc_num as "govt_vdc_num",
		vdc as "govt_vdc",
		ward as "govt_ward",
		tol as "govt_tol",
		reg_no as "govt_reg_no",
		cont_serial as "govt_cont_serial",
		hoh_name as "govt_hoh_name",
		hoh_gender as "govt_hoh_gender",
		enroll_type as "govt_enroll_type"
	from govt.nuwakot_benef) n
ON b.general_info_registration_number = n.govt_reg_no;

alter table surveys_edit.baseline_salme add PRIMARY KEY ("meta_instanceId");

select govt_reg_no, count(*) from surveys_edit.baseline_salme
group by 1;

--script to sync a new reg num in baseline data with govt data

UPDATE surveys_edit.baseline_salme 
SET general_info_registration_number = '124932'
WHERE general_info_registration_number = '124931';

UPDATE surveys_edit.baseline_salme base
SET govt_master_serial = gov.master_serial,
govt_district = gov.district,
govt_vdc_num = gov.vdc_num,
govt_ward = gov.ward,
govt_tol = gov.tol,
govt_reg_no = gov.reg_no,
govt_cont_serial = gov.cont_serial,
govt_hoh_name = gov.hoh_name,
govt_hoh_gender = gov.hoh_gender,
govt_enroll_type = gov.enroll_type
FROM govt.nuwakot_benef gov
WHERE gov.reg_no = '124932' AND base.general_info_registration_number = '124932'



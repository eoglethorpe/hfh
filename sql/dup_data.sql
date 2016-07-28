select * from
(
select way_id, device_id, count(*) as c from surveys.baseline_reconstruction
group by 1,2 
) a
where c > 1 and c < 5

--2
select * from surveys.baseline_reconstruction where way_id like '342038639'
http://hfh-omk.nl/omk/data/submissions/baseline_reconstruction/c40234f6-4c0a-4115-b38e-44ad6f2d0486/1467188775320.jpg
http://hfh-omk.nl/omk/data/submissions/baseline_reconstruction/99015bc9-1d8b-4492-9431-2916c955c7eb/1467425287997.jpg

--4
select local_osm_data from surveys.baseline_reconstruction where way_id like '341639168'
select * from surveys.baseline_reconstruction where image_house in ('1466911191345.jpg', '1466910388816.jpg')

1466911191345.jpg
1466910388816.jpg

--in device
select * from surveys.baseline_reconstruction where way_id in (
'341624463',
'341624462',
'341636452'
)
and device_id like '352975071660275'

341636449	2
342464375	2
341636445	2
341688129	2

--pull multiples
select general_info_registration_number, count(*) from surveys.baseline_reconstruction where way_id in 
(
select a.way_id from
(
select way_id, count(*) as c from surveys.baseline_reconstruction
group by 1
) a
where c > 1 and c < 5
)
group by 1

select device_id, count(*) from surveys.baseline_reconstruction group by 1
delimiter //
drop procedure if exists able_enroll //
create procedure able_enroll(
	in sid char(20),
	in y char(20),
	in sem char(20)
)
begin
select t1.UoSCode,t1.UoSName from unitofstudy t1,uosoffering t2, transcript t3, requires t4
where t2.Year=y and t2.Semester=sem
and t1.UoSCode=t2.UoSCode
and t3.StudId=sid
and t2.UoSCode= (select t4.UoSCode from t4 where t4.PrereqUoSCode=t3.UoSCode or t4.PrereqUoSCode=null)
and t3.Grade != null
and t2.Enrollment < t2.MaxEnrollment
;
end //
delimiter ;
call able_enroll('3213','2020','Q1');
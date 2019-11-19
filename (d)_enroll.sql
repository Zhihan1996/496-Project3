delimiter //
drop procedure if exists enroll_class //
create procedure enroll_class(
	in sid char(20),
    in cid char(20),
	in yr char(20),
	in sem char(20)
)
begin
insert into transcript values(sid,cid,sem,yr,null);
update uosoffering set Enrollment = Enrollment +1 where UoSCode = cid and Semester=sem and Year=yr;
end //
delimiter ;
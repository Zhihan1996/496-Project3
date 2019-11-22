delimiter //
drop procedure if exists transc //
create procedure transc(
	in sid char(20)
)
begin
select t.UoSCode,t.Grade from transcript t
where t.StudId=sid;
end //
delimiter ;
-- call transc('3213');
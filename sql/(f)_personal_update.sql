delimiter //
drop procedure if exists personal_update //
create procedure personal_update(
	in sid char(20),
	in p char(10),
	in addr char(50)
)
begin
update student set Address=addr where Id = sid;
update student set Password=p where Id = sid;
end //
delimiter ;
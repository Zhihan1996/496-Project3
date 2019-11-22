drop table if exists monitor;
create table monitor(item char(20) primary key,c integer);
insert into monitor values('mon',0);
update monitor set c=0 where item='mon';

delimiter //
drop trigger if exists enrollment_trigger //
create trigger enrollment_trigger
after update on uosoffering
for each row
begin
    if (new.MaxEnrollment > 2 * new.Enrollment)
    then update monitor set c=1 where item='mon';
    elseif(new.MaxEnrollment <= 2 * new.Enrollment)
    then update monitor set c=0 where item='mon';
    end if;
end //
delimiter ;
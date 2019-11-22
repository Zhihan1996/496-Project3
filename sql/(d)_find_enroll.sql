delimiter //
drop procedure if exists find_enroll //
create procedure find_enroll(
	in sid char(20),
	in y char(20),
	in sem char(20)
)
begin
select t1.UoSCode, t3.UoSName
from (uosoffering t1 left outer join(select * from transcript where StudId = sid  ) as t2 on t1.UoSCode = t2.UoSCode) left outer join
(requires t4 left outer join(select * from transcript where StudId = sid  ) as t5 on t5.UoSCode = t4.PrereqUoSCode) on t1.UoSCode=t4.UoSCode,
unitofstudy t3,lecture t6,classroom t7
where t1.Year = y and
t1.Semester = sem and
t3.UoSCode = t1.UoSCode and
t6.UoSCode = t1.UoSCode and
t7.ClassroomId = t6.ClassroomId and 
t6.Semester = sem and
t6.Year = y
and t4.PrereqUoSCode is null
union
select t1.UoSCode, t3.UoSName
from (uosoffering t1 left outer join(select * from transcript where StudId = sid  ) as t2 on t1.UoSCode = t2.UoSCode) left outer join
(requires t4 left outer join(select * from transcript where StudId = sid  ) as t5 on t5.UoSCode = t4.PrereqUoSCode) on t1.UoSCode=t4.UoSCode,
unitofstudy t3,lecture t6,classroom t7
where t1.Year = y and
t1.Semester = sem and
t3.UoSCode = t1.UoSCode and
t6.UoSCode = t1.UoSCode and
t7.ClassroomId = t6.ClassroomId and 
t6.Semester = sem and
t6.Year = y
and t5.Grade is not null
group by t1.UoSCode;
end //
-- call find_enroll('3213','2020','Q1');
-- call find_enroll('5123','2020','Q1');
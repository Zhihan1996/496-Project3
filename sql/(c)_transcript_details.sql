delimiter //
drop procedure if exists transcript_details //
create procedure transcript_details(
    in sid char(20),
    in cid char(20)
)
begin
select t1.UoSCode,t1.UoSName,t2.Year,t2.Semester, t3.Enrollment, t3.MaxEnrollment, t4.Name, t2.Grade
from unitofstudy t1,transcript t2,uosoffering t3, faculty t4
where t1.UoSCode=cid 
and t1.UoSCode=t2.UoSCode and t2.StudId=sid and t3.UoSCode=cid and t2.Semester=t3.Semester and t2.Year=t3.Year 
and t3.InstructorId=t4.Id;
end //
delimiter ;
-- call transcript_details('3213', 'COMP3419');
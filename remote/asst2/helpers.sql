-- COMP3311 21T3 Ass2 ... extra database definitions
-- add any views or functions you need into this file
-- note: it must load without error into a freshly created mymyunsw database
-- you must submit this even if you add nothing to it
-- COMP3311 21T3 Ass2 ... extra database definitions
-- add any views or functions you need into this file
-- note: it must load without error into a freshly created mymyunsw database
-- you must submit this even if you add nothing to it



CREATE TYPE TranscriptRecord_q3 AS (
    rule   VARCHAR(64),
    rule_id INTEGER,
	termId INTEGER,
	code CHAR(8),
	term CHAR(4),
	name text,
	mark INTEGER,
	grade CHAR(2),
	uoc INTEGER);



/*
CREATE TYPE TranscriptRecord_modified AS (
    termId INTEGER,
	code CHAR(8),
	term CHAR(4),
	name text,
	mark INTEGER,
	grade CHAR(2),
	uoc INTEGER);

CREATE TYPE GradeType AS enum
	('A', 'A+', 'A-', 'AF', 'AS', 'AW', 'B', 'B+', 'B-', 'C', 'C+',
	 'C-', 'CR', 'D', 'D+', 'D-', 'DN', 'E', 'E+', 'E-', 'EC',
	 'EM', 'F', 'FL', 'HD', 'NA', 'NC', 'NF', 'PE', 'PS', 'PW',
	 'RC', 'RD', 'RS', 'SY', 'UF', 'WD', 'WJ', 'XE');
*/
/*
CREATE TYPe course_enrolment AS (
    student INTEGER,
    course INTEGER,
    mark INTEGER,
    grade GradeType	
);*/

create or replace function
	Q1_helper(zid Integer) returns setof TranscriptRecord_modified
as $$
DECLARE

ret TranscriptRecord_modified;
curr course_enrolment;
course text;
mark Integer;
grade GradeType;
subject Integer;
term Integer;
code text;
courseCode text;
courseName text;
termId Integer;
uoc Integer;

BEGIN
   
	
	for curr in select *  from course_enrolments where student = zid
	loop		
		select c.subject,c.term into subject,term from courses as c where id = curr.course;

        	select t.id,t.code into termId,code from terms as t where id = term;

        	select s.code,name,s.uoc into courseCode,courseName,uoc from subjects as s where id = subject;
	
        select termId,courseCode,code,courseName,curr.mark,curr.grade,uoc into ret;
	return next ret;
	end loop;

	return;
end;
$$
language plpgsql;

--- function 1: return the rules
create or replace function
	get_rules(id_input Integer) returns setof rules
as $$
begin
		return query select * from rules as r where r.id = id_input;
end;
$$
language plpgsql;

-- function 2: return the reuslt of academic object group

create or replace function
	get_academic_object_groups(id_input Integer) returns setof Academic_object_groups
as $$
begin
		return query select * from academic_object_groups  as a where a.id  = id_input;
end;
$$
language plpgsql;


-- transcript is in place
-- this function will get all of the courses 
-- how to pass rule and rule id 
-- cc = [(name, rule,ruleId)]
create or replace function
	Q3_helper(zid Integer) returns setof TranscriptRecord_modified
as $$
DECLARE

ret TranscriptRecord_modified;
curr course_enrolment;
course text;
mark Integer;
grade GradeType;
subject Integer;
term Integer;
code text;
courseCode text;
courseName text;
termId Integer;
uoc Integer;
rule text;
rule_id Integer;

BEGIN
   
	
	for curr in select *  from course_enrolments where student = zid
	loop		
		select c.subject,c.term into subject,term from courses as c where id = curr.course;

        	select t.id,t.code into termId,code from terms as t where id = term;

        	select s.code,name,s.uoc into courseCode,courseName,uoc from subjects as s where id = subject;
	
        select termId,courseCode,code,courseName,curr.mark,curr.grade,uoc into ret;
	return next ret;
	end loop;

	return;
end;
$$
language plpgsql;



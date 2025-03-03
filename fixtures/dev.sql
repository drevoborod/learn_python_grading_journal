INSERT INTO public.educational_groups (id,name) VALUES
	 (1,'класс 1А'),
	 (2,'класс 1Б'),
	 (3,'2-й Бееее');

INSERT INTO public.pupils (id,first_name,last_name,second_name,birth_date,social_ensurance_id,educational_group_id) VALUES
	 (1,'Петя','Васечкин',NULL,NULL,NULL,1),
	 (2,'Вася','Петечкин',NULL,NULL,NULL,1),
	 (3,'Пися','Камушкин',NULL,NULL,NULL,2);


INSERT INTO public.educational_subjects (id,name) VALUES
	 (1,'Биология'),
	 (2,'География'),
	 (3,'Физика'),
	 (4,'Математика');

INSERT INTO public.educational_group_subjects (educational_subject_id,educational_group_id) VALUES
	 (1,1),
	 (2,1),
	 (3,2),
	 (4,2);

INSERT INTO public.grades (value,educational_subject_id,pupil_id,educational_group_id) VALUES
	 (5,2,1,1),
	 (4,3,1,1),
	 (1,3,1,1),
	 (2,4,3,2);


CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	username CHAR(16) NOT NULL,
	email CHAR(128),
	join_date DATE);

CREATE TABLE user_extras (
	user_id INT PRIMARY KEY,
	first_name CHAR(64),
	last_name CHAR(64),
	gender CHAR(1),
	skills TEXT,
	bio TEXT,
	projects TEXT,
	avatar CHAR(256)
	);

CREATE TABLE project_info (
	project_id SERIAL PRIMARY KEY,
	owner CHAR(16),
	title TEXT,
	short_desc TEXT,
	long_desc TEXT,
	skills_need TEXT,
	last_edit DATE
	);

CREATE TABLE project_extras (
	project_id INT,
	update TEXT,
	members TEXT,
	git_link CHAR(256)
	);

CREATE TABLE applications (
	project_id INT,
	user_id INT,
	status CHAR(16),
	date_applied DATE
	);

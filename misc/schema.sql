CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	username VARCHAR NOT NULL,
	email VARCHAR,
	join_date DATE
	);

CREATE TABLE user_extras (
	user_id INT PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	gender CHAR(1),
	bio TEXT,
	projects TEXT,
	avatar VARCHAR
	);

CREATE TABLE user_skills (
    user_id INT,
    skill TEXT
    );

CREATE TABLE project_info (
	project_id SERIAL PRIMARY KEY,
	owner VARCHAR,
	title TEXT,
	short_desc TEXT,
	long_desc TEXT,
	last_edit DATE,
	posted_date DATE
	);

CREATE TABLE project_skills (
    project_id INT,
    skill TEXT
    );

CREATE TABLE project_extras (
	project_id INT,
	update TEXT,
	members TEXT,
	git_link VARCHAR
	);

CREATE TABLE applications (
	project_id INT,
	user_id INT,
	status VARCHAR,
	date_applied DATE
	);

CREATE TABLE skills (
    name VARCHAR,
    approved BOOLEAN,
    count INT
    );

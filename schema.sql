drop table if exists users;
create table users (
	id integer primary key autoincrement,
	name text not null,
	access_token text not null
);

drop table if exists user;
create table user (
  id integer primary key autoincrement,
  email text not null,
  password text not null
);
insert into user (email, password) values ("sequ@me.com", "sequ");
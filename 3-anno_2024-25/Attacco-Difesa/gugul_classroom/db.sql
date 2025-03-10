create schema classroom;

create user 'classroom' identified by 'classroom';

grant all on classroom.* to 'classroom' with grant option;

create table classroom.assignments
(
    id     integer primary key auto_increment,
    name   varchar(256) unique,
    reward varchar(256)
);

create table classroom.tasks
(
    id           integer primary key auto_increment,
    assignment_id integer not null,
    question     varchar(1024),
    answer       varchar(256),

    foreign key (assignment_id) references classroom.assignments (id)
);
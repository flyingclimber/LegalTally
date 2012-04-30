drop table if exists tally;
create table tally (
    id integer primary key auto_increment,
    text varchar(255),
    count integer
);

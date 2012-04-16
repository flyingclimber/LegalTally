drop table if exists tally;
create table tally (
    id integer,
    received integer,
    denied integer
);
insert into tally values (1,0,0);

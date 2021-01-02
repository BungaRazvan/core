create table scrappers (
    id int(11) primary key not null auto_increment,
    provider varchar(30) not null,
    category varchar(30) not null,
    url mediumtext not null,
)

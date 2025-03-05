drop table if exists noaa_dscovr;
create table noaa_dscovr (
    id integer primary key autoincrement,
    time_tag datetime not null unique,
    speed float not null,
    density float not null,
    temperature float not null,
    bx float not null,
    by float not null,
    bz float not null,
    bt float not null,
    vx float,
    vy float,
    vz float,
    propagated_time_tag datetime not null,
    retention_period int
);

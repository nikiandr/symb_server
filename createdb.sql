create table Users(
    Id integer primary key,
    Nickname text unique,
    Password text
);

create table History(
    Id integer primary key,
    Request text,
    Response text,
    UserId integer
);

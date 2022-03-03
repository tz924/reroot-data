
CREATE TABLE stats
(
    stats_id            integer         not null,
    category_name       varchar(50)     null, 
    parameter_name      varchar(100)    null, 
    display_format      varchar(20)     null, 
    category            varchar(50)     null, 
    parameter           varchar(50)     null, 
    metric              varchar(50)     null, 
    data_variable       varchar(100)    null, 
    data_type           varchar(10)     null, 

    primary key (stats_id)
);

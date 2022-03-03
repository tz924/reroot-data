
CREATE TABLE parameters
(
    parameter_id    integer not null, 
    category_name varchar(50)   null, 
    parameter_name varchar(100) null, 
    option_name varchar(100)    null, 
    category    varchar(50)     null, 
    parameter   varchar(50)     null, 
    option      varchar(50)     null,
    data_variable   varchar(50) null,
    data_type   varchar(10)     null, 

    primary key(parameter_id)
);


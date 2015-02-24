

alter table person add column nickname varchar(16);
update person set nickname = 'Joe' where first_name = 'Joseph' and last_name = 'Young';
update person set nickname = 'Josh' where first_name = 'Joshua' and last_name = 'Kobrin';
update person set nickname = 'Jade', first_name = 'Jehbys' where first_name = 'Jade' and last_name = 'Hernandez';

-- Represents a user with email address [username]@tripadvisor.com
drop table if exists user;
create table user (
  id integer primary key autoincrement,
  username string not null,
);

-- Represents a merge machine as [hostname]@tripadvisor.com
drop table if exists machine;
create table machine (
  id integer primary key autoincrement,
  hostname string not null,
);

-- Represents an individual step in the merge process.
drop table if exists step;
create table step (
  id integer primary key autoincrement,
  name string not null,
);

-- Represents an the completion of a step on a machine.
drop table if exists event;
create table event (
  id integer primary key autoincrement,
  machine integer,
  step integer,
  clocktime integer,
);

-- Branch name, committer, and time of grab and ungrab.
-- step_grab may not be null; step_ungrab will be null until the machine is ungrabbed.
drop table if exists branch;
create table branch (
  id integer primary key autoincrement,
  name string,
  userldap string,
  step_grab integer,
  step_ungrab integer
);

-- Cached duration of the particular event.
-- Lazy table: can be calculated offline.
-- Calculated by this.timestamp - prev.timestamp
-- 'o' prefix indicates 'offline'; this table does not need to be up to date.
drop table if exists o_stepduration;
create table o_stepduration (
  id integer primary key autoincrement,
  event integer;
  time integer;
);

-- Current status of the merge machines
-- 'v' prefix indicates 'view'; this table summarizes data found elsewhere.
drop table if exists v_status;
create table v_status (
  machine integer,
  event integer
  branch integer
);

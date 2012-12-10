-- First-Class
-- Represents a user with email address [username]@tripadvisor.com
drop table if exists t_user;
create table t_user (
  id integer primary key autoincrement,
  username string not null
);

-- First-Class
-- Represents a merge machine as [hostname]@tripadvisor.com
drop table if exists t_machine;
create table t_machine (
  id integer primary key autoincrement,
  hostname string not null
);

-- First-Class
-- Represents an individual step in the merge process.
drop table if exists t_step;
create table t_step (
  id integer primary key autoincrement,
  name string not null
);

-- First-Class
-- Branch name and committer.
drop table if exists t_branch;
create table t_branch (
  id integer primary key autoincrement,
  name integer not null,
  user integer not null,
  FOREIGN KEY(user) REFERENCES t_user(id)
);

-- Represents an the completion of a step on a machine.
drop table if exists t_event;
create table t_event (
  id integer primary key autoincrement,
  branch integer not null,
  machine integer not null,
  step integer not null,
  clocktime integer not null,
  FOREIGN KEY(branch) REFERENCES t_branch(id)
  FOREIGN KEY(machine) REFERENCES t_machine(id),
  FOREIGN KEY(step) REFERENCES t_step(id)
);

-- Cached duration of the particular event.
-- Lazy table: can be calculated offline.
-- Calculated by this.timestamp - prev.timestamp
-- 'o' prefix indicates 'offline'; this table does not need to be up to date.
drop table if exists o_stepduration;
create table o_stepduration (
  id integer primary key autoincrement,
  event integer not null,
  time integer not null,
  FOREIGN KEY(event) REFERENCES t_event(id)  
);

-- Current status of the merge machines
-- 'v' prefix indicates 'view'; this table summarizes data found elsewhere.
drop table if exists v_status;
create table v_status (
  machine integer not null,
  event integer not null,
  branch integer not null,
  FOREIGN KEY(machine) REFERENCES t_machine(id),
  FOREIGN KEY(event) REFERENCES t_event(id),
  FOREIGN KEY(branch) REFERENCES t_branch(id)
);

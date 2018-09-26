# nameko-demo

The demo contacts service requires a `contacts` MySQL database table:

```
CREATE TABLE `contacts` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

Relevant libraries/code:
-  https://github.com/onefinestay/nameko-sqlalchemy
-  https://github.com/Overseas-Student-Living/nameko-salesforce
-  https://github.com/timbu/nameko-demo/blob/master/salesforce/source_tracker.py
-  https://github.com/etataurov/nameko-redis
-  https://github.com/Overseas-Student-Living/ddebounce
-  https://github.com/timbu/nameko-demo/blob/master/salesforce/tasks.py
-  https://github.com/nameko/nameko-amqp-retry
-  https://github.com/Overseas-Student-Living/nameko-tracer
-  https://github.com/timbu/nameko-autocrud
-  https://github.com/Overseas-Student-Living/sqlalchemy-filters
-  https://github.com/iky/nameko-slack

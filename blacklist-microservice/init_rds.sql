-- En RDS, la extensión se crea en la base de datos actual
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Solo si decides crear un usuario diferente al 'master' de AWS:
-- CREATE USER blacklist_user WITH PASSWORD 'tu_password';

GRANT ALL PRIVILEGES ON DATABASE blacklist_db TO blacklist_user;
GRANT USAGE ON SCHEMA public TO blacklist_user;
GRANT CREATE ON SCHEMA public TO blacklist_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO blacklist_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO blacklist_user;
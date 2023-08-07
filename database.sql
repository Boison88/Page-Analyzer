CREATE TABLE IF NOT EXISTS urls(
    id bigint GENERATED ALWAYS AS IDENTITY,
    name varchar(255) UNIQUE NOT NULL,
    created_at timestamp DEFAULT now(),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS url_checks(
    id bigint GENERATED ALWAYS AS IDENTITY,
    url_id bigint,
    status_code integer,
    h1 varchar(255),
    title varchar(255),
    description varchar(255),
    created_at timestamp DEFAULT now(),
    PRIMARY KEY(id),
    CONSTRAINT url_checks_url_id_fk
        FOREIGN KEY(url_id)
        REFERENCES urls(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

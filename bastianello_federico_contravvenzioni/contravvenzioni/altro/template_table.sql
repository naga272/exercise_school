CREATE TABLE IF NOT EXISTS vigile(
    nome        varchar(32)   not null,
    cognome     varchar(32)   not null,
    matricola   varchar(32)   not null,
    PRIMARY KEY(matricola),
    FOREIGN KEY (matricola) REFERENCES contravvenzione(matricola)
);


CREATE TABLE IF NOT EXISTS guidatore(
    cod_fisc    varchar(32) not null,    
    nome        varchar(32) not null,
    cognome     varchar(32) not null,
    PRIMARY KEY(cod_fisc),
    FOREIGN KEY(cod_fisc) REFERENCES contravvenzione(cod_fisc)
);


CREATE TABLE IF NOT EXISTS autovettura(
    targa       varchar(32) not null,
    colore      varchar(32) not null,

    PRIMARY KEY(targa),
    FOREIGN KEY(targa) REFERENCES contravvenzione(targa)
);


CREATE TABLE IF NOT EXISTS contravvenzione(
    matricola           varchar(32) not null,
    targa               varchar(32) not null,
    cod_fisc            varchar(32) not null,
    YYYY_MM_DD_HH_mm_SS varchar(32) not null,
    import              INTEGER not null,
    PRIMARY KEY(matricola, targa, cod_fisc)
);
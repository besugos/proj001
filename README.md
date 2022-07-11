# proj001

1 - instalar o docker:
  
  sudo apt update

  sudo apt install apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release

  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

  echo   "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  sudo apt update

  sudo apt install docker-ce  

  sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose  
  
  sudo chmod +x /usr/local/bin/docker-compose  




2 - instalar o postgres:

sudo docker pull postgres:latest
sudo docker run --name proj001 -e POSTGRES_PASSWORD=root -d postgres:latest
sudo docker exec proj001 psql -c "CREATE DATABASE projeto001" -U postgres
docker commit proj001 db-proj001:0.1
sudo docker run --name proj001 --restart always -v $HOME/banco-postgres:/var/lib/postgresql/data -p5432:5432 -e POSTGRES_PASSWORD=root -d db-proj001:0.1


3 - clone o projeto com:
git@github.com:besugos/proj001.git


4 - faça o build do docker:
docker build -t api_proj001:0.3 .


5 - rode o docker compose para criar a relação entre os dockers e executá-los:
docker-compose up -d


6 - abra o projeto no Pycharm e configure o banco na aba Database, com os seguintes parâmetros:
    Host: localhost
    Port: 5432
    User: postgres
    Password: root
    Database: projeto001


7 - Clicar ao lado de "projeto001", onde estará "0 of 2" e selecionar o schema proj001


8 - Clicar com o botão direito em proj001 --> New --> Query console


9 - rodar o script sql abaixo


create table author
(
    author_id serial
        constraint author_pk
            primary key,
    name      varchar,
    picture   varchar
);

alter table author
    owner to postgres;

create table "user"
(
    user_id  serial
        constraint user_pk
            primary key,
    username varchar,
    password varchar,
    type     varchar
);

alter table "user"
    owner to postgres;

create table paper
(
    paper_id        serial
        constraint paper_pk
            primary key,
    category        varchar,
    title           varchar,
    summary         text,
    first_paragraph text,
    body            text,
    author_id       integer not null
);

alter table paper
    owner to postgres;


10 - Pronto, a api está pronta para ser utilizada em localhost:8002. Para a documentação dos endpoints da api, acesso localhost:8002/docs

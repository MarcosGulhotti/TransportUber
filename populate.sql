INSERT INTO usuarios (nome, sobrenome, cpf, email, celular, password_hash, usuario_ativo)
VALUES (
  'Rogerio',
  'Gavia',
  '990.123.254-17',
  'teste@email.com',
  '(48)99988-0099',
  '7878#&$&*$&123',
  'TRUE'
);

INSERT INTO motoristas (nome, sobrenome, email, celular, cpf, cnh, password_hash, motorista_ativo)
VALUES (
  'Daniel',
  'Lambert',
  'tonhao@mail.com',
  '(48)99988-4455'
  '970.124.243-18',
  '00021548729',
  '1234$$$$123',
  'TRUE'
);

INSERT INTO caminhoes (marca, modelo, capacidade_de_carga, motorista_id, placa)
VALUES (
  'Volvo',
  'Volvo FX',
  90.00,
  (SELECT id FROM motoristas WHERE cpf='970.124.243-18'),
  'ZZZ-1342'
);

INSERT INTO categorias (nome)
VALUES (
  'Moveis domesticos'
);

INSERT INTO cargas (disponivel, destino, origem, dono_id, volume)
VALUES (
  'TRUE',
  'ABC Paulista',
  'Curitiba',
  (SELECT id FROM usuarios WHERE cpf='990.123.254-17'),
  999.52
);

INSERT INTO cargas_categorias (categoria_id, carga_id)
VALUES (
  (SELECT id FROM categorias WHERE nome='Moveis domesticos'),
  (SELECT id FROM cargas WHERE volume=999.52)
);
SET TERM ^ ;

create or alter procedure GERAR_REQUISICAO (
    CODCLIENTE varchar(8),
    PEDIDO varchar(18),
    NPEDIDOGMSAP varchar(8),
    PECA varchar(30),
    QTD integer not null)
as
declare variable CD_REQ integer;
declare variable DATA_HOJE date;
declare variable HORA_HOJE time;
declare variable DATAATUAL timestamp;
declare variable ID_CLIENTE_REQ integer;
declare variable ID_PRODUTO numeric(0,0);
declare variable DESCRICAO varchar(190);
declare variable ID_ITEM integer;
declare variable VALOR_UNITARIO CURRENCY;
declare variable VALOR_REQ CURRENCY;
declare variable REF varchar(15);
declare variable CODIGO_FAB varchar(20);
declare variable MARCA varchar(50);
declare variable CODIGO_BARRA varchar(40);
BEGIN
    dataAtual = CURRENT_TIMESTAMP;
    DATA_HOJE = CURRENT_DATE;
    HORA_HOJE = CURRENT_TIME;
    SELECT MAX(ID_ITEM) FROM REQUISICOES_ITENS INTO :ID_ITEM;
    ID_ITEM = COALESCE(ID_ITEM, 0) + 1;


    SELECT ID_PRODUTO FROM produtos p WHERE p.codigo_fab = :PECA ORDER BY descricao rows 1 INTO :ID_PRODUTO;
    SELECT DESCRICAO FROM produtos p WHERE p.codigo_fab = :PECA ORDER BY descricao rows 1 INTO :DESCRICAO;
    SELECT PRECO_TABELA FROM PRODUTO_PRECOS p WHERE p.ID_PRODUTO = :ID_PRODUTO INTO :VALOR_UNITARIO;
    SELECT REF FROM produtos p WHERE p.codigo_fab = :PECA ORDER BY descricao rows 1 INTO :REF;
    SELECT CODIGO_FAB FROM produtos p WHERE p.codigo_fab = :PECA ORDER BY descricao rows 1 INTO :CODIGO_FAB;
    SELECT MARCA FROM produtos p WHERE p.codigo_fab = :PECA ORDER BY descricao rows 1 INTO :MARCA;
    SELECT CODIGO_BARRA FROM produtos p WHERE p.codigo_fab = :PECA ORDER BY descricao rows 1 INTO :CODIGO_BARRA;
    SELECT ID_CLIENTE FROM CLIENTES c where c.DOC_EX = :CODCLIENTE ORDER BY NOME rows 1 INTO :ID_CLIENTE_REQ;
    SELECT MAX(ID_REQUISICAO) FROM REQUISICOES INTO :CD_REQ;
    CD_REQ = COALESCE(CD_REQ, 0) + 1;
    VALOR_REQ = :VALOR_UNITARIO*QTD;


    INSERT INTO REQUISICOES (
        ID_REQUISICAO,
        ES,
        ID_CLIENTE,
        DATA_EMISSAO,
        HORA_EMISSAO,
        NUMERO,
        ID_FUNCIONARIO,
        PEDIDO,
        VALOR_REQUISICAO,
        ID_VEICULO,
        ID_DEPTO,
        COTACAO,
        STATUS,
        VEICULO,
        PLACA,
        ITENS,
        ENTREGUE
    ) VALUES (
        :CD_REQ,
        1,
        :ID_CLIENTE_REQ,
        :DATA_HOJE,
        :HORA_HOJE,
        NULL,
        1,
        :PEDIDO,
        :VALOR_REQ,
        NULL,
        1,
        0,
        1,
        NULL,
        :NPEDIDOGMSAP,
        1,
        0
    );

    INSERT INTO REQUISICOES_ITENS (
        ID_REQUISICAO, 
        ID_ITEM, 
        ID_PRODUTO, 
        DESCRICAO, 
        QTDE, 
        VALOR_UNITARIO, 
        REF, 
        DADOS, 
        CODIGO_FAB, 
        MARCA, 
        CODIGO_BARRA, 
        ENTREGAR, 
        ENTREGUE, 
        DATA_ENTREGA
    ) 
    VALUES (
        :CD_REQ, 
        :ID_ITEM, 
        :ID_PRODUTO, 
        :DESCRICAO, 
        :QTD, 
        :VALOR_UNITARIO, 
        :REF, 
        NULL, 
        :CODIGO_FAB, 
        :MARCA, 
        :CODIGO_BARRA, 
        :QTD, 
        0, 
        NULL
    );

END^

SET TERM ; ^

/* Following GRANT statetements are generated automatically */

GRANT SELECT,INSERT ON REQUISICOES_ITENS TO PROCEDURE GERAR_REQUISICAO;
GRANT SELECT ON PRODUTOS TO PROCEDURE GERAR_REQUISICAO;
GRANT SELECT ON PRODUTO_PRECOS TO PROCEDURE GERAR_REQUISICAO;
GRANT SELECT ON CLIENTES TO PROCEDURE GERAR_REQUISICAO;
GRANT SELECT,INSERT ON REQUISICOES TO PROCEDURE GERAR_REQUISICAO;

/* Existing privileges on this procedure */

GRANT EXECUTE ON PROCEDURE GERAR_REQUISICAO TO SYSDBA;

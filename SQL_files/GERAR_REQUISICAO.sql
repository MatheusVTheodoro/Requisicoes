SET TERM ^ ;

CREATE OR ALTER PROCEDURE GERAR_REQUISICAO (
    CODCLIENTE         VARCHAR(8),
    PEDIDO             VARCHAR(18),
    NPEDIDOGMSAP       VARCHAR(20))
AS
DECLARE VARIABLE CD_REQ INTEGER;
DECLARE VARIABLE DATA_HOJE DATE;
DECLARE VARIABLE HORA_HOJE TIME;
DECLARE VARIABLE dataAtual TIMESTAMP;
DECLARE VARIABLE ID_CLIENTE_REQ INTEGER;

BEGIN
    dataAtual = CURRENT_TIMESTAMP;
    DATA_HOJE = CURRENT_DATE;
    HORA_HOJE = CURRENT_TIME;




    SELECT ID_CLIENTE FROM CLIENTES c where c.DOC_EX = :CODCLIENTE INTO :ID_CLIENTE_REQ;
    SELECT MAX(ID_REQUISICAO) FROM REQUISICOES INTO :CD_REQ;
    CD_REQ = COALESCE(CD_REQ, 0) + 1;

    INSERT INTO REQUISICOES (
        ID_REQUISICAO,
        ES,
        ID_CLIENTE,
        DATA_EMISSAO,
        HORA_EMISSAO,
        NUMERO,
        ID_FUNCIONARIO,
        PEDIDO,
        OBS,
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
        2,
        :ID_CLIENTE_REQ,
        :DATA_HOJE,
        :HORA_HOJE,
        NULL,
        NULL,
        :PEDIDO,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL
    );

END^

SET TERM ; ^

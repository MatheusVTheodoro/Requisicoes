CREATE OR ALTER PROCEDURE GERAR_REQUISICAO_ITENS (
    ID_CLIENTE INTEGER,
    ID_ITEM INTEGER NOT NULL,
    ENTREGAR FLOAT
)
AS
BEGIN
    DECLARE VARIABLE CD_REQ INTEGER;
    
    SELECT MAX(ID_REQUISICAO) 
    FROM REQUISICOES 
    INTO :CD_REQ;
    
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
        NULL, 
        NULL, 
        NULL, 
        NULL, 
        NULL, 
        NULL, 
        NULL, 
        NULL, 
        NULL, 
        :ENTREGAR, 
        NULL, 
        NULL
    );
END^

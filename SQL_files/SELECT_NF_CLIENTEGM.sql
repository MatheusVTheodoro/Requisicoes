SELECT * FROM nota_fiscal JOIN clientes ON nota_fiscal.id_cliente = clientes.id_cliente WHERE clientes.DOC_EX IS NOT NULL;


SELECT nf.NOTA_FISCAL, nf.DATA_EMISSAO, nf.ID_PEDIDO, c.CPF_CNPJ, c.NOME, c.NOME_FANTASIA, reg.cidade, reg.uf, nf.NFE_CHAVE, nf.VALOR_TOTAL
FROM clientes c
JOIN clientes_enderecos ce ON c.id_cliente = ce.id_cliente
JOIN nota_fiscal nf ON nf.id_cliente = c.id_cliente
join regioes reg ON reg.id_regiao = c.id_regiao
WHERE c.DOC_EX IS NOT NULL;
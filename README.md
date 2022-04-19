# DESAFIO_ROIT

O codigo foi desenvolvido em três etapas:

1 - Analise das bases;
2 - Enriquecimento das bases, correção de inconsistecias e criação de DataBase de CNAEs secundarios;
3 - Criação de Database em SQL e desenvolvimento das VIEWs

ESTABELECMENTOS.CSV

**Primeira Etapa** - Python
A primeira parte foi abrir ambos os CSVs em excel e anotar onde tivemos iconsistecias e quais dados poderiam ser substituidos por outros ou teriam que ser removidos da base de dados, foi concluido que a coluna de CNPJ_BASICO que estavam vazias ou com a quantidade de caracteres diferentes de 8 deveriam ser removidos da database e que a coluna de END_UF poderia ser enriquecida utilizando a coluna de END_CEP, além de que deveriam ser realizadas uma série de formatações nas colunas para deixar os dados limpos.

**Segunda Etapa** - Python
Para esse etapa foi utilizado a linguagem Python com as bibliotecas, Pandas e NumPy. Foi transformado o Arquivo CSV em um DataFrame para que fossem realizadas a formatação e limpeza dos dados, a primeira etapa foi criar uma coluna auxiliar para ver quais CNPJs são validos e poderiam ser utilizado, foi utilizado as colunas de cnpj_basico, cnpj_ordem, cnpj_dv, a coluna de cnpj_ordem foi formatada para que todas as strings que tivessem menos de 4 caracteres fossem completas com 0 a até que fossem completas, todos os CNPJs com a quantidade de caracteres diferentes de 14 foram removidos. Na segunda parte foi realizado o processo de enriquecimento dos dados através dos CEPs validos, então foram verificados quais CEPs tinham o numero de caracteres correto assim criando outro DataFrame com as colunas end_cep e end_uf, nesse DataFrame a coluna de end_uf foi checada com o auxilio de um DataFrame de UFs_VALIDOS, então sobrando assim apenas os CEPs com UFs validos, então foi feito um verificação e substituição de dados com os mesmos CEPs por UFs do DataFrame de suporte com os CEPs validos. Terceira etapa foi a criação da DataBase de CNAEs secundarios então primeiro separei dentro de uma sequiencia matricial onde os numeros de CNAE foram separados por ',' e '|', e assim tambem criando um novo DataFrame com apenas os codigos CNAE secundarios separados, depois nesse DataFrame foram adicionadas as colunas de cod_cnae_primeiro e cnpj_basico nesse DataFrame que foi chamado de cnae_df_b. A ultima etapa foi limpar os dados, então com a analise da primeira parte, comecei a formatar coluna por coluna vendo o que poderia ser padronizado. Então foram processados 2 DataFrames para CSV um contendos o cod_cnae_secundarios com os cnpj_basico o outro com a DataBase estabelecimentos tratada.

ESTABELECMENTOS.CSV
Após analise dessa base de dados não foram achadas inconsistencias com os dados então não foram realizados nenhum tipo de procedimento.

**Terceira Etapa**
Primeira etapa foi a Criação da DataBase no SQL, após isso foi feito o upload das 3 bases de dados (cod_cnae_secundarios, Estabelecimentos e empresas), através da ferramenta de import e export do SQL Managment Studio, então foram criadas as VIEWs conforme foram pedidas.

SUMARO VIEWS

3.1 quantidade_cnpj_sem_cnae_secundario  
3.2 QTDE_ESTAB_C_CNAE_4530703 
3.3 QTDE_ESTAB_C_CNAE_4530703_EM_EMPRESAS  
3.4 TOP10_ESTABELECIMENTOS_COM_MAIS_CNAE_SECUNDARIO 

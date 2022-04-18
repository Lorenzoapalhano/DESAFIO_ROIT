import pandas as pd
import numpy as np
import openpyxl

estabelecimentos_path = r"C:\Users\Lorenzo-pc\Desktop\estab-part-00.csv"
empresas_path = r"C:\Users\Lorenzo-pc\Desktop\empresa-part-00.csv"

## Estabelecimentos
cnae_df = pd.DataFrame()
cnae_df_b = pd.DataFrame()
cep_df_valido = pd.DataFrame()
cep_df_valido_2= pd.DataFrame()
sql_carga_estab = pd.DataFrame()

#Organizar lista com todos os UFs e transformar em DataFrames
uf_data = {'end_uf' : ['RO','AC','AM','RR','PA','AP','TO','MA','PI','CE','RN','PB','PE','AL','SE','BA','MG','ES','RJ','SP','PR','SC','RS','MS','MT','GO','DF'],
            'Stats' : ['valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido','valido']}
uf_df = pd.DataFrame(uf_data)
uf_df['end_uf'] = uf_df['end_uf'].astype(str)

#Ler CSV e transformar em DataFrame
estabelecimentos_df = pd.read_csv(estabelecimentos_path)

#Trandformações para enriquecer e limpar o DataFrame
estabelecimentos_df = estabelecimentos_df.dropna(subset=['nome_fantasia','cnpj_basico'])
estabelecimentos_df = estabelecimentos_df.drop(estabelecimentos_df[estabelecimentos_df.cnpj_basico == 'vazio'].index)
estabelecimentos_df['cnpj_ordem'] = estabelecimentos_df['cnpj_ordem'].apply(lambda x: '{0:0>4}'.format(x))
estabelecimentos_df['cnpj_completo'] = estabelecimentos_df['cnpj_basico'].apply(str) + estabelecimentos_df['cnpj_ordem'].apply(str) + estabelecimentos_df['cnpj_dv'].apply(str)
estabelecimentos_df['len_cnpj'] = estabelecimentos_df['cnpj_completo'].str.len()
estabelecimentos_df = estabelecimentos_df.drop(estabelecimentos_df[(estabelecimentos_df.len_cnpj != 14)].index)
estabelecimentos_df['end_uf'] = estabelecimentos_df['end_uf'].str.upper()
estabelecimentos_df_2 = estabelecimentos_df.merge(uf_df, on='end_uf', how='left')
estabelecimentos_df_2['Stats'] = estabelecimentos_df_2['Stats'].fillna('invalido')

#Lista de CEPs com UFs validos
cep_df_valido = estabelecimentos_df_2[estabelecimentos_df_2['Stats'] =='valido']
cep_df_valido_2['end_cep'] = cep_df_valido['end_cep']
cep_df_valido_2['end_uf'] = cep_df_valido['end_uf']
cep_df_valido_2 = cep_df_valido_2.drop_duplicates()

#Substituindo UFs invalidos pelos validos
estabelecimentos_df_val = estabelecimentos_df_2[estabelecimentos_df_2['Stats'] =='valido']
estabelecimentos_df_in = estabelecimentos_df_2[estabelecimentos_df_2['Stats'] =='invalido']
estabelecimentos_df_in = estabelecimentos_df_in.merge(cep_df_valido_2, on= 'end_cep', how= 'outer')
estabelecimentos_df_in['end_uf_x'] = estabelecimentos_df_in['end_uf_y']
estabelecimentos_df_in = estabelecimentos_df_in.dropna(subset= ['end_uf_x','cnpj_basico'])
estabelecimentos_df_in = estabelecimentos_df_in.drop(['end_uf_y'],axis=1)
estabelecimentos_df_in = estabelecimentos_df_in.rename({'end_uf_x' : 'end_uf'} , axis = 1)
sql_carga_estab = pd.concat([estabelecimentos_df_val, estabelecimentos_df_in], axis=0)
sql_carga_estab = sql_carga_estab.drop(['Stats','len_cnpj'],axis=1)

#Transformando os CNAEs secundarios em tabelas e procurando os primarios correspondentes
cnae_df['cod_cnae_fiscal_primaria'] = estabelecimentos_df['cod_cnae_fiscal_primaria']
cnae_df['cod_cnae_fiscal_secundaria'] = estabelecimentos_df['cod_cnae_fiscal_secundaria']
cnae_df['cnpj_basico'] = estabelecimentos_df['cnpj_basico']
cnae_df['index1'] = cnae_df.index
cnae_df_b = pd.DataFrame(cnae_df['cod_cnae_fiscal_secundaria'].str.split(',').explode())
cnae_df_b = pd.DataFrame(cnae_df_b['cod_cnae_fiscal_secundaria'].str.split('|').explode())
cnae_df_b['index1'] = cnae_df_b.index
cnae_df_b = cnae_df_b.merge(cnae_df, on='index1', how='left')
cnae_df_b = cnae_df_b.drop(['index1','cod_cnae_fiscal_secundaria_y'], axis=1)
cnae_df_b = cnae_df_b[['cnpj_basico','cod_cnae_fiscal_primaria','cod_cnae_fiscal_secundaria_x']]
cnae_df_b = cnae_df_b.rename({'cod_cnae_fiscal_secundaria_x' : 'cod_cnae_fiscal_secundaria'} , axis = 1)
cnae_df_b['cod_cnae_fiscal_secundaria'] = pd.to_numeric(cnae_df_b.cod_cnae_fiscal_secundaria.astype(str), errors='coerce').fillna(0).astype(int).astype(str)

#formatações
sql_carga_estab = sql_carga_estab.replace(r'\s+', ' ', regex=True)
sql_carga_estab['cnpj_basico'] = sql_carga_estab['cnpj_basico'].astype(int).round(decimals=1)
sql_carga_estab['cnpj_ordem'] = sql_carga_estab['cnpj_ordem'].astype(int).round(decimals=1)
sql_carga_estab['cnpj_dv'] = sql_carga_estab['cnpj_dv'].astype(int).round(decimals=1)
sql_carga_estab['cod_identificador_matriz_filial'] = sql_carga_estab['cod_identificador_matriz_filial'].astype(int).round(decimals=1)
sql_carga_estab['nome_fantasia'] = sql_carga_estab['nome_fantasia'].astype(str).replace(r'\W+', ' ', regex=True)
sql_carga_estab['cod_situacao_cadastral'] =sql_carga_estab['cod_situacao_cadastral'].astype(int).round(decimals=1)
sql_carga_estab['data_situacao_cadastral'] = pd.to_datetime(sql_carga_estab['data_situacao_cadastral'].astype(str), format='%Y%m%d')
sql_carga_estab['cod_motivo_situacao_cadastral'] = sql_carga_estab['cod_motivo_situacao_cadastral'].astype(int).round(decimals=1)
sql_carga_estab['end_nome_cidade_no_exterior'] = sql_carga_estab['end_nome_cidade_no_exterior'].astype(str)
sql_carga_estab['end_cod_pais'] = sql_carga_estab['end_cod_pais'].astype(str)
sql_carga_estab['data_inicio_atividade'] = pd.to_datetime(sql_carga_estab['data_inicio_atividade'].astype(str), format='%Y%m%d')
sql_carga_estab['cod_cnae_fiscal_primaria'] = sql_carga_estab['cod_cnae_fiscal_primaria'].astype(int).round(decimals=1)
sql_carga_estab['end_tipo_de_logradouro'] = sql_carga_estab['end_tipo_de_logradouro'].astype(str)
sql_carga_estab['end_tipo_de_logradouro'] = sql_carga_estab['end_tipo_de_logradouro'].str.replace('\d+', ' ').str.replace(' A ', '').str.replace(' O ', '')
sql_carga_estab['end_logradouro'] = sql_carga_estab['end_logradouro'].astype(str).str.upper()
sql_carga_estab['end_numero'] = pd.to_numeric(sql_carga_estab['end_numero'],errors= 'coerce')
sql_carga_estab['end_numero'] = sql_carga_estab['end_numero'].fillna(0).astype(int).round().astype(str).replace('0','')
sql_carga_estab['end_complemento'] = sql_carga_estab['end_complemento'].astype(str).str.strip().str.replace('vazio',"").str.replace('em branco','').str.replace('test','')
sql_carga_estab['end_bairro'] = sql_carga_estab['end_bairro'].astype(str).str.upper().replace('.','')
sql_carga_estab['end_cep'] = sql_carga_estab['end_cep'].astype(int).round(decimals=1)
sql_carga_estab['end_uf'] = sql_carga_estab['end_uf'].astype(str)
sql_carga_estab['end_cod_municipio'] = sql_carga_estab['end_cod_municipio'].astype(int).round(decimals=1)
sql_carga_estab['ddd1'] = pd.to_numeric(sql_carga_estab['ddd1'],errors='coerce',downcast= 'integer')
sql_carga_estab['ddd1'] = np.where(sql_carga_estab['ddd1']>100,'',sql_carga_estab['ddd1'])
sql_carga_estab['ddd1'] = sql_carga_estab['ddd1'].astype(str).str.replace('.0','').str.replace('nan','')
sql_carga_estab['telefone1'] = pd.to_numeric(sql_carga_estab['telefone1'],errors= 'coerce',downcast= 'integer')
sql_carga_estab['telefone1'] = sql_carga_estab['telefone1'].fillna(0).astype(int).round().astype(str).replace('0','')
sql_carga_estab['ddd2'] = pd.to_numeric(sql_carga_estab['ddd2'],errors='coerce',downcast= 'integer')
sql_carga_estab['ddd2'] = np.where(sql_carga_estab['ddd2']>100,'',sql_carga_estab['ddd2'])
sql_carga_estab['ddd2'] = sql_carga_estab['ddd2'].astype(str).str.replace('.0','').str.replace('nan','')
sql_carga_estab['telefone2'] = pd.to_numeric(sql_carga_estab['telefone2'],errors= 'coerce',downcast= 'integer')
sql_carga_estab['telefone2'] = sql_carga_estab['telefone2'].fillna(0).astype(int).round().astype(str).replace('0','')
sql_carga_estab['dddfax'] = pd.to_numeric(sql_carga_estab['dddfax'],errors= 'coerce',downcast= 'integer')
sql_carga_estab['dddfax'] = sql_carga_estab['dddfax'].astype(str).str.replace('.0','').str.replace('nan','')
sql_carga_estab['fax'] = pd.to_numeric(sql_carga_estab['fax'],errors= 'coerce',downcast= 'integer')
sql_carga_estab['fax'] = sql_carga_estab['fax'].astype(str).str.replace('.0','').str.replace('nan','')
sql_carga_estab['email'] = sql_carga_estab['email'].str.lower()
sql_carga_estab['email'] = np.where(sql_carga_estab['email'].str.contains('@'),sql_carga_estab['email'],'')
sql_carga_estab['cod_situacao_especial'] = sql_carga_estab['cod_situacao_especial'].astype(str).str.replace('nulo',"").str.replace('em branco','')
sql_carga_estab['data_situacao_especial'] = sql_carga_estab['data_situacao_especial'].astype(str)
sql_carga_estab = sql_carga_estab.replace('nan','')
sql_carga_estab = sql_carga_estab.drop(['cod_cnae_fiscal_secundaria'],axis=1)
sql_carga_estab = sql_carga_estab.round()

#Preparando arquivos CSVs para carga no SQL
sql_carga_estab.to_csv(r'D:\sql_estab.csv', index=False)
cnae_df_b.to_csv(r'D:\sql_cnae.csv', index=False)

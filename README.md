# KMZ to Shapefile Converter (Multi-layer & Topology Repair)

Este projeto automatiza a conversão de arquivos KMZ (KML compactados) para o formato ESRI Shapefile usando Python.

##  Funcionalidades
- **Extração Automática:** Descompacta arquivos KMZ e localiza o KML interno.
- **Multi-camadas:** Identifica e processa todas as camadas presentes no arquivo original.
- **Correção Topológica:** Utiliza `shapely.validation.make_valid` para corrigir geometrias inválidas (como auto-interseções) antes da exportação.
- **Saída Pronta:** Agrupa todos os componentes do Shapefile (.shp, .shx, .dbf, .prj) em um arquivo ZIP para download.

##  Tecnologias
- [GeoPandas](https://geopandas.org/)
- [Fiona](https://fiona.readthedocs.io/)
- [Shapely](https://shapely.readthedocs.io/)

##  Como usar
1. Faça o upload do seu arquivo `.kmz` para o ambiente.
2. Execute a função `extrair_e_converter_kmz('nome_do_seu_arquivo.kmz')`.
3. Baixe o arquivo `shapefiles_resultado.zip` gerado.

import os
import zipfile
import shutil
import geopandas as gpd
import fiona
from shapely.validation import make_valid

# Habilitar o suporte a KML/LIBKML no Fiona
fiona.drvsupport.supported_drivers['KML'] = 'rw'
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

def extrair_e_converter_kmz(kmz_path, output_zip="shapefiles_resultado.zip"):
    temp_dir = "temp_kmz_extract"
    shp_dir = "output_shapefiles"
    
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(shp_dir, exist_ok=True)

    # 1. Extrair o conteúdo do KMZ (que é essencialmente um ZIP)
    print(f"Extraindo {kmz_path}...")
    with zipfile.ZipFile(kmz_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Localizar o arquivo .kml extraído
    kml_file = None
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith('.kml'):
                kml_file = os.path.join(root, file)
                break

    if not kml_file:
        print("Nenhum arquivo KML encontrado dentro do KMZ.")
        return

    # 2. Identificar as camadas KML
    print("Lendo camadas do KML...")
    camadas = fiona.listlayers(kml_file)
    
    for camada in camadas:
        print(f"Processando camada: {camada}")
        try:
            # Ler a camada específica preservando os atributos
            gdf = gpd.read_file(kml_file, driver='KML', layer=camada)
            
            # 3. Verificação e Correção de Inconsistências Topológicas
            gdf['geometry'] = gdf['geometry'].apply(lambda geom: make_valid(geom) if geom is not None else geom)
            
            # Remover geometrias vazias após a correção, se houver
            gdf = gdf[~gdf.is_empty & gdf['geometry'].notnull()]
            
            if gdf.empty:
                print(f"A camada {camada} ficou vazia após a correção topológica. Ignorando.")
                continue
                
            # 4. Converter para Shapefile
            nome_seguro = "".join([c for c in camada if c.isalnum() or c in (' ', '_')]).rstrip()
            shp_path = os.path.join(shp_dir, f"{nome_seguro}.shp")
            
            gdf.to_file(shp_path, driver='ESRI Shapefile')
            print(f"Shapefile gerado: {shp_path}")
            
        except Exception as e:
            print(f"Erro ao processar a camada {camada}: {e}")

    # 5. Gerar arquivo ZIP com os Shapefiles resultantes
    print(f"Compactando Shapefiles em {output_zip}...")
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(shp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.basename(file_path))

    # Limpeza dos diretórios temporários
    shutil.rmtree(temp_dir)
    shutil.rmtree(shp_dir)
    print(f"Processo concluído com sucesso! Arquivo gerado: {output_zip}")


if __name__ == '__main__':
    # Substitua pelo nome do seu arquivo
    extrair_e_converter_kmz('seu_arquivo.kmz')

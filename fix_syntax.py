import re

def fix_syntax():
    with open('Presai_v26_repo/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # El problema parece estar en las comillas escapadas dentro de las plantillas literales
    # o en el uso de comillas simples/dobles mezcladas incorrectamente.
    
    # Corregir Ubicación/Profesional en OC (asegurar que no haya errores de escape)
    # Buscamos la sección inyectada y la limpiamos
    project_info_fix = """
    <div class="sub" style="margin-bottom:6px; font-weight:700; color:#333;">PROYECTO: ${esc(document.getElementById("pObra").value||"—")}</div>
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 12px;">
      <div class="sub" style="font-weight:700; color:#333; margin-bottom:0;">UBICACIÓN PROYECTO: ${esc(document.getElementById("pLocation").value||"—")}</div>
      <div class="sub" style="font-weight:700; color:#333; margin-bottom:0; text-align:right;">PROFESIONAL A CARGO: ${esc(document.getElementById("pProf").value||"—")}</div>
    </div>
    """
    
    # Limpiar cualquier residuo de inyecciones anteriores fallidas
    pattern_to_clean = r'<div class="sub" style="margin-bottom:6px; font-weight:700; color:#333;">PROYECTO:[\s\S]*?<div class="grid2">'
    if re.search(pattern_to_clean, content):
        content = re.sub(pattern_to_clean, project_info_fix + '<div class="grid2">', content)

    # Revisar si hay errores de escape en el código de la firma (base64 largo)
    # A veces los editores rompen las líneas de base64 o meten caracteres extraños.
    
    # También revisamos el modal de materiales por si acaso
    content = content.replace('Suma productos seleccionados', 'Suma productos seleccionados')
    content = content.replace('Suma pagina Total Ref.', 'Suma pagina Total Ref.')

    with open('Presai_v26_repo/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_syntax()

import re

def apply_changes():
    with open('Presai_v26_repo/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Modificar cmp_rowHtml para que el botón +SC esté inactivo por defecto
    old_btn = r'<button class="bs" onclick="cmp_addToSC\(\'\$\{lm\.id\}\'\)" style="font-size:10px;padding:2px 7px">\+ SC</button>'
    new_btn = r'<button id="btn-add-sc-${lm.id}" class="bs" onclick="cmp_addToSC(\'${lm.id}\')" style="font-size:10px;padding:2px 7px;opacity:0.5;pointer-events:none" disabled>+ SC</button>'
    content = re.sub(old_btn, new_btn, content)

    # 2. Actualizar cmp_updateSumaSeleccionados para activar/desactivar botones
    update_suma_old = """function cmp_updateSumaSeleccionados(){
  const filtered = cmp_getFilteredLista();
  const selectedIds = Array.from(document.querySelectorAll('.cmp-lm-chk:checked')).map(cb=>cb.value);
  const sumaSeleccionados = filtered.filter(lm=>selectedIds.includes(lm.id)).reduce((a,lm)=>a+lm.totalRef,0);
  document.getElementById('cmp-suma-sel').textContent = fmtCLP(sumaSeleccionados);
}"""

    update_suma_new = """function cmp_updateSumaSeleccionados(){
  const filtered = cmp_getFilteredLista();
  const allChks = document.querySelectorAll('.cmp-lm-chk');
  const selectedIds = [];
  
  allChks.forEach(chk => {
    const id = chk.value;
    const btn = document.getElementById('btn-add-sc-' + id);
    if (chk.checked) {
      selectedIds.push(id);
      if (btn) {
        btn.disabled = false;
        btn.style.opacity = '1';
        btn.style.pointerEvents = 'auto';
      }
    } else {
      if (btn) {
        btn.disabled = true;
        btn.style.opacity = '0.5';
        btn.style.pointerEvents = 'none';
      }
    }
  });

  const sumaSeleccionados = filtered.filter(lm=>selectedIds.includes(lm.id)).reduce((a,lm)=>a+lm.totalRef,0);
  const elSuma = document.getElementById('cmp-suma-sel');
  if (elSuma) elSuma.textContent = fmtCLP(sumaSeleccionados);
}"""
    content = content.replace(update_suma_old, update_suma_new)

    # 3. Extraer la firma de SC y agregarla a OC
    # Firma en SC está en cmp_printSC
    firma_pattern = r'(<div class="firma-box" style="margin-top:40px; display:flex; justify-content:space-around; align-items:flex-end;">[\s\S]*?<\/div>\s*<\/div>\s*<\/div>)'
    firma_match = re.search(firma_pattern, content)
    if firma_match:
        firma_html = firma_match.group(1)
        # Final de OC en cmp_printOC
        oc_print_end_marker = r'\${oc\.notas\?`<div style="margin-top:14px;font-size:11px;color:#555;border-top:1px solid #ddd;padding-top:10px"><span style="font-style:italic; color:#64748b;">\${esc\(oc\.notas\)}</span></div>`:""}'
        content = content.replace(oc_print_end_marker, oc_print_end_marker + "\n    " + firma_html)

    with open('Presai_v26_repo/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    apply_changes()

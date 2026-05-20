import re

def apply_changes():
    with open('Presai_v26_repo/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Actualizar cmp_newSC para incluir el historial inicial
    sc_init_match = re.search(r'const sc = \{[\s\S]*?estado:\'borrador\',', content)
    if sc_init_match:
        initial_history = "historial: [{ fecha: new Date().toLocaleString(), estado: 'creacion' }],"
        content = content.replace("estado:'borrador',", f"estado:'creacion', {initial_history}")

    # 2. Actualizar cmp_newOC para incluir el historial inicial
    oc_init_match = re.search(r'const oc = \{[\s\S]*?estado:\'emitida\',', content)
    if oc_init_match:
        initial_history = "historial: [{ fecha: new Date().toLocaleString(), estado: 'creacion' }],"
        content = content.replace("estado:'emitida',", f"estado:'creacion', {initial_history}")

    # 3. Función auxiliar para renderizar el historial (inyectar en el script)
    # Buscamos un lugar apropiado, por ejemplo antes de cmp_editSC
    helper_functions = """
function cmp_renderHistorial(doc) {
  if (!doc.historial) doc.historial = [{ fecha: new Date().toLocaleString(), estado: 'creacion' }];
  const items = doc.historial.map(h => `
    <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid var(--border);font-size:11px">
      <span style="color:var(--txt2)">${h.fecha}</span>
      <span style="font-weight:600;color:var(--navy)">${h.estado.toUpperCase()}</span>
    </div>
  `).join('');
  
  const uniqueStates = ['creacion', 'para aprobación', 'aprobada'];
  const hasUnique = doc.historial.some(h => uniqueStates.includes(h.estado) && h.estado !== 'creacion');
  // Nota: 'creacion' ya ocurrió, así que evaluamos si 'para aprobación' o 'aprobada' ya están.
  const paraAprobacionExists = doc.historial.some(h => h.estado === 'para aprobación');
  const aprobadaExists = doc.historial.some(h => h.estado === 'aprobada');

  const availableStates = ['revisada', 'enviada', 'anulada'];
  if (!paraAprobacionExists) availableStates.push('para aprobación');
  if (!aprobadaExists) availableStates.push('aprobada');

  const options = availableStates.map(s => `<option value="${s}">${s.charAt(0).toUpperCase() + s.slice(1)}</option>`).join('');

  return `
    <div class="no-print" style="margin-top:16px;padding-top:16px;border-top:2px dashed var(--border2)">
      <div style="font-size:11px;font-weight:700;color:var(--navy);margin-bottom:8px;text-transform:uppercase;letter-spacing:0.5px">Historial de Estados</div>
      <div style="background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:10px;max-height:120px;overflow-y:auto;margin-bottom:10px">
        ${items}
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <select id="hist-new-estado" style="flex:1;padding:6px 10px;border:1.5px solid var(--border2);border-radius:6px;font-family:var(--ff);font-size:12px;background:var(--bg);color:var(--txt)">
          ${options}
        </select>
        <button class="bs addp" onclick="cmp_addHistorialEstado('${doc.id}', '${doc.id.startsWith('sc') ? 'sc' : 'oc'}')" style="font-size:11px;padding:6px 12px;background:var(--navy);color:#fff">Actualizar Estado</button>
      </div>
    </div>`;
}

function cmp_addHistorialEstado(id, type) {
  const list = type === 'sc' ? comprasData.solicitudes : comprasData.ordenesCompra;
  const doc = list.find(d => d.id === id);
  if (!doc) return;
  const newEstado = document.getElementById('hist-new-estado').value;
  if (!doc.historial) doc.historial = [];
  doc.historial.push({ fecha: new Date().toLocaleString(), estado: newEstado });
  doc.estado = newEstado;
  markUnsaved();
  if (type === 'sc') cmp_editSC(id); else cmp_editOC(id);
}
"""
    content = content.replace("function cmp_editSC(id){", helper_functions + "\nfunction cmp_editSC(id){")

    # 4. Inyectar el historial en el modal de SC (antes del cierre de los botones)
    sc_modal_insertion = "      ${cmp_renderHistorial(sc)}\n      <div style=\"display:flex;justify-content:flex-end;gap:10px\">"
    content = content.replace('<div style="display:flex;justify-content:flex-end;gap:10px">', sc_modal_insertion, 1)

    # 5. Inyectar el historial en el modal de OC (antes del cierre de los botones)
    # Tenemos que ser cuidadosos porque hay varios divs de botones. Buscamos el de OC específicamente.
    # El de OC está después de oc-edit-notas.
    oc_modal_pattern = r'(<textarea id="oc-edit-notas"[\s\S]*?<\/textarea>\s*<\/div>\s*)(<div style="display:flex;justify-content:flex-end;gap:10px">)'
    content = re.sub(oc_modal_pattern, r'\1${cmp_renderHistorial(oc)}\n\2', content)

    with open('Presai_v26_repo/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    apply_changes()

/**
 * Función para alternar entre el selector de categorías y el input de nueva categoría.
 * Limpia el campo que no se está usando para evitar confusiones en el backend.
 */
function toggleCategoriaMode() {
    const selectMode = document.getElementById('select-mode');
    const inputMode = document.getElementById('input-mode');
    
    // Buscamos los inputs por su atributo 'name'
    const inputField = document.querySelector('input[name="nueva_categoria_input"]');
    const selectField = document.querySelector('select[name="categoria_id"]');

    // Verificamos si el modo select está oculto
    if (selectMode.style.display === 'none') {
        // --- VOLVER A MODO SELECTOR ---
        selectMode.style.display = 'flex';
        inputMode.style.display = 'none';
        
        // Limpiamos el input de texto para que no se envíe
        if(inputField) inputField.value = ''; 
        
    } else {
        // --- CAMBIAR A MODO NUEVA CATEGORÍA ---
        selectMode.style.display = 'none';
        inputMode.style.display = 'block';
        
        // Reseteamos el select para que no haya un ID seleccionado
        if(selectField) selectField.value = ''; 
        
        // Ponemos el foco en el input para escribir rápido
        if(inputField) inputField.focus();
    }
}